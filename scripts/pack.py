#!/usr/bin/env python3
"""Ferramentas do pack: lista de mods do README, changelog de mods e arquivos externos.

Lê os metadados do packwiz (pack/pack.toml e pack/mods/*.pw.toml).

Uso:
  python3 scripts/pack.py versao              # imprime a versão do pack.toml
  python3 scripts/pack.py neoforge            # imprime a versão do NeoForge do pack.toml
  python3 scripts/pack.py readme              # regenera a lista de mods no README.md
  python3 scripts/pack.py readme --check      # falha se a lista do README estiver desatualizada
  python3 scripts/pack.py mudancas <ref-git>  # mods adicionados/removidos/atualizados desde <ref-git>
  python3 scripts/pack.py proxima-beta        # próxima versão beta pelo SemVer (o motivo vai para o stderr)
  python3 scripts/pack.py externo <jar> [opções]
      # anexa o jar à release arquivos-servidor e cria o .pw.toml que aponta para ele.
      # Opções: --lado server|both|client (padrão server), --nome, --versao, --autor,
      # --licenca, --origem (o padrão de cada uma vem dos metadados do jar) e --simular,
      # que mostra o que seria feito sem enviar nem gravar nada. Veja docs/arquivos-externos.md.
"""
import hashlib
import json
import re
import subprocess
import sys
import tomllib
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
        "opcional": dados.get("option", {}).get("optional", False),
        "link": link,
    }


def mods_atuais():
    return {p.name: ler_mod(p.read_text()) for p in sorted((PACK / "mods").glob("*.pw.toml"))}


def mods_em(ref):
    """Mods do pack em um ref do git; vazio se o ref não tiver o pack."""
    git = ["git", "-C", str(RAIZ)]
    ls = subprocess.run(git + ["ls-tree", "--name-only", f"{ref}:pack/mods"],
                        capture_output=True, text=True)
    if ls.returncode != 0:
        return {}
    mods = {}
    for nome in ls.stdout.split():
        if nome.endswith(".pw.toml"):
            texto = subprocess.run(git + ["show", f"{ref}:pack/mods/{nome}"],
                                   capture_output=True, text=True, check=True).stdout
            mods[nome] = ler_mod(texto)
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
    mods = list(mods_atuais().values())
    servidor = [m for m in mods if m["lado"] == "server"]
    cliente = [m for m in mods if m["lado"] != "server"]
    obrigatorios = [m for m in cliente if not m["opcional"]]
    opcionais = [m for m in cliente if m["opcional"]]
    return "\n".join([
        INICIO,
        "<!-- Gerado por scripts/pack.py readme. Não edite à mão. -->",
        "",
        f"O pack tem **{len(mods)} mods**. O jogador recebe {len(cliente)} "
        f"({len(obrigatorios)} obrigatórios e {len(opcionais)} opcionais), e o servidor, "
        f"{len(mods) - sum(1 for m in mods if m['lado'] == 'client')}.",
        "",
        "### Obrigatórios",
        "Necessários para entrar no servidor. O launcher instala todos.",
        "",
        tabela(obrigatorios),
        "",
        "### Opcionais",
        "Melhorias visuais e de qualidade de vida. O launcher pergunta quais você quer na instalação.",
        "",
        tabela(opcionais),
        "",
        "### Só no servidor",
        "Administração, desempenho e geração de mundo. O launcher do jogador ignora estes.",
        "",
        tabela(servidor),
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


def cmd_mudancas(ref):
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


def main(args):
    if args[:1] == ["versao"]:
        print(versao())
    elif args[:1] == ["neoforge"]:
        print(tomllib.loads((PACK / "pack.toml").read_text())["versions"]["neoforge"])
    elif args[:1] == ["readme"]:
        cmd_readme("--check" in args)
    elif args[:1] == ["mudancas"] and len(args) == 2:
        cmd_mudancas(args[1])
    elif args[:1] == ["proxima-beta"]:
        cmd_proxima_beta()
    elif args[:1] == ["externo"]:
        cmd_externo(args[1:])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
