# Campos do projeto na CurseForge

Copie cada campo, na ordem, para o formulário de **Edit Project** em
<https://authors.curseforge.com>. Os textos públicos ficam em inglês. Projeto ID 1752945.

Quando o pack mudar (mods de destaque, número de mods, instalação), atualize o
texto em [`descricao.md`](descricao.md) e rode
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
| Logo | [`imagens/icone.png`](imagens/icone.png) |
| Imagem de capa (Images) | [`imagens/banner.png`](imagens/banner.png), com o título "IUNA Mark II" |

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

Editor em **Markdown**. A descrição está em
[`descricao.md`](descricao.md). Mudou o pack, atualize-a à mão. Para colar:

```sh
python3 scripts/curseforge.py descricao
```

Depois de colar, rode `python3 scripts/curseforge.py descricao --marcar` e faça
o commit do `descricao.sha256`. Hoje todo mod do `.zip` vem da própria
CurseForge. Se algum dia um mod for no `overrides/` (de fora da CurseForge),
acrescente ao `descricao.md` uma seção "Credits for mods not hosted on
CurseForge" com cada um, o autor e a licença.
