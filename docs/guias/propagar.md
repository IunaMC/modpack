# Propagar uma estável

Depois de uma estável do modpack, leva a mesma versão ao pack da staff
(`modpack-moderacao`) e às configs (`minecraft-config`). O mapa entre os três
repositórios está no
[processo de propagar](https://github.com/IunaMC/docs/blob/main/processo/propagar.md).

**Skill:** `/propagar [versão]`. O [`/estavel`](publicar-estavel.md) a chama no
fim.

## Antes

- A Release da estável terminou verde.
- Os clones `iunamc.modpack-moderacao` e `iunamc.minecraft-config` ficam ao
  lado do `modpack`, com a árvore limpa. O `minecraft-config` tem de estar na
  `devel/devel`. Para outros caminhos, use `MODERACAO_DIR` e `CONFIGS_DIR`.

## Passos

```sh
bash scripts/op.sh propagar <versão>
```

O alvo faz, em ordem, e para no primeiro passo vermelho:

1. **Moderação.** Se a `base.toml` da `main` já está na versão, pula. Senão,
   dispara o *Acompanhar pack base* (se a branch `base/v<versão>` ainda não
   existe), refaz o commit do bot com a sua assinatura
   (`commit --amend --reset-author -S -s` e `push --force-with-lease`, porque o
   Actions não tem a chave de quem mantém), abre o PR (`Closes` da issue de
   pack base, se houver), espera o Validar, mostra o `MUDANCAS.md`, faz o
   merge commit (nunca rebase), espera o Release de lá e alinha a
   `devel/devel` com a `main`.
2. **Configs.** Grava a versão em `MODPACK` (sem o `v`) e faz o commit
   `build: testa com o modpack <versão>` e o push, se ainda não estiver.

## Depois

A versão das configs não é publicada aqui: é o `/versao` do `minecraft-config`,
que testa o servidor com o pack novo. Depois vem o
[envio ao servidor](https://github.com/IunaMC/docs/blob/main/processo/enviar-configs.md).
