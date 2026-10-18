---
name: beta
description: Prepara e publica a próxima versão beta do modpack pela devel/devel (versão no pack.toml, README, MUDANCAS.md, commit e push).
argument-hint: "[versão, ex.: 3.3.0-beta.1]"
disable-model-invocation: true
effort: low
---

Prepare a próxima beta do pack. Versão pedida: `$ARGUMENTS` (vazio = calcule).

1. Confira: branch `devel/devel`, árvore limpa e em dia com `origin/devel/devel`. Se não estiver, pare e diga o que falta.
2. Versão atual: `python3 scripts/pack.py versao`. Sem versão pedida:
   - atual `X.Y.Z-beta.N` → `X.Y.Z-beta.N+1`;
   - atual estável → rode `python3 scripts/pack.py mudancas <última tag estável>`. Mod adicionado, removido, atualizado ou movido = MINOR; nada muda para o jogador = PATCH; troca de Minecraft/NeoForge ou mundo novo = MAJOR (pergunte antes). Resultado: `<nova>-beta.1`.
3. Troque `version` em `pack/pack.toml`, rode `packwiz refresh` dentro de `pack/` e `python3 scripts/pack.py readme`.
4. Reescreva o `MUDANCAS.md` no formato da versão anterior: título `# Mudanças — v<versão>, <resumo curto>`, a linha de beta ("Beta: sai como pre-release e o servidor não a instala."), quem precisa reinstalar e as seções Adicionou/Atualizou/Removeu com link do Modrinth, versão, licença e lado. Use `python3 scripts/pack.py mudancas <tag anterior>` e as mensagens dos commits como fonte.
5. Commit único: `git commit -S -s -m "build: prepara a versao <versão>"`. Sem `Co-Authored-By` nem menção ao Claude.
6. `git push`. O `release.yaml` cria a tag e a pre-release. Confira com `gh run list --branch devel/devel --limit 3` e, quando terminar, `gh release view v<versão>`. Se o CI falhar, mostre o erro e pare.

Responda só com a versão publicada, o link da release e o status do CI.
