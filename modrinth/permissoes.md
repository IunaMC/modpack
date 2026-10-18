# Permissões dos arquivos externos

Desde 23/06/2026, uma versão de modpack com arquivos que não estão no Modrinth
fica **retida** até cada arquivo ter origem e permissão na página
**Permissions** do projeto
([notícia](https://modrinth.com/news/article/modpack-permissions)). Para cada
arquivo há quatro opções, com um link ou uma explicação curta:

- **License:** a licença do projeto permite redistribuir. Prova: link para a
  fonte (o Modrinth faz o link de volta que algumas licenças pedem).
- **Your project:** você fez o conteúdo.
- **Special permission:** o dono deu permissão verificável. Exige prova.
- **No permission:** sem permissão. Serve de lembrete: consiga a permissão ou
  tire o arquivo.

A página agrupa arquivos do mesmo projeto entre versões; atualizações de um
arquivo já identificado costumam não pedir nova permissão.

Segundo a [ajuda do Modrinth](https://support.modrinth.com/en/articles/8797527),
também vale como permissão uma frase do autor na descrição do projeto
autorizando o uso em modpacks, e, quando o autor responde a um pedido, a prova
é a captura de tela da resposta enviada na aba **Moderation** do projeto.

## Como a licença foi conferida

Exportei o pack (`cd pack && packwiz mr export`), abri cada jar de
`overrides/mods/` e `server-overrides/mods/` e li o campo `license` do
`META-INF/neoforge.mods.toml`. Depois conferi o arquivo de licença do
repositório de código e, quando não havia, a licença mostrada na página do
CurseForge. Conferência de 16/10/2026, versão 3.0.0 do pack.

## Arquivos que o jogador recebe (`overrides/mods/`)

| Mod | Arquivo | Licença no jar | Licença verificada | Opção | Link de prova |
| --- | --- | --- | --- | --- | --- |
| The Twilight Forest | `twilightforest-1.21.1-4.8.3345-universal.jar` | LGPL 2.1 | Código LGPL 2.1, mas sons e estruturas **All Rights Reserved** (README do repositório) | **No permission** | https://github.com/TeamTwilight/twilightforest#licensing |
| Ice and Fire CE | `iceandfire-2.1.3.jar` | LGPL-3.0 | LGPL 3.0 ou posterior (`LICENSE`) | **License** | https://github.com/IAFEnvoy/IceAndFire-CE/blob/master/LICENSE |
| Uranus | `uranus-3.0-beta.1.jar` | LGPL-3.0 | LGPL 3.0 ou posterior (`LICENSE`) | **License** | https://github.com/IAFEnvoy/Uranus/blob/master/LICENSE |
| Flux Networks | `FluxNetworks-1.21.1-8.0.0.jar` | MIT | MIT (`LICENSE`) | **License** | https://github.com/SonarSonic/Flux-Networks/blob/1.20/LICENSE |
| Building Gadgets 2 | `buildinggadgets2-1.3.9.jar` | MIT | MIT (`LICENSE`) | **License** | https://github.com/Direwolf20-MC/BuildingGadgets2/blob/main/LICENSE |
| Refurbished Furniture | `refurbished_furniture-neoforge-1.21.1-1.0.22.jar` | MIT | MIT (`LICENSE` do repositório e `LICENSE_refurbished_furniture` no jar) | **License** | https://github.com/MrCrayfish/MrCrayfishFurnitureMod-Refurbished/blob/26.1.2/LICENSE |
| Framework | `framework-neoforge-1.21.1-0.13.11.jar` | LGPLv2.1 | LGPL 2.1 (`LICENSE` e `LICENSE_framework` no jar) | **License** | https://github.com/MrCrayfish/Framework/blob/multiloader/26.3/LICENSE |
| ObserverLib | `observerlib-1.10.3.jar` | LGPL 3.0 | LGPL 3.0 (`LICENCE`) | **License** | https://github.com/HellFirePvP/ObserverLib/blob/master/LICENCE |
| AE2 JEI Integration | `ae2jeiintegration-1.2.1.jar` | LGPL-3.0 | LGPL 3.0 (`LICENSE`) | **License** | https://github.com/mezz/AE2-JEI-Integration/blob/master/LICENSE |
| Cosmetic Armor Reworked | `cosmeticarmorreworked-1.21.1-v1-neoforge.jar` | MMPL 1.0.1 | MMPL 1.0.1 (`LICENSE.txt` no repositório e no jar) | **License** | https://github.com/zlainsama/CosmeticArmorReworked/blob/master/LICENSE.txt |
| Monsters & Spellbooks | `monsterspellbooks-0.0.16.3.jar` | All Rights Reserved | **MIT** na página do CurseForge, que diz: "Fell free to add to modpacks" | **License** | https://www.curseforge.com/minecraft/mc-mods/monsters-spellbooks-iss (cole também a frase da descrição) |
| Astral Sorcery | `AstralSorcery-2.0.1.20.jar` | All Rights Reserved | Licença própria de código visível. Proíbe redistribuir o código, mas diz: "only the original author or modpacks may distribute compiled binary versions of this code" | **License**, com a frase citada; se a moderação recusar, **Special permission** com a resposta do autor | https://github.com/HellFirePvP/AstralSorcery/blob/1.21.1/LICENSE |
| Fire's Ender Expansion | `firesenderexpansion-2.5.1.jar` | All Rights Reserved | All Rights Reserved (CurseForge). O repositório só tem o `TEMPLATE_LICENSE.txt` do MDK do NeoForge, que não é a licença do mod | **Resolvido:** o Modrinth reconheceu o arquivo sozinho, e o autor também autorizou o uso no pack em 17/10/2026 | https://github.com/FireOfPower/firesenderexpansion-1.21.1/issues/4#issuecomment-6229744399 |
| Mob Grinding Utils | `mob_grinding_utils-1.1.10+mc1.21.1.jar` | All rights reserved | All Rights Reserved (CurseForge). O repositório não tem licença | **No permission** até o autor responder; depois **Special permission** | Resposta do autor na issue (ver abaixo) |

## Arquivos baixados de outro site (a partir da 3.1.0)

Não ficam embutidos: o `modrinth.index.json` aponta para o anexo da
pré-release [`arquivos-servidor`](https://github.com/IunaMC/modpack/releases/tag/arquivos-servidor),
porque o autor não publica o jar com link fixo. É só de servidor
(`client: unsupported`), mas aparece na página Permissions.

| Mod | Arquivo | Licença no jar | Licença verificada | Opção | Link de prova |
| --- | --- | --- | --- | --- | --- |
| LuckPerms Placeholders | `LuckPerms-Fabric-Placeholders.jar` | MIT | MIT (`LICENSE.txt`) | **License** | https://github.com/LuckPerms/placeholders/blob/master/LICENSE.txt |

## Pedidos aos autores

Abertos em 17/10/2026. Quando houver resposta, marque **Special permission** e
cole o link da issue.

- Fire's Ender Expansion: https://github.com/FireOfPower/firesenderexpansion-1.21.1/issues/4
  (autorizado pelo autor em 17/10/2026; o Modrinth já reconhecia o arquivo)
- Mob Grinding Utils: https://github.com/vadis365/Mob-Grinding-Utils/issues/372
  (sem resposta; fechado em 18/10/2026)
- The Twilight Forest: sem pedido. A Team Twilight já recusou várias vezes
  liberar o mod em packs do Modrinth (issues
  [#1798](https://github.com/TeamTwilight/twilightforest/issues/1798),
  [#2358](https://github.com/TeamTwilight/twilightforest/issues/2358),
  [#2380](https://github.com/TeamTwilight/twilightforest/issues/2380) e
  [#2435](https://github.com/TeamTwilight/twilightforest/issues/2435)).

## Arquivos só do servidor (fora do `.mrpack` publicado)

O Modrinth confere todos os arquivos externos do `.mrpack`, inclusive os de
`server-overrides/`. Desde a v3.0.0, o workflow de release tira
`server-overrides/` do `.mrpack` (o servidor IUNA instala pelo
packwiz-installer, que baixa do CurseForge direto da fonte). Por isso estes
cinco **não aparecem** na página Permissions. A tabela fica como referência,
caso algum dia voltem para o arquivo.

| Mod | Arquivo | Licença no jar | Licença verificada | Opção | Link de prova |
| --- | --- | --- | --- | --- | --- |
| Crash Utilities | `crashutilities-9.0.4.jar` | MIT | MIT (`LICENSE`) | **License** | https://github.com/Darkere/CrashUtilities/blob/master/LICENSE |
| Better End Cities Better End | `BetterEndCities-BetterEnd-1.21.jar` | `LicenseRef-Datapack` (sem licença; é um datapack convertido em mod) | **MIT** na página do CurseForge | **License** | https://www.curseforge.com/minecraft/mc-mods/better-end-cities-better-end |
| Cupboard | `cupboard-1.21.1-4.2.jar` | ARR | **All Rights Reserved** (CurseForge) | Fora do `.mrpack` | https://www.curseforge.com/minecraft/mc-mods/cupboard |
| Fast Async World Save | `fastasyncworldsave-1.21-2.6.jar` | ARR | **All Rights Reserved** (CurseForge) | Fora do `.mrpack` | https://www.curseforge.com/minecraft/mc-mods/fast-async-world-save-forge-fabric |
| Smooth Chunk Save | `smoothchunk-1.21-4.1.jar` | ARR | **All Rights Reserved** (CurseForge) | Fora do `.mrpack` | https://www.curseforge.com/minecraft/mc-mods/smooth-chunk-save |

## O que isso muda no plano

- **O `.mrpack` publicado tem 14 arquivos externos, todos em `overrides/mods/`.
  Resolvidos: 11.** Os 9 de licença aberta, Monsters & Spellbooks e Fire's
  Ender Expansion, que o Modrinth reconheceu sozinho.
- **Monsters & Spellbooks não depende mais de pedido.** O jar diz "All Rights
  Reserved", mas a página do CurseForge mostra MIT e autoriza o uso em
  modpacks. O mod também está no Modrinth
  ([`3DnnAUlF`](https://modrinth.com/mod/3DnnAUlF), MIT), mas só até a 0.0.15;
  o pack usa a 0.0.16.3. Quando a 0.0.16.x sair lá, troque com
  `packwiz mr add 3DnnAUlF` e o arquivo deixa de ser externo.
- **Astral Sorcery pode passar pela licença.** A licença do autor libera
  modpacks para distribuir o jar compilado. Vale tentar **License** citando
  a frase e manter o pedido ao autor como plano B.
- **Faltam 2 do jogador, e ficam assim por decisão:** Mob Grinding Utils
  (pedido sem resposta) e The Twilight Forest (equipe recusa). Os dois
  continuam no pack, porque o objetivo é o `.mrpack` completo. Por isso as
  versões no Modrinth ficam retidas, e a distribuição é pelo GitHub.
- **Os 3 mods All Rights Reserved do servidor** (Cupboard, Fast Async World
  Save e Smooth Chunk Save, do autor someaddon) já não vão no `.mrpack`, nem
  no do GitHub nem no do Modrinth. Nada a fazer.
- **A release do GitHub redistribui Mob Grinding Utils e The Twilight Forest**
  (com partes All Rights Reserved) em `overrides/mods/`. A regra do Modrinth não alcança o GitHub,
  mas a licença do autor sim. A solução é a mesma: a permissão do autor, ou
  tirar o mod do pack.
