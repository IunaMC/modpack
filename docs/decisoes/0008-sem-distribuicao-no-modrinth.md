# 0008: o pack não é distribuído no Modrinth

- **Data:** 27/10/2026
- **Estado:** aceita
- **Substitui:** a [0007](0007-mrpack-reduzido-no-modrinth.md)

## Contexto

O projeto `iuna` está em `processing` no Modrinth desde 17/10/2026 e a página
pública dá 404. A [0007](0007-mrpack-reduzido-no-modrinth.md) tentou destravar a
aprovação com um `.mrpack` reduzido, sem o Twilight Forest e o Mob Grinding
Utils, mas o caminho custou uma pasta `modrinth/`, um script próprio, um
workflow, a lista `[[reduzido.fora]]`, a página Permissions e um passo a mais
para quem instalasse por lá.

A CurseForge já opera: o projeto foi aprovado em 22/10/2026 e recebe o pack
completo, com os dois mods, a cada versão. O `.mrpack` completo da release do
GitHub atende quem prefere importar o arquivo.

## Decisão

- O pack deixa de ser publicado no Modrinth. Saem a pasta `modrinth/`, o
  `scripts/modrinth.py`, o workflow Modrinth, o passo "Publicar no Modrinth" do
  Release, o `.mrpack` reduzido e a regra de permissões da página Permissions.
- A CurseForge é a única loja do pack. Continua valendo a fonte dupla: todo
  `.pw.toml` que não é `server` tem `[update.modrinth]` e `[update.curseforge]`
  para o mesmo arquivo, conferidos pelo `scripts/curseforge.py verificar`.
- O Modrinth continua como **fonte** dos mods: o `packwiz update` o segue, e o
  servidor e o `.mrpack` baixam de `cdn.modrinth.com`.
- O `.mrpack` completo segue na release do GitHub (`iuna.club/mrpack`).
- O logo e o banner, que a CurseForge usa, ficam em `curseforge/imagens/`.

## Consequências

- Mod novo só da CurseForge não precisa de permissão em lugar nenhum além da
  licença, que já vale para a CurseForge e para a release do GitHub.
- O projeto `iuna` no Modrinth e o secret `MODRINTH_TOKEN` não são mais usados
  pelo repositório. Arquivar o projeto ou apagar o secret é com o dono, no site
  e nas configurações do GitHub.
- Se a CurseForge sair do ar ou recusar o pack, sobra só o `.mrpack` do GitHub.
  Um plano B para esse caso fica fora desta decisão.
