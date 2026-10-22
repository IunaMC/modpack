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

Editor em **Markdown**. A descrição é própria da CurseForge, em
[`descricao.md`](descricao.md), e **não** é gerada da do Modrinth: as duas
começam parecidas, mas cada plataforma tem a sua instalação, os seus mods
(aqui entram Twilight Forest e Mob Grinding Utils) e os seus créditos. Mudou o
pack, atualize as duas à mão. Para colar:

```sh
python3 scripts/curseforge.py descricao
```

Depois de colar, rode `python3 scripts/curseforge.py descricao --marcar` e faça
o commit do `descricao.sha256`. O português não vai para a CurseForge, que só
recebe o inglês. Se algum mod for no `overrides/` (de fora da CurseForge), a
seção "Credits for mods not hosted on CurseForge" do `descricao.md` lista cada
um; hoje ela diz que não há nenhum.
