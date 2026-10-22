#!/usr/bin/env python3
"""Página e versões do IUNA no Modrinth, a partir dos arquivos de modrinth/.

A configuração fica em modrinth/projeto.toml. Os comandos que falam com o
Modrinth leem o token de MODRINTH_TOKEN; sem ele, avisam e saem sem erro.

Uso:
  python3 scripts/modrinth.py verificar                      # confere modrinth/ sem acessar a rede
  python3 scripts/modrinth.py sincronizar [--simular]        # aplica nome, textos, links, ícone e galeria
  python3 scripts/modrinth.py reduzir <completo.mrpack> <reduzido.mrpack>
                                                             # tira os mods de [[reduzido.fora]]
  python3 scripts/modrinth.py publicar <versão> <.mrpack> <notas.md> [--simular]
                                                             # envia a versão reduzida, se ainda não existir
  python3 scripts/modrinth.py limpar [--apagar]              # lista (ou apaga) as versões completas antigas

--simular mostra o que mudaria, sem mudar nada. O limpar só apaga com --apagar.
"""
import hashlib
import json
import os
import re
import sys
import tomllib
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "modrinth"
PACK = RAIZ / "pack"
# O .mrpack reduzido termina assim; o limpar reconhece as versões por isso.
SUFIXO = "-modrinth.mrpack"
API = "https://api.modrinth.com/v2"
REPO = os.environ.get("GITHUB_REPOSITORY", "IunaMC/modpack")
AGENTE = f"{REPO} (github.com/{REPO})"
TIPOS = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
SHA1 = re.compile(r"/([0-9a-f]{40})[_.]")
LINKS = {"codigo": "source_url", "issues": "issues_url", "wiki": "wiki_url", "discord": "discord_url"}


def config():
    return tomllib.loads((PASTA / "projeto.toml").read_text())


def sha1(caminho):
    return hashlib.sha1(caminho.read_bytes()).hexdigest()


def sha1_da_url(url):
    achado = SHA1.search(url or "")
    return achado.group(1) if achado else None


def sem_titulo(texto):
    """Tira o "# Título" do topo: o Modrinth já mostra o nome."""
    return re.sub(r"\A# .*\n+", "", texto).strip()


def vazio(valor):
    return valor or None


def fora(cfg=None):
    """Mods que o .mrpack do Modrinth não leva, com o arquivo de cada um."""
    lista = []
    for item in (cfg or config()).get("reduzido", {}).get("fora", []):
        caminho = PACK / "mods" / f"{item['pw']}.pw.toml"
        pw = tomllib.loads(caminho.read_text()) if caminho.is_file() else {}
        cf = pw.get("update", {}).get("curseforge", {})
        lista.append({**item, "caminho": caminho, "existe": caminho.is_file(), "nome": pw.get("name", item["pw"]),
                      "arquivo": pw.get("filename"), "file_id": cf.get("file-id")})
    return lista


# --- verificar ---------------------------------------------------------------

