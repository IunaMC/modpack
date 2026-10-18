# modpack

Pack IUNA (Minecraft 1.21.1, NeoForge) em packwiz, fonte única do jogador e do servidor: `side = server` marca o que é só do servidor. O servidor instala da `main` a cada boot. Repositório público: nada de host, hardware, IPs ou segredos aqui.

- **Commits:** `git commit -S -s`, Conventional Commits em português, um commit por mod ou dependência, dependências antes dos mods: `feat(mods): adiciona|remove|atualiza <Nome> <versão>`, `feat(deps): …`, `build(workflows): …`, `docs: …`. Não repita "mod" no texto, o escopo já diz. Nunca `Co-Authored-By` nem menção ao Claude, nem em commit, PR, issue ou release.
- **Branches:** trabalho na `devel/devel`. Beta (`X.Y.Z-beta.N`) sai por push na `devel/devel`; estável sai pelo PR para a `main` com merge commit (`gh pr merge --merge`). Nunca rebase-merge: recria os commits sem assinatura. A `main` recusa beta e qualquer mudança em `pack/` sem versão nova. O merge apaga a `devel/devel` remota: depois, `git fetch --prune` e `git merge --ff-only origin/main`.
- **Versão (SemVer, em `version` do `pack/pack.toml`):** MAJOR exige mundo novo ou reinstalar tudo; MINOR é qualquer mod adicionado, atualizado ou removido (remover mod de conteúdo também é MINOR); PATCH não muda nada para o jogador. Notas no `MUDANCAS.md`.
- **Dependências:** dependência de mod obrigatório nunca leva `[option] optional`, mesmo que opcionais também a usem.
- **CurseForge:** todo `.pw.toml` que não é `server` tem `[update.modrinth]` e `[update.curseforge]` para o mesmo arquivo. O `packwiz update` só segue o Modrinth: depois dele, `python3 scripts/curseforge.py verificar --corrigir`.
- Depois de mudar mods: `cd pack && packwiz refresh` e `python3 scripts/pack.py readme`. O teste de boot é o workflow Validar (`/testar`); localmente, `scripts/testar-servidor.sh` (veja `docs/servidor-local.md`).
- **Modrinth:** a página sai de `modrinth/` (não edite pelo site). Ela é em inglês, com o português recolhível; todo o resto é em português do Brasil.
- **Skills:** `/add-mod`, `/remover-mod`, `/beta`, `/estavel`, `/propagar`, `/testar`, `/spark`. Use a skill da tarefa em vez de fazer à mão.
