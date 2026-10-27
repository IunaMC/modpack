# Publicar a estável

Leva a versão da `devel/devel` para a `main` por PR. O servidor passa a
instalá-la no próximo reinício.

**Skill:** `/estavel [versão]`, que no fim chama o `/propagar`.

## Antes

- Validar verde na `devel/devel`.
- Ao menos uma beta desta versão (tag `v<versão>-beta.*`).

## Passos

O alvo `estavel` faz os passos mecânicos em ordem e **para no primeiro
vermelho**:

```sh
bash scripts/op.sh estavel [versão] [--corpo <arquivo.md>] [--major] [--sem-beta]
```

A versão padrão é a da beta atual sem o `-beta.N`. `--sem-beta` autoriza
publicar sem beta desta versão e `--major` confirma uma mudança MAJOR (o
script acrescenta "MAJOR confirmado" ao corpo do PR).

1. O comando troca `version` em `pack/pack.toml` e roda o `refresh` e o README.
   Se o `MUDANCAS.md` não tiver o título `# Mudanças — v<versão>, <resumo>`, ou
   ainda tiver a linha "Beta: …", **para antes do commit**. Reescreva-o
   comparando com a **última estável**, sem a linha "Beta: …":

   ```sh
   python3 scripts/pack.py mudancas estavel
   ```

2. Rode de novo. Ele faz o commit `build: prepara a versao <versão>`
   (assinado), o push e espera o Validar desse commit (`op.sh ci`).
3. Sem PR aberto, ele para pedindo o corpo. Escreva o arquivo com Resumo, Mods
   (o que muda para o jogador), outras mudanças e Testes (Validar verde, betas
   publicadas) e passe com `--corpo`. O título do PR sai do título do
   `MUDANCAS.md`. Antes de abrir, ele confere as
   [regras da `main`](../referencia/versionamento.md#o-que-entra-na-main) com
   `pack.py conferir` e depois espera o job *Entrada na main*.
4. Com tudo verde, faz o merge com merge commit, nunca `--rebase`
   ([por quê](../decisoes/0002-merge-commit-assinado.md)) e nunca
   `--delete-branch`: a `devel/devel` é permanente.
5. Espera o Release da `main` e mostra o resultado do passo "Publicar na
   CurseForge" ([decisão 0008](../decisoes/0008-sem-distribuicao-no-modrinth.md)).
   Se o Release falhar, a release do GitHub ainda vale.
6. Alinha a `devel/devel` com a `main` (`merge --ff-only` e push), mesmo que o
   Release tenha falhado, porque o merge já aconteceu.
7. [Propague](https://github.com/IunaMC/docs/blob/main/processo/propagar.md) a
   versão para a moderação e as configs (`bash scripts/op.sh propagar`).

## Conferir

```sh
gh release view v<versão>
```

```sh
python3 scripts/curseforge.py status
```

A CurseForge revisa cada arquivo antes de mostrar. Veja o
[README da CurseForge](../../curseforge/README.md).
