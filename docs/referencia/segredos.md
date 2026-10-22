# Segredos

Nomes e permissões, nunca valores.

| Nome | Tipo | Usado por | Permissão | Renovar em |
| --- | --- | --- | --- | --- |
| `MODRINTH_TOKEN` | secret | Release, Modrinth | Página e versões do projeto | modrinth.com → Settings → PATs |
| `CURSEFORGE_TOKEN` | secret | Release | Envio de arquivos (token de upload, não a API key do Studios) | authors.curseforge.com → My API Tokens |
| `CURSEFORGE_PROJECT_ID` | variable | Release | ID do projeto na CurseForge | — |
| `MINECRAFT_CONFIG_TOKEN` | secret | Validar | Contents read no `minecraft-config` | GitHub → fine-grained PAT |
| `RESUMO_TOKEN` | secret | Resumo semanal | Contents, Actions, Issues e PRs read no `modpack`, `modpack-moderacao` e `minecraft-config` | GitHub → fine-grained PAT |

- Sem o `RESUMO_TOKEN`, o Resumo tenta o `MINECRAFT_CONFIG_TOKEN` e, por fim, o
  token do próprio workflow (que só lê este repositório).
- Sem o `MINECRAFT_CONFIG_TOKEN`, o Validar sobe o servidor só com os mods e
  avisa.
- Sem os tokens das plataformas, os scripts avisam e saem sem erro.
- Ao gerar um PAT, anote a data de expiração. O Resumo semanal mostra quantos
  dias faltam para o `RESUMO_TOKEN` e o `MINECRAFT_CONFIG_TOKEN` vencerem, com
  aviso abaixo de 14 dias (só a data sai na issue, nunca o token). Token
  vencido aparece como "recusado" no Resumo e como falha no Validar. Rodando
  `bash scripts/op.sh resumo` na sua máquina, exporte os dois nomes para ver a
  seção Tokens.

Para trocar um valor:

```sh
gh secret set <NOME> -R IunaMC/modpack
```

Os segredos das configs (token do bot e IDs do Discord, como marcadores
`{{NOME}}`) ficam no `minecraft-config`, documentados no `docs/segredos.md` de
lá.
