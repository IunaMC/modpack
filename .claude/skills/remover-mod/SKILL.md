---
name: remover-mod
description: Remove um mod do pack pelo packwiz, junto com as dependências que ficarem órfãs, avisa das configs que sobram no minecraft-config e faz um commit por item. Use quando o usuário pedir para tirar um mod do pack.
argument-hint: "<nome do mod no pack> [motivo]"
model: sonnet
effort: low
allowed-tools:
  - Read
  - Bash(git status *)
  - Bash(git log *)
  - Bash(git diff *)
  - Bash(git add *)
  - Bash(git commit *)
  - Bash(cd pack && packwiz *)
  - Bash(packwiz *)
  - Bash(python3 scripts/pack.py *)
  - Bash(ls *)
  - Bash(cat *)
  - Bash(grep *)
---

Remova do pack: `$ARGUMENTS`.

## Estado atual
- Branch: !`git status -sb | head -1`
- Arquivos alterados: !`git status --porcelain || true`

## Passos
1. A branch tem que ser `devel/devel` e a árvore tem que estar limpa. Se não estiver, pare e avise.
2. Ache o `.pw.toml` (`ls pack/mods | grep -i <nome>`) e anote nome, versão e lado.
3. Rode `python3 scripts/pack.py orfas <nome>`. Ele lista as dependências obrigatórias que ficam sem uso (em cadeia), quem ainda exige o mod e as configs do `minecraft-config` que citam cada um. Na dúvida, mantenha a dependência e liste no fim como "talvez órfã".
4. Mod de conteúdo (`side = both`) tira blocos e itens do mundo: avise o usuário e espere o OK antes de remover.
5. `cd pack && packwiz remove <nome>` para o mod e para cada dependência órfã. Depois, `cd pack && packwiz refresh` e `python3 scripts/pack.py readme`.
6. Configs que sobram: as que o `pack.py orfas` listou. Não apague nada lá; liste no fim.
7. Um commit por item, o mod primeiro e as dependências depois, sempre com `git commit -S -s`:
   - mod: `feat(mods): remove <Nome> <versão>`, com o motivo no corpo;
   - dependência: `feat(deps): remove <Nome> <versão>`, com o corpo "Ninguém mais no pack usa."
   Cada commit leva o `.pw.toml` apagado, `pack/index.toml`, `pack/pack.toml` e o `README.md`, se ele mudou.
8. Não faça push e não mexa na versão. Remover mod é MINOR; isso fica para o `/beta`, que avisa no `MUDANCAS.md` o que some.

Responda só com o que saiu, os commits, as dependências "talvez órfãs" e as configs que sobraram no minecraft-config.
