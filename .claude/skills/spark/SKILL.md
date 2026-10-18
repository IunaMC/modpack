---
name: spark
description: Analisa perfis do Spark (.json exportado pelo viewer) do servidor e aponta as causas de lag com números, comparando com o diagnóstico anterior. Use quando o usuário mandar um perfil do Spark ou pedir para analisar o desempenho do servidor.
argument-hint: "<perfil.json ou pasta> [janela do pico]"
effort: medium
allowed-tools:
  - Read
  - Bash(python3 .claude/skills/spark/spark.py *)
  - Bash(python3 */.claude/skills/spark/spark.py *)
  - Bash(ls *)
---

Analise o perfil: `$ARGUMENTS`. Sem caminho, use o `.json` mais novo de `~/Downloads/Spark`.

## Ferramenta
`python3 .claude/skills/spark/spark.py <comando> <perfil.json>` (caminho a partir da raiz do repo):
- `resumo`: período, jogadores, MSPT, GC, flags, `simulation-distance` e as janelas de 1 min;
- `mods`: % do tick por etapa (entidades, chunks, spawn, block entities, eventos, save) e por mod;
- `pico <janela>…`: o que cresceu no minuto do pico em relação à mediana dos outros;
- `metodo <Classe.metodo>`: quanto um método custou e em que minutos.

Leia o perfil só por ele. O arquivo tem até 120 MB: nunca abra com Read nem com `cat`.

## Passos
1. Leia a memória do diagnóstico de performance antes. Ela tem os culpados já medidos e o que foi descartado com dados; não refaça o que já está lá.
2. `resumo`. Repare:
   - `simulation-distance` 8 = o servidor ainda roda sem as configs do repo. Diga isso antes de concluir qualquer coisa sobre otimização.
   - janela marcada com `*` = a JVM parou (GC ou safepoint). Peça o `logs/gc.log` daquele horário em vez de procurar culpado no tick.
   - um "tick" de dezenas de minutos com 0 jogadores é o Tick Stasis pausando o servidor vazio, não travamento.
3. `mods` para a divisão geral. Self atribuído ao Observable ou a outro mod de mixin costuma ser artefato.
4. Para os 2 ou 3 minutos de maior `max`, rode `pico`. Pico recorrente a cada 5 min é o autosave (~0,2 s por jogador online). Chunk carregado de forma síncrona (`managedBlock`, `getChunk`) é jogador entrando em terreno novo.
5. Confirme cada suspeita com `metodo`, que dá a % no perfil inteiro.

Não proponha desligar chunkloading de mods nem nada que a memória diga que o usuário recusou.

Responda com: período e jogadores, MSPT mediano e o pior pico, a divisão do tick, até 5 causas com % e minuto, o que mudou desde o último diagnóstico e o próximo passo. Depois, atualize a memória do diagnóstico com os números novos.
