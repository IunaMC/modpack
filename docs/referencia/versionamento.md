# Versionamento, branches e commits

As regras fixas deste repositório. O `CLAUDE.md` repete o mínimo para o Claude
Code; quando os dois divergirem, esta página vale e o `CLAUDE.md` é corrigido.

## Versão

SemVer em `version`, no [`pack/pack.toml`](../../pack/pack.toml):

| Parte | Quando sobe | Exemplos |
| --- | --- | --- |
| **MAJOR** | Exige mundo novo ou reinstalar tudo | Minecraft, NeoForge, troca de formato do pack, reset |
| **MINOR** | Qualquer mod adicionado, atualizado ou removido | Mod novo, atualização, remoção de mod de conteúdo |
| **PATCH** | Nada muda para o jogador | Config, docs, CI |

- **Beta:** `X.Y.Z-beta.N`, publicada por push na `devel/devel` como
  *pre-release*. O servidor não a instala.
- **Estável:** `X.Y.Z`, publicada pelo merge na `main`.
- As notas da versão ficam no [`MUDANCAS.md`](../../MUDANCAS.md). O Release
  junta a elas a lista de mods mudados desde a release anterior (a estável
  compara com a estável anterior).
- `python3 scripts/pack.py proxima-beta` sugere a próxima versão pelos
  commits.

## Branches

Duas branches de integração, permanentes, levam à `main`. Cada uma recebe as
branches curtas do seu assunto.

```text
devel/<tarefa> ──PR──► devel/devel ──PR──► main ◄──PR── docs/docs ◄──PR── docs/<assunto>
```

| Branch | Papel | Regras |
| --- | --- | --- |
| `main` | Só estáveis; o servidor instala daqui | Recebe só PR, com merge commit, da `devel/devel` ou da `docs/docs`. O job *Entrada na main* tem de passar ([regras](#o-que-entra-na-main)) |
| `devel/devel` | Integração: pack, scripts, CI e docs ligados a código; betas | Permanente. Depois de cada estável, volta a alinhar com `git merge --ff-only origin/main`; depois de um merge da `docs/docs`, com `git merge origin/main` |
| `devel/<tarefa>` | Trabalho de uma tarefa, opcional | Sai da `devel/devel` e volta para ela por PR. Pode ser apagada depois |
| `docs/docs` | Integração: documentação que não depende de código | Permanente. Não pode mexer em `pack/`. Depois de cada merge na `main`, recebe a `main` (`git merge origin/main`) |
| `docs/<assunto>` | Uma mudança de documentação | Sai da `docs/docs` e volta para ela por PR. Pode ser apagada depois |

Documentação que acompanha uma mudança de código (o guia de um script novo,
por exemplo) vai no mesmo PR do código, pela `devel/devel`. A `docs/docs` é
para o que pode chegar à `main` sem esperar uma versão: correções, páginas
novas, links ([guia](../guias/publicar-docs.md)).

Na `devel/devel`, uma versão estável não publica nada. Os motivos estão nas
decisões [0002](../decisoes/0002-merge-commit-assinado.md) e
[0003](../decisoes/0003-devel-permanente-main-estavel.md).

## O que entra na main

O servidor instala a `main` a cada boot, então ela tem duas proteções:

- **Trava, antes do merge:** o workflow
  [*Entrada na main*](../../.github/workflows/main.yaml) roda em todo PR para a
  `main`, e o *ruleset* da `main` só libera o merge com ele verde. O ruleset
  também exige PR, aceita só merge commit, exige commits assinados e bloqueia
  force push e exclusão da branch.
- **Alarme, depois do merge:** o [Release](../../.github/workflows/release.yaml)
  repete a conferência em todo push na `main` que mexe em `pack/` e não
  publica nada se ela falhar.

As duas rodam `python3 scripts/pack.py conferir <base> <topo>`, que também roda
na sua máquina:

```sh
python3 scripts/pack.py conferir origin/main HEAD --ramo devel/devel
```

| O PR… | Resultado |
| --- | --- |
| Não mexe em `pack/` (docs, CI, scripts) | ✅ entra, sem release |
| Mexe em `pack/` e sobe a versão | ✅ entra, e o Release publica |
| Mexe em `pack/` sem subir a versão | ❌ "suba a versão no `pack/pack.toml`" |
| Só sobe a versão, sem mudar mais nada no pack | ❌ para reenviar uma versão às plataformas, rode o Release à mão |
| Traz versão beta | ❌ beta só sai da `devel/devel` |
| Pula versão ou volta (`3.3.0` → `3.6.0` ou `3.2.1`) | ❌ só vale a próxima: `3.3.1`, `3.4.0` ou `4.0.0` |
| Sobe a MAJOR | ❌ até o corpo do PR ter a frase "MAJOR confirmado" |
| Vem de outra branch que não `devel/devel` ou `docs/docs` | ❌ |
| Vem da `docs/docs` e mexe em `pack/` | ❌ leve pela `devel/devel` |

Tudo que estiver dentro de `pack/` conta como mudança do pack, inclusive
configs, `servers.dat` e outros arquivos da instância quando entrarem.

## Commits

- Assinados e com DCO: `git commit -S -s`.
- [Conventional Commits](https://www.conventionalcommits.org/pt-br/) em
  português:

  | Tipo | Uso |
  | --- | --- |
  | `feat(mods): adiciona\|remove\|atualiza <Nome> <versão>` | Um commit por mod |
  | `feat(deps): …` | Dependência, sempre antes do mod que a usa |
  | `build: prepara a versao <versão>` | Troca de versão |
  | `build(workflows): …` | Workflows e actions |
  | `feat(scripts): …`, `fix(scripts): …` | Scripts |
  | `docs: …`, `docs(<área>): …` | Documentação |

- Não repita "mod" no texto: o escopo já diz.
- Sem `Co-Authored-By` nem menção a ferramentas de IA, em commit, PR, issue ou
  release.
- PR mergeado com `gh pr merge --merge`. Nunca `--rebase`, que recria os
  commits sem assinatura.
