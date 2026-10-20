# Publicar a estável

Leva a versão da `devel/devel` para a `main` por PR. O servidor passa a
instalá-la no próximo reinício.

**Skill:** `/estavel [versão]`, que no fim chama o `/propagar`.

## Antes

- Validar verde na `devel/devel`.
- Ao menos uma beta desta versão (tag `v<versão>-beta.*`).

## Passos

1. Troque `version` em `pack/pack.toml` pela versão sem `-beta`, rode
   `bash scripts/op.sh refresh` e reescreva o `MUDANCAS.md` comparando com a
   **última estável**, sem a linha "Beta: …":

   ```sh
   python3 scripts/pack.py mudancas estavel
   ```

2. Commit e push, e espere o Validar desse commit:

   ```sh
   git commit -S -s -am "build: prepara a versao <versão>"
   ```

   ```sh
   git push
   ```

3. Abra o PR, com Resumo, Mods, outras mudanças e Testes no corpo. Se a versão
   for MAJOR, o corpo também leva a frase "MAJOR confirmado":

   ```sh
   gh pr create --base main --head devel/devel --title "Versão <versão>: <resumo>"
   ```

4. Espere o job *Entrada na main* ficar verde: sem ele, o GitHub não libera o
   merge ([regras](../referencia/versionamento.md#o-que-entra-na-main)). Para
   conferir antes de abrir o PR:

   ```sh
   python3 scripts/pack.py conferir origin/main HEAD --ramo devel/devel
   ```

   Depois, faça merge com merge commit,
   [nunca rebase](../decisoes/0002-merge-commit-assinado.md) e nunca apagando
   a branch:

   ```sh
   gh pr merge <número> --merge
   ```

5. Acompanhe o Release da `main` e confira os passos "Publicar no Modrinth" e
   "Publicar na CurseForge":

   ```sh
   gh run watch $(gh run list -w release.yaml -b main -L1 --json databaseId -q '.[0].databaseId')
   ```

6. Alinhe a `devel/devel` com a `main`. Ela é permanente: nunca a apague.

   ```sh
   git fetch && git merge --ff-only origin/main && git push
   ```

7. [Propague](https://github.com/IunaMC/docs/blob/main/processo/propagar.md) a
   versão para a moderação e as configs.

## Conferir

```sh
gh release view v<versão>
```

```sh
python3 scripts/curseforge.py status
```

A CurseForge revisa cada arquivo antes de mostrar. Veja o
[README da CurseForge](../../curseforge/README.md).
