# 0007: o Modrinth recebe um .mrpack reduzido

- **Data:** 22/10/2026
- **Estado:** substituída pela [0008](0008-sem-distribuicao-no-modrinth.md) em 27/10/2026
- **Origem:** consequência da [0005](0005-mrpack-completo-sem-cortar-mods.md)

## Contexto

O projeto `iuna` está em `processing` no Modrinth desde 17/10/2026 e a página
pública dá 404. O que trava a aprovação são dois jars embutidos em
`overrides/mods/` sem permissão na página Permissions: **The Twilight Forest**
(a equipe recusou em
[TeamTwilight/twilightforest#2985](https://github.com/TeamTwilight/twilightforest/issues/2985))
e **Mob Grinding Utils** (pedido sem resposta).

Pastel Shaders e Super Duper Vanilla chegaram a ser apontados como sem
permissão, mas não são problema. Os dois são baixados de `cdn.modrinth.com`, e o
índice só faz referência a eles, sem redistribuir nada. Arquivo hospedado no
próprio Modrinth não passa pela página Permissions.

Os dois mods cortados são `side = both`, e o Twilight Forest – Dungeons &
Villages (do Modrinth) depende do Twilight. Sem os dois jars, o jogo não abre
e o NeoForge mostra qual mod falta.

## Decisão

- A [0005](0005-mrpack-completo-sem-cortar-mods.md) continua valendo. O
  `pack/`, o `.mrpack` da release do GitHub, a CurseForge e o servidor seguem
  completos.
- O Modrinth recebe um `.mrpack` **reduzido**, gerado do completo por
  `scripts/modrinth.py reduzir`. O comando tira os jars da lista
  `[[reduzido.fora]]` de `modrinth/projeto.toml` e nada mais. O Dungeons &
  Villages fica no reduzido: o pack continua o mesmo e a tela de erro aponta o
  que falta.
- O reduzido se chama `IUNA-<versão>-modrinth.mrpack` e não vai para a release
  do GitHub, para ninguém o baixar pelo `iuna.club/mrpack` por engano.
- O corte não se disfarça. A página diz no começo quais mods ficam de fora e
  como adicioná-los pelo launcher, e o `verificar` exige o nome de cada um nas
  duas descrições. O changelog de cada versão leva o arquivo exato de cada mod
  na CurseForge.
- As versões antigas, que embutem os dois jars, saem do Modrinth com
  `scripts/modrinth.py limpar`. Apagar é irreversível: o comando só lista, e
  quem apaga é o dono do projeto, com `--apagar`, depois de a primeira versão
  reduzida estar lá.

## Consequências

- No Modrinth, quem instala o pack tem um passo a mais: adicionar dois mods
  pela CurseForge. O Prism faz isso pelo próprio launcher. No Modrinth App, que
  só busca no Modrinth, o jogador baixa os jars e os põe na pasta `mods`.
- Mod novo sem permissão no Modrinth entra na lista `[[reduzido.fora]]` e nas
  duas descrições, não sai do pack.
- O servidor e o teste de boot não mudam. O Validar gera o reduzido do
  `.mrpack` de teste para conferir a lista.
