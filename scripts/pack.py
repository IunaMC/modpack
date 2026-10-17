#!/usr/bin/env python3
"""Ferramentas do pack: lista de mods do README e changelog de mods.

Lê os metadados do packwiz (pack/pack.toml e pack/mods/*.pw.toml).

Uso:
  python3 scripts/pack.py versao              # imprime a versão do pack.toml
  python3 scripts/pack.py readme              # regenera a lista de mods no README.md
  python3 scripts/pack.py readme --check      # falha se a lista do README estiver desatualizada
  python3 scripts/pack.py mudancas <ref-git>  # mods adicionados/removidos/atualizados desde <ref-git>
"""
import subprocess
import sys
import tomllib
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PACK = RAIZ / "pack"
README = RAIZ / "README.md"
INICIO = "<!-- lista-de-mods:inicio -->"
FIM = "<!-- lista-de-mods:fim -->"
LADOS = {"both": "Cliente e servidor", "client": "Cliente", "server": "Servidor"}


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
    obrigatorios = [m for m in mods if not m["opcional"]]
    opcionais = [m for m in mods if m["opcional"]]
    return "\n".join([
        INICIO,
        "<!-- Gerado por scripts/pack.py readme. Não edite à mão. -->",
        "",
        f"O pack tem **{len(mods)} mods**: {len(obrigatorios)} obrigatórios e {len(opcionais)} opcionais.",
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


def main(args):
    if args[:1] == ["versao"]:
        print(versao())
    elif args[:1] == ["readme"]:
        cmd_readme("--check" in args)
    elif args[:1] == ["mudancas"] and len(args) == 2:
        cmd_mudancas(args[1])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
