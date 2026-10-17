# Publicar no Modrinth

Parte 1: a primeira publicação, feita à mão. Parte 2: o plano para o workflow
de release publicar sozinho as versões seguintes. A parte 2 ainda **não está
implementada**.

## Parte 1: primeira publicação

### Antes de começar

- [ ] Decisões de [`projeto.md`](projeto.md) tomadas: nome, slug, licença e
      aviso de IA já estão; falta o Discord.
- [ ] Ícone e capturas da galeria prontos.
- [ ] Respostas dos autores de Fire's Ender Expansion e Mob Grinding Utils
      (e, se quiser garantir, de Astral Sorcery) salvas como captura de tela.
      Sem elas, dá para criar o projeto e enviar a versão, mas a revisão não
      anda. Veja [`permissoes.md`](permissoes.md).
- [ ] A versão a publicar já tem release no GitHub (a v3.0.0 já tem).

### 1. Gerar o `.mrpack` do Modrinth

Use o `.mrpack` da release do GitHub. Desde a v3.0.0 o workflow de release já
tira `server-overrides/` (os jars só de servidor, alguns All Rights Reserved),
então o arquivo serve como está:

```sh
gh release download v3.0.0 -R IunaMC/modpack-cliente -p '*.mrpack'
unzip -l IUNA-3.0.0.mrpack | grep -E 'overrides/mods/'
```

A última linha deve listar 14 jars, todos em `overrides/mods/`, e nenhum em
`server-overrides/`.

### 2. Criar a organização

Já feito: a organização é a **IUNA** (`iuna`). Veja a seção 5 de
[`projeto.md`](projeto.md).

### 3. Criar o projeto

1. Na página da organização, crie um projeto do tipo **Modpack**.
2. Nome `IUNA`, URL `iuna`, visibilidade **Public**.
3. Resumo: o de [`projeto.md`](projeto.md).
4. Em **Settings**:
   - **General:** ícone.
   - **Description:** cole o conteúdo de [`descricao.en.md`](descricao.en.md) (o inglês é o idioma principal da página) e,
     no fim, o português dentro de um bloco recolhível, assim:

     ```markdown
     <details>
     <summary>Português</summary>

     (conteúdo de descricao.md)

     </details>
     ```

     Troque os `<...>` (Discord e as permissões de Fire's Ender Expansion e
     Mob Grinding Utils na tabela de créditos) pelos valores reais, ou apague
     as linhas.
   - **Tags:** principais `technology`, `magic`, `adventure`; adicionais
     `kitchen-sink`, `multiplayer`, `combat`.
   - **Environments:** *Client and server, required on both*.
   - **License:** a escolhida (ex.: MIT, com a URL do `LICENSE` do repositório).
   - **Links:** source, issues e, se houver, Discord público e wiki.
   - **Disclosures:** marque *Contains AI-generated content* se mantiver os
     textos como estão.
5. **Gallery:** envie as capturas e marque a do Create como destacada.

### 4. Enviar a versão

1. Em **Versions → Create version**, envie `IUNA-3.0.0.mrpack`.
2. Preencha:
   - **Version number:** `3.0.0`
   - **Version title:** `IUNA 3.0.0`
   - **Release channel:** `Release`
   - **Loaders:** NeoForge · **Game versions:** 1.21.1 (o Modrinth lê do
     `.mrpack`; confira)
   - **Environment:** *Client and server*
   - **Changelog:** o conteúdo de `MUDANCAS.md`
   - **Dependencies:** nenhuma. Os mods externos são creditados sozinhos na
     página da versão.
3. Salve. A versão fica **retida** por ter arquivos externos.

### 5. Resolver as permissões

1. Abra **Settings → Permissions** (ou o aviso na versão).
2. Para cada arquivo, marque a opção e cole o link de [`permissoes.md`](permissoes.md).
3. Para os que dependem do autor, marque **Special permission** e envie a
   captura da resposta na aba **Moderation** do projeto. Enquanto não houver
   resposta, marque **No permission**.
4. Quando todos estiverem *Completed*, envie o projeto para revisão
   (**Submit for review**). A maioria sai em 24 a 48 horas.

### 6. Depois da aprovação

- [ ] Troque o link provisório no `README.md` pelo link real.
- [ ] Anuncie na comunidade.
- [ ] Siga a parte 2 para automatizar as próximas versões.

## Parte 2: plano para automatizar (não implementado)

### O que muda no repositório

- **Secret** `MODRINTH_TOKEN`: token pessoal (PAT) da conta que publica, criado
  em *Settings → Personal access tokens* do Modrinth, só com o escopo
  **Create versions** (`VERSION_CREATE`) e com validade definida. Renove antes
  de vencer.
