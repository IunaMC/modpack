# Adicionar um mod

Põe um mod do Modrinth no pack, com as dependências e a fonte da CurseForge,
um commit por item.

**Skill:** `/add-mod <slug> [server|client|both]`.

## Antes

- Na `devel/devel`, com a árvore limpa (`git switch devel/devel && git status`).
- `packwiz` e Python 3 instalados.

## Passos

1. Adicione pelo packwiz e aceite as dependências que ele oferecer:

   ```sh
   cd pack && packwiz modrinth add <slug> -y && cd ..
   ```

2. Escolha o lado de cada mod novo e das dependências, à mão: `side = "client"`,
   `"server"` ou `"both"` no `.pw.toml`. É decisão de uma pessoa, porque a
   declaração do Modrinth ou da CurseForge pode estar errada, faltar ou não
   dizer tudo (há mod de cliente que ganha recursos se estiver no servidor).
   Um mod de conteúdo marcado como `client` ou `server` impede o jogador de
   entrar no servidor. Para ver o que o Modrinth declara e a licença, sem gravar
   nada:

   ```sh
   python3 scripts/pack.py lado pack/mods/<arquivo>.pw.toml...
   ```

3. Nenhum mod é opcional: o pack não usa `[option]`, porque a escolha só
   existe no Modrinth e o pack também vive na CurseForge.
4. Mod baixado do Modrinth não precisa de permissão no `.mrpack`, mesmo All
   Rights Reserved: o arquivo só aponta para o CDN do Modrinth. Só o jar que
   existe apenas na CurseForge vai embutido e precisa de permissão na página
   Permissions ([`modrinth/permissoes.md`](../../modrinth/permissoes.md)). Sem
   ela, o mod entra em `[[reduzido.fora]]` do `modrinth/projeto.toml` e nas
   descrições, e sai só do `.mrpack` do Modrinth
   ([decisão 0007](../decisoes/0007-mrpack-reduzido-no-modrinth.md)).
5. Todo mod que não é `server` precisa da fonte da CurseForge. O Project ID
   fica na lateral da página do mod em curseforge.com:

   ```sh
   python3 scripts/curseforge.py ligar pack/mods/<arquivo>.pw.toml <Project ID>
   ```

   Se a CurseForge não tiver o mesmo arquivo, o mod precisa de uma versão que
   exista nas duas fontes.
6. Recalcule o índice e a lista de mods:

   ```sh
   bash scripts/op.sh refresh
   ```

7. Um commit por item, dependências primeiro, levando o `.pw.toml`,
   `pack/index.toml`, `pack/pack.toml` e o `README.md`:

   ```sh
   git commit -S -s -m "feat(deps): adiciona <Nome> <versão>"
   ```

   ```sh
   git commit -S -s -m "feat(mods): adiciona <Nome> <versão>"
   ```

   No mod, um corpo curto dizendo o que ele faz. Se ele for só de um lado,
   acrescente "no servidor" ou "no cliente" ao título.

Não mexa na versão: ela sobe na [beta](publicar-beta.md).

## Conferir

```sh
bash scripts/op.sh conferir
```

O Validar roda no próximo push e sobe o servidor com o mod.

Jar sem download fixo, fora do Modrinth e da CurseForge:
[arquivos externos](arquivos-externos.md).
