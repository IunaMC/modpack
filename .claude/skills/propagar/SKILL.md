---
name: propagar
description: Depois de uma estável do modpack, leva a versão nova ao pack de moderação (base.toml pelo Acompanhar pack base, commit reassinado, PR e merge) e ao MODPACK do minecraft-config. Use quando o usuário pedir para propagar ou sincronizar a versão nova do modpack com a moderação e as configs.
argument-hint: "[versão do modpack, ex.: 3.3.0]"
model: sonnet
effort: low
allowed-tools:
  - Bash(bash scripts/op.sh propagar*)
  - Bash(git -C ../iunamc.modpack-moderacao *)
  - Bash(git -C ../iunamc.minecraft-config *)
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
- `MODPACK` das configs: !`cat ../iunamc.minecraft-config/MODPACK 2>/dev/null || echo "(clone não encontrado)"`
- Árvores: !`git -C ../iunamc.modpack-moderacao status -sb | head -1; git -C ../iunamc.minecraft-config status -sb | head -1`

## Passos
1. Rode `bash scripts/op.sh propagar <versão sem o v>` (em segundo plano). Ele dispara o Acompanhar pack base se preciso, refaz o commit do bot com a assinatura de quem mantém, abre o PR da moderação, espera o Validar, faz o merge commit, espera o Release, alinha a `devel/devel` de lá e grava o `MODPACK` das configs. Para no primeiro passo vermelho: mostre o erro e pare.
2. Não publique a versão das configs aqui. Isso é com o `/versao` de lá, que testa o servidor com o modpack novo.

Responda só com: o link do PR e da release da moderação, o commit das configs e o que falta (o `/versao` no minecraft-config e o envio pelo FileZilla).
