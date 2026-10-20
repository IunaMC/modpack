# 0004: páginas das plataformas como código

- **Data:** 17/10/2026 (Modrinth); 18/10/2026 (CurseForge)
- **Estado:** aceita
- **Origem:** `6eaef95` (página do Modrinth a partir de `modrinth/`) e
  `aa76656` (projeto da CurseForge documentado)

## Contexto

Editar a página do projeto no site não deixa histórico, revisão nem como
desfazer, e o texto se perde de vista entre uma versão e outra.

## Decisão

- **Modrinth:** a página inteira sai de [`modrinth/`](../../modrinth/README.md)
  (nome, resumo, categorias, links, descrição, ícone e galeria). O workflow
  Modrinth mostra o que mudaria fora da `main` e aplica na `main`. Não se
  edita pelo site.
- **CurseForge:** sem API de edição, a descrição também sai do repositório
  ([`curseforge/`](../../curseforge/README.md)), mas é colada à mão. O
  `curseforge.py descricao --marcar` registra o que foi colado, e o `status`
  avisa quando o site está desatualizado.

## Consequências

- Mudar a página é um commit, revisado como qualquer outro.
- Uma edição feita no site do Modrinth some no próximo push.
- A descrição é em inglês, com o português recolhível. É a única exceção ao
  português como idioma principal.
