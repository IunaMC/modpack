# Publicar documentação

Leva uma mudança só de documentação à `main` sem esperar uma versão do pack.
Documentação que acompanha código vai junto do código, pela `devel/devel`.

## Antes

- A mudança não mexe em `pack/`. Se mexer, o job *Entrada na main* recusa o PR.
- A `docs/docs` está em dia com a `main`:

  ```sh
  git fetch && git switch docs/docs && git merge origin/main
  ```

## Passos

1. Crie a branch do assunto a partir da `docs/docs`:

   ```sh
   git switch -c docs/<assunto> docs/docs
   ```

2. Escreva, confira e faça o commit:

   ```sh
   npx markdownlint-cli2 '**/*.md'
   ```

   ```sh
   git commit -S -s -am "docs: <o que mudou>"
   ```

3. Envie e abra o PR para a `docs/docs`. O workflow Docs confere links e estilo:

   ```sh
   git push -u origin docs/<assunto>
   ```

   ```sh
   gh pr create --base docs/docs --head docs/<assunto> --title "docs: <o que mudou>"
   ```

4. Com o Docs verde, faça merge com merge commit e apague a branch do assunto:

   ```sh
   gh pr merge <número> --merge --delete-branch
   ```

5. Quando quiser publicar o que se juntou na `docs/docs`, abra o PR para a
   `main`. O job *Entrada na main* tem de passar:

   ```sh
   gh pr create --base main --head docs/docs --title "docs: <resumo>"
   ```

   ```sh
   gh pr merge <número> --merge
   ```

6. Leve a `main` de volta para as duas branches de integração:

   ```sh
   git fetch && git switch docs/docs && git merge origin/main && git push
   ```

   ```sh
   git switch devel/devel && git merge origin/main && git push
   ```

   A `devel/devel` recebe um merge comum aqui, não `--ff-only`: ela pode ter
   trabalho que a `main` ainda não tem.

## Conferir

A mudança aparece na `main`, e nenhuma release nova sai, porque o `pack/` não
mudou.
