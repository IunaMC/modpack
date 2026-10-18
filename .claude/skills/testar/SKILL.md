---
name: testar
description: Testa se o servidor do pack sobe — pelo CI (Validar) por padrão, ou localmente com scripts/testar-servidor.sh.
argument-hint: "[local] [configs] [manter]"
disable-model-invocation: true
effort: low
---

Teste o boot do servidor. Argumentos: `$ARGUMENTS`.

**Sem `local` (padrão): pelo CI.** A máquina tem pouco disco e memória, e o CI sobe o servidor com as configs do `minecraft-config`.
1. Se houver commits locais sem push na `devel/devel`, faça `git push`.
2. `gh run list --workflow validar.yaml --branch devel/devel --limit 1`. Se estiver rodando, `gh run watch <id> --exit-status` em segundo plano.
3. Se falhar, `gh run view <id> --log-failed` e mostre só as linhas que explicam o erro. Os ~110 ERROR/FATAL de sempre no log não contam.

**Com `local`:**
1. Confira com `df -h .` e `free -g`. Com menos de 6 GB livres de disco ou de memória, avise e pare.
2. Monte o comando: `MEMORIA=4G bash scripts/testar-servidor.sh`, mais `--configs` se pedido, `--segredos ~/.config/iuna/segredos.env` se esse arquivo existir e `--configs` foi pedido, e `--manter` se pedido.
3. Sem `manter`: rode em segundo plano e espere terminar. Com `manter`: abra num terminal do usuário, porque ele vai usar o console.

Responda só com: passou ou falhou, o tempo até o "Done" e, se falhou, a causa.