- **Variável** `MODRINTH_PROJECT_ID`: o ID do projeto (8 caracteres, aparece
  em *Settings → General* ou em `GET https://api.modrinth.com/v2/project/iuna`).
  Usar o ID, e não o slug, evita quebrar se o slug mudar.
- Sem a variável, o passo é pulado: o workflow continua só com a release do
  GitHub.

### Onde entra no `release.yaml`

Depois do passo **Criar tag e release**, com a condição
`vars.MODRINTH_PROJECT_ID != ''`. Este passo **não** deve depender de
`steps.versao.outputs.existe`: assim, se o envio ao Modrinth falhar, rodar o
workflow de novo pela aba Actions publica só no Modrinth. Para isso, quando a
release do GitHub já existir, o `.mrpack` vem de
`gh release download "v$VERSAO" -p '*.mrpack'` em vez do export (e os passos
do packwiz e do export passam a rodar só quando precisarem).

1. **Montar o `.mrpack` do Modrinth:** usar o mesmo arquivo da release, que
   já sai sem `server-overrides/`. Se algum mod do jogador ficar sem
   permissão, ler a lista de jars a tirar de um arquivo versionado (ex.:
   `modrinth/sem-permissao.txt`) e rodar `zip -d`, para que liberar um
   mod seja só apagar uma linha.
2. **Conferir se a versão já existe no Modrinth**, para poder rodar de novo
   sem duplicar:
   `GET https://api.modrinth.com/v2/project/$MODRINTH_PROJECT_ID/version`
   e procurar `version_number == "$VERSAO"`.
3. **Criar a versão** com `POST https://api.modrinth.com/v2/version`
   ([documentação](https://docs.modrinth.com/api/operations/createversion/)).

### A chamada

`multipart/form-data` com duas partes: `data` (JSON) e o arquivo. O cabeçalho
`Authorization` leva o token puro, e o `User-Agent` precisa identificar o
projeto ([regras da API](https://docs.modrinth.com/api/)).

```sh
jq -n \
  --arg projeto "$MODRINTH_PROJECT_ID" \
  --arg versao "$VERSAO" \
  --arg mc "$(cd pack && sed -n 's/^minecraft = "\(.*\)"/\1/p' pack.toml)" \
  --arg tipo "$( [[ "$VERSAO" == *-* ]] && echo beta || echo release )" \
  --rawfile notas "$RUNNER_TEMP/notas.md" \
  '{
     project_id: $projeto,
     name: ("IUNA " + $versao),
     version_number: $versao,
     changelog: $notas,
     dependencies: [],
     game_versions: [$mc],
     loaders: ["neoforge"],
     version_type: $tipo,
     featured: true,
     status: "listed",
     environment: "client_and_server",
     file_parts: ["arquivo"],
     primary_file: "arquivo"
   }' > "$RUNNER_TEMP/versao.json"

curl --fail-with-body -sS https://api.modrinth.com/v2/version \
  -H "Authorization: $MODRINTH_TOKEN" \
  -H "User-Agent: IunaMC/modpack-cliente (github.com/IunaMC/modpack-cliente)" \
  -F "data=<$RUNNER_TEMP/versao.json;type=application/json" \
  -F "arquivo=@IUNA-$VERSAO.mrpack;type=application/x-modrinth-modpack+zip"
```

Campos obrigatórios da versão, pela
[OpenAPI](https://docs.modrinth.com/openapi.yaml): `project_id`, `file_parts`,
`name`, `version_number`, `game_versions`, `version_type`, `loaders`,
`featured` e `dependencies`. `loaders` é `["neoforge"]` e `game_versions` vem
do `pack.toml`.

### Action pronta ou curl?

- **curl (recomendado):** são duas chamadas, sem dependência de terceiros e
  com o token só no passo que precisa dele. É o mesmo padrão do workflow, que
  já usa `gh` direto.
- **[`Kir-Antipov/mc-publish`](https://github.com/Kir-Antipov/mc-publish):** a
  action mais usada para publicar no Modrinth e CurseForge. Se preferir, fixe
  pelo SHA do commit (não pela tag) e informe `loaders` e `game-versions` à
  mão, porque ela é pensada para jars de mod.

### Limites da automação

- **Arquivo externo novo trava a versão.** Se uma release trouxer um mod do
  CurseForge que ainda não está na página Permissions, a versão fica retida
  até alguém marcar a permissão no site. Atualizar um mod que já está lá
  costuma não pedir nada novo. O workflow pode avisar: comparar os jars em
  `overrides/` com os da release anterior e emitir um `::warning::` com os
  novos.
- **Mod sem permissão entrando no pack** precisa ir para a lista de exclusão
  antes da release, ou a versão fica retida.
- **Token vencido** faz o passo falhar com 401. A release do GitHub já terá
  saído; basta renovar o secret e rodar o workflow de novo pela aba Actions,
  que a conferência do passo 2 evita duplicar.
