# Configurações padrão do cliente

O pack entrega os padrões do cliente pelo YOSBR (`pack/config/yosbr/`). O mod
copia cada arquivo para a instância **só se ele ainda não existir**. Quem já
joga mantém as próprias escolhas, e quem instala agora começa com os padrões.
Por isso a mudança de um padrão não alcança quem já tem o arquivo.

## Onde cada coisa fica

| Arquivo no pack | Destino na instância |
| --- | --- |
| `pack/config/yosbr/options.txt` | `options.txt` |
| `pack/config/yosbr/config/<arquivo>` | `config/<arquivo>` |

## O que o pack define

- **`options.txt`:** gráficos leves (`graphicsMode` rápido, nuvens rápidas,
  `biomeBlendRadius` 1, `entityDistanceScaling` 0,75, `simulationDistance` 8,
  V-Sync desligado), dicas avançadas nos itens, sem tutorial, e as teclas dos
  mods que brigavam pela mesma tecla. Volume, FOV, sensibilidade, resource
  packs e idioma ficam por conta do jogador.
- **LambDynamicLights:** `mode = "fast"`, com menos atualizações de luz.
- **More Overlays:** `update_interval_frames = 4`, para o scanner de luz.

## Teclas

O `options.txt` só lista as teclas que mudaram. As habilidades de combate
(Iron's Spells em `V`, Cataclysm em Home, End, Insert e acento grave, rolar em
vírgula) e os utilitários mais usados ficaram com teclas próprias. As teclas de
mods que quase ninguém usa no jogo ficaram sem tecla; o jogador liga pelo menu
*Controles*.

## Como mudar um padrão

1. Jogue uma instância nova, mude a opção e copie a linha (ou o arquivo) para
   o caminho acima.
2. Em config de mod, copie o arquivo inteiro e mude só o valor. Nada de
   segredo, caminho local, waypoint ou favorito.
3. `cd pack && packwiz refresh`.
