# 0005: o pack não perde mods por causa de uma plataforma

- **Data:** 18/10/2026
- **Estado:** aceita
- **Origem:** `4f5b1aa` (Twilight Forest sem permissão no Modrinth) e
  `bb59119` (envio do pack completo à CurseForge)

## Contexto

O Modrinth retém versões de modpack com arquivos de fora até cada um ter
permissão na página Permissions. Dois mods
ficaram sem ela:

- **The Twilight Forest:** o código é LGPL, mas sons e estruturas são All
  Rights Reserved, e a Team Twilight recusou o pedido de novo em
  [TeamTwilight/twilightforest#2985](https://github.com/TeamTwilight/twilightforest/issues/2985).
- **Mob Grinding Utils:** o pedido
  [vadis365/Mob-Grinding-Utils#372](https://github.com/vadis365/Mob-Grinding-Utils/issues/372)
  ficou sem resposta.

## Decisão

- O `.mrpack` do GitHub e o pack do servidor **nunca perdem mods** para
  agradar uma plataforma. O Twilight Forest é parte do servidor.
- O pack completo é publicado na CurseForge, onde esses mods estão hospedados.
- Não se abre pedido novo à Team Twilight.

## Consequências

- No Modrinth, as versões com esses mods ficam retidas.
- Um `.mrpack` reduzido só para o Modrinth foi feito na
  [0007](0007-mrpack-reduzido-no-modrinth.md) e abandonado na
  [0008](0008-sem-distribuicao-no-modrinth.md): o pack não é mais distribuído
  no Modrinth, e a CurseForge é a única loja.
