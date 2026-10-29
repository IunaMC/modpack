# Otimização do pack

Registro da revisão de 29/10/2026: o que foi avaliado, o que entrou, o que
saiu e como foi medido. Serve de ponto de partida para a próxima revisão.

## Mods avaliados

| Mod | Decisão | Motivo |
| --- | --- | --- |
| Saturn | **removido** | O log do servidor acusava conflitos de mixin dele com ModernFix e outros mods (`getTemperature`, `getSlotsForFace`, pool de threads). Sem ele, os conflitos caíram de 12 para 7. O ganho nunca foi medido. |
| No Chat Reports 2.9.1 | **entrou**, cliente e servidor | Build NeoForge nativa, sem dependências. Tira a assinatura do chat e o botão de denúncia. |
| Enhanced Block Entities Reloaded 0.13.3 | **entrou**, cliente | Build NeoForge para 1.21.1, exige MatLib. Os alvos dos mixins de Sodium (`RenderSection`, `RenderSectionManager`, `BuiltSectionInfo`) existem no Sodium 0.8.13 do pack. Não foi visto rodando (veja "Limites"). |
| Very Many Players | não entra | Só existe Fabric (1.21.1) e Forge (1.20); não há build NeoForge. Rodar a Fabric pelo Connector, mexendo na rede do servidor, não vale o risco. |
| Sodium Dynamic Lights | não entra | O pack já tem o LambDynamicLights. |
| More Chat History | não entra | Só Fabric no 1.21.1. |
| Debugify | não entra | Só Fabric no 1.21.1. |

Já existem no pack e não foram duplicados: Sodium, Sodium Extra, Iris,
ImmediatelyFast, Entity Culling, Dynamic FPS, ModernFix, FerriteCore, Lithium,
Krypton Reno, NoisiumForked, Immersive Optimization.

## Configurações

- **Fabulously Optimized** (referência, versão Fabric 1.21.1): quase tudo
  nele é escolha de gosto ou específico do Fabric. Aproveitado: chuva rápida
  no Sodium (`weather_quality`) e a coleta de lixo do Dynamic FPS quando o
  jogo perde o foco (`run_garbage_collector`), ambos na mesma versão do
  Dynamic FPS. Ficaram de fora: luz dinâmica de entidades desligada (muda o
  jogo), `simulationDistance` (o servidor já usa 6) e as teclas.
- **Opções do jogo** (`options.txt`): sem aviso de multijogador, sem tela de
  acessibilidade na primeira abertura, sem pergunta de telemetria.
- **ModernFix:** o patch `remove_biome_temperature_cache` fica desligado no
  cliente, porque o Lithium faz o mesmo e os dois sobrescrevem
  `Biome.getTemperature` (aviso de conflito no log).
- Tudo isso vai em `config/yosbr/` e só vale para quem instala agora (o
  YOMBR não sobrescreve arquivo existente). Veja
  [configs do cliente](configs-do-cliente.md).
- **Servidor:** o `modernfix-mixins.properties` do repo de configs tinha
  linhas `chave=true # (default)`, que o ModernFix ignora com aviso a cada
  boot. Foi limpo; o servidor já rodava com os padrões.
- **ModernFix `dynamic_resources`:** não ligado. Economiza RAM no cliente,
  mas com ~350 mods que mexem em modelos (Puzzles Lib, Continuity, EMF) o
  risco de quebrar visual é alto sem teste em jogo.

## Medições

Método: `scripts/testar-servidor.sh` com `MEMORIA=4G`, mesmas configs, dois
bootes em pasta nova (mundo novo). Cliente: instância do Prism com o pack
instalado pelo packwiz-installer (`-s client`), 6 GB, lendo o `debug.log`.

| Medida | Antes | Depois |
| --- | --- | --- |
| Servidor, tempo até pronto | 355 s | 356 s |
| Servidor, "Done" do mundo | 106,6 s | 117 a 133 s (ruído da máquina) |
| Linhas `ERROR` no boot | 108 | 104 (pack final, com IUNA Compat) |
| Conflitos de mixin no boot | 12 | 7 |
| Cliente (pack 3.9.0), do início ao último atlas | cerca de 4 min 40 s | não medido |

Conclusão honesta: as mudanças deste ciclo não alteram o tempo de boot de
forma mensurável. O ganho esperado está em jogo (block entities no cliente,
logs mais limpos), e o servidor não mostrou diferença nos 2 bootes.

## Limites e próximos passos

- A rodada do cliente "depois" (com Enhanced Block Entities) não chegou a
  rodar; conferir o `debug.log` na primeira beta e, se houver erro de mixin,
  remover o mod.
- Erros de conteúdo que se repetem no boot do servidor, que dependem de
  atualização dos mods: receitas do Twilight Forest Dungeons & Villages
  (`tf_dnv`), Monster Spellbooks (tags e receitas), Sable com
  `copycats:copycat_catwalk`, chaves antigas do Jupiter para o Refined
  Storage e receitas de ferraria do KubeJS (Hazen 'n Stuff).
- Mods de servidor com função parecida, para avaliar com perfil do Spark
  antes de tirar qualquer um: Fast Async World Save, Smooth Chunk Save e
  ServerCore; Immersive Optimization, AI Improvements e TT20.
- `skip_redundant_saves` do ModernFix pode aliviar o autosave; está desligado
  por padrão por risco de compatibilidade. Só testar com perfil.
