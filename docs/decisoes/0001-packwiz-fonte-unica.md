# 0001: packwiz como fonte única do jogador e do servidor

- **Data:** 16/10/2026
- **Estado:** aceita
- **Origem:** `44212fe` (prova de conceito em packwiz), `5139593` (pack como
  fonte única), versão `3.0.0`

## Contexto

Até a v2.2.4, o pack do jogador era um `.zip` montado à mão, e os mods do
servidor ficavam num repositório à parte (`modpack-servidor`). Os dois podiam
divergir, e cada versão exigia montar e enviar arquivos.

## Decisão

O pack vive em `pack/` como metadados do [packwiz](https://packwiz.infra.link/):
um `.pw.toml` por mod, com origem, hash e lado (`side`), sem nenhum jar no
repositório. O mesmo pack serve aos dois lados: `side = "server"` marca o que é
só do servidor, e `side = "client"` o que é só do jogador.

## Consequências

- O `.mrpack` e o `.zip` da CurseForge saem do pack por `packwiz mr export` e
  `packwiz curseforge export`.
- O servidor instala pelo `packwiz-installer`
  ([IunaMC/docs, decisão 0002](https://github.com/IunaMC/docs/blob/main/decisoes/0002-servidor-instala-da-main.md)).
- Quem vinha do `.zip` antigo precisa de uma instância nova.
- Jar sem download fixo precisa de um caminho próprio
  ([arquivos externos](../guias/arquivos-externos.md)).
- O `modpack-servidor` foi arquivado.
