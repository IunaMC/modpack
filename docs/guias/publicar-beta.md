# Publicar uma beta

Solta a próxima versão como *pre-release*: GitHub e CurseForge. O
servidor não a instala.

**Skill:** `/beta [versão]`.

## Antes

- Na `devel/devel`, com a árvore limpa.
- Depois de uma estável, o próprio `op.sh beta` alinha a `devel/devel` à
  `main` (`git merge --ff-only`); se não for possível avançar, ele para.

## Passos

O alvo `beta` faz tudo o que é mecânico e só para onde precisa de gente:

```sh
bash scripts/op.sh beta [versão] [--major]
```

Ele confere a branch e a árvore, avança a `devel/devel` com a `main`, escolhe
a versão (a que você passar, ou a sugerida pelo SemVer; MAJOR só com
`--major`, depois de confirmar com a equipe, veja os
[critérios](../referencia/versionamento.md#versão)), troca `version` em
`pack/pack.toml`, roda o `refresh` e o README.

1. Se o `MUDANCAS.md` não tiver o título `# Mudanças — v<versão>, <resumo>`, o
   comando **para antes do commit** e mostra os mods mudados. Reescreva o
   arquivo no formato do atual: a linha "Beta: sai como pre-release e o
   servidor não a instala.", quem precisa reinstalar e as seções Adicionou,
   Atualizou e Removeu. A lista de mods sai de:

   ```sh
   python3 scripts/pack.py mudancas ultima
   ```

2. Rode `bash scripts/op.sh beta` de novo. Com o título certo, ele faz o commit
   `build: prepara a versao <versão>` (assinado), o push, espera o Release e
   mostra o link da pre-release.

## Conferir

O Release cria a tag, a pre-release e o envio às plataformas. O `op.sh beta`
já espera por ele; para rever depois:

```sh
gh run list --branch devel/devel --limit 3
```

```sh
gh release view v<versão>
```
