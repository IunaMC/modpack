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

| Branch | Papel | Regras |
| --- | --- | --- |
| `devel/devel` | Desenvolvimento e betas | Permanente: nunca é apagada. Depois de cada estável, volta a alinhar com `git merge --ff-only origin/main` |
| `main` | Só estáveis; o servidor instala daqui | Recebe só PR da `devel/devel`, com merge commit. O Release recusa beta e qualquer mudança em `pack/` sem versão nova |

Na `devel/devel`, uma versão estável não publica nada. Os motivos estão nas
decisões [0002](../decisoes/0002-merge-commit-assinado.md) e
[0003](../decisoes/0003-devel-permanente-main-estavel.md).

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
