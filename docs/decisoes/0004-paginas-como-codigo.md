# 0004: páginas das plataformas como código

- **Data:** 17/10/2026 (Modrinth); 18/10/2026 (CurseForge)
- **Estado:** aceita; a parte do Modrinth saiu com a
  [0008](0008-sem-distribuicao-no-modrinth.md) em 27/10/2026
- **Origem:** `6eaef95` (página do Modrinth a partir de `modrinth/`) e
  `aa76656` (projeto da CurseForge documentado)

## Contexto

Editar a página do projeto no site não deixa histórico, revisão nem como
desfazer, e o texto se perde de vista entre uma versão e outra.

## Decisão

- **Modrinth** (até a 0008): a página inteira saía de `modrinth/`
  (nome, resumo, categorias, links, descrição, ícone e galeria), aplicada
  pelo workflow Modrinth na `main`.
- **CurseForge:** sem API de edição, a descrição também sai do repositório
  ([`curseforge/`](../../curseforge/README.md)), mas é colada à mão. O
  `curseforge.py descricao --marcar` registra o que foi colado, e o `status`
  avisa quando o site está desatualizado.

## Consequências

- Mudar a página é um commit, revisado como qualquer outro.
- A descrição da CurseForge é em inglês. É a única exceção ao português como
  idioma principal.
