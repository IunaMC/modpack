---
name: add-mod
description: Adiciona um mod do Modrinth ao pack pelo packwiz, com as dependências e a fonte da CurseForge, e faz um commit por item no padrão do repo. Use quando o usuário pedir para adicionar um mod ao pack.
argument-hint: "<slug ou link do Modrinth> [server|client|both]"
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

Adicione ao pack: `$ARGUMENTS`. O lado (`client`, `server` ou `both`) é escolha do usuário, nunca sua: vem dos argumentos; sem lado nos argumentos, pergunte por mod novo e dependência (passo 3) e não adivinhe. Nenhum mod é opcional.

## Estado atual
- Branch: !`git status -sb | head -1`
- Arquivos alterados: !`git status --porcelain || true`

## Passos
1. A branch tem que ser `devel/devel` e a árvore tem que estar limpa. Se não estiver, pare e avise.
2. `cd pack && packwiz modrinth add <slug> -y`. Aceite as dependências que ele oferecer.
3. Para cada mod novo e dependência, defina o lado: se não veio nos argumentos, pergunte ao usuário antes de seguir. Mostre o que o Modrinth declara (`python3 scripts/pack.py lado pack/mods/<arquivo>.pw.toml...`, só informa e mostra a licença) como dado, não como resposta: ele pode estar errado ou incompleto. Grave o `side` à mão no `.pw.toml`. Mod do Modrinth não precisa de permissão no `.mrpack`, mesmo All Rights Reserved. Só jar que existe apenas na CurseForge vai embutido: avise o usuário que ele precisa de permissão na página Permissions (`modrinth/permissoes.md`) ou de entrar em `[[reduzido.fora]]` do `modrinth/projeto.toml` (decisão 0007).
4. Não use `[option]`: o pack não tem mod opcional. Rode `cd pack && packwiz refresh` e `python3 scripts/pack.py readme`.
5. Todo mod que não é `server` precisa da fonte da CurseForge, senão o pack de lá sai incompleto. Para cada um, ache o Project ID na lateral da página do mod em curseforge.com (procure pelo nome; se não souber, pergunte ao usuário) e rode `python3 scripts/curseforge.py ligar pack/mods/<arquivo>.pw.toml <Project ID>`. Se a CurseForge não tiver o mesmo arquivo, pare e avise: o mod precisa de uma versão que exista nas duas fontes. Depois, `cd pack && packwiz refresh`.
6. Um commit por item, dependências primeiro, sempre com `git commit -S -s` e sem `Co-Authored-By`:
   - dependência: `feat(deps): adiciona <Nome> <versão>`
   - mod: `feat(mods): adiciona <Nome> <versão>[ no servidor|no cliente]`, com um corpo curto dizendo o que ele faz.
   Cada commit leva o `.pw.toml`, `pack/index.toml`, `pack/pack.toml` e o `README.md`, se ele mudou.
7. Não faça push e não mexa na versão. Isso fica para o `/beta`.

Responda só com a lista do que entrou (nome, versão, lado e licença) e os commits.
