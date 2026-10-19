---
name: propagar
description: Depois de uma estável do modpack, leva a versão nova ao pack de moderação (base.toml pelo Acompanhar pack base, commit reassinado, PR e merge) e ao MODPACK do minecraft-config. Use quando o usuário pedir para propagar ou sincronizar a versão nova do modpack com a moderação e as configs.
argument-hint: "[versão do modpack, ex.: 3.3.0]"
model: sonnet
effort: low
allowed-tools:
  - Read
  - Edit
  - Bash(git -C ../iunamc.modpack-moderacao *)
  - Bash(git -C ../iunamc.minecraft-config *)
  - Bash(gh workflow run *)
  - Bash(gh run *)
  - Bash(gh pr *)
  - Bash(gh issue *)
  - Bash(gh release *)
  - Bash(gh api repos/IunaMC/*)
  - Bash(cat *)
---

Propague a versão do modpack: `$ARGUMENTS` (vazio = a última estável abaixo). Os outros dois repos ficam ao lado deste: `../iunamc.modpack-moderacao` e `../iunamc.minecraft-config`.

## Estado atual
- Última estável do modpack: !`gh release list -R IunaMC/modpack --exclude-pre-releases --limit 1 --json tagName -q '.[0].tagName' || true`
- Base da moderação na main: !`gh api repos/IunaMC/modpack-moderacao/contents/base.toml -q .content | base64 -d | grep '^tag' || true`
- Issues e PRs de base na moderação: !`gh issue list -R IunaMC/modpack-moderacao --state open --search "Pack base" --json number,title -q '.[] | "issue #\(.number) \(.title)"'; gh pr list -R IunaMC/modpack-moderacao --json number,headRefName -q '.[] | "PR #\(.number) \(.headRefName)"' || true`
- `MODPACK` das configs: !`cat ../iunamc.minecraft-config/MODPACK 2>/dev/null || echo "(clone não encontrado)"`
- Árvores: !`git -C ../iunamc.modpack-moderacao status -sb | head -1; git -C ../iunamc.minecraft-config status -sb | head -1`

## 1. Moderação
Pule se a base já é a versão pedida.
1. Sem branch `base/v<versão>` nem issue, dispare o Acompanhar pack base em vez de esperar o horário diário: `gh workflow run acompanhar-base.yaml -R IunaMC/modpack-moderacao` (enquanto a `main` de lá não tiver o arquivo novo, ele ainda se chama `acompanhar-cliente.yaml`) e espere com `gh run watch <id> -R IunaMC/modpack-moderacao --exit-status`.
2. O commit do bot vem sem assinatura. Recrie com a sua:
   `git -C ../iunamc.modpack-moderacao fetch --prune`, `checkout base/v<versão>`, `commit --amend --no-edit --reset-author -S -s` e `push --force-with-lease`.
3. Sem PR da branch, crie: `gh pr create -R IunaMC/modpack-moderacao --base main --head base/v<versão> --title "Pack base v<versão>" --body "Closes #<issue>"`.
4. Espere o Validar do push e mostre o `MUDANCAS.md` da branch. Se estiver verde, `gh pr merge <número> -R IunaMC/modpack-moderacao --merge`, nunca `--rebase`, e acompanhe o Release de lá.
5. Volte a `devel/devel` de lá para a `main`: `checkout devel/devel`, `fetch --prune`, `merge --ff-only origin/main`.

## 2. Configs
1. A árvore do `minecraft-config` tem que estar limpa e na `devel/devel`. Se o `MODPACK` já é a versão pedida, pule.
2. Troque o conteúdo do `../iunamc.minecraft-config/MODPACK` pela versão, sem o `v`.
3. `git -C ../iunamc.minecraft-config commit -S -s -am "build: testa com o modpack <versão>"` e `push`.
4. Não publique a versão das configs aqui. Isso é com o `/versao` de lá, que testa o servidor com o modpack novo.

Responda só com: o link do PR e da release da moderação, o commit das configs e o que falta (o `/versao` no minecraft-config e o envio pelo FileZilla).
