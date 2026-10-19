# Workflows

Os workflows deste repositório e o que roda igual na sua máquina.

| Workflow | Quando roda | O que faz | Equivalente local |
| --- | --- | --- | --- |
| [Validar](../../.github/workflows/validar.yaml) | Push fora da `main` que mexe em `pack/`, `scripts/`, `README.md` ou `.github/` (o resultado aparece no PR); manual | Confere a lista de mods do README, a fonte da CurseForge e o índice; exporta `.mrpack` e `.zip`; sobe um servidor com as configs da `main` do `minecraft-config` | `bash scripts/op.sh conferir` e `bash scripts/testar-servidor.sh --configs` ([servidor local](../guias/servidor-local.md)) |
| [Release](../../.github/workflows/release.yaml) | Push na `main` ou na `devel/devel` com versão nova; manual | Tag, GitHub Release com o `.mrpack` e as notas, envio ao Modrinth e à CurseForge | `cd pack && packwiz mr export`, depois `python3 scripts/modrinth.py publicar <v> <mrpack> MUDANCAS.md --simular`; `cd pack && packwiz curseforge export -o ../IUNA.zip`, depois `python3 scripts/curseforge.py publicar <v> IUNA.zip MUDANCAS.md --simular` |
| [Modrinth](../../.github/workflows/modrinth.yaml) | Push que muda `modrinth/`; manual | Fora da `main`, mostra o que mudaria; na `main`, aplica textos, links e galeria | `python3 scripts/modrinth.py sincronizar --simular` |
| [Docs](../../.github/workflows/docs.yaml) | Push ou PR que muda algum `.md`; manual | Links internos e âncoras (`lychee --offline`) e estilo (`markdownlint-cli2`) | `npx markdownlint-cli2 '**/*.md'` |
| [Atualizações de mods](../../.github/workflows/atualizacoes.yaml) | Segunda, 10h23 UTC; manual | Issue com os mods que têm versão nova | `cd pack && packwiz update --all`, `git diff`, depois `git checkout pack/` |
| [Resumo semanal](../../.github/workflows/resumo.yaml) | Segunda, 10h53 UTC; manual | Issue "Resumo semanal" com o estado dos três repositórios | `bash scripts/op.sh resumo` |

Os workflows de agenda só rodam na `main`. Um workflow novo começa a valer
depois da estável seguinte.

## Peças compartilhadas

- [`.github/actions/packwiz`](../../.github/actions/packwiz/action.yml):
  instala o packwiz numa versão fixa e falha se o `index.toml` estiver
  desatualizado.
- [`.github/dependabot.yml`](../../.github/dependabot.yml): atualiza as
  actions todo mês, com commits `build(workflows): …`.

Os tokens que eles usam estão em [segredos](segredos.md).