def tamanho_png(caminho):
    dados = caminho.read_bytes()[:24]
    if dados[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return int.from_bytes(dados[16:20], "big"), int.from_bytes(dados[20:24], "big")


def verificar():
    cfg = config()
    erros = []

    def imagem(rel, limite):
        caminho = PASTA / rel
        if not caminho.is_file():
            erros.append(f"{rel}: arquivo não existe")
        elif caminho.suffix.lower() not in TIPOS:
            erros.append(f"{rel}: use PNG, JPEG ou WebP")
        elif caminho.stat().st_size > limite:
            erros.append(f"{rel}: maior que {limite // 1024} KiB")
        return caminho

    if not 3 <= len(cfg["nome"]) <= 64:
        erros.append("nome: precisa ter de 3 a 64 caracteres")
    if not 3 <= len(cfg["resumo"]) <= 255:
        erros.append("resumo: precisa ter de 3 a 255 caracteres")
    if not 1 <= len(cfg["categorias"]) <= 3:
        erros.append("categorias: de 1 a 3")

    icone = imagem(cfg["icone"], 256 * 1024)
    if icone.is_file() and (dim := tamanho_png(icone)) and (dim[0] != dim[1] or dim[0] < 256):
        erros.append(f"{cfg['icone']}: precisa ser quadrado e ter 256×256 ou mais (tem {dim[0]}×{dim[1]})")

    arquivos = [g["arquivo"] for g in cfg.get("galeria", [])]
    for rel in arquivos:
        imagem(rel, 5 * 1024 * 1024)
    if len(set(arquivos)) != len(arquivos):
        erros.append("galeria: a mesma imagem aparece duas vezes")
    if sum(1 for g in cfg.get("galeria", []) if g.get("destaque")) > 1:
        erros.append("galeria: só uma imagem pode ter destaque = true")
    banner = cfg["descricao"].get("banner")
    if banner and banner not in arquivos:
        erros.append(f"descricao.banner: {banner} precisa estar na galeria")

    for chave in ("principal", "traducao"):
        if rel := cfg["descricao"].get(chave):
            if not (PASTA / rel).is_file():
                erros.append(f"descricao.{chave}: {rel} não existe")

    # A página não pode esconder o corte: cada mod de fora aparece na abertura
    # (antes da primeira seção) das duas descrições, não só nos créditos.
    textos = [(PASTA / cfg["descricao"][c]).read_text().split("\n## ")[0] for c in ("principal", "traducao")
              if cfg["descricao"].get(c) and (PASTA / cfg["descricao"][c]).is_file()]
    for mod in fora(cfg):
        if not mod["existe"]:
            erros.append(f"reduzido.fora: pack/mods/{mod['pw']}.pw.toml não existe; tire o item da lista")
        elif not mod["file_id"]:
            erros.append(f"reduzido.fora: {mod['pw']} não tem [update.curseforge]")
        if not mod.get("curseforge", "").startswith("https://www.curseforge.com/"):
            erros.append(f"reduzido.fora: {mod['pw']} precisa do link da página na CurseForge")
        if any(mod["nome"] not in texto for texto in textos):
            erros.append(f"descrição: {mod['nome']} fica fora do .mrpack do Modrinth e precisa ser citado na abertura das duas descrições")
    if not erros:
        corpo = montar_corpo(cfg, None)
        if len(corpo) > 65536:
            erros.append(f"descrição: {len(corpo)} caracteres, o limite é 65536")
        if sobra := re.findall(r"<[a-zçãõé-]+>", corpo.replace("<details>", "").replace("<summary>", "")):
            erros.append(f"descrição: placeholders sem preencher: {', '.join(sorted(set(sobra)))}")

    for erro in erros:
        print(f"::error file=modrinth/projeto.toml::{erro}")
    if erros:
        sys.exit(1)
    print("modrinth/ ok")


# --- API ---------------------------------------------------------------------

def token():
    valor = os.environ.get("MODRINTH_TOKEN", "").strip()
    if not valor and (arquivo := Path.home() / ".config/modrinth/token").is_file():
        valor = arquivo.read_text().strip()
    return valor


def chamar(metodo, caminho, corpo=None, tipo=None, consulta=None):
    url = API + caminho + ("?" + urllib.parse.urlencode(consulta) if consulta else "")
    cabecalhos = {"Authorization": token(), "User-Agent": AGENTE}
    if isinstance(corpo, (dict, list)):
        corpo, tipo = json.dumps(corpo).encode(), "application/json"
    if tipo:
        cabecalhos["Content-Type"] = tipo
    pedido = urllib.request.Request(url, data=corpo, method=metodo, headers=cabecalhos)
    try:
        with urllib.request.urlopen(pedido, timeout=600) as resposta:
            texto = resposta.read().decode()
    except urllib.error.HTTPError as erro:
        print(f"::error::{metodo} {caminho}: HTTP {erro.code}: {erro.read().decode()[:500]}")
        sys.exit(1)
    return json.loads(texto) if texto else None


def exigir_token():
    if token():
        return True
    print("::notice::MODRINTH_TOKEN não configurado; nada foi enviado ao Modrinth.")
    return False


# --- sincronizar -------------------------------------------------------------

def montar_corpo(cfg, url_banner):
    desc = cfg["descricao"]
    partes = []
    if desc.get("banner"):
        url = url_banner or f"https://cdn.modrinth.com/data/{cfg['id']}/images/{sha1(PASTA / desc['banner'])}{Path(desc['banner']).suffix.lower()}"
        titulo = next((g["titulo"] for g in cfg.get("galeria", []) if g["arquivo"] == desc["banner"]), cfg["nome"])
        partes.append(f"![{titulo}]({url})")
    partes.append(sem_titulo((PASTA / desc["principal"]).read_text()))
    if desc.get("traducao"):
        traducao = sem_titulo((PASTA / desc["traducao"]).read_text())
        partes.append(f"<details>\n<summary>{desc.get('traducao_titulo', 'Translation')}</summary>\n\n{traducao}\n\n</details>")
    return "\n\n".join(partes) + "\n"


def sincronizar(simular):
    verificar()
    if not exigir_token():
        return
    cfg = config()
    pid = cfg["id"]
    atual = chamar("GET", f"/project/{pid}")
    acao = "[simulação] " if simular else ""

    # Ícone: o nome do arquivo no CDN é o sha1 do original.
    icone = PASTA / cfg["icone"]
    if sha1_da_url(atual.get("icon_url")) != sha1(icone):
        print(f"{acao}ícone: envia {cfg['icone']}")
        if not simular:
            chamar("PATCH", f"/project/{pid}/icon", icone.read_bytes(),
                   TIPOS[icone.suffix.lower()], {"ext": icone.suffix.lower().lstrip(".")})

    # Galeria: cada imagem é reconhecida pelo sha1 do arquivo.
    remotas = {sha1_da_url(g.get("raw_url") or g["url"]): g for g in atual.get("gallery", [])}
    desejadas = []
    for ordem, item in enumerate(cfg.get("galeria", [])):
        caminho = PASTA / item["arquivo"]
        desejadas.append((sha1(caminho), caminho, item, ordem))
    hashes = {h for h, *_ in desejadas}
    for h, remota in remotas.items():
        if h not in hashes:
            print(f"{acao}galeria: apaga \"{remota.get('title')}\"")
            if not simular:
                chamar("DELETE", f"/project/{pid}/gallery", consulta={"url": remota["url"]})
    for h, caminho, item, ordem in desejadas:
        meta = {"featured": str(bool(item.get("destaque"))).lower(), "title": item.get("titulo", ""),
                "description": item.get("descricao", ""), "ordering": str(ordem)}
        remota = remotas.get(h)
        if remota is None:
            print(f"{acao}galeria: envia {item['arquivo']}")
            if not simular:
                chamar("POST", f"/project/{pid}/gallery", caminho.read_bytes(), TIPOS[caminho.suffix.lower()],
                       {"ext": caminho.suffix.lower().lstrip("."), **meta})
        elif (remota.get("featured"), remota.get("title") or "", remota.get("description") or "", remota.get("ordering")) != \
                (bool(item.get("destaque")), meta["title"], meta["description"], ordem):
            print(f"{acao}galeria: atualiza \"{meta['title']}\"")
            if not simular:
                chamar("PATCH", f"/project/{pid}/gallery", consulta={"url": remota["url"], **meta})

    # Campos do projeto: só manda o que mudou.
    url_banner = None
    if banner := cfg["descricao"].get("banner"):
        h = sha1(PASTA / banner)
        galeria = atual.get("gallery", []) if simular else chamar("GET", f"/project/{pid}").get("gallery", [])
        url_banner = next((g.get("raw_url") for g in galeria if sha1_da_url(g.get("raw_url") or g["url"]) == h), None)
    desejado = {
        "title": cfg["nome"],
        "description": cfg["resumo"],
        "body": montar_corpo(cfg, url_banner),
        "categories": cfg["categorias"],
        "additional_categories": cfg.get("categorias_extras", []),
        "license_id": cfg["licenca"],
        "license_url": vazio(cfg.get("licenca_url")),
        **{campo: vazio(cfg.get("links", {}).get(chave)) for chave, campo in LINKS.items()},
    }
    existente = {
        "title": atual.get("title"),
        "description": atual.get("description"),
        "body": atual.get("body"),
        "categories": atual.get("categories"),
        "additional_categories": atual.get("additional_categories"),
        "license_id": (atual.get("license") or {}).get("id"),
        "license_url": (atual.get("license") or {}).get("url"),
        **{campo: atual.get(campo) for campo in LINKS.values()},
    }
    mudancas = {}
    for campo, valor in desejado.items():
        antes = existente.get(campo)
        if isinstance(valor, list):
            igual = sorted(valor) == sorted(antes or [])
        elif campo == "body":
            igual = (valor or "").strip() == (antes or "").strip()
        else:
            igual = valor == antes
        if not igual:
            mudancas[campo] = valor
            print(f"{acao}{campo}: {'(texto)' if campo == 'body' else json.dumps(antes, ensure_ascii=False)} -> "
                  f"{'(texto novo, %d caracteres)' % len(valor) if campo == 'body' else json.dumps(valor, ensure_ascii=False)}")
    if mudancas and not simular:
        chamar("PATCH", f"/project/{pid}", mudancas)
    if not mudancas:
        print("campos do projeto: nada mudou")


# --- reduzir -----------------------------------------------------------------

def reduzir(entrada, saida):
    """Copia o .mrpack completo sem os jars dos mods de [[reduzido.fora]]."""
    entrada, saida = Path(entrada), Path(saida)
    mods = fora()
    tirar = {f"overrides/mods/{m['arquivo']}" for m in mods}
    erros = [f"{m['pw']}: pack/mods/{m['pw']}.pw.toml não existe" for m in mods if not m["existe"]]
    with zipfile.ZipFile(entrada) as z:
        nomes = set(z.namelist())
        erros += [f"{nome} não está em {entrada.name}" for nome in sorted(tirar - nomes)]
        if erros:
            for erro in erros:
                print(f"::error file=modrinth/projeto.toml::reduzido.fora: {erro}")
            sys.exit(1)
        with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as nova:
            for info in z.infolist():
                if info.filename not in tirar:
                    nova.writestr(info, z.read(info))
    for m in mods:
        print(f"fora do .mrpack do Modrinth: {m['nome']} ({m['arquivo']})")
    print(f"{saida.name}: {saida.stat().st_size // 1024} KiB (o completo tem {entrada.stat().st_size // 1024} KiB)")


def fora_do_arquivo(mods):
    """Seção do changelog com o arquivo exato de cada mod que se baixa à parte."""
    linhas = [
        "## Not included in this file · Fora deste arquivo",
        "",
        "These mods don't allow redistribution through Modrinth. Add the exact files below from "
        "CurseForge, or the game will not start. In Prism Launcher: *Edit → Mods → Download mods → "
        "CurseForge*. In the Modrinth App, download the `.jar` and put it in the instance's `mods` folder.",
        "",
        "Estes mods não permitem a redistribuição pelo Modrinth. Adicione da CurseForge os arquivos "
        "abaixo, ou o jogo não abre. No Prism Launcher: *Edit → Mods → Download mods → CurseForge*. "
        "No Modrinth App, baixe o `.jar` e ponha na pasta `mods` da instância.",
        "",
    ]
    linhas += [f"- [{m['nome']}]({m['curseforge'].rstrip('/')}/files/{m['file_id']}): `{m['arquivo']}`" for m in mods]
    return "\n".join(linhas) + "\n"


# --- publicar ----------------------------------------------------------------

def multipart(dados, arquivo, nome_arquivo, tipo):
    fronteira = uuid.uuid4().hex
    corpo = (
        f"--{fronteira}\r\nContent-Disposition: form-data; name=\"data\"\r\n"
        f"Content-Type: application/json\r\n\r\n{json.dumps(dados)}\r\n"
        f"--{fronteira}\r\nContent-Disposition: form-data; name=\"arquivo\"; filename=\"{nome_arquivo}\"\r\n"
        f"Content-Type: {tipo}\r\n\r\n"
    ).encode() + arquivo.read_bytes() + f"\r\n--{fronteira}--\r\n".encode()
    return corpo, f"multipart/form-data; boundary={fronteira}"


def publicar(versao, mrpack, notas, simular):
    cfg = config()
    mrpack, notas = Path(mrpack), Path(notas)
    with zipfile.ZipFile(mrpack) as z:
        indice = json.loads(z.read("modrinth.index.json"))
        embutidos = [n for n in z.namelist() if n.startswith("overrides/mods/") and n.endswith(".jar")]
    # O Modrinth só recebe o reduzido: nenhum jar de fora pode ter ficado.
    mods = fora(cfg)
    if sobra := [m["nome"] for m in mods if f"overrides/mods/{m['arquivo']}" in embutidos]:
        print(f"::error::{mrpack.name} ainda tem {', '.join(sobra)}. Gere o arquivo com: python3 scripts/modrinth.py reduzir")
        sys.exit(1)
    if not mrpack.name.endswith(SUFIXO):
        print(f"::error::{mrpack.name}: o .mrpack do Modrinth precisa terminar em {SUFIXO}")
        sys.exit(1)
    changelog = notas.read_text()
    if mods:
        changelog = changelog.rstrip() + "\n\n" + fora_do_arquivo(mods)
    deps = indice["dependencies"]
    loaders = [nome.removesuffix("-loader") for nome in deps if nome != "minecraft"]
    externos = [f["path"] for f in indice["files"]
                if not all(u.startswith("https://cdn.modrinth.com/") for u in f["downloads"])]
    tipo = "alpha" if "alpha" in versao else "beta" if "-" in versao else "release"
    dados = {
        "project_id": cfg["id"],
        "name": cfg.get("versao", {}).get("nome", "IUNA {versao}").format(versao=versao),
        "version_number": versao,
        "changelog": changelog,
        "dependencies": [],
        "game_versions": [deps["minecraft"]],
        "loaders": loaders,
        "version_type": tipo,
        "featured": True,
        "status": "listed",
        "environment": cfg.get("versao", {}).get("ambiente", "client_and_server"),
        "file_parts": ["arquivo"],
        "primary_file": "arquivo",
    }
    print(f"versão {versao} ({tipo}), {', '.join(loaders)} {deps['minecraft']}, {mrpack.name}")
    print(f"arquivos de fora do Modrinth: {len(embutidos)} embutidos e {len(externos)} baixados de outro site")
    print(f"mods que se baixam à parte: {', '.join(m['nome'] for m in mods) or 'nenhum'}")
    if not exigir_token():
        return
    if any(v["version_number"] == versao for v in chamar("GET", f"/project/{cfg['id']}/version")):
        print(f"::notice::A versão {versao} já está no Modrinth; nada foi enviado.")
        return
    if simular:
        print(f"[simulação] enviaria {mrpack.name}")
        return
    corpo, tipo_corpo = multipart(dados, mrpack, mrpack.name, "application/x-modrinth-modpack+zip")
    for tentativa in range(3):
        try:
            criada = chamar("POST", "/version", corpo, tipo_corpo)
            print(f"versão enviada: https://modrinth.com/project/{cfg['id']}/version/{criada['id']}")
            break
        except SystemExit:
            # O Modrinth às vezes responde 500 (deadlock no banco) e aceita na
            # tentativa seguinte. Antes de repetir, confere se não entrou.
            if any(v["version_number"] == versao for v in chamar("GET", f"/project/{cfg['id']}/version")):
                print("versão enviada (o Modrinth respondeu com erro, mas ela entrou)")
                break
            if tentativa == 2:
                raise
            print("tentando de novo...")
    print(f"::notice::Versão {versao} enviada ao Modrinth. Se ela trouxer arquivo de fora do Modrinth "
          "que ainda não está na página Permissions, ela fica retida até alguém marcar a permissão no site.")


# --- limpar ------------------------------------------------------------------

def limpar(apagar):
    """Versões cujo arquivo não é o reduzido: embutem mods sem permissão e travam a moderação."""
    if not exigir_token():
        return
    pid = config()["id"]
    versoes = chamar("GET", f"/project/{pid}/version", consulta={"include_changelog": "false"})

    def principal(v):
        return next((f["filename"] for f in v["files"] if f.get("primary")), v["files"][0]["filename"] if v["files"] else "")

    reduzidas = [v for v in versoes if principal(v).endswith(SUFIXO)]
    antigas = [v for v in versoes if not principal(v).endswith(SUFIXO)]
    print(f"{len(versoes)} versões no Modrinth: {len(reduzidas)} reduzidas e {len(antigas)} completas")
    for v in antigas:
        print(f"  {v['version_number']} ({principal(v)}, {v['date_published'][:10]})")
    if not antigas:
        return
    if not reduzidas:
        print("::warning::Nenhuma versão reduzida no Modrinth ainda. Publique uma antes de apagar as completas.")
        return
    if not apagar:
        print("Nada foi apagado. Para apagar estas versões (não tem volta): python3 scripts/modrinth.py limpar --apagar")
        return
    for v in antigas:
        chamar("DELETE", f"/version/{v['id']}")
        print(f"apagada: {v['version_number']}")


def main():
    args = [a for a in sys.argv[1:] if a not in ("--simular", "--apagar")]
    simular = "--simular" in sys.argv
    if args == ["verificar"]:
        verificar()
    elif args == ["sincronizar"]:
        sincronizar(simular)
    elif len(args) == 3 and args[0] == "reduzir":
        reduzir(*args[1:])
    elif len(args) == 4 and args[0] == "publicar":
        publicar(*args[1:], simular)
    elif args == ["limpar"]:
        limpar("--apagar" in sys.argv)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
