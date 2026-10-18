#!/usr/bin/env python3
"""Resumo semanal dos três repos da IunaMC, em Markdown no stdout.

Uso: python3 scripts/resumo.py

Lê pelo `gh api` (token em GH_TOKEN): versões e alinhamento entre o modpack, a
moderação e as configs, o último resultado de cada workflow na main e na
devel/devel, commits da devel/devel fora da main e PRs e issues abertos. O
resumo vai para uma issue pública: dos repos privados só saem versões,
contagens e o resultado do CI, nunca títulos.
"""
import base64
import json
import re
import subprocess

ORG = "IunaMC"
REPOS = {"modpack": "Modpack", "modpack-moderacao": "Moderação", "minecraft-config": "Configs"}
PUBLICO = "modpack"


def api(caminho):
    r = subprocess.run(["gh", "api", caminho], capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 else None


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
    out.append("- Lembrete: o envio das configs ao servidor é manual; confira se a release acima já está lá.")

    out.append("\n## CI\n")
    total = 0
    for repo, nome in REPOS.items():
        linhas, falhas = ci(repo)
        total += falhas
        for l in linhas:
            out.append(f"- **{nome}:** {l}")
    if total == 0:
        out.append("- Tudo verde na `main` e na `devel/devel`.")

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
            partes.append(f"{cmp['ahead_by']} commit(s) na `devel/devel` fora da `main`")
        partes.append(f"{len(prs)} PR(s) e {len(issues)} issue(s) abertos")
        out.append(f"- **{nome}:** " + ", ".join(partes) + ".")
        if repo == PUBLICO:
            for i in prs + issues:
                out.append(f"  - #{i['number']} {i['title']}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
