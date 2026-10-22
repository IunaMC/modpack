#!/usr/bin/env python3
"""Resumo semanal dos três repos da IunaMC, em Markdown no stdout.

Uso: python3 scripts/resumo.py

Lê pelo `gh api` (token em GH_TOKEN; RESUMO_TOKEN e MINECRAFT_CONFIG_TOKEN, se
definidos, só têm a validade consultada): versões e alinhamento entre o modpack, a
moderação e as configs, o último resultado de cada workflow na main e na
devel/devel, commits da devel/devel fora da main (com aviso quando parados há
muito tempo), as releases das configs ainda não enviadas ao servidor (issues
`envio`), se a última versão já aparece na CurseForge e PRs e issues abertos. O
resumo vai para uma issue pública: dos repos privados só saem versões,
contagens e o resultado do CI, nunca títulos.
"""
import base64
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

ORG = "IunaMC"
PARADO = 14  # dias de commit na devel/devel sem estável que viram aviso
REPOS = {"modpack": "Modpack", "modpack-moderacao": "Moderação", "minecraft-config": "Configs"}
PUBLICO = "modpack"
TOKENS = ("RESUMO_TOKEN", "MINECRAFT_CONFIG_TOKEN")  # secrets com validade
AVISO_TOKEN = 14  # dias para vencer que viram aviso


def api(caminho):
    r = subprocess.run(["gh", "api", caminho], capture_output=True, text=True)
    if r.returncode != 0:
        # Vai para o log do workflow, não para a issue: mostra qual permissão falta.
        motivo = (r.stderr.strip().splitlines() or ["sem detalhe"])[-1]
        print(f"::warning::gh api {caminho.split('?')[0]}: {motivo}", file=sys.stderr)
        return None
    return json.loads(r.stdout)


def vencimento(token):
    """Data em que o token vence, pelo cabeçalho github-authentication-token-expiration.

    Devolve (data, None), (None, None) se o token não vence ou (None, motivo) se
    a consulta falhou. O token só viaja para o gh e nunca é impresso.
    """
    r = subprocess.run(["gh", "api", "-i", "rate_limit"], capture_output=True, text=True,
                       env={**os.environ, "GH_TOKEN": token})
    cabecalho = re.search(r"^github-authentication-token-expiration:\s*(\S+ \S+)", r.stdout, re.M | re.I)
    if cabecalho:
        return datetime.strptime(cabecalho.group(1), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc), None
    if r.returncode != 0 and "401" in r.stdout + r.stderr:
        return None, "recusado pelo GitHub (vencido ou revogado)"
    return (None, None) if r.returncode == 0 else (None, "sem resposta do GitHub")


def tokens():
    """Uma linha por token com os dias que faltam para vencer; só a data, nunca o valor."""
    linhas = []
    for nome in TOKENS:
        token = os.environ.get(nome)
        if not token:
            linhas.append(f"- **`{nome}`:** não definido neste ambiente.")
            continue
        data, erro = vencimento(token)
        if erro:
            linhas.append(f"- **`{nome}`:** ❌ {erro}: gere outro e atualize o secret.")
        elif data is None:
            linhas.append(f"- **`{nome}`:** sem data de validade.")
        else:
            dias = (data - datetime.now(timezone.utc)).days
            aviso = " ⚠️ gere outro antes disso e atualize o secret." if dias < AVISO_TOKEN else ""
            linhas.append(f"- **`{nome}`:** vence em {data:%d/%m/%Y} ({dias} dias).{aviso}")
    return linhas


def arquivo(repo, caminho, ref="main"):
    d = api(f"repos/{ORG}/{repo}/contents/{caminho}?ref={ref}")
    return base64.b64decode(d["content"]).decode() if d else None


def releases(repo):
    rels = api(f"repos/{ORG}/{repo}/releases?per_page=30") or []
    rels = [r for r in rels if re.fullmatch(r"v\d+\.\d+\.\d+(-beta\.\d+)?", r["tag_name"])]
    estavel = next((r["tag_name"] for r in rels if not r["prerelease"]), None)
    beta = next((r["tag_name"] for r in rels if r["prerelease"]), None)
    return estavel, beta


def toml_valor(texto, chave):
    m = re.search(rf'^{chave}\s*=\s*"([^"]*)"', texto or "", re.M)
    return m.group(1) if m else None


def dias_desde(data):
    return (datetime.now(timezone.utc) - datetime.fromisoformat(data.replace("Z", "+00:00"))).days


def curseforge():
    """Versões enviadas que ainda não aparecem e o estado da descrição (scripts/curseforge.py)."""
    import curseforge as cf
    try:
        faltam = [v for v, aparece in cf.estado_versoes() if not aparece]
    except Exception:
        return ["não consegui consultar a API pública."]
    linhas = ["todas as versões enviadas estão publicadas." if not faltam else
              f"⚠️ não aparecem ({', '.join(f'`{v}`' for v in faltam)}): em revisão ou recusadas, "
              "confira em authors.curseforge.com."]
    return linhas + [f"descrição do site: {cf.estado_descricao()}"]


