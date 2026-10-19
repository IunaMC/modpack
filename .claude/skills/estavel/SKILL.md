---
name: estavel
description: Publica a versão estável do modpack pelo PR da devel/devel para a main (versão, MUDANCAS.md, PR, merge commit, Release, Modrinth e CurseForge) e deixa a devel/devel pronta de novo. Use quando o usuário pedir para soltar ou publicar a estável do modpack.
argument-hint: "[versão, ex.: 3.3.0]"
model: sonnet
effort: low
allowed-tools:
  - Read
  - Edit
  - Bash(git status *)
  - Bash(git log *)
  - Bash(git diff *)
  - Bash(git show *)
  - Bash(git tag *)
  - Bash(git -c versionsort.suffix=- tag *)
  - Bash(git fetch *)
  - Bash(git merge --ff-only *)
  - Bash(git add *)
  - Bash(git commit *)
  - Bash(git push *)
  - Bash(python3 scripts/pack.py *)
  - Bash(cd pack && packwiz refresh*)
  - Bash(gh run *)
  - Bash(gh pr *)
  - Bash(gh release view *)
---

Publique a estável do pack. Versão pedida: `$ARGUMENTS` (vazio = a da beta atual sem o `-beta.N`).

## Estado atual
- Branch: !`git status -sb | head -1`
- Arquivos alterados: !`git status --porcelain || true`
- Versão no pack.toml: !`python3 scripts/pack.py versao`
- Última estável: !`git fetch -q --tags 2>/dev/null; git tag --list 'v*' --sort=-v:refname | grep -v -- -beta | head -1`
- Mods desde a última estável: !`python3 scripts/pack.py mudancas estavel || true`
- Commits que ainda não estão na main: !`git log --oneline origin/main..HEAD || true`
- Validar na devel/devel: !`gh run list --workflow validar.yaml --branch devel/devel --limit 1 || true`
- PR aberto: !`gh pr list --head devel/devel --json number,url -q '.[] | "#\(.number) \(.url)"' || true`
- `MUDANCAS.md` atual: !`cat MUDANCAS.md`

## Passos
1. A branch tem que ser `devel/devel`, a árvore limpa e o último Validar verde. Se faltar algo, pare e diga o quê.
2. Se nenhuma beta desta versão saiu (não há tag `v<versão>-beta.*`), pergunte se pode publicar sem beta.
3. Troque `version` em `pack/pack.toml` pela estável, rode `cd pack && packwiz refresh` e `python3 scripts/pack.py readme`.
4. Reescreva o `MUDANCAS.md` no formato do atual: título `# Mudanças — v<versão>, <resumo>`, quem precisa reinstalar e as seções Adicionou, Atualizou e Removeu, comparando com a **última estável**, não com as betas. Tire a linha "Beta: …".
5. Um commit: `git commit -S -s -m "build: prepara a versao <versão>"`, depois `git push`. Espere o Validar desse commit com `gh run watch <id> --exit-status` em segundo plano. Se falhar, mostre o erro e pare.
6. Sem PR aberto, crie: `gh pr create --base main --head devel/devel --title "Versão <versão>: <resumo>" --body "<corpo>"`, com as seções Resumo, Mods (o que muda para o jogador), outras mudanças e Testes (Validar verde, betas publicadas). Sem menção ao Claude.
7. `gh pr merge <número> --merge`, nunca `--rebase` e nunca `--delete-branch`: a `devel/devel` é permanente.
8. Acompanhe o Release da `main`: `gh run list --workflow release.yaml --branch main --limit 1` e `gh run watch <id> --exit-status`. Confira os passos "Publicar no Modrinth" e "Publicar na CurseForge" (`gh run view <id>`); se um falhar, mostre o erro, mas a release do GitHub já vale. Depois, `gh release view v<versão>`.
9. Alinhe a `devel/devel` com a `main`: `git fetch`, `git merge --ff-only origin/main` e `git push`.

10. Se o Release terminou verde, siga direto para a skill `/propagar` com a versão, sem esperar novo pedido: a estável só termina com a moderação e as configs alinhadas.

Responda só com a versão, os links do PR e da release, o status do Modrinth e da CurseForge e o resultado do `/propagar`.
