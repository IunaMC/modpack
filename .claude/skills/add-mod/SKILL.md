---
name: add-mod
description: Adiciona um mod do Modrinth ao pack pelo packwiz, com as dependências, e faz um commit por item no padrão do repo.
argument-hint: "<slug ou link do Modrinth> [server|client|both] [opcional]"
disable-model-invocation: true
effort: low
---

Adicione ao pack: `$ARGUMENTS`. Lado padrão: `both`. Só é opcional se "opcional" estiver nos argumentos.

1. Confira: branch `devel/devel` e árvore limpa. Se não, pare e avise.
2. Dentro de `pack/`: `packwiz modrinth add <slug> -y`. Aceite as dependências que ele oferecer.
3. Para cada `.pw.toml` novo: ajuste `side`. Se for opcional, coloque `[option]` com `optional = true`, `default = true` e uma `description` curta em inglês, como nos outros. **Dependência de mod obrigatório nunca é opcional.** Depois, `packwiz refresh`.
4. Confira a licença na página do Modrinth. Se for ARR ou sem licença, avise antes de commitar, porque isso trava a página no Modrinth (ver `modrinth/permissoes.md`).
5. `python3 scripts/pack.py readme`.
6. Um commit por item, dependências primeiro, todos com `git commit -S -s` e sem `Co-Authored-By`:
   - dependência: `feat(deps): adiciona <Nome> <versão>`
   - mod: `feat(mods): adiciona <Nome> <versão>[ no servidor|no cliente]`, com um corpo curto dizendo o que ele faz.
   Os arquivos de cada commit: o `.pw.toml`, `pack/index.toml`, `pack/pack.toml` e o `README.md`, se mudou.
7. Não faça push nem mexa na versão: isso é o `/beta`.

Responda só com a lista do que entrou (nome, versão, lado, licença) e os commits.
