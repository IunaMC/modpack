# IUNA Modpack

Modpack do servidor IUNA: Minecraft **1.21.1** com NeoForge **21.1.253**.

Este repositório é a **fonte única** do pack, do jogador e do servidor. O pack é
mantido com o [packwiz](https://packwiz.infra.link/): cada mod é um `.pw.toml`
em [`pack/mods/`](pack/mods), sem nenhum jar, e o campo `side` diz onde ele
roda. A cada versão, o CI gera um `.mrpack` que qualquer launcher compatível
instala com um clique.

## Instalação

1. Baixe o `IUNA-<versão>.mrpack` da [última release](../../releases/latest).
2. Importe no launcher:
   - **Prism Launcher:** *Add Instance → Import* e escolha o arquivo.
   - **Modrinth App:** *+ (Create instance) → Import from file*.
3. Escolha os mods opcionais que quiser. Todos vêm marcados por padrão.
4. Abra o jogo e entre no servidor.

O launcher baixa os mods do Modrinth na hora. Os poucos que só existem no
CurseForge já vêm dentro do `.mrpack`.

**Para atualizar**, importe o `.mrpack` da versão nova numa instância nova. Se
você vem do zip antigo (até a v2.2.4), crie também uma instância nova: o
`.mrpack` não aproveita a pasta `mods` montada à mão. Para levar seus mundos,
prints e configurações, copie as pastas `saves`, `screenshots` e `config` da
instância antiga.

## Servidor

O servidor instala os mods a partir do mesmo pack, com o
[packwiz-installer](https://github.com/packwiz/packwiz-installer). Ele baixa
só os mods `server` e `both` e apaga os que saíram do pack. No comando de
inicialização, antes do Java do servidor:

```sh
java -jar packwiz-installer-bootstrap.jar -g -s server \
  https://raw.githubusercontent.com/IunaMC/modpack-cliente/v<versão>/pack/pack.toml
```

Apontar para a tag (`v<versão>`) e não para a `main` garante que o servidor só
mude quando uma release sair.

## Manutenção

Os comandos rodam dentro de `pack/`, com o packwiz instalado.

| Tarefa | Comando |
| --- | --- |
| Adicionar um mod do Modrinth | `packwiz mr add <slug-ou-link>` |
| Adicionar um mod do CurseForge | `packwiz cf add <slug-ou-link>` |
| Atualizar um mod | `packwiz update <nome>` |
| Remover um mod | `packwiz remove <nome>` |
| Recalcular o índice após editar um `.pw.toml` à mão | `packwiz refresh` |
| Gerar o `.mrpack` localmente | `packwiz mr export` |

Ao adicionar um mod, confira no `.pw.toml`:
- `side`: `both` para mods de conteúdo, que precisam estar nos dois lados;
  `client` para mods só visuais ou de interface; `server` para administração,
  desempenho e geração de mundo. Um mod de conteúdo marcado como `client` ou
  `server` impede o jogador de entrar no servidor.
- `[option] optional = true` para os mods opcionais, com uma `description` curta.

Depois de mudar mods, regenere a lista abaixo com
`python3 scripts/pack.py readme`. O CI confere o índice e a lista em todo push
e deixa um `.mrpack` de teste nos artefatos da execução.

### Versão e release

A versão fica em `version`, no [`pack/pack.toml`](pack/pack.toml), e segue
SemVer:
- **MAJOR:** exige mundo novo ou reinstalar tudo (Minecraft, NeoForge, troca de
  formato do pack, reset).
- **MINOR:** qualquer mod adicionado, atualizado ou removido.
- **PATCH:** nada muda para o jogador (config, docs, CI).

Para publicar, suba a versão no `pack.toml`, escreva o
[`MUDANCAS.md`](MUDANCAS.md) e faça merge na `main`. O workflow de release cria
a tag `v<versão>`, anexa o `.mrpack` e junta ao changelog a lista de mods
adicionados, atualizados e removidos desde a release anterior.

## Mods

<!-- lista-de-mods:inicio -->
<!-- Gerado por scripts/pack.py readme. Não edite à mão. -->

O pack tem **348 mods**. O jogador recebe 285 (253 obrigatórios e 32 opcionais), e o servidor, 308.

### Obrigatórios
Necessários para entrar no servidor. O launcher instala todos.

| Mod | Arquivo | Lado |
| --- | --- | --- |
| [Accelerated Decay](https://modrinth.com/mod/laX5CckD) | `accelerated-decay-neoforge-21.0.0.jar` | Cliente e servidor |
| [Accessories](https://modrinth.com/mod/jtmvUHXj) | `accessories-neoforge-1.1.0-beta.53+1.21.1.jar` | Cliente e servidor |
| [Ace's Spell Utils](https://modrinth.com/mod/7Jy4rK9m) | `aces_spell_utils-1.2.7.2-1.21.1.jar` | Cliente e servidor |
| [AE2 Import Export Card](https://modrinth.com/mod/qelfSMnn) | `ae2importexportcard-1.21.1-1.9.1.jar` | Cliente e servidor |
| [AE2 JEI Integration](https://www.curseforge.com/projects/1074338) | `ae2jeiintegration-1.2.1.jar` | Cliente e servidor |
| [Alex's Caves Continued](https://modrinth.com/mod/cO2CvXug) | `alexscaves-1.1.1-neoforge+1.21.1.jar` | Cliente e servidor |
| [Alex's Caves Continued Delight](https://modrinth.com/mod/7sC7Bn8p) | `accdelight-1.0.0-neoforge+1.21.1.jar` | Cliente e servidor |
| [Alex's Mobs Continued](https://modrinth.com/mod/kYIaHHfw) | `alexsmobs-2.2.2-neoforge+1.21.1.jar` | Cliente e servidor |
| [Alex's Mobs Continued Delight](https://modrinth.com/mod/iY124w4e) | `amcdelight-1.0.1-neoforge+1.21.1.jar` | Cliente e servidor |
| [Amendments](https://modrinth.com/mod/6iTJugQR) | `amendments-1.21-2.1.10-neoforge.jar` | Cliente e servidor |
| [Apotheosis](https://modrinth.com/mod/rqFWfVlz) | `Apotheosis-1.21.1-8.9.0.jar` | Cliente e servidor |
| [Apothic Attributes](https://modrinth.com/mod/DGaH8Rh0) | `ApothicAttributes-1.21.1-2.11.0.jar` | Cliente e servidor |
| [Apothic-Enchanting](https://modrinth.com/mod/pL8MtgqY) | `ApothicEnchanting-1.21.1-1.6.3.jar` | Cliente e servidor |
| [Apothic-Spawners](https://modrinth.com/mod/DfxVkOAO) | `ApothicSpawners-1.21.1-1.4.0.jar` | Cliente e servidor |
| [Applied Energistics 2](https://modrinth.com/mod/XxWD5pD3) | `appliedenergistics2-19.2.18.jar` | Cliente e servidor |
| [Aquaculture 2](https://modrinth.com/mod/Vl1uNAuy) | `Aquaculture-1.21.1-2.7.21.jar` | Cliente e servidor |
| [Aquaculture Delight](https://modrinth.com/mod/U9GJqWrI) | `aquaculturedelight-1.2.0-neoforge-1.21.1.jar` | Cliente e servidor |
| [Architectury API](https://modrinth.com/mod/lhGA9TYQ) | `architectury-13.0.11-neoforge.jar` | Cliente e servidor |
| [Ars Nouveau](https://modrinth.com/mod/TKB6INcv) | `ars_nouveau-1.21.1-5.13.3.jar` | Cliente e servidor |
| [Ars Ocultas](https://modrinth.com/mod/Tsw8vbks) | `ars_ocultas-1.21.1-2.6.1.jar` | Cliente e servidor |
| [Artifacts](https://modrinth.com/mod/P0Mu4wcQ) | `artifacts-neoforge-13.2.5.jar` | Cliente e servidor |
| [Asterism Arcanum \| Addon for Iron's Spells and Spellbooks](https://modrinth.com/mod/XImLIVFt) | `asterismarcanum-1.21.1-0.1.0.jar` | Cliente e servidor |
| [Astral Sorcery](https://www.curseforge.com/projects/241721) | `AstralSorcery-2.0.1.20.jar` | Cliente e servidor |
| [Athena](https://modrinth.com/mod/b1ZV3DIJ) | `athena-neoforge-1.21.1-4.0.6.jar` | Cliente e servidor |
| [AzureLib](https://modrinth.com/mod/7zlUOZvb) | `azurelib-neo-1.21.1-3.1.14.jar` | Cliente e servidor |
| [BaguetteLib](https://modrinth.com/mod/OfKzpbRU) | `baguettelib-1.21.1-NeoForge-2.0.7.jar` | Cliente e servidor |
| [Balm](https://modrinth.com/mod/MBAkmtvl) | `balm-neoforge-1.21.1-21.0.66.jar` | Cliente e servidor |
| [Barbeque's Delight [Forge/NeoForge]](https://modrinth.com/mod/rtu7uERF) | `barbequesdelight-1.3.0.jar` | Cliente e servidor |
| [BCLib: New Dawn](https://modrinth.com/mod/7bdKEtKC) | `bclib-21.0.26.jar` | Cliente e servidor |
| [Better Combat](https://modrinth.com/mod/5sy6g3kz) | `bettercombat-neoforge-2.4.0+1.21.1.jar` | Cliente e servidor |
| [BetterEnd: New Dawn](https://modrinth.com/mod/IcERKldh) | `BetterEnd-21.0.35.jar` | Cliente e servidor |
| [Biomes O' Plenty](https://modrinth.com/mod/HXF82T3G) | `BiomesOPlenty-neoforge-1.21.1-21.1.0.14.jar` | Cliente e servidor |
| [Bookshelf](https://modrinth.com/mod/uy4Cnpcm) | `bookshelf-neoforge-1.21.1-21.1.81.jar` | Cliente e servidor |
| [Botany Pots](https://modrinth.com/mod/U6BUTZ7K) | `botanypots-neoforge-1.21.1-21.1.44.jar` | Cliente e servidor |
| [Botany Trees](https://modrinth.com/mod/mvs7RoIW) | `botanytrees-neoforge-1.21.1-21.1.7.jar` | Cliente e servidor |
| [Brazilian Delight](https://modrinth.com/mod/Bgz35D5U) | `braziliandelight-fabric-3.0.1+1.21.1.jar` | Cliente e servidor |
| [Brewin' And Chewin'](https://modrinth.com/mod/hIu9KJTT) | `BrewinAndChewin-neoforge-4.5.0+1.21.1.jar` | Cliente e servidor |
| [Building Gadgets](https://www.curseforge.com/projects/298187) | `buildinggadgets2-1.3.9.jar` | Cliente e servidor |
| [Caelus API](https://modrinth.com/mod/40FYwb4z) | `caelus-neoforge-7.0.1+1.21.1.jar` | Cliente e servidor |
| [Camera Mod](https://modrinth.com/mod/oiuNWinn) | `camera-neoforge-1.21.1-1.0.22.jar` | Cliente e servidor |
| [Carry On](https://modrinth.com/mod/joEfVgkn) | `carryon-neoforge-1.21.1-2.2.6.13.jar` | Cliente e servidor |
| [Carry On Extend](https://modrinth.com/mod/JbqjOoQj) | `CarryOnExtend-Architectury-neoforge-1.5.2.jar` | Cliente e servidor |
| [Cataclysm Weaponery](https://modrinth.com/mod/S5OkaSK0) | `cataclysm_weaponery-3.0.0-neoforge-1.21.1.jar` | Cliente |
| [Cataclysm: Spellbooks](https://modrinth.com/mod/3FEg0A8D) | `cataclysm_spellbooks-1.1.14-1.21.jar` | Cliente e servidor |
| [Chipped](https://modrinth.com/mod/BAscRYKm) | `chipped-neoforge-1.21.1-4.0.2.jar` | Cliente e servidor |
| [Cloth Config API](https://modrinth.com/mod/9s6osm5g) | `cloth-config-15.0.140-neoforge.jar` | Cliente e servidor |
| [Cobweb](https://modrinth.com/mod/dQcfqGbl) | `cobweb-neoforge-1.21-1.4.0.jar` | Cliente e servidor |
| [CodeChicken Lib](https://modrinth.com/mod/2gq0ALnz) | `CodeChickenLib-1.21.1-4.6.1.529.jar` | Cliente e servidor |
| [CodxLib](https://modrinth.com/mod/6oyMM4yX) | `codxlib-1.6.1-neoforge+1.21.1.jar` | Cliente e servidor |
| [Colorful Hearts](https://modrinth.com/mod/wQfMUdZT) | `colorfulhearts-neoforge-1.21.1-10.5.9.jar` | Cliente |
| [Combat Roll](https://modrinth.com/mod/wGKYL7st) | `combat_roll-neoforge-2.0.6+1.21.1.jar` | Cliente e servidor |
| [Comforts](https://modrinth.com/mod/SaCpeal4) | `comforts-neoforge-9.0.5+1.21.1.jar` | Cliente e servidor |
| [Common Capabilities](https://modrinth.com/mod/oFXrCkDI) | `commoncapabilities-1.21.1-neoforge-2.11.6.jar` | Cliente e servidor |
| [Compass to Map: JourneyMap](https://modrinth.com/mod/Y6HhXts4) | `compass2map-2.0.4-neoforge-1.21.1.jar` | Cliente e servidor |
| [Connector Extras](https://modrinth.com/mod/FYpiwiBR) | `ConnectorExtras-1.12.1+1.21.1.jar` | Cliente e servidor |
| [Construction Sticks](https://modrinth.com/mod/ooyjDLZt) | `ConstructionSticks-1.21.1-1.5.0.jar` | Cliente e servidor |
| [Continuity](https://modrinth.com/mod/1IjD5062) | `continuity-3.0.0+1.21.neoforge.jar` | Cliente |
| [CoroUtil](https://modrinth.com/mod/rLLJ1OZM) | `coroutil-neoforge-1.21.0-1.3.8.jar` | Cliente e servidor |
| [Corpse](https://modrinth.com/mod/WrpuIfhw) | `corpse-neoforge-1.21.1-1.1.13.jar` | Cliente e servidor |
| [Corpse x Cosmetic Armor Reworked Compat](https://modrinth.com/mod/VrbUxhCI) | `cosmeticcorpsecompat-1.21.1-NeoForge-4.0.1.jar` | Cliente e servidor |
| [Corpse x Curios API Compat](https://modrinth.com/mod/pJGcKPh1) | `corpsecurioscompat-1.21.1-NeoForge-4.0.1.jar` | Cliente e servidor |
| [Cosmetic Armor Reworked](https://www.curseforge.com/projects/237307) | `cosmeticarmorreworked-1.21.1-v1-neoforge.jar` | Cliente e servidor |
| [Crate Delight](https://modrinth.com/mod/9rlXSyLg) | `cratedelight-26.07.01-1.21-neoforge.jar` | Cliente e servidor |
| [Create](https://modrinth.com/mod/LNytGWDc) | `create-1.21.1-6.0.10.jar` | Cliente e servidor |
| [Create Aeronautics](https://modrinth.com/mod/oWaK0Q19) | `create-aeronautics-bundled-1.21.1-1.3.2.jar` | Cliente e servidor |
| [Create Crafts & Additions](https://modrinth.com/mod/kU1G12Nn) | `createaddition-1.7.2.jar` | Cliente e servidor |
| [Create Deco](https://modrinth.com/mod/sMvUb4Rb) | `createdeco-2.1.3.jar` | Cliente e servidor |
| [Create: Central Kitchen](https://modrinth.com/mod/btq68HMO) | `create-central-kitchen-2.6.2.jar` | Cliente e servidor |
| [Create: Copycats+](https://modrinth.com/mod/UT2M39wf) | `copycats-3.0.9+mc.1.21.1-neoforge.jar` | Cliente e servidor |
| [Create: Dragons Plus](https://modrinth.com/mod/dzb1a5WV) | `CreateDragonsPlus-1.11.9.jar` | Cliente e servidor |
| [Create: New Age](https://modrinth.com/mod/FTeXqI9v) | `create-new-age-1.2.0+neoforge-mc1.21.1.jar` | Cliente e servidor |
| [Create: Sophisticated Backpacks Compat](https://modrinth.com/mod/BAEkFrvn) | `create_sophback_compat-1.0.jar` | Cliente e servidor |
| [Create: Structures Arise](https://modrinth.com/mod/9enMEvoc) | `Create-Structures-Arise-1.21.1-NeoForge-176.49.49.jar` | Cliente e servidor |
| [CreativeCore](https://modrinth.com/mod/OsZiaDHq) | `CreativeCore_NEOFORGE_v2.13.50_mc1.21.1.jar` | Cliente e servidor |
| [Creeper Overhaul](https://modrinth.com/mod/MI1LWe93) | `CreeperOverhaul-neoforge-1.21.1-4.0.6.jar` | Cliente e servidor |
| [Cristel Lib](https://modrinth.com/mod/cl223EMc) | `cristellib-neoforge-1.21.1-3.1.7.jar` | Cliente e servidor |
| [Cucumber Library](https://modrinth.com/mod/Rw1NrDzF) | `Cucumber-1.21.1-8.0.16.jar` | Cliente e servidor |
| [Curios API](https://modrinth.com/mod/vvuO3ImH) | `curios-neoforge-9.5.1+1.21.1.jar` | Cliente e servidor |
| [Cyclops Core](https://modrinth.com/mod/Z9DM0LJ4) | `cyclopscore-1.21.1-neoforge-1.30.0.jar` | Cliente e servidor |
| [Decocraft](https://modrinth.com/mod/IZJSgKZe) | `decocraft-3.0.11-1.21.1-neoforge.jar` | Cliente e servidor |
| [Delight Lib](https://modrinth.com/mod/rmDY6fYt) | `delightlib-26.05.18-1.21-neoforge.jar` | Cliente e servidor |
| [Deltabox Lib](https://modrinth.com/mod/FDGHOWuC) | `deltaboxlib-fabric-3.0.1+1.21.1.jar` | Cliente e servidor |
| [Despawn Tweaks](https://modrinth.com/mod/ahQrpeXp) | `despawntweaks-neoforge-1.0.0-1.21.1.jar` | Cliente e servidor |
| [Dynamic FPS](https://modrinth.com/mod/LQ3K71Q1) | `dynamic-fps-3.11.4+minecraft-1.21.0-neoforge.jar` | Cliente |
| [Easy Anvils](https://modrinth.com/mod/OZBR5JT5) | `EasyAnvils-v21.1.0-1.21.1-NeoForge.jar` | Cliente e servidor |
| [Easy NPC](https://modrinth.com/mod/CgGEe1h3) | `easy_npc_bundle-neoforge-1.21.1-7.14.0.jar` | Cliente e servidor |
| [Easy NPC: Config UI](https://modrinth.com/mod/uTGjf7vA) | `easy_npc_config_ui-neoforge-1.21.1-7.14.0.jar` | Cliente e servidor |
| [Easy NPC: Core](https://modrinth.com/mod/Epm6R3P2) | `easy_npc-neoforge-1.21.1-7.14.0.jar` | Cliente e servidor |
| [ElevatorMod](https://modrinth.com/mod/hi2dSXTu) | `elevatorid-neoforge-1.21.1-1.11.4.jar` | Cliente e servidor |
| [Emotecraft](https://modrinth.com/mod/pZ2wrerK) | `emotecraft-for-MC1.21.1-2.4.12-neoforge.jar` | Cliente e servidor |
| [Ender IO](https://modrinth.com/mod/49ZofO4f) | `enderio-8.2.12-beta.jar` | Cliente e servidor |
| [Ender Storage](https://modrinth.com/mod/BbrHg80P) | `EnderStorage-1.21.1-2.13.0.191.jar` | Cliente e servidor |
| [Enderman Overhaul](https://modrinth.com/mod/Lq6ojcWv) | `endermanoverhaul-neoforge-1.21.1-2.0.3.jar` | Cliente e servidor |
| [Even Better Nether](https://modrinth.com/mod/ZSdhSrVt) | `evenbetternether-1.3.0-neoforge-1.21.1.jar` | Cliente e servidor |
| [EvilCraft](https://modrinth.com/mod/3ANq2btA) | `evilcraft-1.21.1-neoforge-1.2.98.jar` | Cliente e servidor |
| [Expanded Delight](https://modrinth.com/mod/e9V6wFcR) | `expandeddelight-0.1.4.jar` | Cliente e servidor |
| [Explorer's Compass](https://modrinth.com/mod/RV1qfVQ8) | `ExplorersCompass-1.21.1-3.4.0-neoforge.jar` | Cliente e servidor |
| [Extreme Reactors](https://modrinth.com/mod/idkvShUy) | `ExtremeReactors2-1.21.1-2.4.9.jar` | Cliente e servidor |
| [Fabric Language Kotlin](https://modrinth.com/mod/Ha28R6CL) | `fabric-language-kotlin-1.14.1+kotlin.2.4.20.jar` | Cliente e servidor |
| [Farmer's Delight](https://modrinth.com/mod/R2OftAxM) | `FarmersDelight-1.21.1-1.3.4.jar` | Cliente e servidor |
| [Farmer's Respite Unofficial Port](https://modrinth.com/mod/AioQLjKj) | `farmersrespite-1.21.1-3.0.1.jar` | Cliente e servidor |
| [FastFurnace](https://modrinth.com/mod/9X0318ev) | `FastFurnace-1.21.1-9.0.1.jar` | Cliente e servidor |
| [FerriteCore](https://modrinth.com/mod/uXXizFIs) | `ferritecore-7.0.3-neoforge.jar` | Cliente e servidor |
| [Fire's Ender Expansion](https://www.curseforge.com/projects/1245989) | `firesenderexpansion-2.5.1.jar` | Cliente e servidor |
| [Flux Networks](https://www.curseforge.com/projects/248020) | `FluxNetworks-1.21.1-8.0.0.jar` | Cliente e servidor |
| [Forbidden and Arcanus](https://modrinth.com/mod/MdlnLS7Q) | `forbidden_arcanus-2.6.1.jar` | Cliente e servidor |
| [Forge Config API Port](https://modrinth.com/mod/ohNO6lps) | `ForgeConfigAPIPort-v21.1.6-1.21.1-NeoForge.jar` | Cliente e servidor |
| [Forgified Fabric API](https://modrinth.com/mod/Aqlf1Shp) | `forgified-fabric-api-0.116.15+2.3.5+1.21.1.jar` | Cliente e servidor |
| [Fragmentum](https://modrinth.com/mod/49C5QgTK) | `fragmentum-5.1.1+1.21.1-neoforge.jar` | Cliente e servidor |
| [FramedBlocks](https://modrinth.com/mod/wbgfS34j) | `FramedBlocks-10.6.1.jar` | Cliente e servidor |
| [Framework](https://www.curseforge.com/projects/549225) | `framework-neoforge-1.21.1-0.13.11.jar` | Cliente e servidor |
| [Functional Storage](https://modrinth.com/mod/cO40ZIg3) | `functionalstorage-1.21.1-1.5.7.jar` | Cliente e servidor |
| [Fzzy Config](https://modrinth.com/mod/hYykXjDp) | `fzzy_config-0.7.7+1.21+neoforge.jar` | Cliente e servidor |
| [Gadgets Against Grind](https://modrinth.com/mod/IeYLjzpn) | `gag-neoforge-1.21.1-5.2.0.jar` | Cliente e servidor |
| [Geckolib](https://modrinth.com/mod/8BmcQJ2H) | `geckolib-neoforge-1.21.1-4.9.3.jar` | Cliente e servidor |
| [GlitchCore](https://modrinth.com/mod/s3dmwKy5) | `GlitchCore-neoforge-1.21.1-2.1.0.2.jar` | Cliente e servidor |
| [GuideME](https://modrinth.com/mod/Ck4E7v7R) | `guideme-21.1.19.jar` | Cliente e servidor |
| [Handcrafted](https://modrinth.com/mod/pJmCFF0p) | `handcrafted-neoforge-1.21.1-4.0.3.jar` | Cliente e servidor |
| [Hazen 'n Stuff](https://modrinth.com/mod/I94FeWYD) | `hazennstuff-1.4.0.14.jar` | Cliente e servidor |
| [HazentouveLib](https://modrinth.com/mod/nZaIUw7C) | `hazentouvelib-1.0.9.jar` | Cliente e servidor |
| [IceAndFire Community Edition](https://www.curseforge.com/projects/1040076) | `iceandfire-2.1.3.jar` | Cliente e servidor |
| [Iceberg](https://modrinth.com/mod/5faXoLqX) | `Iceberg-1.21.1-neoforge-1.3.2.jar` | Cliente |
| [ImmediatelyFast](https://modrinth.com/mod/5ZwdcRci) | `ImmediatelyFast-NeoForge-1.6.14+1.21.1.jar` | Cliente |
| [Industrial Foregoing](https://modrinth.com/mod/lWxpUd04) | `industrialforegoing-1.21-3.6.39.jar` | Cliente e servidor |
| [Integrated API](https://modrinth.com/mod/V6fKbpBN) | `integrated_api-neoforge-1.21.1-1.8.2.jar` | Cliente e servidor |
| [Integrated Crafting](https://modrinth.com/mod/qwpACdla) | `integratedcrafting-1.21.1-neoforge-1.7.2.jar` | Cliente e servidor |
| [Integrated Dungeons and Structures](https://modrinth.com/mod/Z8OZShAU) | `idas-1.13.7+1.21.1-neoforge.jar` | Cliente e servidor |
| [Integrated Dynamics](https://modrinth.com/mod/yYzdQHJI) | `integrateddynamics-1.21.1-neoforge-1.38.0.jar` | Cliente e servidor |
| [Integrated Terminals](https://modrinth.com/mod/HmLJoQ1K) | `integratedterminals-1.21.1-neoforge-1.10.0.jar` | Cliente e servidor |
| [Integrated Tunnels](https://modrinth.com/mod/Etqy1Omb) | `integratedtunnels-1.21.1-neoforge-1.13.0.jar` | Cliente e servidor |
| [Iris Shaders](https://modrinth.com/mod/YL57xq9U) | `iris-neoforge-1.8.14-beta.1+mc1.21.1.jar` | Cliente |
| [Iron Chests](https://modrinth.com/mod/P3iIrPH3) | `ironchest-1.21-neoforge-16.0.7.jar` | Cliente e servidor |
| [Iron Furnaces](https://modrinth.com/mod/yPlaLxD1) | `ironfurnaces-neoforge-1.21.1-4.3.2.jar` | Cliente e servidor |
| [Iron's Lib](https://modrinth.com/mod/9nfaJPtX) | `irons_lib-1.21.1-2.2.0.jar` | Cliente e servidor |
| [Iron's Spells 'n Spellbooks](https://modrinth.com/mod/s4OWxYQQ) | `irons_spellbooks-1.21.1-3.16.3.jar` | Cliente e servidor |
| [Item Obliterator](https://modrinth.com/mod/3ESR84kR) | `Item-Obliterator-NeoForge-MC1.21.1-2.3.0.jar` | Cliente e servidor |
| [JourneyMap](https://modrinth.com/mod/lfHFW1mp) | `journeymap-neoforge-1.21.1-6.0.9.jar` | Cliente e servidor |
| [JourneyMap Teams](https://modrinth.com/mod/EV5wjtvP) | `JourneyMap-Teams-neoforge-1.21.1-1.3.1.jar` | Cliente e servidor |
| [Jupiter](https://modrinth.com/mod/XbiLGMMU) | `jupiter-2.3.7-1.21.1-neoforge.jar` | Cliente e servidor |
| [Just Enough Items (JEI)](https://modrinth.com/mod/u6dRKJwZ) | `jei-1.21.1-neoforge-19.57.0.450.jar` | Cliente e servidor |
| [Konkrete](https://modrinth.com/mod/J81TRJWm) | `konkrete_neoforge_1.9.9_MC_1.21.jar` | Cliente |
| [Kotlin for Forge](https://modrinth.com/mod/ordsPcFz) | `kotlinforforge-5.12.0-all.jar` | Cliente e servidor |
| [L_Ender's Cataclysm](https://modrinth.com/mod/46KJle7n) | `L_Ender's Cataclysm 1.21.1-3.33.jar` | Cliente e servidor |
| [Lightman's Currency](https://modrinth.com/mod/wvMc8AJt) | `lightmanscurrency-1.21-2.3.0.6.jar` | Cliente e servidor |
| [Lionfish-API](https://modrinth.com/mod/FoVacERa) | `lionfishapi-3.1.jar` | Cliente e servidor |
| [Lithium](https://modrinth.com/mod/gvQqBUqZ) | `lithium-neoforge-0.15.4+mc1.21.1.jar` | Cliente e servidor |
| [Lithostitched](https://modrinth.com/mod/XaDC71GB) | `lithostitched-1.8.0-neoforge-21.1.jar` | Cliente e servidor |
| [Lootr](https://modrinth.com/mod/EltpO5cN) | `lootr-neoforge-1.21.1-1.11.38.127.jar` | Cliente e servidor |
| [Macaw's Bridges](https://modrinth.com/mod/GURcjz8O) | `mcw-bridges-3.1.2-mc1.21.1neoforge.jar` | Cliente e servidor |
| [Mahou Tsukai](https://modrinth.com/mod/7jOxn6qJ) | `mahoutsukai-1.21.1-v1.36.27.jar` | Cliente e servidor |
| [McJtyLib](https://modrinth.com/mod/1Zu0uTEE) | `mcjtylib-1.21-9.0.21.jar` | Cliente e servidor |
| [Mekanism](https://modrinth.com/mod/Ce6I4WUE) | `Mekanism-1.21.1-10.7.19.85.jar` | Cliente e servidor |
| [Mekanism Additions](https://modrinth.com/mod/a6F3uASn) | `MekanismAdditions-1.21.1-10.7.19.85.jar` | Cliente e servidor |
| [Mekanism Generators](https://modrinth.com/mod/OFVYKsAk) | `MekanismGenerators-1.21.1-10.7.19.85.jar` | Cliente e servidor |
| [Mekanism Tools](https://modrinth.com/mod/tqQpq1lt) | `MekanismTools-1.21.1-10.7.19.85.jar` | Cliente e servidor |
| [Mermod](https://modrinth.com/mod/ORiydwz3) | `mermod-neoforge-3.3.2+1.21.1.jar` | Cliente e servidor |
| [MezzConfig](https://modrinth.com/mod/7tEfOcA7) | `mezz_config-1.21.1-neoforge-0.6.8-standalone.jar` | Cliente e servidor |
| [MmmMmmMmmMmm](https://modrinth.com/mod/Adega8YN) | `dummmmmmy-1.21-2.1.2-neoforge.jar` | Cliente e servidor |
| [Mob Grinding Utils](https://www.curseforge.com/projects/254241) | `mob_grinding_utils-1.1.10+mc1.21.1.jar` | Cliente e servidor |
| [ModernFix](https://modrinth.com/mod/nmDcB62a) | `modernfix-neoforge-5.27.26+mc1.21.1.jar` | Cliente e servidor |
| [Modonomicon](https://modrinth.com/mod/692GClaE) | `modonomicon-1.21.1-neoforge-1.120.7.jar` | Cliente e servidor |
| [Monsters & Spellbooks: Iron's Spells 'n Spellbooks Addon](https://www.curseforge.com/projects/1428928) | `monsterspellbooks-0.0.16.3.jar` | Cliente e servidor |
| [Moonlight Lib](https://modrinth.com/mod/twkfQtEc) | `moonlight-1.21.1-3.7.0-neoforge.jar` | Cliente e servidor |
| [More Delight (for Farmer's Delight)](https://modrinth.com/mod/znHQQtuU) | `moredelight-26.05.20a-1.21-neoforge.jar` | Cliente e servidor |
| [Mowzie's Cataclysm](https://modrinth.com/mod/7UsJsd1y) | `mowzies_cataclysm-1.2.2.jar` | Cliente e servidor |
| [Mowzie's Mobs](https://modrinth.com/mod/BFbX9xcm) | `mowziesmobs-1.21.1-1.8.2.jar` | Cliente e servidor |
| [MrCrayfish's Furniture Mod: Refurbished](https://www.curseforge.com/projects/897116) | `refurbished_furniture-neoforge-1.21.1-1.0.22.jar` | Cliente e servidor |
| [Mystical Agradditions](https://modrinth.com/mod/pl0jGXIx) | `MysticalAgradditions-1.21.1-8.0.15.jar` | Cliente e servidor |
| [Mystical Agriculture](https://modrinth.com/mod/C95ReXie) | `MysticalAgriculture-1.21.1-8.0.28.jar` | Cliente e servidor |
| [Mystical Customization](https://modrinth.com/mod/lNK9A4rh) | `MysticalCustomization-1.21.1-6.0.2.jar` | Cliente e servidor |
| [Nature's Compass](https://modrinth.com/mod/fPetb5Kh) | `NaturesCompass-1.21.1-3.4.0-neoforge.jar` | Cliente e servidor |
| [Necronomicon API](https://modrinth.com/mod/P1Kv5EAO) | `Necronomicon-NeoForge-1.6.0+1.21.jar` | Cliente e servidor |
| [Not Enough Animations](https://modrinth.com/mod/MPCX6s5C) | `notenoughanimations-neoforge-1.12.6-mc1.21.1.jar` | Cliente |
| [Not Enough Crashes](https://modrinth.com/mod/yM94ont6) | `notenoughcrashes-neoforge-4.4.9+1.21.1.jar` | Cliente |
| [ObserverLib](https://www.curseforge.com/projects/316833) | `observerlib-1.10.3.jar` | Cliente e servidor |
| [Occultism](https://modrinth.com/mod/sbJh4AZw) | `occultism-1.21.1-neoforge-1.224.4.jar` | Cliente e servidor |
| [Ocean's Delight](https://modrinth.com/mod/DGiq4ZSW) | `oceansdelight-neoforge-1.0.4-1.21.1.jar` | Cliente e servidor |
| [Overflowing Bars](https://modrinth.com/mod/XD7XOrAF) | `OverflowingBars-v21.1.1-1.21.1-NeoForge.jar` | Cliente |
| [oωo (owo-lib)](https://modrinth.com/mod/ccKDOlHs) | `owo-lib-neoforge-0.12.15.5-beta.1+1.21.jar` | Cliente e servidor |
| [Pam's HarvestCraft 2 - Food Extended](https://modrinth.com/mod/bdPeAbPS) | `pamhc2foodextended-NEOFORGE-1.21.1-1.0.0.jar` | Cliente e servidor |
| [Pam's HarvestCraft 2 - Trees](https://modrinth.com/mod/KDzWXxuG) | `pamhc2trees-NEOFORGE-1.21.1-1.0.4.jar` | Cliente e servidor |
| [Pam's HarvestCraft 2: Crops](https://modrinth.com/mod/5xO6VNlk) | `pamhc2crops-NEOFORGE-1.21.1-1.0.0.jar` | Cliente e servidor |
| [Pam's HarvestCraft 2: Food Core](https://modrinth.com/mod/Z9OywhE4) | `pamhc2foodcore-NEOFORGE-1.21.1-1.0.2.jar` | Cliente e servidor |
| [Paragliders](https://modrinth.com/mod/esqWA0aQ) | `Paraglider-neoforge-21.1.5.jar` | Cliente e servidor |
| [Patchouli](https://modrinth.com/mod/nU0bVIaL) | `Patchouli-1.21.1-93-NEOFORGE.jar` | Cliente e servidor |
| [Petting - Tame any mob!](https://modrinth.com/mod/vf91JXwf) | `petting-4.2.2-neoforge-1.21.1.jar` | Cliente e servidor |
| [Pipez](https://modrinth.com/mod/iRmWy6ga) | `pipez-neoforge-1.21.1-1.2.31.jar` | Cliente e servidor |
| [Placebo](https://modrinth.com/mod/tCkE8p2N) | `Placebo-1.21.1-9.9.2.jar` | Cliente e servidor |
| [Player Animation Library](https://modrinth.com/mod/ha1mEyJS) | `PlayerAnimationLibNeoforge-1.1.6+mc.1.21.1.jar` | Cliente e servidor |
| [PlayerRevive](https://modrinth.com/mod/ABIMzABM) | `PlayerRevive_NEOFORGE_v2.1.2_mc1.21.1.jar` | Cliente e servidor |
| [Polymorph](https://modrinth.com/mod/tagwiZkJ) | `polymorph-neoforge-1.2.0+1.21.1.jar` | Cliente e servidor |
| [Prickle](https://modrinth.com/mod/aaRl8GiW) | `prickle-neoforge-1.21.1-21.1.11.jar` | Cliente e servidor |
| [Prometheus](https://modrinth.com/mod/7Z7a9JyH) | `prometheus-neoforge-1.21-1.2.5.jar` | Cliente e servidor |
| [Puzzles Lib](https://modrinth.com/mod/QAGBst4M) | `puzzleslib-v21.1.62-mc1.21.1+neoforge.jar` | Cliente e servidor |
| [Quark](https://modrinth.com/mod/qnQsVE2z) | `Quark-4.1-486.jar` | Cliente e servidor |
| [Quick Skin](https://modrinth.com/mod/zAIE84Ch) | `Quick Skin - NeoForge - 1.21.1-3.0.1.jar` | Cliente e servidor |
| [Refined Storage](https://modrinth.com/mod/KDvYkUg3) | `refinedstorage-neoforge-2.0.9.jar` | Cliente e servidor |
| [Refined Storage - JEI Integration](https://modrinth.com/mod/VzR5wiLo) | `refinedstorage-jei-integration-neoforge-1.0.0.jar` | Cliente e servidor |
| [Regions Unexplored](https://modrinth.com/mod/Tkikq67H) | `regions-unexplored-0.6.2-neoforge-21.1.jar` | Cliente e servidor |
| [Relics](https://modrinth.com/mod/OCJRPujW) | `relics-1.21.1-0.12.8.jar` | Cliente e servidor |
| [Reliquary Reincarnations](https://modrinth.com/mod/fQO83PId) | `reliquary-1.21.1-2.0.80.1570.jar` | Cliente e servidor |
| [Resourceful Config](https://modrinth.com/mod/M1953qlQ) | `resourcefulconfig-neoforge-1.21-3.0.11.jar` | Cliente e servidor |
| [Resourceful Lib](https://modrinth.com/mod/G1hIVOrD) | `resourcefullib-neoforge-1.21-3.0.12.jar` | Cliente e servidor |
| [RFTools Base](https://modrinth.com/mod/hIO8IsD8) | `rftoolsbase-1.21-6.0.11.jar` | Cliente e servidor |
| [RFTools Builder](https://modrinth.com/mod/e0IclJLr) | `rftoolsbuilder-1.21-7.0.7.jar` | Cliente e servidor |
| [RFTools Utility](https://modrinth.com/mod/7n3HbHSE) | `rftoolsutility-1.21-7.0.12.jar` | Cliente e servidor |
| [Sable](https://modrinth.com/mod/T9PomCSv) | `sable-neoforge-1.21.1-2.0.6.jar` | Cliente e servidor |
| [SecurityCraft](https://modrinth.com/mod/v8jzRtAt) | `[1.21.1] SecurityCraft v1.10.2.1.jar` | Cliente e servidor |
| [ShatterLib \| OctoLib](https://modrinth.com/mod/RH2KUdKJ) | `OctoLib-NEOFORGE-0.6.2+1.21.jar` | Cliente e servidor |
| [Silent Lib](https://modrinth.com/mod/BQhuHQo4) | `silent-lib-1.21.1-neoforge-10.6.0.jar` | Cliente e servidor |
| [Silent's Power Scale](https://modrinth.com/mod/YCjSHxCP) | `power-scale-1.21.1-neoforge-0.3.1.1.jar` | Cliente e servidor |
| [Simple Hats](https://modrinth.com/mod/iSkQCp6b) | `simplehats-neoforge-1.21.1-0.4.0.jar` | Cliente e servidor |
| [Simple Magnets](https://modrinth.com/mod/YyNQVpOu) | `simplemagnets-1.1.12c-neoforge-mc1.21.jar` | Cliente e servidor |
| [Simple Voice Chat](https://modrinth.com/mod/9eGKb6K1) | `voicechat-neoforge-1.21.1-2.6.24.jar` | Cliente e servidor |
| [Simply Swords](https://modrinth.com/mod/bK3Ubu9p) | `simplyswords-neoforge-1.70.2-1.21.1.jar` | Cliente e servidor |
| [Simply Tooltips](https://modrinth.com/mod/6avVoBVB) | `SimplyTooltips-neoforge-0.1.5.jar` | Cliente |
| [Sinytra Connector](https://modrinth.com/mod/u58R1TMW) | `connector-2.0.0-beta.17+1.21.1-full.jar` | Cliente e servidor |
| [SmartBrainLib](https://modrinth.com/mod/PuyPazRT) | `SmartBrainLib-neoforge-1.21.1-1.16.11.jar` | Cliente e servidor |
| [Sodium](https://modrinth.com/mod/AANobbMI) | `sodium-neoforge-0.8.13+mc1.21.1.jar` | Cliente |
| [Sodium Extra](https://modrinth.com/mod/PtjYWJkn) | `sodium-extra-neoforge-0.9.4+mc1.21.1.jar` | Cliente |
| [Somake Spells - Iron's Spells Addon](https://modrinth.com/mod/uoNbtac8) | `somakespells-1.0.8-1.21.1-fix.jar` | Cliente e servidor |
| [Sophisticated Backpacks](https://modrinth.com/mod/TyCTlI4b) | `sophisticatedbackpacks-1.21.1-3.26.7.2182.jar` | Cliente e servidor |
| [Sophisticated Core](https://modrinth.com/mod/nmoqTijg) | `sophisticatedcore-1.21.1-1.5.5.2363.jar` | Cliente e servidor |
| [Sophisticated Storage](https://modrinth.com/mod/hMlaZH8f) | `sophisticatedstorage-1.21.1-1.6.1.2147.jar` | Cliente e servidor |
| [Soul Fire'd](https://modrinth.com/mod/d6MhxwRo) | `soul-fire-d-neoforge-1.21-6.1.0.jar` | Cliente e servidor |
| [Storage Drawers](https://modrinth.com/mod/guitPqEi) | `StorageDrawers-neoforge-1.21.1-13.11.4.jar` | Cliente e servidor |
| [SuperMartijn642's Config Lib](https://modrinth.com/mod/LN9BxssP) | `supermartijn642configlib-1.1.8-neoforge-mc1.21.jar` | Cliente e servidor |
| [SuperMartijn642's Core Lib](https://modrinth.com/mod/rOUBggPv) | `supermartijn642corelib-1.1.24b-neoforge-mc1.21.jar` | Cliente e servidor |
| [Supplementaries](https://modrinth.com/mod/fFEIiSDQ) | `supplementaries-1.21.1-3.9.9-neoforge.jar` | Cliente e servidor |
| [TerraBlender](https://modrinth.com/mod/kkmrDlKT) | `TerraBlender-neoforge-1.21.1-4.1.0.8.jar` | Cliente e servidor |
| [The Aether](https://modrinth.com/mod/YhmgMVyu) | `aether-1.21.1-1.5.10-neoforge.jar` | Cliente e servidor |
| [The Twilight Forest](https://www.curseforge.com/projects/227639) | `twilightforest-1.21.1-4.8.3345-universal.jar` | Cliente e servidor |
| [Titanium](https://modrinth.com/mod/1Ro7m06l) | `titanium-1.21-4.0.50.jar` | Cliente e servidor |
| [TorchMaster](https://modrinth.com/mod/Tl8ESrhX) | `torchmaster-neoforge-1.21.1-21.1.13.jar` | Cliente e servidor |
| [Towns and Towers](https://modrinth.com/mod/DjLobEOy) | `t_and_t-fabric-neoforge-1.13.11.jar` | Cliente e servidor |
| [TrashSlot](https://modrinth.com/mod/vRYk0bv7) | `trashslot-neoforge-1.21.1-21.1.11.jar` | Cliente e servidor |
| [Twilight Forest - Dungeons & Villages](https://modrinth.com/mod/eDeSn4Ds) | `tf_dnv-2.0.3.jar` | Cliente e servidor |
| [TxniLib](https://modrinth.com/mod/vBbPDuOs) | `txnilib-neoforge-1.0.24-1.21.1.jar` | Cliente e servidor |
| [Uranus](https://www.curseforge.com/projects/1010827) | `uranus-3.0-beta.1.jar` | Cliente e servidor |
| [Valhelsia Core](https://modrinth.com/mod/HsdNFinx) | `valhelsia_core-neoforge-1.21.1-1.1.4.jar` | Cliente e servidor |
| [Veggies Delight (A Farmer's Delight Add-on)](https://modrinth.com/mod/emQ94xri) | `VeggiesDelight-1.21.1-1.9.3.jar` | Cliente e servidor |
| [WATERFrAMES: Multimedia Displays](https://modrinth.com/mod/eBzFuVTM) | `waterframes-NEOFORGE-mc1.21.1-v2.1.23.jar` | Cliente e servidor |
| [WATERMeDIA: Multimedia API](https://modrinth.com/mod/G922NeHS) | `watermedia-2.1.37.jar` | Cliente |
| [WATERMeDIA: Youtube Extension](https://modrinth.com/mod/P0w3IrnX) | `watermedia_youtube_plugin-2.1.2.jar` | Cliente |
| [WATERViSION: VideoPlayer](https://modrinth.com/mod/dGGbEGoV) | `watervision-NF-mc1.21.1-v0.1.0-alpha.jar` | Cliente e servidor |
| [Waystones](https://modrinth.com/mod/LOpKHB2A) | `waystones-neoforge-1.21.1-21.1.46.jar` | Cliente e servidor |
| [What Are They Up To (Watut)](https://modrinth.com/mod/AtB5mHky) | `watut-neoforge-1.21.0-1.2.7.jar` | Cliente e servidor |
| [WorldWeaver: New Dawn](https://modrinth.com/mod/R8uGDQpB) | `worldweaver-21.0.26.jar` | Cliente e servidor |
| [WunderLib: New Dawn](https://modrinth.com/mod/HZmhgdJk) | `wunderlib-21.0.10.jar` | Cliente e servidor |
| [Xray Snitch](https://modrinth.com/mod/AKunSbDQ) | `xray_snitch-1.3.jar` | Cliente e servidor |
| [YUNG's API](https://modrinth.com/mod/Ua7DFN59) | `YungsApi-1.21.1-NeoForge-5.1.9.jar` | Cliente e servidor |
| [ZeroCore](https://modrinth.com/mod/rHpb85Mf) | `ZeroCore2-1.21.1-2.4.9.jar` | Cliente e servidor |
| [Zeta](https://modrinth.com/mod/MVARlG2f) | `Zeta-1.1-40.jar` | Cliente e servidor |

### Opcionais
Melhorias visuais e de qualidade de vida. O launcher pergunta quais você quer na instalação.

| Mod | Arquivo | Lado |
| --- | --- | --- |
| [3D Skin Layers](https://modrinth.com/mod/zV5r3pPn) | `skinlayers3d-neoforge-1.11.3-mc1.21.1.jar` | Cliente |
| [[EMF] Entity Model Features](https://modrinth.com/mod/4I1XuqiY) | `entity_model_features-3.3.11-1.21-neoforge.jar` | Cliente |
| [[ETF] Entity Texture Features](https://modrinth.com/mod/BVzZfTc1) | `entity_texture_features-7.2.5-1.21-neoforge.jar` | Cliente |
| [AmbientSounds](https://modrinth.com/mod/fM515JnW) | `AmbientSounds_NEOFORGE_v6.3.9_mc1.21.1.jar` | Cliente |
| [AppleSkin](https://modrinth.com/mod/EsAfCjCV) | `appleskin-neoforge-mc1.21-3.0.9.jar` | Cliente e servidor |
| [Better Advancements](https://modrinth.com/mod/Q2OqKxDG) | `BetterAdvancements-NeoForge-1.21.1-0.4.3.21.jar` | Cliente |
| [Better Ping Display [Forge/NeoForge]](https://modrinth.com/mod/ZvaHbwoZ) | `BetterPingDisplay-1.21.1-1.1.jar` | Cliente |
| [Better Third Person](https://modrinth.com/mod/G1s2WpNo) | `BetterThirdPerson-neoforge-1.9.0.jar` | Cliente |
| [Chat Heads](https://modrinth.com/mod/Wb5oqrBJ) | `chat_heads-0.15.7-neoforge-1.21.jar` | Cliente |
| [Controlling](https://modrinth.com/mod/xv94TkTM) | `Controlling-neoforge-1.21.1-19.0.5.jar` | Cliente |
| [Crash Assistant](https://modrinth.com/mod/ix1qq8Ux) | `CrashAssistant-neoforge-1.20.6-1.21.4-1.11.12.jar` | Cliente |
| [Custom Player Animations](https://modrinth.com/mod/EhthJpjM) | `cpa-5.9.10-neoforge+1.21.1.jar` | Cliente |
| [Durability Tooltip](https://modrinth.com/mod/smUP7V3r) | `durabilitytooltip-1.2.0-neoforge-mc1.21.jar` | Cliente |
| [Enchantment Descriptions](https://modrinth.com/mod/UVtY3ZAC) | `enchdesc-neoforge-1.21.1-21.1.11.jar` | Cliente e servidor |
| [Entity Culling](https://modrinth.com/mod/NNAgCjsB) | `entityculling-neoforge-1.11.2-mc1.21.1.jar` | Cliente |
| [FallingTree](https://modrinth.com/mod/Fb4jn8m6) | `FallingTree-1.21.1-1.21.1.11.jar` | Cliente e servidor |
| [Fast IP Ping](https://modrinth.com/mod/9mtu0sUO) | `fast-ip-ping-v1.0.12-mc1.21.1-neoforge.jar` | Cliente |
| [InventoryHUD+](https://modrinth.com/mod/Kp2uclYl) | `inventoryhud.neoforged.1.21.1-3.4.28.jar` | Cliente |
| [Item Highlighter](https://modrinth.com/mod/cVNW5lr6) | `Highlighter-1.21-neoforge-1.1.11.jar` | Cliente |
| [Jade Addons (Neo/Forge)](https://modrinth.com/mod/xuDOzCLy) | `JadeAddons-1.21.1-NeoForge-6.1.2.jar` | Cliente e servidor |
| [Jade 🔍](https://modrinth.com/mod/nvQzSEkH) | `Jade-1.21.1-NeoForge-15.10.6.jar` | Cliente e servidor |
| [Just Enough Breeding (JEBr)](https://modrinth.com/mod/9Pk89J3g) | `justenoughbreeding-neoforge-1.21.1-3.3.1.jar` | Cliente e servidor |
| [Just Enough Mekanism Multiblocks](https://modrinth.com/mod/kRaE85yQ) | `JustEnoughMekanismMultiblocks-1.21.1-7.21.jar` | Cliente |
| [Just Enough Professions (JEP)](https://modrinth.com/mod/kB56GtWA) | `JustEnoughProfessions-neoforge-1.21.1-4.0.5.jar` | Cliente e servidor |
| [Just Enough Resources (JER)](https://modrinth.com/mod/uEfK2CXF) | `JustEnoughResources-NeoForge-1.21.1-1.6.0.17.jar` | Cliente |
| [Just Zoom](https://modrinth.com/mod/iAiqcykM) | `justzoom_neoforge_3.0.1_MC_1.21.1.jar` | Cliente |
| [LambDynamicLights - Dynamic Lights](https://modrinth.com/mod/yBW8D80W) | `lambdynamiclights-4.8.11+1.21.1.jar` | Cliente |
| [More Overlays Updated](https://modrinth.com/mod/Thy5Pqut) | `moreoverlays-1.24.2-mc1.21.1-neoforge.jar` | Cliente |
| [Mouse Tweaks](https://modrinth.com/mod/aC3cM3Vq) | `MouseTweaks-neoforge-mc1.21-2.26.1.jar` | Cliente |
| [Ping Wheel](https://modrinth.com/mod/QQXAdCzh) | `Ping-Wheel-1.12.2-neoforge-1.21.1.jar` | Cliente e servidor |
| [Searchables](https://modrinth.com/mod/fuuu3xnx) | `Searchables-neoforge-1.21.1-1.0.2.jar` | Cliente |
| [Sound Physics Remastered](https://modrinth.com/mod/qyVF9oeo) | `sound-physics-remastered-neoforge-1.21.1-1.5.1.jar` | Cliente |

### Só no servidor
Administração, desempenho e geração de mundo. O launcher do jogador ignora estes.

| Mod | Arquivo | Lado |
| --- | --- | --- |
| [AI Improvements: Performance Tuning](https://modrinth.com/mod/DSVgwcji) | `AI-Improvements-1.21-0.5.3.jar` | Servidor |
| [Almanac](https://modrinth.com/mod/Gi02250Z) | `Almanac-1.21.1-2-neoforge-1.5.2.jar` | Servidor |
| [BanHammer](https://modrinth.com/mod/Wpqg0ciI) | `banhammer-0.11.1+1.21.jar` | Servidor |
| [Better End Cities Better End](https://www.curseforge.com/projects/959460) | `BetterEndCities-BetterEnd-1.21.jar` | Servidor |
| [CalcMod: NeoForged](https://modrinth.com/mod/7uxk5PIo) | `calcmod-neoforged-1.4.2+neoforge.1.21.1.jar` | Servidor |
| [Chunky](https://modrinth.com/mod/fALzjamp) | `Chunky-NeoForge-1.4.23.jar` | Servidor |
| [Clumps](https://modrinth.com/mod/Wnxd13zP) | `Clumps-neoforge-1.21.1-19.0.0.1.jar` | Servidor |
| [Collective](https://modrinth.com/mod/e0M1UDsY) | `collective-1.21.1-8.42.jar` | Servidor |
| [Crash Utilities](https://www.curseforge.com/projects/371813) | `crashutilities-9.0.4.jar` | Servidor |
| [CraterLib](https://modrinth.com/mod/Nn8Wasaq) | `CraterLib-Neoforge-1.21-3.1.3.jar` | Servidor |
| [Cupboard](https://www.curseforge.com/projects/326652) | `cupboard-1.21.1-4.2.jar` | Servidor |
| [Dungeon Crawl](https://modrinth.com/mod/q0rRg4lH) | `DungeonCrawl-NeoForge-1.21-2.3.17.jar` | Servidor |
| [Dungeons and Taverns](https://modrinth.com/mod/tpehi7ww) | `dungeons-and-taverns-v4.4.4.jar` | Servidor |
| [EasyAuth](https://modrinth.com/mod/aZj58GfX) | `easyauth-mc1.21-3.3.6.jar` | Servidor |
| [Essential Commands](https://modrinth.com/mod/6VdDUivB) | `essential_commands-0.35.2-mc1.21.jar` | Servidor |
| [Fast Async World Save[Forge/Neo/Fabric]](https://www.curseforge.com/projects/951499) | `fastasyncworldsave-1.21-2.6.jar` | Servidor |
| [Flan](https://modrinth.com/mod/Si383TIH) | `flan-1.21.1-1.12.8-neoforge.jar` | Servidor |
| [GriefLogger](https://modrinth.com/mod/8oGVUFuX) | `grieflogger-1.2.10-1.21.1-neoforge.jar` | Servidor |
| [Harvest with ease](https://modrinth.com/mod/W4Ajthd2) | `harvest-with-ease-neoforge-1.21-9.4.0.jar` | Servidor |
| [Immersive Optimization](https://modrinth.com/mod/vNZgQmjg) | `immersive_optimization-neoforge-1.21.1-0.2.0.jar` | Servidor |
| [Inv View Forge/NeoForge](https://modrinth.com/mod/RXM1nxge) | `inv_view-4.2.1-neoforge+1.21.1.jar` | Servidor |
| [Krypton Reno](https://modrinth.com/mod/JkxWVYwU) | `krypton_fnp-neoforge-1.21.1-0.2.28.1-1.21.1.jar` | Servidor |
| [Leashable Players](https://modrinth.com/mod/BKyMf6XK) | `leashmod-1.1.0.jar` | Servidor |
| [Leaves Be Gone](https://modrinth.com/mod/AVq17PqV) | `LeavesBeGone-v21.1.1-1.21.1-NeoForge.jar` | Servidor |
| [Let Me Despawn](https://modrinth.com/mod/vE2FN5qn) | `letmedespawn-1.21.x-neoforge-1.5.0.jar` | Servidor |
| [Log Begone](https://modrinth.com/mod/9ON3zv6e) | `logbegone-neoforge-1.21.1-1.0.3.jar` | Servidor |
| [LuckPerms](https://modrinth.com/mod/Vebnzrzj) | `LuckPerms-NeoForge-5.4.150.jar` | Servidor |
| [LuckPerms Placeholders](https://github.com/IunaMC/modpack/releases/download/arquivos-servidor/LuckPerms-Fabric-Placeholders.jar) | `LuckPerms-Fabric-Placeholders.jar` | Servidor |
| [Maintenance Mode](https://modrinth.com/mod/QOkEkSap) | `MaintenanceMode-Universal-1.3.4.jar` | Servidor |
| [MixinTrace Reloaded](https://modrinth.com/mod/wx2WW8va) | `MixinTrace reloaded [NEOFORGE]-1.1.0+1.21.jar` | Servidor |
| [NetherPortalFix](https://modrinth.com/mod/nPZr02ET) | `netherportalfix-neoforge-1.21.1-21.1.1.jar` | Servidor |
| [No Random Ticks](https://modrinth.com/mod/K2uLi5au) | `norandomticks-0.4-1.21.1.jar` | Servidor |
| [NoisiumForked](https://modrinth.com/mod/hasdd01q) | `noisium-neoforge-2.7.0+mc1.21-1.21.1.jar` | Servidor |
| [Observable](https://modrinth.com/mod/VYRu7qmG) | `observable-5.4.4.jar` | Servidor |
| [Saturn](https://modrinth.com/mod/2eT495vq) | `saturn-mc1.21.1-0.1.5.jar` | Servidor |
| [Server Chat Log History](https://modrinth.com/mod/HZ6y1yNV) | `server_chat_log_history-1.10+1.21.1.jar` | Servidor |
| [Server Performance - Smooth Chunk Save](https://www.curseforge.com/projects/582327) | `smoothchunk-1.21-4.1.jar` | Servidor |
| [ServerCore](https://modrinth.com/mod/4WWQxlQP) | `servercore-neoforge-1.5.19+1.21.1.jar` | Servidor |
| [Simple Discord Link](https://modrinth.com/mod/Sh0YauEf) | `SimpleDiscordLink-Universal-3.4.5.jar` | Servidor |
| [Skin Restorer](https://modrinth.com/mod/ghrZDhGW) | `skinrestorer-2.11.0+1.21-neoforge.jar` | Servidor |
| [Skin Shuffle](https://modrinth.com/mod/3s19I5jr) | `SkinShuffle-2.9.1+1.21.jar` | Servidor |
| [spark](https://modrinth.com/mod/l6YH9Als) | `spark-1.10.124-neoforge.jar` | Servidor |
| [Starter Kit](https://modrinth.com/mod/6L3ydNi8) | `starterkit-1.21.1-8.3.jar` | Servidor |
| [Structory](https://modrinth.com/mod/aKCwCJlY) | `Structory_26.2_v1.3.7.jar` | Servidor |
| [Styled Chat](https://modrinth.com/mod/doqSKB0e) | `styled-chat-2.6.1+1.21.jar` | Servidor |
| [Styled Player List](https://modrinth.com/mod/DQIfKUHf) | `styledplayerlist-3.5.1+1.21.jar` | Servidor |
| [Terralith](https://modrinth.com/mod/8oi3bsk5) | `Terralith_1.21.1_v2.6.2_Neoforge.jar` | Servidor |
| [Tick Stasis](https://modrinth.com/mod/t6XBQ2xn) | `tick-stasis-1.1.1.jar` | Servidor |
| [TT20 (TPS Fixer)](https://modrinth.com/mod/YS3ZignI) | `tt20-0.8.5+mc1.21.1-neoforge.jar` | Servidor |
| [Vanishmod](https://modrinth.com/mod/MihN2cw5) | `Vanishmod-1.21.1-1.1.21.jar` | Servidor |
| [View Distance Fix](https://modrinth.com/mod/nxrXbh5K) | `viewdistancefix-fabric-1.21.1-1.0.2.jar` | Servidor |
| [Waystones Teleport Pets](https://modrinth.com/mod/VaCl9OtG) | `WaystonesTeleportPets-1.2-neoforge-1.21.1.jar` | Servidor |
| [When Dungeons Arise](https://modrinth.com/mod/8DfbfASn) | `DungeonsArise-1.21.1-2.1.68-release.jar` | Servidor |
| [When Dungeons Arise: Seven Seas](https://modrinth.com/mod/ZsrrjDbP) | `DungeonsAriseSevenSeas-1.21.x-1.0.4-neoforge.jar` | Servidor |
| [World Border](https://modrinth.com/mod/nN96GjON) | `worldborder-1.21.1-5.0.jar` | Servidor |
| [YUNG's Better Desert Temples](https://modrinth.com/mod/XNlO7sBv) | `YungsBetterDesertTemples-1.21.1-NeoForge-4.1.5.jar` | Servidor |
| [YUNG's Better Dungeons](https://modrinth.com/mod/o1C1Dkj5) | `YungsBetterDungeons-1.21.1-NeoForge-5.1.4.jar` | Servidor |
| [YUNG's Better End Island](https://modrinth.com/mod/2BwBOmBQ) | `YungsBetterEndIsland-1.21.1-NeoForge-3.1.2.jar` | Servidor |
| [YUNG's Better Jungle Temples](https://modrinth.com/mod/z9Ve58Ih) | `YungsBetterJungleTemples-1.21.1-NeoForge-3.1.2.jar` | Servidor |
| [YUNG's Better Mineshafts](https://modrinth.com/mod/HjmxVlSr) | `YungsBetterMineshafts-1.21.1-NeoForge-5.1.1.jar` | Servidor |
| [YUNG's Better Nether Fortresses](https://modrinth.com/mod/Z2mXHnxP) | `YungsBetterNetherFortresses-1.21.1-NeoForge-3.1.5.jar` | Servidor |
| [YUNG's Better Ocean Monuments](https://modrinth.com/mod/3dT9sgt4) | `YungsBetterOceanMonuments-1.21.1-NeoForge-4.1.2.jar` | Servidor |
| [YUNG's Better Strongholds](https://modrinth.com/mod/kidLKymU) | `YungsBetterStrongholds-1.21.1-NeoForge-5.1.3.jar` | Servidor |
<!-- lista-de-mods:fim -->
