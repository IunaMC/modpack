#!/usr/bin/env python3
"""Fonte da CurseForge dos mods e envio do pack à CurseForge.

Todo mod de cliente tem, além da fonte do Modrinth, um [update.curseforge]
apontando para o mesmo arquivo na CurseForge. O `packwiz update` só segue o
Modrinth, então depois de atualizar um mod o arquivo da CurseForge fica para
trás; o `verificar` acusa isso e o `--corrigir` acha o arquivo certo.

O envio lê o token de CURSEFORGE_TOKEN (token de upload, de
authors.curseforge.com → My API Tokens) e o projeto de CURSEFORGE_PROJECT_ID;
sem eles, avisa e sai sem erro.

Uso:
  python3 scripts/curseforge.py verificar [--corrigir]
      # confere se cada mod de cliente aponta para o mesmo arquivo nas duas fontes
  python3 scripts/curseforge.py ligar <mod.pw.toml> <Project ID na CurseForge>
      # acrescenta o [update.curseforge] de um mod novo, pelo mesmo arquivo do pack
  python3 scripts/curseforge.py publicar <versão> <.zip> <notas.md> [--simular]
      # envia o .zip do packwiz curseforge export, se a versão ainda não estiver lá
  python3 scripts/curseforge.py status
      # quais releases já aparecem na CurseForge e se a descrição do site está em dia
  python3 scripts/curseforge.py descricao [--marcar]
      # imprime a descrição para colar no site; --marcar registra que o site recebeu esta

A CurseForge não tem API para editar o projeto nem para ver arquivos em revisão:
a API de upload só envia e altera arquivos, e as APIs de leitura (a do site e a
Core API) só mostram arquivos aprovados. Por isso a descrição é colada à mão, e
o `status` só distingue "aparece" de "não aparece" (em revisão ou recusado).
"""
import hashlib
import json
import os
import re
import sys
import tomllib
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PACK = RAIZ / "pack"
# API do site: pública, sem chave, usada só para ler arquivos de projetos.
SITE = "https://www.curseforge.com/api/v1"
# API de upload dos autores: pede o token de upload.
UPLOAD = "https://minecraft.curseforge.com/api"
AGENTE = "Mozilla/5.0 (IunaMC/modpack)"
PROJETO = "1752945"
GITHUB = "https://api.github.com/repos/IunaMC/modpack/releases?per_page=10"
# Primeira versão enviada pelo Release; as anteriores nunca foram à CurseForge.
PRIMEIRA = "3.3.0-beta.1"
MARCA = RAIZ / "curseforge" / "descricao.sha256"


def pedir(url, corpo=None, tipo=None, token=None):
    cabecalhos = {"User-Agent": AGENTE, "Accept": "application/json"}
    if token:
        cabecalhos["X-Api-Token"] = token
    if tipo:
        cabecalhos["Content-Type"] = tipo
    pedido = urllib.request.Request(url, data=corpo, headers=cabecalhos,
                                    method="POST" if corpo else "GET")
    try:
        with urllib.request.urlopen(pedido, timeout=600) as resposta:
            return json.loads(resposta.read().decode() or "null")
    except urllib.error.HTTPError as erro:
        print(f"::error::{url}: HTTP {erro.code}: {erro.read().decode()[:500]}")
        sys.exit(1)


# --- verificar ---------------------------------------------------------------

def arquivos_do_projeto(projeto):
    """Todos os arquivos de um projeto, do mais novo ao mais velho."""
    pagina = 0
    while True:
        lote = pedir(f"{SITE}/mods/{projeto}/files?pageIndex={pagina}&pageSize=50"
                     "&sort=dateCreated&sortDescending=true&removeAlphas=false")["data"]
        yield from lote
        if len(lote) < 50:
            return
        pagina += 1


def conferir(caminho):
    """(caminho, problema, file-id certo ou None). problema None = tudo certo."""
    dados = tomllib.loads(caminho.read_text())
    if dados.get("side", "both") == "server" or dados["download"].get("mode") == "metadata:curseforge":
        return caminho, None, None
    cf = dados.get("update", {}).get("curseforge")
    if not cf:
        return caminho, "sem [update.curseforge]", None
    arquivo = pedir(f"{SITE}/mods/{cf['project-id']}/files/{cf['file-id']}")["data"]
    if arquivo and arquivo["fileName"].casefold() == dados["filename"].casefold():
        return caminho, None, None
    certo = next((a["id"] for a in arquivos_do_projeto(cf["project-id"])
                  if a["fileName"].casefold() == dados["filename"].casefold()), None)
    if certo == cf["file-id"]:
        return caminho, None, None
    problema = (f"a CurseForge aponta para {arquivo['fileName']}, o pack usa {dados['filename']}" if arquivo
                else f"o arquivo {cf['file-id']} não está disponível na CurseForge")
    return caminho, problema, certo


