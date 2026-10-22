---
name: add-mod
description: Adiciona um mod do Modrinth ao pack pelo packwiz, com as dependências e a fonte da CurseForge, e faz um commit por item no padrão do repo. Use quando o usuário pedir para adicionar um mod ao pack.
argument-hint: "<slug ou link do Modrinth> [server|client|both] [opcional]"
model: sonnet
effort: low
allowed-tools:
  - Read
  - Edit
  - Bash(git status *)
  - Bash(git log *)
  - Bash(git diff *)
  - Bash(git add *)
  - Bash(git commit *)
  - Bash(cd pack && packwiz *)
  - Bash(packwiz *)
  - Bash(python3 scripts/pack.py *)
  - Bash(python3 scripts/curseforge.py *)
  - Bash(ls *)
  - Bash(cat *)
  - Bash(grep *)
---

Adicione ao pack: `$ARGUMENTS`. O lado vem dos argumentos; sem lado, vale o que o `pack.py lado` gravar (passo 3); lado dado nos argumentos vence, ajuste o `side` à mão. Só é opcional se "opcional" estiver nos argumentos.

## Estado atual
- Branch: !`git status -sb | head -1`
- Arquivos alterados: !`git status --porcelain || true`
- Exemplo de mod opcional: !`grep -l '^optional = true' pack/mods/*.pw.toml | head -1 | xargs cat`

## Passos
1. A branch tem que ser `devel/devel` e a árvore tem que estar limpa. Se não estiver, pare e avise.
2. `cd pack && packwiz modrinth add <slug> -y`. Aceite as dependências que ele oferecer.
3. Para cada mod novo, grave o lado pelo Modrinth: `python3 scripts/pack.py lado pack/mods/<arquivo>.pw.toml...`. Ele muda o `side` (`client_side` unsupported → `server`; `server_side` unsupported → `client`; senão `both`) e avisa se a licença é All Rights Reserved ou falta: avise o usuário antes de commitar, porque isso trava a página no Modrinth (ver `modrinth/permissoes.md`).
4. Para mod opcional, copie o bloco `[option]` do exemplo acima, com uma `description` curta em inglês. **Dependência de mod obrigatório nunca é opcional.** Depois, rode `cd pack && packwiz refresh` e `python3 scripts/pack.py readme`.
5. Todo mod que não é `server` precisa da fonte da CurseForge, senão o pack de lá sai incompleto. Para cada um, ache o Project ID na lateral da página do mod em curseforge.com (procure pelo nome; se não souber, pergunte ao usuário) e rode `python3 scripts/curseforge.py ligar pack/mods/<arquivo>.pw.toml <Project ID>`. Se a CurseForge não tiver o mesmo arquivo, pare e avise: o mod precisa de uma versão que exista nas duas fontes. Depois, `cd pack && packwiz refresh`.
6. Um commit por item, dependências primeiro, sempre com `git commit -S -s` e sem `Co-Authored-By`:
   - dependência: `feat(deps): adiciona <Nome> <versão>`
   - mod: `feat(mods): adiciona <Nome> <versão>[ no servidor|no cliente]`, com um corpo curto dizendo o que ele faz.
   Cada commit leva o `.pw.toml`, `pack/index.toml`, `pack/pack.toml` e o `README.md`, se ele mudou.
7. Não faça push e não mexa na versão. Isso fica para o `/beta`.

Responda só com a lista do que entrou (nome, versão, lado e licença) e os commits.
