# Remover um mod

Tira um mod do pack, junto com as dependências que ficarem órfãs, um commit
por item.

**Skill:** `/remover-mod <nome> [motivo]`.

## Antes

- Na `devel/devel`, com a árvore limpa.
- Mod de conteúdo (`side = "both"`) apaga blocos e itens do mundo: combine com
  a staff antes.

## Passos

1. Ache o `.pw.toml` (`ls pack/mods | grep -i <nome>`) e anote nome, versão e
   lado.
2. Veja quais dependências obrigatórias dele ficariam sem uso, quais mods
   exigem o que vai sair e, se o `../iunamc.minecraft-config` existir, quais
   arquivos de config citam cada um. O comando não remove nada:

   ```sh
   python3 scripts/pack.py orfas <nome>
   ```

   Ele segue as dependências em cadeia e só olha o Modrinth. Mantenha as que
   outro mod do pack ainda usa e, na dúvida, mantenha também.
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
- Configs que sobraram no `minecraft-config`: a lista do `pack.py orfas`
  (passo 2). Não apague por aqui: a limpeza é feita no repositório das
  configs.