def verificar(corrigir):
    mods = sorted(p for pasta in ("mods", "resourcepacks", "shaderpacks")
                  for p in (PACK / pasta).glob("*.pw.toml"))
    with ThreadPoolExecutor(8) as grupo:
        resultados = list(grupo.map(conferir, mods))
    problemas = [r for r in resultados if r[1]]
    corrigidos = 0
    for caminho, problema, certo in problemas:
        nome = caminho.relative_to(RAIZ)
        if corrigir and certo:
            texto = re.sub(r"(\[update\.curseforge\][^\[]*?file-id = )\d+", rf"\g<1>{certo}",
                           caminho.read_text())
            caminho.write_text(texto)
            corrigidos += 1
            print(f"corrigido: {nome} → file-id {certo}")
        elif certo:
            print(f"::error file={nome}::{problema}. Rode: python3 scripts/curseforge.py verificar --corrigir")
        else:
            print(f"::error file={nome}::{problema}, e a CurseForge não tem esse arquivo. "
                  "Volte o mod para uma versão que exista nas duas fontes.")
    print(f"{len(mods)} arquivos conferidos, {len(problemas)} com problema" +
          (f", {corrigidos} corrigidos (rode packwiz refresh em pack/)" if corrigidos else ""))
    if len(problemas) > corrigidos:
        sys.exit(1)


def ligar(caminho, projeto):
    caminho = Path(caminho)
    texto = caminho.read_text()
    if "[update.curseforge]" in texto:
        sys.exit(f"{caminho} já tem [update.curseforge].")
    if not projeto.isdigit():
        sys.exit("Passe o Project ID numérico, que fica na lateral da página do mod na CurseForge.")
    nome = tomllib.loads(texto)["filename"]
    certo = next((a["id"] for a in arquivos_do_projeto(projeto)
                  if a["fileName"].casefold() == nome.casefold()), None)
    if not certo:
        sys.exit(f"O projeto {projeto} não tem o arquivo {nome}. Escolha uma versão que exista nas duas fontes.")
    caminho.write_text(texto.rstrip("\n") + f"\n[update.curseforge]\nfile-id = {certo}\nproject-id = {projeto}\n")
    print(f"{caminho}: CurseForge {projeto}, arquivo {certo}. Rode packwiz refresh em pack/.")


# --- publicar ----------------------------------------------------------------

def multipart(metadados, arquivo):
    fronteira = uuid.uuid4().hex
    corpo = (
        f"--{fronteira}\r\nContent-Disposition: form-data; name=\"metadata\"\r\n"
        f"Content-Type: application/json\r\n\r\n{json.dumps(metadados)}\r\n"
        f"--{fronteira}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{arquivo.name}\"\r\n"
        "Content-Type: application/zip\r\n\r\n"
    ).encode() + arquivo.read_bytes() + f"\r\n--{fronteira}--\r\n".encode()
    return corpo, f"multipart/form-data; boundary={fronteira}"


def id_da_versao(token, minecraft):
    tipos = {t["id"] for t in pedir(f"{UPLOAD}/game/version-types", token=token)
             if t["slug"].startswith("minecraft-")}
    achado = next((v["id"] for v in pedir(f"{UPLOAD}/game/versions", token=token)
                   if v["gameVersionTypeID"] in tipos and v["name"] == minecraft), None)
    if not achado:
        sys.exit(f"::error::A CurseForge não tem o Minecraft {minecraft} na lista de versões.")
    return achado


