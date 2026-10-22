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
  - Bash(bash scripts/op.sh beta*)
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
1. Se a sugerida for MAJOR, pergunte antes de seguir; só com o OK rode o script com `--major`.
2. Rode `bash scripts/op.sh beta <versão>` (sem a versão, ele usa a sugerida). Ele confere a branch e a árvore, avança a `devel/devel` com a `main`, troca a versão, roda `refresh` e `readme`. Se parar com "O MUDANCAS.md não tem o título da v<versão>" (saída 3), vá ao passo 3. Qualquer outra parada: mostre a mensagem e pare.
3. Reescreva o `MUDANCAS.md` no formato do atual: título `# Mudanças — v<versão>, <resumo curto>`, a linha "Beta: sai como pre-release e o servidor não a instala.", quem precisa reinstalar e as seções Adicionou, Atualizou e Removeu, cada mod com link do Modrinth, versão, licença e lado. A fonte são os mods e os commits listados acima.
4. Rode `bash scripts/op.sh beta` de novo (a mesma versão). Ele faz o commit assinado `build: prepara a versao <versão>`, o push, espera o Release e mostra o link. Sem `Co-Authored-By` e sem menção ao Claude. Se o Release falhar, mostre o erro e pare.

Responda só com a versão publicada, o link da release e o status do CI.
