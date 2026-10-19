# IUNA na CurseForge

O pack da CurseForge é o mesmo do `.mrpack`, **com** o Twilight Forest e o Mob
Grinding Utils, que o Modrinth não aceita. A página é feita à mão no site: a
API de upload da CurseForge envia arquivos, mas não edita o projeto, e nenhuma
API mostra arquivo em revisão. Mantenha esta pasta igual ao que está no site:

```sh
python3 scripts/curseforge.py descricao            # texto para colar no editor Markdown
python3 scripts/curseforge.py descricao --marcar   # depois de colar; commit do descricao.sha256
python3 scripts/curseforge.py status               # versões que já aparecem e se a descrição está em dia
```

| Arquivo | Uso |
| --- | --- |
| [`projeto.md`](projeto.md) | Campos para preencher ao criar ou editar o projeto |
| [`../modrinth/descricao.en.md`](../modrinth/descricao.en.md) | A descrição. É a mesma do Modrinth, mais a seção de créditos do `projeto.md` |
| [`../modrinth/imagens/`](../modrinth/imagens) | Logo e banner, os mesmos do Modrinth |

## Criar o projeto (uma vez)

1. Em <https://authors.curseforge.com>, entre em **Create Project** →
   **Minecraft** → **Modpacks** e preencha com o [`projeto.md`](projeto.md).
2. O projeto fica em revisão e só aparece em público depois que o primeiro
   arquivo for aprovado.
3. Em **My API Tokens**, gere um token. É o token de **upload**, enviado no
   header `X-Api-Token`; não é a API key do CurseForge for Studios. Depois,
   salve o token e o ID do projeto (aparece na lateral da página do projeto):

```sh
gh secret set CURSEFORGE_TOKEN -R IunaMC/modpack
```

```sh
gh variable set CURSEFORGE_PROJECT_ID -R IunaMC/modpack
```

## Como funciona

- **Versões:** o workflow [`Release`](../.github/workflows/release.yaml), depois
  do Modrinth, gera o `.zip` com `packwiz curseforge export` e o envia pelo
  [`scripts/curseforge.py`](../scripts/curseforge.py) (`beta` ou `release`,
  com as notas da release). Cada arquivo passa pela revisão da CurseForge.
- **Fonte de cada mod:** todo mod de cliente tem `[update.curseforge]` apontando
  para o mesmo arquivo do `.mrpack`. O `packwiz update` só segue o Modrinth.
  Depois de atualizar, rode:

```sh
python3 scripts/curseforge.py verificar --corrigir
```

  O Validar falha se algum mod ficar diferente nas duas fontes. Para um mod
  novo, use `python3 scripts/curseforge.py ligar <mod.pw.toml> <Project ID>`
  (o `/add-mod` já faz isso).

## Regras que pesam

- Um pack público só pode trazer mods hospedados na CurseForge ou que estejam na
  [lista de aprovados](https://docs.google.com/spreadsheets/d/176Wv-PZUo9hFxy6oC6N8tWdquBLPRtSuLbNK-r0_byM)
  ([regras](https://support.curseforge.com/support/solutions/articles/9000197908)).
  Permissão pessoal do autor não vale. Mod de fora precisa de crédito na
  descrição.
- Os mods `side = "server"` não entram no `.zip` da CurseForge. Eles continuam
  em `pack/` e no `.mrpack`, para o servidor.