def envios():
    """Issues "Enviar configs X.Y.Z ao servidor" abertas: releases que ainda não chegaram ao servidor."""
    issues = api(f"repos/{ORG}/minecraft-config/issues?state=open&labels=envio&per_page=20")
    if issues is None:
        return "- **Envio ao servidor:** sem acesso às issues das configs."
    versoes = [m.group(1) for i in issues if (m := re.search(r"Enviar configs (\S+) ao servidor", i["title"]))]
    if not versoes:
        return "- **Envio ao servidor:** nenhuma release pendente; o servidor está com a última."
    return (f"- **Envio ao servidor:** ⚠️ {len(versoes)} pendente(s), versão {', '.join(f'`{v}`' for v in versoes)}: "
            "envie pelo FileZilla e feche a issue no repositório das configs.")


def ci(repo):
    """Último resultado de cada workflow na main e na devel/devel."""
    linhas, falhas = [], 0
    for ramo in ("main", "devel/devel"):
        d = api(f"repos/{ORG}/{repo}/actions/runs?branch={ramo}&per_page=40")
        if d is None:
            return ["sem acesso ao CI"], 0
        vistos = {}
        for run in d["workflow_runs"]:
            vistos.setdefault(run["name"], run)
        for nome, run in sorted(vistos.items()):
            estado = run["conclusion"] or run["status"]
            if estado not in ("success", "skipped", "in_progress", "queued"):
                falhas += 1
                linhas.append(f"❌ {nome} na `{ramo}`: {estado} ({run['created_at'][:10]}) {run['html_url']}")
    return linhas, falhas


def main():
    out = []
    pack_estavel, pack_beta = releases("modpack")
    versao_devel = toml_valor(arquivo("modpack", "pack/pack.toml", "devel/devel"), "version")

    out.append("## Versões\n")
    out.append(f"- **Modpack:** estável `{pack_estavel}`, última beta `{pack_beta}`, "
               f"`devel/devel` em `{versao_devel or 'sem branch'}`.")

    base = arquivo("modpack-moderacao", "base.toml")
    if base is None:
        out.append("- **Moderação:** sem acesso.")
    else:
        tag_base = toml_valor(base, "tag")
        mod_estavel, _ = releases("modpack-moderacao")
        aviso = "" if tag_base == pack_estavel else f" ⚠️ atrás do modpack `{pack_estavel}`: rode o `/propagar`."
        out.append(f"- **Moderação:** versão `{mod_estavel}`, pack base `{tag_base}`.{aviso}")

    versao_cfg = arquivo("minecraft-config", "VERSAO")
    if versao_cfg is None:
        out.append("- **Configs:** sem acesso.")
    else:
        versao_cfg, modpack_cfg = versao_cfg.strip(), (arquivo("minecraft-config", "MODPACK") or "").strip()
        cfg_estavel, _ = releases("minecraft-config")
        avisos = []
        if f"v{versao_cfg}" != cfg_estavel:
            avisos.append(f"⚠️ `VERSAO` {versao_cfg} na main ainda sem release")
        if f"v{modpack_cfg}" != pack_estavel:
            avisos.append(f"⚠️ testadas com o modpack {modpack_cfg}, não com o `{pack_estavel}`")
        out.append(f"- **Configs:** release `{cfg_estavel}`, testadas com o modpack `{modpack_cfg}`."
                   + (" " + "; ".join(avisos) + "." if avisos else ""))
    out.append(envios())

    out.append("\n## Lojas\n")
    for linha in curseforge():
        out.append(f"- **CurseForge:** {linha}")

    out.append("\n## CI\n")
    total = 0
    for repo, nome in REPOS.items():
        linhas, falhas = ci(repo)
        total += falhas
        for l in linhas:
            out.append(f"- **{nome}:** {l}")
    if total == 0:
        out.append("- Tudo verde na `main` e na `devel/devel`.")

    out.append("\n## Tokens\n")
    out.extend(tokens())

    out.append("\n## Pendências\n")
    for repo, nome in REPOS.items():
        cmp = api(f"repos/{ORG}/{repo}/compare/main...devel/devel")
        prs = api(f"repos/{ORG}/{repo}/pulls?state=open&per_page=50")
        issues = api(f"repos/{ORG}/{repo}/issues?state=open&per_page=50")
        if prs is None or issues is None:
            out.append(f"- **{nome}:** sem acesso.")
            continue
        issues = [i for i in issues if "pull_request" not in i]
        partes = []
        if cmp and cmp["ahead_by"]:
            parte = f"{cmp['ahead_by']} commit(s) na `devel/devel` fora da `main`"
            dias = dias_desde(cmp["commits"][0]["commit"]["committer"]["date"]) if cmp["commits"] else 0
            if dias >= PARADO:
                parte += f" ⚠️ o mais antigo tem {dias} dias: hora de uma estável"
            partes.append(parte)
        partes.append(f"{len(prs)} PR(s) e {len(issues)} issue(s) abertos")
        out.append(f"- **{nome}:** " + ", ".join(partes) + ".")
        if repo == PUBLICO:
            for i in prs + issues:
                out.append(f"  - #{i['number']} {i['title']}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
