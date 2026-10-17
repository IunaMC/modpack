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
| The Twilight Forest | `twilightforest-1.21.1-4.8.3345-universal.jar` | LGPL 2.1 | LGPL 2.1 ou posterior (`LICENSE` do repositório) | **License** | https://github.com/TeamTwilight/twilightforest/blob/latest/LICENSE |
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
| Fire's Ender Expansion | `firesenderexpansion-2.5.1.jar` | All Rights Reserved | All Rights Reserved (CurseForge). O repositório só tem o `TEMPLATE_LICENSE.txt` do MDK do NeoForge, que não é a licença do mod | **No permission** até o autor responder; depois **Special permission** | Captura da resposta do autor (pedido em `~/Documents`) |
| Mob Grinding Utils | `mob_grinding_utils-1.1.10+mc1.21.1.jar` | All rights reserved | All Rights Reserved (CurseForge). O repositório não tem licença | **No permission** até o autor responder; depois **Special permission** | Captura da resposta do autor (pedido em `~/Documents`) |

## Arquivos só do servidor (`server-overrides/mods/`)

O Modrinth confere todos os arquivos externos do `.mrpack`, inclusive os de
`server-overrides/`; a notícia não abre exceção para eles.

| Mod | Arquivo | Licença no jar | Licença verificada | Opção | Link de prova |
| --- | --- | --- | --- | --- | --- |
| Crash Utilities | `crashutilities-9.0.4.jar` | MIT | MIT (`LICENSE`) | **License** | https://github.com/Darkere/CrashUtilities/blob/master/LICENSE |
| Better End Cities Better End | `BetterEndCities-BetterEnd-1.21.jar` | `LicenseRef-Datapack` (sem licença; é um datapack convertido em mod) | **MIT** na página do CurseForge | **License** | https://www.curseforge.com/minecraft/mc-mods/better-end-cities-better-end |
| Cupboard | `cupboard-1.21.1-4.2.jar` | ARR | **All Rights Reserved** (CurseForge) | **No permission**, ou tirar do `.mrpack` do Modrinth | https://www.curseforge.com/minecraft/mc-mods/cupboard |
| Fast Async World Save | `fastasyncworldsave-1.21-2.6.jar` | ARR | **All Rights Reserved** (CurseForge) | **No permission**, ou tirar do `.mrpack` do Modrinth | https://www.curseforge.com/minecraft/mc-mods/fast-async-world-save-forge-fabric |
| Smooth Chunk Save | `smoothchunk-1.21-4.1.jar` | ARR | **All Rights Reserved** (CurseForge) | **No permission**, ou tirar do `.mrpack` do Modrinth | https://www.curseforge.com/minecraft/mc-mods/smooth-chunk-save |

## O que isso muda no plano

- **Resolvidos pela licença: 13 de 19.** Os 10 de licença aberta, mais Crash
  Utilities, Better End Cities e Monsters & Spellbooks.
- **Monsters & Spellbooks não depende mais de pedido.** O jar diz "All Rights
  Reserved", mas a página do CurseForge mostra MIT e autoriza o uso em
  modpacks. O mod também está no Modrinth
  ([`3DnnAUlF`](https://modrinth.com/mod/3DnnAUlF), MIT), mas só até a 0.0.15;
  o pack usa a 0.0.16.3. Quando a 0.0.16.x sair lá, troque com
  `packwiz mr add 3DnnAUlF` e o arquivo deixa de ser externo.
- **Astral Sorcery pode passar pela licença.** A licença do autor libera
  modpacks para distribuir o jar compilado. Vale tentar **License** citando
  a frase e manter o pedido ao autor como plano B.
- **Faltam 2 do jogador:** Fire's Ender Expansion e Mob Grinding Utils. Sem
  resposta dos autores, a versão fica retida. As saídas são esperar a
  permissão ou tirar o mod do pack (versão MINOR). Fire's Ender Expansion
  depende de Ace's Spell Utils, que pode sair junto se nada mais usar.
- **3 mods do servidor são All Rights Reserved** (Cupboard, Fast Async World
  Save e Smooth Chunk Save, todos do autor someaddon). O servidor IUNA não usa
  o `.mrpack`: ele instala pelo packwiz-installer a partir do `pack.toml`.
  Então o mais simples é **tirar os três do `.mrpack` enviado ao Modrinth**
  (veja [`publicar.md`](publicar.md)). Quem montar um servidor pelo `.mrpack`
  do Modrinth fica só sem essas três otimizações. A outra saída é pedir
  permissão ao someaddon.
- **O mesmo vale para a release do GitHub.** O `.mrpack` anexado às releases
  também redistribui os jars All Rights Reserved. A regra do Modrinth não
  alcança o GitHub, mas a licença dos autores sim. Vale aplicar a mesma
  solução lá quando as permissões saírem.
