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

O formato **não tem** ícone, autor, links nem changelog. `author` do
`pack.toml` não entra no índice. Ícone, descrição longa, links e notas ficam no
projeto do Modrinth (`modrinth/`), e os launchers só os mostram quando o pack é
instalado pela página do projeto, não ao importar o arquivo. O ícone da
instância importada vem da pasta da instância (assunto da sessão da instância).

## Decisão

- `description` entra no `pack/pack.toml` (em português, uma frase), para o
  `summary` do índice aparecer ao importar.
- Nada mais cabe no `.mrpack` como metadado; não se tenta contornar.

## Notas para a instância criada ao importar

- O `name` vira o nome da instância: "IUNA Mark II" (marco da segunda
  temporada). O projeto no Modrinth ainda se chama "IUNA 2", nome que é
  independente do `pack.toml`.
- Ícone: `pack/icon.png` vira `overrides/icon.png` no `.mrpack` (conferido com
  `packwiz modrinth export`); o Modrinth App usa como ícone da instância. O
  Prism ignora e deixa o usuário escolher.
- Só `overrides/` e `client-overrides/` são aplicados ao cliente; o
  `server-overrides/` é ignorado por launchers e o workflow o tira do arquivo.
- Hoje o `.mrpack` leva só `overrides/mods/` (jars só da CurseForge). `pack/`
  não tem `config/`, `options.txt` nem `servers.dat`: qualquer um desses entra
  como arquivo no `pack/` (packwiz o põe em `overrides/`).
- `servers.dat` com o servidor (`jogar.iuna.club`, nome "IUNA") fica em
  `pack/config/yosbr/servers.dat`. O YOSBR o copia para a raiz da instância
  só na primeira abertura e nunca sobrescreve, então a lista do jogador
  sobrevive às atualizações. Em `overrides/` direto, cada atualização
  apagaria os servidores que ele adicionou. Decidido em 22/10/2026.
- `options.txt` em `overrides/` sobrescreve o do jogador a cada atualização do
  pack; arquivos que o jogador edita (options, servers.dat) merecem atenção.
