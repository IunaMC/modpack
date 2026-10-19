# 0002: commits assinados e merge commit na `main`

- **Data:** 18/10/2026
- **Estado:** aceita
- **Origem:** PR [#10](https://github.com/IunaMC/modpack/pull/10), mergeado
  por rebase, e `c56fc44` (regras no `CLAUDE.md`)

## Contexto

O PR #10 foi mergeado com rebase. O GitHub recriou os commits na `main` sem a
assinatura GPG, e eles deixaram de aparecer como verificados.

## Decisão

- Todo commit sai com `git commit -S -s`: assinatura GPG e `Signed-off-by`.
- A `main` só recebe PR com merge commit (`gh pr merge --merge`). Rebase-merge
  e squash-merge estão fora.
- Sem `Co-Authored-By` nem menção a ferramentas de IA: a autoria é de quem
  assina.

## Consequências

- O histórico da `main` tem os commits originais, verificados, mais um merge
  commit por versão.
- Commits antigos com atribuição continuam na história. Reescrever mudaria
  todos os SHAs, e isso foi descartado.
- Commit de bot (o *Acompanhar pack base* da moderação) precisa ser reassinado
  antes do PR.
