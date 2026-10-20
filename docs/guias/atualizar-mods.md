# Atualizar mods

Leva um mod, ou todos, para a versão nova, nas duas fontes.

A issue semanal **Atualizações de mods** lista o que tem versão nova.

## Antes

- Na `devel/devel`, com a árvore limpa.

## Passos

1. Atualize pelo packwiz, um mod ou todos (`--all`):

   ```sh
   cd pack && packwiz update <mod> && cd ..
   ```

2. O `packwiz update` só segue o Modrinth. Leve a CurseForge para o mesmo
   arquivo e recalcule o índice e a lista de mods:

   ```sh
   bash scripts/op.sh corrigir
   ```

3. Um commit por mod, levando o `.pw.toml`, `pack/index.toml`,
   `pack/pack.toml` e o `README.md`:

   ```sh
   git commit -S -s -m "feat(mods): atualiza <Nome> <versão>"
   ```

   Dependência usa `feat(deps): …`.

Atualizar mod é MINOR, e a versão sobe na [beta](publicar-beta.md).

## Conferir

```sh
bash scripts/op.sh conferir
```

Para só ver o que mudaria, sem ficar com a mudança:
`cd pack && packwiz update --all`, `git diff` e depois `git checkout pack/`.