def publicar(versao, arquivo, notas, simular):
    token = os.environ.get("CURSEFORGE_TOKEN", "").strip()
    projeto = os.environ.get("CURSEFORGE_PROJECT_ID", "").strip()
    arquivo, notas = Path(arquivo), Path(notas)
    minecraft = tomllib.loads((PACK / "pack.toml").read_text())["versions"]["minecraft"]
    tipo = "alpha" if "alpha" in versao else "beta" if "-" in versao else "release"
    nome = f"IUNA {versao}"
    print(f"versão {versao} ({tipo}), Minecraft {minecraft}, {arquivo.name}")
    if not token or not projeto:
        print("::notice::CURSEFORGE_TOKEN ou CURSEFORGE_PROJECT_ID não configurado; nada foi enviado à CurseForge.")
        return
    # Arquivo ainda em revisão pode não aparecer aqui; por isso o workflow só
    # chama o envio uma vez por release.
    try:
        if any(a["displayName"] == nome for a in arquivos_do_projeto(projeto)):
            print(f"::notice::A versão {versao} já está na CurseForge; nada foi enviado.")
            return
    except SystemExit:
        print("::warning::Não deu para listar os arquivos do projeto (ainda não aprovado?); enviando assim mesmo.")
    metadados = {
        "changelog": notas.read_text(),
        "changelogType": "markdown",
        "displayName": nome,
        "releaseType": tipo,
        "gameVersions": [id_da_versao(token, minecraft)],
    }
    if simular:
        print(f"[simulação] enviaria {arquivo.name} com {json.dumps({**metadados, 'changelog': '…'})}")
        return
    corpo, tipo_corpo = multipart(metadados, arquivo)
    enviado = pedir(f"{UPLOAD}/projects/{projeto}/upload-file", corpo, tipo_corpo, token)
    print(f"::notice::Versão {versao} enviada à CurseForge (arquivo {enviado['id']}). "
          "Ela passa pela revisão da CurseForge antes de aparecer.")


# --- descrição e status --------------------------------------------------------

def descricao():
    """A descrição do site: a do Modrinth sem o título, mais a seção extra do projeto.md."""
    texto = (RAIZ / "modrinth" / "descricao.en.md").read_text()
    texto = re.sub(r"\A# [^\n]*\n+", "", texto)
    extra = re.search(r"```md\n(.*?)```", (RAIZ / "curseforge" / "projeto.md").read_text(), re.S)
    return texto.rstrip("\n") + "\n\n" + (extra.group(1).strip() + "\n" if extra else "")


def estado_descricao():
    atual = hashlib.sha256(descricao().encode()).hexdigest()
    if not MARCA.exists():
        return "sem registro do que está no site: confira e rode `curseforge.py descricao --marcar`"
    if MARCA.read_text().strip() == atual:
        return "em dia com o repositório"
    return "⚠️ mudou no repositório: cole `curseforge.py descricao` no site e rode `--marcar`"


def chave(versao):
    base, _, beta = versao.partition("-beta.")
    return tuple(map(int, base.split("."))) + ((int(beta),) if beta else (10**6,))


def estado_versoes():
    """(versão, aparece?) das releases enviadas à CurseForge, da mais nova à mais velha."""
    req = urllib.request.Request(GITHUB, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(req, timeout=30) as r:
        tags = [t["tag_name"].lstrip("v") for t in json.load(r)]
    tags = [t for t in tags if re.fullmatch(r"\d+\.\d+\.\d+(-beta\.\d+)?", t) and chave(t) >= chave(PRIMEIRA)]
    nomes = {a["displayName"] for a in arquivos_do_projeto(PROJETO)}
    return [(t, f"IUNA {t}" in nomes) for t in tags]


def status():
    for versao, aparece in estado_versoes():
        print(f"{versao}: {'publicada' if aparece else 'não aparece (em revisão ou recusada)'}")
    print(f"descrição: {estado_descricao()}")


def main():
    args = [a for a in sys.argv[1:] if a not in ("--simular", "--corrigir", "--marcar")]
    if args == ["verificar"]:
        verificar("--corrigir" in sys.argv)
    elif len(args) == 3 and args[0] == "ligar":
        ligar(*args[1:])
    elif len(args) == 4 and args[0] == "publicar":
        publicar(*args[1:], "--simular" in sys.argv)
    elif args == ["status"]:
        status()
    elif args == ["descricao"]:
        if "--marcar" in sys.argv:
            MARCA.write_text(hashlib.sha256(descricao().encode()).hexdigest() + "\n")
            print(f"Registrado em {MARCA.relative_to(RAIZ)}: o site tem a descrição atual. Faça o commit.")
        else:
            print(descricao(), end="")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
