# modpack

Pack IUNA (Minecraft 1.21.1, NeoForge) em packwiz, fonte única do jogador e do servidor: `side = server` marca o que é só do servidor. O servidor instala da `main` a cada boot.

- **Commits:** um commit por mod ou dependência, dependências antes dos mods: `feat(mods): adiciona|remove|atualiza <Nome> <versão>`, `feat(deps): …`, `build(workflows): …`, `docs: …`. Não repita "mod" no texto, o escopo já diz.
- **Branches:** trabalho na `devel/devel` (ou em `devel/<tarefa>` com PR para ela); documentação sem código pela `docs/docs` (ou `docs/<assunto>` com PR para ela). A `main` só recebe PR da `devel/devel` ou da `docs/docs`, e o job *Entrada na main* (`python3 scripts/pack.py conferir`) tem de passar: `pack/` mudou exige versão nova, só a versão mudar é recusado, MAJOR pede "MAJOR confirmado" no corpo do PR. Beta (`X.Y.Z-beta.N`) sai por push na `devel/devel`; estável sai pelo PR para a `main` com merge commit (`gh pr merge --merge`). Nunca rebase-merge: recria os commits sem assinatura. A `main` recusa beta e qualquer mudança em `pack/` sem versão nova. A `devel/devel` é permanente como a `main` e nunca é apagada (o repo não apaga branch no merge). Depois do merge, `git fetch` e `git merge --ff-only origin/main` na `devel/devel`, e `git push`; a `docs/docs` recebe `git merge origin/main`.
- **Versão (SemVer, em `version` do `pack/pack.toml`):** MAJOR exige mundo novo ou reinstalar tudo; MINOR é qualquer mod adicionado, atualizado ou removido (remover mod de conteúdo também é MINOR); PATCH não muda nada para o jogador. Notas no `MUDANCAS.md`.
- **Opcionais:** o pack não tem mod opcional (nenhum `[option]` nos `.pw.toml`): a escolha só existe no Modrinth e o pack também vive na CurseForge.
- **CurseForge:** todo `.pw.toml` que não é `server` tem `[update.modrinth]` e `[update.curseforge]` para o mesmo arquivo. O `packwiz update` só segue o Modrinth: depois dele, `python3 scripts/curseforge.py verificar --corrigir`.
- Depois de mudar mods: `cd pack && packwiz refresh` e `python3 scripts/pack.py readme`. O teste de boot é o workflow Validar (`/testar`); localmente, `scripts/testar-servidor.sh` (veja `docs/guias/servidor-local.md`).
- **Modrinth:** a página sai de `modrinth/` (não edite pelo site).
- **Documentação:** guias, referência e decisões em `docs/` (índice em `docs/README.md`); regras completas de versão, branch e commit em `docs/referencia/versionamento.md`. O que atravessa repos fica em `IunaMC/docs` (local `../iunamc.docs`), com o padrão de escrita. Mudou skill, workflow ou script: atualize o guia no mesmo commit.
- **Skills:** `/add-mod`, `/remover-mod`, `/beta`, `/estavel`, `/propagar`, `/testar`, `/spark`. Use a skill da tarefa em vez de fazer à mão.

<!-- regras-comuns:inicio -->
## Regras comuns da IunaMC

Texto oficial em
[IunaMC/docs](https://github.com/IunaMC/docs/blob/main/referencia/claude.md).
Não edite este bloco: mude lá e rode `scripts/regras-comuns.py sincronizar`.

- **Commits:** `git commit -S -s`, [Conventional Commits](https://www.conventionalcommits.org/pt-br/) em português. Nunca `Co-Authored-By` nem menção ao Claude, nem em commit, PR, issue ou release.
- **Idioma:** português do Brasil em código comentado, documentação, commits, PRs e issues. A única exceção é a página do Modrinth, em inglês com o português recolhível.
- **Repositório público:** nada de host, hardware, IP, DNS interno, caminho local nem segredo. Isso fica nos repositórios privados, e a página pública só diz que existe.
- **Uma sessão por tarefa:** tarefa sem relação com a anterior abre sessão nova, porque o histórico é reenviado a cada mensagem.
- **Antes de perguntar ao usuário:** leia a memória, o `git log` e as sessões anteriores. Pergunte só o que não estiver registrado.
- **Modelo e esforço:** a skill fixa o modelo no cabeçalho; sem skill, siga a tabela. Em subagente, passe o `model` dela.

  | Tarefa | Modelo | Esforço |
  | --- | --- | --- |
  | Mecânica: commit, mover arquivos, atualizar notas, conferir o CI | Haiku ou Sonnet | baixo |
  | Rotina com algum julgamento: revisar config, escrever guia | Sonnet | médio |
  | Decisão de projeto, depuração, análise de crash | Opus | alto |
<!-- regras-comuns:fim -->
