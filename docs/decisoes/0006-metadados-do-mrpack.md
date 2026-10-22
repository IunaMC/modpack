# 0006: o que o .mrpack leva além dos mods

- **Data:** 22/10/2026
- **Estado:** aceita

## Contexto

O `.mrpack` é um zip com `modrinth.index.json` e as pastas `overrides/`,
`client-overrides/` e `server-overrides/`
([formato oficial](https://docs.modrinth.com/modpacks/format)). O
`packwiz mr export` gera o índice a partir do `pack/pack.toml`.

## O que o formato aceita

| Campo do índice | Origem no pack | Estado |
| --- | --- | --- |
| `name` | `name` do `pack.toml` ("IUNA Mark II") | ok; é o nome padrão da instância ao importar |
| `versionId` | `version` | ok |
| `summary` | `description` | **faltava**, agora preenchido |
| `dependencies` | `[versions]` (minecraft, neoforge) | ok |
| `files[].env` | `side` de cada `.pw.toml` | ok |

O formato **não tem** campo de ícone, autor, links nem changelog
([doc do Modrinth](https://support.modrinth.com/en/articles/8802351-modrinth-modpack-format-mrpack)).
`author` do `pack.toml` não entra no índice. O que cada launcher faz, lido no
código deles:

- **Modrinth App** (`install_mrpack.rs`): usa como ícone da instância um
  `icon.png` na raiz do zip, em `overrides/` ou em `client-overrides/`. Se o
  `overrides/` ou o `client-overrides/` tem `options.txt`,
  `config/yosbr/options.txt` ou `config/defaultoptions/options.txt`, ele trata
  isso como as opções padrão do pack. Descrição, links e ícone do projeto só
  vêm quando a instalação parte da página do projeto.
- **Prism**: o ícone é o que o usuário escolhe ao importar, ou um genérico
  "modrinth"; o `summary` não é lido. Em atualização, o `overrides/` sempre
  sobrescreve (o código tem um TODO sobre isso).

## Decisão

- `description` entra no `pack/pack.toml` (em português, uma frase), para o
  `summary` do índice aparecer ao importar.
- Nada mais cabe no `.mrpack` como metadado; não se tenta contornar.

- `name` passa a ser "IUNA Mark II".
- Seguir com `overrides/icon.png` (ícone no Modrinth App) e com um mod de
  opções padrão, o YOSBR (NeoForge), para o `options.txt`. Os dois entram
  nas sessões da instância e do cliente, não aqui.

## Notas para a instância criada ao importar

- O `name` vira o nome da instância e agora é "IUNA Mark II".
- Ícone: `overrides/icon.png` no pack faz o Modrinth App usar o ícone; no
  Prism não funciona (o usuário escolhe). Um `icon.png` em `overrides/` cairia
  na pasta da instância; avaliar se vale.
- Só `overrides/` e `client-overrides/` são aplicados ao cliente; o
  `server-overrides/` é ignorado e o workflow o tira do arquivo.
- Hoje o `.mrpack` leva só `overrides/mods/` (jars só da CurseForge). `pack/`
  não tem `config/`, `options.txt` nem `servers.dat`.
- `options.txt` em `overrides/` é sobrescrito a cada atualização no Prism. Para
  opções que o jogador possa mudar, o caminho é um mod de opções padrão
  (YOSBR), que só copia se o arquivo não existir; o Modrinth
  App já reconhece esses caminhos.
