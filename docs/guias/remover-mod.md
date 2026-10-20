# Remover um mod

Tira um mod do pack, junto com as dependências que ficarem órfãs, um commit
por item.

**Skill:** `/remover-mod <nome> [motivo]`.

## Antes

- Na `devel/devel`, com a árvore limpa.
- Mod de conteúdo (`side = "both"`) apaga blocos e itens do mundo: combine com
  a staff antes.

## Passos

1. Ache o `.pw.toml` (`ls pack/mods | grep -i <nome>`) e anote nome, versão,
   lado e o `mod-id` de `[update.modrinth]`.
2. Veja quais dependências obrigatórias dele ficariam sem uso:
   `https://api.modrinth.com/v2/version/<version do [update.modrinth]>`, campo
   `dependencies` com `dependency_type` igual a `required`. Mantenha as que
   outro mod do pack ainda usa.
3. Remova o mod e cada dependência órfã:

   ```sh
   cd pack && packwiz remove <nome> && cd ..
   ```

4. Recalcule o índice e a lista de mods:

   ```sh
   bash scripts/op.sh refresh
   ```

5. Um commit por item, o mod primeiro, levando o `.pw.toml` apagado,
   `pack/index.toml`, `pack/pack.toml` e o `README.md`:

   ```sh
   git commit -S -s -m "feat(mods): remove <Nome> <versão>"
   ```

   ```sh
   git commit -S -s -m "feat(deps): remove <Nome> <versão>"
   ```

   No mod, o motivo no corpo. Na dependência, "Ninguém mais no pack usa."

Remover mod é MINOR, e a versão sobe na [beta](publicar-beta.md).

## Conferir

- `bash scripts/op.sh conferir`.
- Configs que sobraram no `minecraft-config`:
  `grep -rli <mod-id> ../iunamc.minecraft-config/config/`. Não apague por
  aqui: a limpeza é feita no repositório das configs.
