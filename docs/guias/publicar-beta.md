# Publicar uma beta

Solta a próxima versão como *pre-release*: GitHub, Modrinth e CurseForge. O
servidor não a instala.

**Skill:** `/beta [versão]`.

## Antes

- Na `devel/devel`, com a árvore limpa.
- Depois de uma estável, alinhada à `main`:

  ```sh
  git fetch && git merge --ff-only origin/main
  ```

## Passos

1. Veja a versão sugerida pelo SemVer e o motivo:

   ```sh
   bash scripts/op.sh versao
   ```

   Se a sugestão for MAJOR, confirme com a equipe antes
   ([critérios](../referencia/versionamento.md#versão)).
2. Troque `version` em `pack/pack.toml` (ex.: `3.4.0-beta.1`) e rode
   `bash scripts/op.sh refresh`.
3. Reescreva o `MUDANCAS.md` no formato do atual: título
   `# Mudanças — v<versão>, <resumo>`, a linha "Beta: sai como pre-release e o
   servidor não a instala.", quem precisa reinstalar e as seções Adicionou,
   Atualizou e Removeu. A lista de mods sai de:

   ```sh
   python3 scripts/pack.py mudancas ultima
   ```

4. Um commit e push:

   ```sh
   git commit -S -s -am "build: prepara a versao <versão>"
   ```

   ```sh
   git push
   ```

## Conferir

O Release cria a tag, a pre-release e o envio às plataformas:

```sh
gh run list --branch devel/devel --limit 3
```

```sh
gh release view v<versão>
```
