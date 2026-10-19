# Manual de operação

Como o IUNA é mantido, passo a passo, para quem opera **sem** o Claude Code.
Cada skill (`/beta`, `/estavel`…) é só um atalho para os comandos abaixo: se
o Claude sumir, nada para.

## Repositórios

| Repositório | Visibilidade | Papel |
| --- | --- | --- |
| [`modpack`](https://github.com/IunaMC/modpack) | público | Fonte única do pack (packwiz). Jogador e servidor instalam daqui; `side = server` marca o que é só do servidor. |
| `modpack-moderacao` | privado | Pack da staff: herda o `modpack` pelo `base.toml` e soma mods de moderação. |
| `minecraft-config` | privado | `config/` e `server.properties` do servidor. O arquivo `MODPACK` diz com qual versão do pack ele foi testado. |
| `minecraft-infra` | privado | Anotações da infraestrutura. |
| [`issues`](https://github.com/IunaMC/issues) | público | Bugs e sugestões da comunidade. |
| [`.github`](https://github.com/IunaMC/.github) | público | Perfil da organização e modelos de issue. |

Fluxo de uma versão:

```
mod novo ─► modpack devel/devel ─► beta (pre-release) ─► PR para main ─► estável
                                                                      │
              servidor de produção instala a main a cada boot ◄───────┤
                                                                      ├─► moderação (base.toml)
                                                                      └─► minecraft-config (MODPACK) ─► release ─► envio manual ao servidor
```

## Ferramentas

- `git` com assinatura GPG configurada, [`gh`](https://cli.github.com/) logado,
  [`packwiz`](https://packwiz.infra.link/), Python 3, Java 21 (só para o teste local).
- Regras de commit, branch e versão: [`CLAUDE.md`](../CLAUDE.md). Resumo:
  `git commit -S -s`, Conventional Commits em português, um commit por mod,
  trabalho na `devel/devel`, merge na `main` só por PR com `--merge`.

## Tarefas

### Adicionar um mod (`/add-mod`)

```bash
git switch devel/devel && git status            # árvore limpa
cd pack && packwiz modrinth add <slug> -y && cd ..
```

1. Lado de cada mod novo: veja `client_side`/`server_side` em
   `https://api.modrinth.com/v2/project/<slug>` (`unsupported` no cliente →
   `side = "server"`; no servidor → `"client"`; senão `"both"`). Licença
   All Rights Reserved trava a página do Modrinth (`modrinth/permissoes.md`).
2. Todo mod que não é `server` precisa da fonte da CurseForge (Project ID na
   lateral da página do mod em curseforge.com):
   `python3 scripts/curseforge.py ligar pack/mods/<arquivo>.pw.toml <Project ID>`.
3. `cd pack && packwiz refresh && cd .. && python3 scripts/pack.py readme`.
4. Um commit por item, dependências antes:
   `git commit -S -s -m "feat(mods): adiciona <Nome> <versão>"`, levando o
   `.pw.toml`, `pack/index.toml`, `pack/pack.toml` e o `README.md`.

Jar sem download fixo (fora do Modrinth e da CurseForge):
`python3 scripts/pack.py externo <jar>` ([arquivos externos](arquivos-externos.md)).

### Remover um mod (`/remover-mod`)

`cd pack && packwiz remove <nome>`, depois `refresh` e `readme` como acima.
Confira se alguma dependência ficou órfã e remova também. Procure as configs
que sobram no `minecraft-config` (`grep -rli <mod-id> config/`). Commit
`feat(mods): remove <Nome> <versão>` com o motivo. Remover mod de conteúdo
apaga blocos do mundo: combine com a staff antes.

### Atualizar mods

A issue semanal **Atualizações de mods** lista o que tem versão nova.

```bash
cd pack && packwiz update <mod> && cd ..
python3 scripts/curseforge.py verificar --corrigir   # o packwiz só segue o Modrinth
cd pack && packwiz refresh && cd .. && python3 scripts/pack.py readme
```

### Beta (`/beta`)

1. `python3 scripts/pack.py proxima-beta` sugere a versão pelo SemVer.
2. Troque `version` em `pack/pack.toml`, rode `refresh` e `readme`.
3. Reescreva o `MUDANCAS.md` (`python3 scripts/pack.py mudancas <última tag>`
   dá a lista de mods), com a linha "Beta: sai como pre-release…".
4. `git commit -S -s -am "build: prepara a versao X.Y.Z-beta.N" && git push`.
   O workflow Release cria a pre-release, envia ao Modrinth e à CurseForge.

### Estável (`/estavel`)

1. Validar verde na `devel/devel` e ao menos uma beta da versão.
2. `version` sem `-beta`, `refresh`, `readme`, `MUDANCAS.md` comparando com a
   **última estável**; commit `build: prepara a versao X.Y.Z`, `git push`.
3. `gh pr create --base main --head devel/devel --title "Versão X.Y.Z: <resumo>"`
4. `gh pr merge <n> --merge` (**nunca** `--rebase`: perde as assinaturas).
5. Acompanhe: `gh run watch $(gh run list -w release.yaml -b main -L1 --json databaseId -q '.[0].databaseId')`.
6. `git fetch --prune && git merge --ff-only origin/main` (o merge apagou a
   `devel/devel` remota; o próximo push a recria).

O servidor pega a versão nova no próximo reinício.

### Propagar (`/propagar`)

- **Moderação:** o workflow *Acompanhar pack base* de lá abre a branch
  `base/vX.Y.Z` (diário, ou `gh workflow run acompanhar-base.yaml -R IunaMC/modpack-moderacao`).
  O commit do bot vem sem assinatura: faça checkout da branch,
  `git commit --amend --no-edit --reset-author -S -s`, `git push --force-with-lease`,
  abra o PR para a `main` e faça merge com `--merge`.
- **Configs:** no `minecraft-config`, escreva a versão em `MODPACK`, commit
  `build: testa com o modpack X.Y.Z`, push, e publique a versão de lá
  (`VERSAO` + `MUDANCAS.md`; veja `docs/versoes.md` daquele repo).

### Enviar as configs ao servidor (só manual)

Pelo FileZilla, seguindo `docs/enviar-ao-servidor.md` do `minecraft-config`:
baixar antes os tomls do Simple Discord Link (token e IDs), trocar a pasta
`config/` inteira pela do `.zip` da release, preencher os marcadores e
reiniciar. **Nunca** apagar `world/`. Feche a issue de envio depois.

## Workflows e o equivalente local

| Workflow | Quando roda | O que faz | Rodar na sua máquina |
| --- | --- | --- | --- |
| Validar | push fora da `main`, PR, manual | confere README, fonte da CurseForge, exporta `.mrpack` e sobe um servidor de verdade com as configs | `bash scripts/testar-servidor.sh --configs` (veja [servidor local](servidor-local.md)); `MEMORIA=4G` em máquina modesta |
| Release | push na `main`/`devel/devel` com versão nova | tag, release com `.mrpack`, Modrinth e CurseForge | `cd pack && packwiz mr export`; `python3 scripts/modrinth.py publicar <v> <mrpack> MUDANCAS.md --simular`; `cd pack && packwiz curseforge export -o ../IUNA.zip`; `python3 scripts/curseforge.py publicar <v> IUNA.zip MUDANCAS.md --simular` |
| Modrinth | push que muda `modrinth/` | atualiza textos, links e galeria do projeto | `python3 scripts/modrinth.py sincronizar --simular` (sem `--simular` com `MODRINTH_TOKEN`) |
| Atualizações de mods | segunda, 10h23 UTC | issue com os mods que têm versão nova | `cd pack && packwiz update --all` e `git diff` (depois `git checkout pack/`) |
| Resumo semanal | segunda, 10h53 UTC | issue "Resumo semanal" com o estado dos repos | `python3 scripts/resumo.py` |

Na moderação: *Validar*, *Release* e *Acompanhar pack base*. No
`minecraft-config`: *Release*, que sobe o servidor com as configs antes de
publicar o `.zip`.

## Segredos (nomes, nunca valores)

| Nome | Onde | Para quê | Renovar em |
| --- | --- | --- | --- |
| `MODRINTH_TOKEN` | secret do modpack | página e versões no Modrinth | modrinth.com → Settings → PATs |
| `CURSEFORGE_TOKEN` | secret do modpack | envio de arquivos | authors.curseforge.com → My API Tokens |
| `CURSEFORGE_PROJECT_ID` | variable do modpack | projeto da CurseForge | — |
| `MINECRAFT_CONFIG_TOKEN` | secret do modpack | ler `minecraft-config` e `modpack-moderacao` (Validar, Resumo) | GitHub → fine-grained PAT; anote a data de expiração |
| marcadores `{{NOME}}` | secrets do `minecraft-config` | token do bot e IDs do Discord no teste | `docs/segredos.md` de lá |

Token vencido aparece como falha no Validar ou "sem acesso" no Resumo.

## O que só uma pessoa faz

- Enviar as configs ao servidor (FileZilla) e reiniciar pelo painel.
- Descrição e imagens do projeto na CurseForge (a API de upload não edita o projeto).
- Pedidos de permissão no Modrinth e a moderação de lá.
- Atalhos de download no domínio (Cloudflare).
- Cargos: LuckPerms pelo console, sincronia com o Discord.
- Gerar e renovar os tokens da tabela acima.

## Se o GitHub cair

O servidor roda o `packwiz-installer-bootstrap` contra a `main` a cada boot.
Sem acesso ao GitHub o instalador falha, mas os jars da última instalação
continuam na pasta `mods/`. Se a falha impedir a subida, tire temporariamente
o instalador do comando de inicialização no painel e o servidor sobe com o
que já tem. Para reinstalar do
zero sem GitHub, use o `.mrpack` da última release guardado fora do GitHub.

## Uso do Claude Code

- `CLAUDE.md` em cada repo guarda as regras fixas; hooks locais barram commit
  sem assinatura ou com atribuição.
- Skills em `.claude/skills/` (modpack: `add-mod`, `remover-mod`, `beta`,
  `estavel`, `propagar`, `testar`, `spark`). Cada uma descreve os mesmos passos
  deste manual; se uma mudar, atualize esta página.
- Checagens recorrentes ficam no GitHub Actions, não no Claude.
- Regra da casa: nada que o Claude faz pode existir só na conversa. Todo
  processo novo ganha um passo manual aqui.
