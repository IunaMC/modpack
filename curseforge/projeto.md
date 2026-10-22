# Campos do projeto na CurseForge

Copie cada campo, na ordem, para o formulário de **Edit Project** em
<https://authors.curseforge.com>. Os textos públicos ficam em inglês, como no
Modrinth. Projeto ID 1752945.

Esta página reflete o pack **3.4.0** (290 mods para o jogador, 2 resource packs
e 7 shaders). Quando a versão mudar, atualize o texto em
[`../modrinth/descricao.en.md`](../modrinth/descricao.en.md) e rode
`python3 scripts/curseforge.py descricao` para ter o que colar.

## Aba Description / Project Details

| Campo | Valor |
| --- | --- |
| Project name | `IUNA 2` |
| Summary (máx. 200 caracteres) | A Brazilian Minecraft community made for friends — and yes, we ‘don’t have a name’. |
| Main category | Tech |
| Additional categories | Magic, Adventure and RPG, Multiplayer, Exploration, Extra Large |
| Game version / loader | Minecraft 1.21.1, NeoForge (vem do arquivo enviado) |
| License | MIT License |
| Logo | [`../modrinth/imagens/icone.png`](../modrinth/imagens/icone.png) |
| Imagem de capa (Images) | [`../modrinth/imagens/banner.png`](../modrinth/imagens/banner.png), com o título "IUNA Mark II" |

O Summary tem 85 caracteres, bem abaixo do limite.

## Links (Project Links)

| Campo | Valor |
| --- | --- |
| Website | <https://wiki.iuna.club> |
| Source | <https://github.com/IunaMC/modpack> |
| Issues | <https://github.com/IunaMC/modpack/issues> |
| Wiki | <https://wiki.iuna.club> |
| Discord | em branco: não há convite público registrado. O servidor é fechado e as instruções ficam nos canais da comunidade |

## Description

Editor em **Markdown**. Cole a saída de:

```sh
python3 scripts/curseforge.py descricao
```

Ela é o [`../modrinth/descricao.en.md`](../modrinth/descricao.en.md) sem o
`# IUNA` do topo, mais a seção extra abaixo. Depois de colar, rode
`python3 scripts/curseforge.py descricao --marcar` e faça o commit do
`descricao.sha256`.

O que a descrição cobre hoje: o pack (Minecraft 1.21.1, NeoForge), a contagem
de mods, o aviso de que o servidor é fechado, as categorias de conteúdo
(tecnologia, magia, exploração com Twilight Forest, combate, comida,
construção, convivência, desempenho), os sete shaders e os dois resource packs,
o KubeJS, os mods opcionais, requisitos, singleplayer, versões e créditos. O
português (`modrinth/descricao.md`) não vai para a CurseForge, que só recebe o
inglês.

## Seção extra da descrição

Entra no fim da descrição. A parte de instalação existe porque o texto do
Modrinth fala de Modrinth App; na CurseForge o caminho é outro. A seção de
créditos só é obrigatória se algum mod for no `overrides/` (mod de fora da
CurseForge). Hoje a lista está vazia.

```md
## Installing from CurseForge

**CurseForge app:** open the page and click **Install**, or search for "IUNA"
in the Minecraft modpacks tab.

**Prism Launcher:** *Add Instance → CurseForge*, search for "IUNA" and pick the
version. You can also download the `.zip` from *Files* and use *Add Instance →
Import*.

The launcher installs NeoForge and downloads the mods for you. Everything else
in this page (requirements, updating, versions) works the same here. Unlike the
Modrinth version, this one includes The Twilight Forest and Mob Grinding Utils.

## Credits for mods not hosted on CurseForge

This pack includes the following mods from outside CurseForge, with thanks to
their authors:

- (none)
```
