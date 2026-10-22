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
  - Bash(bash scripts/op.sh *)
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
1. Se nenhuma beta desta versão saiu (não há tag `v<versão>-beta.*`), pergunte se pode publicar sem beta (então use `--sem-beta`). Se a versão for MAJOR, pergunte e só com o OK use `--major`.
2. Rode `bash scripts/op.sh estavel <versão>` (em segundo plano; sem versão, ele usa a da beta atual). Ele confere a branch, troca a versão, roda `refresh` e `readme`, commita (assinado), faz o push, espera o Validar, abre o PR, espera *Entrada na main*, faz `gh pr merge --merge`, espera o Release e alinha a `devel/devel`. Para no primeiro passo vermelho: mostre o erro e pare.
3. Saída 3 com "O MUDANCAS.md não tem o título…" ou "ainda tem a linha 'Beta: …'": reescreva o `MUDANCAS.md` no formato do atual: título `# Mudanças — v<versão>, <resumo>`, quem precisa reinstalar e as seções Adicionou, Atualizou e Removeu, comparando com a **última estável**, não com as betas, sem a linha "Beta: …". Rode o script de novo.
4. Saída 3 com "Sem PR aberto": escreva o corpo do PR em um arquivo fora do repo (seções Resumo, Mods, outras mudanças e Testes; sem menção ao Claude) e rode o script com `--corpo <arquivo>`.

10. Se o Release terminou verde, siga direto para a skill `/propagar` com a versão, sem esperar novo pedido: a estável só termina com a moderação e as configs alinhadas.

Responda só com a versão, os links do PR e da release, o status do Modrinth e da CurseForge e o resultado do `/propagar`.
