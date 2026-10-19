---
name: beta
description: Prepara e publica a próxima versão beta do modpack pela devel/devel (versão no pack.toml, README, MUDANCAS.md, commit e push). Use quando o usuário pedir para soltar ou publicar uma beta do modpack.
argument-hint: "[versão, ex.: 3.3.0-beta.1]"
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
  - Bash(packwiz refresh*)
  - Bash(cd pack && packwiz refresh*)
  - Bash(gh run *)
  - Bash(gh release view *)
---

Prepare a próxima beta do pack. Versão pedida: `$ARGUMENTS` (vazio = use a sugerida abaixo).

## Estado atual
- Branch: !`git status -sb | head -1`
- Arquivos alterados: !`git status --porcelain || true`
- Versão no pack.toml: !`python3 scripts/pack.py versao`
- Sugerida (e o motivo): !`python3 scripts/pack.py proxima-beta 2>&1`
- Última tag: !`git -c versionsort.suffix=- tag --list 'v*' --sort=-v:refname | head -1`
- Mods desde a última tag: !`python3 scripts/pack.py mudancas ultima || true`
- Commits recentes (os que vêm depois da última tag entram): !`git log --oneline --decorate -20 || true`
- `MUDANCAS.md` atual: !`cat MUDANCAS.md`

## Passos
1. A branch tem que ser `devel/devel` e a árvore tem que estar limpa. Se a remota aparecer como `[gone]` (o merge de uma estável a apaga), rode `git fetch --prune` e `git merge --ff-only origin/main`. Se não der para avançar assim, pare e diga o que falta.
2. Se a sugerida for MAJOR, pergunte antes de seguir.
3. Troque `version` em `pack/pack.toml`, rode `cd pack && packwiz refresh` e depois `python3 scripts/pack.py readme`.
4. Reescreva o `MUDANCAS.md` no formato do atual: título `# Mudanças — v<versão>, <resumo curto>`, a linha "Beta: sai como pre-release e o servidor não a instala.", quem precisa reinstalar e as seções Adicionou, Atualizou e Removeu, cada mod com link do Modrinth, versão, licença e lado. A fonte são os mods e os commits listados acima.
5. Um commit só: `git commit -S -s -m "build: prepara a versao <versão>"`. Sem `Co-Authored-By` e sem menção ao Claude.
6. `git push`. O `release.yaml` cria a tag e a pre-release. Acompanhe com `gh run list --branch devel/devel --limit 3`. Quando terminar, rode `gh release view v<versão>`. Se o CI falhar, mostre o erro e pare.

Responda só com a versão publicada, o link da release e o status do CI.
