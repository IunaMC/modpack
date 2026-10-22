# Documentação

Como manter o pack. A instalação para jogadores e o comando do servidor estão
no [README](../README.md) principal. O que atravessa repositórios
(arquitetura, ciclo de versão entre os repositórios, cargos, glossário) está
em [IunaMC/docs](https://github.com/IunaMC/docs).

## Guias

| Guia | Skill |
| --- | --- |
| [Adicionar um mod](guias/adicionar-mod.md) | `/add-mod` |
| [Remover um mod](guias/remover-mod.md) | `/remover-mod` |
| [Atualizar mods](guias/atualizar-mods.md) | — |
| [Publicar uma beta](guias/publicar-beta.md) | `/beta` |
| [Publicar a estável](guias/publicar-estavel.md) | `/estavel` |
| [Propagar uma estável](guias/propagar.md) | `/propagar` |
| [Publicar documentação](guias/publicar-docs.md) | — |
| [Arquivos externos](guias/arquivos-externos.md) | — |
| [Servidor local e teste de boot](guias/servidor-local.md) | `/testar` |

## Referência

- [Versionamento, branches e commits](referencia/versionamento.md)
- [Workflows](referencia/workflows.md)
- [Scripts e skills](referencia/scripts.md)
- [Segredos](referencia/segredos.md)

## Decisões

- [0001: packwiz como fonte única do jogador e do servidor](decisoes/0001-packwiz-fonte-unica.md)
- [0002: commits assinados e merge commit na `main`](decisoes/0002-merge-commit-assinado.md)
- [0003: `devel/devel` permanente e `main` só com estáveis](decisoes/0003-devel-permanente-main-estavel.md)
- [0004: páginas das plataformas como código](decisoes/0004-paginas-como-codigo.md)
- [0005: o pack não perde mods por causa de uma plataforma](decisoes/0005-mrpack-completo-sem-cortar-mods.md)
- [0006: o que o .mrpack leva além dos mods](decisoes/0006-metadados-do-mrpack.md)
- [0007: o Modrinth recebe um .mrpack reduzido](decisoes/0007-mrpack-reduzido-no-modrinth.md)

## Plataformas

- [Modrinth](../modrinth/README.md): a página sai de `modrinth/`.
- [CurseForge](../curseforge/README.md): o projeto e a revisão dos arquivos.

O padrão de escrita desta documentação está em
[IunaMC/docs](https://github.com/IunaMC/docs/blob/main/referencia/padrao-de-escrita.md).
