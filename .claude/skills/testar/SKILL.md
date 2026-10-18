---
name: testar
description: Testa se o servidor do pack sobe, pelo CI (Validar) por padrão ou localmente com scripts/testar-servidor.sh.
argument-hint: "[local] [configs] [manter]"
disable-model-invocation: true
model: sonnet
effort: low
allowed-tools:
  - Bash(git status *)
  - Bash(git log *)
  - Bash(git push *)
  - Bash(gh run *)
  - Bash(df *)
  - Bash(free *)
  - Bash(MEMORIA=* bash scripts/testar-servidor.sh*)
  - Bash(bash scripts/testar-servidor.sh*)
  - Bash(tail *)
  - Bash(grep *)
---

Teste o boot do servidor. Argumentos: `$ARGUMENTS`.

## Estado atual
- Branch: !`git status -sb | head -1`
- Commits sem push: !`git log --oneline @{u}..HEAD 2>/dev/null || echo "(sem branch remota)"`
- Últimos runs do Validar: !`gh run list --workflow validar.yaml --branch "$(git branch --show-current)" --limit 3 || true`
- Disco e memória livres: !`df -h --output=avail . | tail -1; free -g | awk '/Mem/{print $7 " GB de memória disponível"}'`

## Pelo CI (padrão, sem `local`)
A máquina tem pouco disco e pouca memória. O CI sobe o servidor com as configs do `minecraft-config`.
1. Se houver commits sem push, rode `git push`. O Validar começa sozinho.
2. Pegue o run mais recente e espere em segundo plano: `gh run watch <id> --exit-status`.
3. Se falhar, rode `gh run view <id> --log-failed` e mostre só as linhas que explicam o erro. Os cerca de 110 ERROR/FATAL que sempre aparecem no log não contam.

## Local (com `local`)
1. Com menos de 6 GB livres de disco ou de memória (veja acima), avise e pare.
2. O comando é `MEMORIA=4G bash scripts/testar-servidor.sh`, com estas opções:
   - `--configs`, se pedido;
   - `--segredos ~/.config/iuna/segredos.env`, se o arquivo existir e `--configs` foi pedido;
   - `--manter`, se pedido.
3. Sem `manter`: rode em segundo plano e espere terminar. Com `manter`: abra num terminal do usuário, porque ele vai usar o console.

Responda só com: passou ou falhou, o tempo até o "Done" e, se falhou, a causa.
