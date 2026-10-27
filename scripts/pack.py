#!/usr/bin/env python3
"""Ferramentas do pack: lista de mods do README, changelog de mods, arquivos externos e as regras da main.

Lê os metadados do packwiz (pack/pack.toml e os .pw.toml de pack/mods, pack/resourcepacks e pack/shaderpacks).

Uso:
  python3 scripts/pack.py versao              # imprime a versão do pack.toml
  python3 scripts/pack.py neoforge            # imprime a versão do NeoForge do pack.toml
  python3 scripts/pack.py readme              # regenera a lista de mods no README.md
  python3 scripts/pack.py readme --check      # falha se a lista do README estiver desatualizada
  python3 scripts/pack.py mudancas <ref-git>  # mods adicionados/removidos/atualizados desde <ref-git>
      # <ref-git> pode ser "estavel" (última tag estável) ou "ultima" (última tag, beta inclusive).
  python3 scripts/pack.py proxima-beta        # próxima versão beta pelo SemVer (o motivo vai para o stderr)
  python3 scripts/pack.py externo <jar> [opções]
      # anexa o jar à release arquivos-servidor e cria o .pw.toml que aponta para ele.
      # Opções: --lado server|both|client (padrão server), --nome, --versao, --autor,
      # --licenca, --origem (o padrão de cada uma vem dos metadados do jar) e --simular,
      # que mostra o que seria feito sem enviar nem gravar nada. Veja docs/guias/arquivos-externos.md.
  python3 scripts/pack.py lado <arquivo.pw.toml>...
      # só informa: mostra o que o Modrinth declara para cliente e servidor e a licença, sem gravar
      # nada. O side de cada mod é escolha de uma pessoa, a declaração do Modrinth pode estar errada.
      # Veja docs/guias/adicionar-mod.md.
  python3 scripts/pack.py orfas <mod>
      # <mod> é o nome do arquivo em pack/mods (sem .pw.toml) ou parte do nome. Mostra as dependências
      # obrigatórias que ficariam sem uso se ele saísse e, se ../iunamc.minecraft-config existir
      # (ou MINECRAFT_CONFIG_DIR), os arquivos de config que citam cada um. Não remove nada.
      # Veja docs/guias/remover-mod.md.
  python3 scripts/pack.py soltos
      # falha se o índice tiver arquivo solto (sem .pw.toml) fora de config/yosbr/. O servidor instala
      # o pack inteiro, e um arquivo solto em config/ sobrescreveria a config do minecraft-config.
      # Veja docs/guias/configs-do-cliente.md.
  python3 scripts/pack.py conferir <base> <topo> [--ramo <branch>]
      # confere as regras de versão do que entra na main, de <base> até <topo> (ex.: origin/main HEAD).
      # --ramo também confere a branch de origem do PR; o corpo do PR vem de CORPO_PR.
      # Veja docs/referencia/versionamento.md.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tomllib
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PACK = RAIZ / "pack"
README = RAIZ / "README.md"
INICIO = "<!-- lista-de-mods:inicio -->"
FIM = "<!-- lista-de-mods:fim -->"
LADOS = {"both": "Cliente e servidor", "client": "Cliente", "server": "Servidor"}
REPO = "IunaMC/modpack"
RELEASE_EXTERNOS = "arquivos-servidor"
PASTA_CLIENTE = "config/yosbr/"


def ler_mod(texto):
    dados = tomllib.loads(texto)
    update = dados.get("update", {})
    if "modrinth" in update:
        link = f"https://modrinth.com/mod/{update['modrinth']['mod-id']}"
    elif "curseforge" in update:
        link = f"https://www.curseforge.com/projects/{update['curseforge']['project-id']}"
    else:
        link = dados.get("download", {}).get("url", "")
    return {
        "nome": dados["name"].strip(),
        "arquivo": dados["filename"],
        "lado": dados.get("side", "both"),
        "link": link,
    }


PASTAS = ("mods", "resourcepacks", "shaderpacks")


def mods_atuais():
    """Mods, resource packs e shaders do pack, pela chave "pasta/arquivo"."""
    return {f"{p.parent.name}/{p.name}": ler_mod(p.read_text())
            for pasta in PASTAS for p in sorted((PACK / pasta).glob("*.pw.toml"))}


def mods_em(ref):
    """Mods do pack em um ref do git; vazio se o ref não tiver o pack."""
    git = ["git", "-C", str(RAIZ)]
    mods = {}
    for pasta in PASTAS:
        ls = subprocess.run(git + ["ls-tree", "--name-only", f"{ref}:pack/{pasta}"],
                            capture_output=True, text=True)
        if ls.returncode != 0:
            continue
        for nome in ls.stdout.split():
            if nome.endswith(".pw.toml"):
                texto = subprocess.run(git + ["show", f"{ref}:pack/{pasta}/{nome}"],
                                       capture_output=True, text=True, check=True).stdout
                mods[f"{pasta}/{nome}"] = ler_mod(texto)
    return mods


def versao():
    return tomllib.loads((PACK / "pack.toml").read_text())["version"]


def tabela(mods):
    linhas = ["| Mod | Arquivo | Lado |", "| --- | --- | --- |"]
    for m in sorted(mods, key=lambda m: m["nome"].casefold()):
        nome = m["nome"].replace("|", "\\|")
        linhas.append(f"| [{nome}]({m['link']}) | `{m['arquivo']}` | {LADOS.get(m['lado'], m['lado'])} |")
    return "\n".join(linhas)


def lista_readme():
    todos = mods_atuais()
    mods = [m for k, m in todos.items() if k.startswith("mods/")]
    extras = [m for k, m in todos.items() if not k.startswith("mods/")]
    servidor = [m for m in mods if m["lado"] == "server"]
    cliente = [m for m in mods if m["lado"] != "server"]
    return "\n".join([
        INICIO,
        "<!-- Gerado por scripts/pack.py readme. Não edite à mão. -->",
        "",
        f"O pack tem **{len(mods)} mods**. O jogador recebe {len(cliente)}, "
        f"e o servidor, {len(mods) - sum(1 for m in mods if m['lado'] == 'client')}.",
        "",
        "### Mods do jogador",
        "Todos obrigatórios para entrar no servidor. O launcher instala todos.",
        "",
        tabela(cliente),
        "",
        "### Só no servidor",
        "Administração, desempenho e geração de mundo. O launcher do jogador ignora estes.",
        "",
        tabela(servidor),
        "",
        "### Resource packs e shaders",
        "Vêm na instância do jogador; ative em Opções → Pacotes de recursos ou Shaders.",
        "",
        tabela(extras),
        FIM,
    ])


def cmd_readme(checar):
    texto = README.read_text()
    if INICIO not in texto or FIM not in texto:
        sys.exit(f"README.md sem os marcadores {INICIO} e {FIM}")
    antes, resto = texto.split(INICIO, 1)
    depois = resto.split(FIM, 1)[1]
    novo = antes + lista_readme() + depois
    if checar:
        if novo != texto:
            sys.exit("A lista de mods do README.md está desatualizada. Rode: python3 scripts/pack.py readme")
        print("README.md em dia.")
    else:
        README.write_text(novo)


def ultima_tag(estavel):
    tags = subprocess.run(["git", "-c", "versionsort.suffix=-", "tag", "--list", "v*", "--sort=-v:refname"],
                          capture_output=True, text=True).stdout.split()
    return next((t for t in tags if not (estavel and "-beta" in t)), "HEAD")


def cmd_mudancas(ref):
    if ref in ("estavel", "ultima"):
        ref = ultima_tag(ref == "estavel")
    antigos, atuais = mods_em(ref), mods_atuais()
    if not antigos:
        print(f"_Sem comparação: `{ref}` não tem o pack em packwiz._")
        return
    grupos = {"Adicionados": [], "Atualizados": [], "Removidos": []}
    for chave, m in atuais.items():
        if chave not in antigos:
            grupos["Adicionados"].append(f"- [{m['nome']}]({m['link']}) `{m['arquivo']}`")
        elif antigos[chave]["arquivo"] != m["arquivo"]:
            grupos["Atualizados"].append(
                f"- [{m['nome']}]({m['link']}): `{antigos[chave]['arquivo']}` → `{m['arquivo']}`")
    for chave, m in antigos.items():
        if chave not in atuais:
            grupos["Removidos"].append(f"- [{m['nome']}]({m['link']}) `{m['arquivo']}`")
    if not any(grupos.values()):
        print("_Nenhum mod mudou._")
        return
    for titulo, itens in grupos.items():
        if itens:
            print(f"### {titulo} ({len(itens)})\n" + "\n".join(sorted(itens, key=str.casefold)) + "\n")


def metadados_jar(jar):
    """Nome, versão, autor, licença e origem declarados no jar (Fabric ou NeoForge)."""
    with zipfile.ZipFile(jar) as z:
        nomes = set(z.namelist())
        if "fabric.mod.json" in nomes:
            d = json.loads(z.read("fabric.mod.json"))
            autores = [a["name"] if isinstance(a, dict) else a for a in d.get("authors", [])]
            licenca = d.get("license", "")
            return {
                "nome": d.get("name", ""),
                "versao": d.get("version", ""),
                "autor": ", ".join(autores),
                "licenca": " / ".join(licenca) if isinstance(licenca, list) else licenca,
                "origem": d.get("contact", {}).get("sources") or d.get("contact", {}).get("repo")
                          or d.get("contact", {}).get("homepage", ""),
            }
        for arquivo in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml"):
            if arquivo in nomes:
                d = tomllib.loads(z.read(arquivo).decode())
                mod = d.get("mods", [{}])[0]
                versao = mod.get("version", "")
                if "${" in versao and "META-INF/MANIFEST.MF" in nomes:
                    manifesto = z.read("META-INF/MANIFEST.MF").decode(errors="replace")
                    achado = re.search(r"^Implementation-Version:\s*(\S+)", manifesto, re.M)
                    versao = achado.group(1) if achado else ""
                return {
                    "nome": mod.get("displayName", ""),
                    "versao": "" if "${" in versao else versao,
                    "autor": mod.get("authors", ""),
                    "licenca": d.get("license", ""),
                    "origem": mod.get("displayURL", "") or d.get("issueTrackerURL", ""),
                }
    return {}


def opcao(args, nome, padrao=""):
    if nome in args:
        i = args.index(nome)
        if i + 1 >= len(args):
            sys.exit(f"Falta o valor de {nome}.")
        return args[i + 1]
    return padrao


def gh(*args, **kwargs):
    return subprocess.run(["gh", *args, "-R", REPO], check=True, text=True, **kwargs)


def cmd_externo(args):
    if not args or args[0].startswith("--"):
        sys.exit(__doc__)
    jar = Path(args[0]).expanduser().resolve()
    if not jar.is_file() or jar.suffix != ".jar":
        sys.exit(f"Não achei o jar: {jar}")
    simular = "--simular" in args
    meta = metadados_jar(jar)
    info = {campo: opcao(args, f"--{campo}", meta.get(campo, ""))
            for campo in ("nome", "versao", "autor", "licenca", "origem")}
    lado = opcao(args, "--lado", "server")
    if lado not in LADOS:
        sys.exit(f"--lado deve ser um de: {', '.join(LADOS)}")
    faltando = [campo for campo, valor in info.items() if not valor]
    if faltando:
        sys.exit("O jar não informa " + ", ".join(faltando) + ". Passe "
                 + " ".join(f"--{campo} <valor>" for campo in faltando) + ".")

    # Anexo com o mesmo nome nunca é substituído: o hash mudaria e as versões
    # antigas do pack, que apontam para a mesma URL, deixariam de instalar.
    if not re.search(r"\d", jar.stem):
        sys.exit(f"O nome {jar.name} não tem versão. Renomeie para algo como "
                 f"{jar.stem}-{info['versao']}.jar antes de anexar.")
    slug = re.sub(r"[^a-z0-9]+", "-", info["nome"].casefold()).strip("-")
    destino = PACK / "mods" / f"{slug}.pw.toml"
    if destino.exists():
        sys.exit(f"{destino.relative_to(RAIZ)} já existe. Para atualizar, apague-o (packwiz remove) e rode de novo.")
    release = json.loads(gh("release", "view", RELEASE_EXTERNOS, "--json", "assets,body",
                            capture_output=True).stdout)
    if any(a["name"] == jar.name for a in release["assets"]):
        sys.exit(f"A release {RELEASE_EXTERNOS} já tem um anexo {jar.name}. Use outro nome (com a versão nova).")

    url = f"https://github.com/{REPO}/releases/download/{RELEASE_EXTERNOS}/{jar.name}"
    pw_toml = "\n".join([
        f'name = "{info["nome"]}"',
        f'filename = "{jar.name}"',
        f'side = "{lado}"',
        "",
        "[download]",
        f'url = "{url}"',
        'hash-format = "sha512"',
        f'hash = "{hashlib.sha512(jar.read_bytes()).hexdigest()}"',
        "",
    ])
    linha = (f"| `{jar.name}` | {info['nome']} {info['versao']} | {info['autor']} | "
             f"{info['licenca']} | [{info['origem'].rstrip('/').split('/', 3)[-1]}]({info['origem']}) |")
    corpo = release["body"].rstrip("\n").split("\n")
    ultima = max(i for i, l in enumerate(corpo) if l.startswith("|"))
    corpo.insert(ultima + 1, linha)

    print(f"==> Anexar {jar.name} à release {RELEASE_EXTERNOS}")
    print(f"==> Criar {destino.relative_to(RAIZ)}:\n{pw_toml}")
    print(f"==> Linha nova na tabela da release:\n{linha}\n")
    if simular:
        print("Simulação: nada foi enviado nem gravado.")
        return
    sys.stdout.flush()

    gh("release", "upload", RELEASE_EXTERNOS, str(jar))
    gh("release", "edit", RELEASE_EXTERNOS, "--notes", "\n".join(corpo) + "\n")
    destino.write_text(pw_toml)
    subprocess.run(["packwiz", "refresh"], cwd=PACK, check=True)
    cmd_readme(False)
    print(f"\nPronto. Confira a licença ({info['licenca']}), suba a versão (MINOR), escreva o "
          f"MUDANCAS.md e faça o commit:\n  feat(mods): adiciona {info['nome']} {info['versao']}"
          + (" no servidor" if lado == "server" else ""))


def ultima_estavel():
    tags = subprocess.run(["git", "-C", str(RAIZ), "tag", "--list", "v*", "--sort=-v:refname"],
                          capture_output=True, text=True, check=True).stdout.split()
    return next((t for t in tags if "-" not in t), None)


def cmd_proxima_beta():
    """Beta seguinte a uma beta, ou a primeira beta depois da estável pelo SemVer:
    MAJOR se o Minecraft ou o NeoForge mudou, MINOR se algum mod mudou, PATCH se nada mudou."""
    atual = versao()
    beta = re.fullmatch(r"(\d+\.\d+\.\d+)-beta\.(\d+)", atual)
    if beta:
        print(f"{beta[1]}-beta.{int(beta[2]) + 1}")
        print(f"beta seguinte a {atual}", file=sys.stderr)
        return
    tag = ultima_estavel()
    maior, menor, patch = map(int, atual.split("."))
    if tag is None:
        motivo, nova = "sem estável anterior", (maior, menor, patch + 1)
    else:
        antes = subprocess.run(["git", "-C", str(RAIZ), "show", f"{tag}:pack/pack.toml"],
                               capture_output=True, text=True, check=True).stdout
        if tomllib.loads(antes)["versions"] != tomllib.loads((PACK / "pack.toml").read_text())["versions"]:
            motivo, nova = f"MAJOR: Minecraft ou NeoForge mudou desde {tag}", (maior + 1, 0, 0)
        elif mods_em(tag) != mods_atuais():
            motivo, nova = f"MINOR: mods mudaram desde {tag}", (maior, menor + 1, 0)
        else:
            motivo, nova = f"PATCH: nenhum mod mudou desde {tag}", (maior, menor, patch + 1)
    print("{}.{}.{}-beta.1".format(*nova))
    print(motivo, file=sys.stderr)


RAMOS_DA_MAIN = {"devel/devel": "pack, scripts, CI e docs", "docs/docs": "só documentação"}


def git(*args):
    return subprocess.run(["git", "-C", str(RAIZ), *args], capture_output=True, text=True,
                          check=True).stdout


def numeros(versao):
    return tuple(map(int, versao.split("-")[0].split(".")))


def cmd_conferir(base, topo, ramo=None, corpo=""):
    """Regras para o que entra na main, de base até topo:
    - pack/ mudou além da versão  → precisa de versão nova;
    - só a versão mudou           → recusado (para reenviar, rode o Release à mão);
    - versão nova                 → estável, sem tag ainda e a próxima depois da última estável;
    - MAJOR                       → com --pr, o corpo do PR precisa ter "MAJOR confirmado";
    - nada em pack/               → passa, sem release (docs, CI, scripts).
    Com ramo, também confere de onde o PR vem (devel/devel ou docs/docs)."""
    erros = []
    origem = git("merge-base", base, topo).strip()
    mudou = [p for p in git("diff", "--name-only", origem, topo, "--", "pack/").split() if p]
    antes = tomllib.loads(git("show", f"{origem}:pack/pack.toml"))
    depois = tomllib.loads(git("show", f"{topo}:pack/pack.toml"))
    va, vd = antes["version"], depois["version"]
    so_versao = mudou == ["pack/pack.toml"] and \
        {k: v for k, v in antes.items() if k != "version"} == {k: v for k, v in depois.items() if k != "version"}

    if ramo is not None and ramo not in RAMOS_DA_MAIN:
        erros.append(f"A main só recebe PR de {' ou '.join(RAMOS_DA_MAIN)}, e este vem de '{ramo}'.")
    if ramo == "docs/docs" and mudou:
        erros.append("A docs/docs é só de documentação, e este PR muda o pack/: leve a mudança pela devel/devel.")
    if "-" in vd:
        erros.append(f"A main só recebe versões estáveis, e '{vd}' é beta.")

    if not mudou:
        caso = "nada mudou em pack/: entra sem release"
    elif va == vd:
        caso = "pack/ mudou sem versão nova"
        erros.append(f"O pack/ mudou ({len(mudou)} arquivo(s)), mas a versão continua {va}. Suba a versão no pack/pack.toml.")
    elif so_versao:
        caso = "só a versão mudou"
        erros.append(f"Só a versão mudou ({va} → {vd}), sem nenhuma mudança no pack. "
                     "Para reenviar uma versão às plataformas, rode o Release à mão (workflow_dispatch).")
    else:
        caso = f"versão nova: {va} → {vd}"

    if va != vd and "-" not in vd:
        if git("tag", "--list", f"v{vd}").strip():
            erros.append(f"A tag v{vd} já existe.")
        tag = ultima_estavel()
        if tag:
            a, b, c = numeros(tag[1:])
            proximas = {(a, b, c + 1): "PATCH", (a, b + 1, 0): "MINOR", (a + 1, 0, 0): "MAJOR"}
            tipo = proximas.get(numeros(vd))
            if tipo is None:
                validas = ", ".join("{}.{}.{}".format(*v) for v in proximas)
                erros.append(f"{vd} não é a próxima versão depois de {tag}: use {validas}.")
            elif tipo == "MAJOR" and ramo is not None and "MAJOR confirmado" not in corpo:
                erros.append(f"{vd} é MAJOR (mundo novo ou reinstalar tudo): escreva \"MAJOR confirmado\" "
                             "no corpo do PR para seguir.")

    print(f"{git('rev-parse', '--short', origem).strip()}..{git('rev-parse', '--short', topo).strip()}: {caso}")
    for erro in erros:
        print(f"::error::{erro}" if os.environ.get("GITHUB_ACTIONS") else f"ERRO: {erro}")
    if erros:
        sys.exit(1)
    print("ok")


def cmd_soltos():
    """O packwiz-installer leva ao servidor todo arquivo solto do pack: o side só vale nos .pw.toml.
    Os padrões do cliente ficam em config/yosbr/, que só o YOMBR (só cliente) lê."""
    indice = tomllib.loads((PACK / "index.toml").read_text())
    fora = [f["file"] for f in indice["files"]
            if not f.get("metafile") and not f["file"].startswith(PASTA_CLIENTE)]
    for arquivo in fora:
        print(f"::error::{arquivo}" if os.environ.get("GITHUB_ACTIONS") else f"ERRO: {arquivo}")
    if fora:
        sys.exit(f"{len(fora)} arquivo(s) solto(s) fora de {PASTA_CLIENTE}: o servidor também os instalaria. "
                 f"Padrão do cliente vai em pack/{PASTA_CLIENTE} (veja docs/guias/configs-do-cliente.md).")
    print("ok")


def modrinth(caminho):
    """GET na API do Modrinth, já decodificado."""
    req = urllib.request.Request(f"https://api.modrinth.com/v2/{caminho}",
                                 headers={"User-Agent": f"{REPO} (github.com/{REPO})"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def pasta_configs():
    candidatas = [os.environ.get("MINECRAFT_CONFIG_DIR"), RAIZ.parent / "iunamc.minecraft-config"]
    return next((Path(c) for c in candidatas if c and (Path(c) / "config").is_dir()), None)


def configs_que_citam(pasta, nomes):
    """Arquivos de config/ cujo nome ou conteúdo cita algum dos nomes (slug, com - ou _)."""
    variantes = {v.casefold() for n in nomes for v in (n, n.replace("-", "_"), n.replace("-", ""))}
    achados = []
    for arq in sorted((pasta / "config").rglob("*")):
        if not arq.is_file() or arq.stat().st_size > 5_000_000:
            continue
        texto = arq.relative_to(pasta).as_posix().casefold()
        try:
            texto += "\n" + arq.read_text(errors="ignore").casefold()
        except OSError:
            continue
        if any(v in texto for v in variantes):
            achados.append(arq.relative_to(pasta).as_posix())
    return achados


def cmd_orfas(alvo):
    if not alvo:
        sys.exit(__doc__)
    arquivos = sorted((PACK / "mods").glob("*.pw.toml"))
    mods = {}
    for arq in arquivos:
        d = tomllib.loads(arq.read_text())
        m = d.get("update", {}).get("modrinth")
        if m:
            mods[arq.name.removesuffix(".pw.toml")] = {"nome": d["name"], "projeto": m["mod-id"], "versao": m["version"]}
    achados = [k for k, m in mods.items() if alvo.casefold() in (k.casefold(), m["nome"].casefold())] \
        or [k for k, m in mods.items() if alvo.casefold() in k.casefold() or alvo.casefold() in m["nome"].casefold()]
    if len(achados) != 1:
        sys.exit(f"{'Nenhum mod' if not achados else 'Vários mods'} de pack/mods bate com '{alvo}'"
                 + (f": {', '.join(achados)}." if achados else "."))
    raiz = achados[0]

    # Uma consulta só traz as dependências da versão de cada mod do pack.
    versoes = modrinth("versions?ids=" + urllib.parse.quote(json.dumps([m["versao"] for m in mods.values()])))
    obrigatorias = {}
    for v in versoes:
        dono = next(k for k, m in mods.items() if m["versao"] == v["id"])
        obrigatorias[dono] = {dep["project_id"] for dep in v["dependencies"]
                              if dep["dependency_type"] == "required" and dep.get("project_id")}
    por_projeto = {m["projeto"]: k for k, m in mods.items()}

    saem, mantidas = [raiz], {}
    mudou = True
    while mudou:
        mudou = False
        for dono in list(saem):
            for projeto in sorted(obrigatorias.get(dono, ())):
                dep = por_projeto.get(projeto)
                if not dep or dep in saem:
                    continue
                usam = [k for k, deps in obrigatorias.items() if projeto in deps and k not in saem]
                if usam:
                    mantidas[dep] = usam
                else:
                    saem.append(dep)
                    mantidas.pop(dep, None)
                    mudou = True
    orfas = saem[1:]

    print(f"Sai: {mods[raiz]['nome']} ({raiz}).")
    dependem = [k for k, deps in obrigatorias.items() if mods[raiz]["projeto"] in deps]
    if dependem:
        print("ATENÇÃO: exigem o mod que sai (saem junto ou o pack quebra): "
              + ", ".join(mods[k]["nome"] for k in dependem))
    print("Dependências que ficam sem uso:" + ("" if orfas else " nenhuma."))
    for k in orfas:
        print(f"  - {mods[k]['nome']} ({k})")
    for k, usam in sorted(mantidas.items()):
        print(f"Fica: {mods[k]['nome']}, ainda é exigida por " + ", ".join(mods[u]["nome"] for u in usam[:5])
              + (f" e mais {len(usam) - 5}" if len(usam) > 5 else "") + ".")
    print("(Só vale para o Modrinth. Dependências 'embedded' ou opcionais não contam; na dúvida, mantenha.)")

    pasta = pasta_configs()
    if not pasta:
        print("Configs: ../iunamc.minecraft-config não encontrado, não conferi.")
        return
    slugs = {k: modrinth(f"project/{mods[k]['projeto']}")["slug"] for k in saem}
    print("Configs que citam quem sai (confira antes de apagar; nada foi apagado):")
    for k in saem:
        citam = configs_que_citam(pasta, {slugs[k], k})
        print(f"  {mods[k]['nome']}: " + (", ".join(citam[:10]) + (f" e mais {len(citam) - 10}" if len(citam) > 10 else "")
                                          if citam else "nenhum arquivo."))


def cmd_lado(arquivos):
    if not arquivos:
        sys.exit(__doc__)
    erros = 0
    for arquivo in arquivos:
        caminho = Path(arquivo)
        dados = tomllib.loads(caminho.read_text())
        mod_id = dados.get("update", {}).get("modrinth", {}).get("mod-id")
        if not mod_id:
            print(f"{caminho.name}: sem [update.modrinth], side atual {dados.get('side', 'both')}.")
            continue
        req = urllib.request.Request(f"https://api.modrinth.com/v2/project/{mod_id}",
                                     headers={"User-Agent": f"{REPO} (github.com/{REPO})"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                projeto = json.load(r)
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"ERRO: {caminho.name}: não consegui ler o projeto {mod_id} no Modrinth ({e}).")
            erros += 1
            continue
        licenca = projeto.get("license", {}).get("id") or ""
        print(f"{dados['name']}: side atual {dados.get('side', 'both')}; Modrinth declara cliente "
              f"{projeto['client_side']}, servidor {projeto['server_side']}; licença {licenca or 'não informada'}.")
    if erros:
        sys.exit(1)


def main(args):
    if args[:1] == ["conferir"] and len(args) >= 3:
        cmd_conferir(args[1], args[2], opcao(args, "--ramo", None), os.environ.get("CORPO_PR", ""))
    elif args[:1] == ["versao"]:
        print(versao())
    elif args[:1] == ["neoforge"]:
        print(tomllib.loads((PACK / "pack.toml").read_text())["versions"]["neoforge"])
    elif args[:1] == ["readme"]:
        cmd_readme("--check" in args)
    elif args[:1] == ["mudancas"] and len(args) == 2:
        cmd_mudancas(args[1])
    elif args[:1] == ["proxima-beta"]:
        cmd_proxima_beta()
    elif args[:1] == ["orfas"]:
        cmd_orfas(" ".join(args[1:]))
    elif args[:1] == ["soltos"]:
        cmd_soltos()
    elif args[:1] == ["lado"]:
        cmd_lado(args[1:])
    elif args[:1] == ["externo"]:
        cmd_externo(args[1:])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
