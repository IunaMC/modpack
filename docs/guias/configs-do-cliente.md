# Configurações padrão do cliente

O pack entrega os padrões do cliente pelo YOMBR (Your Options Must Be Respected,
`pack/config/yosbr/`). O mod é nativo do NeoForge e só existe na CurseForge.
Ele lê a mesma pasta do antigo YOSBR, que nunca rodou: o YOSBR é um mod Fabric
que depende de um language adapter, e o Sinytra Connector não o executa.

Regras de cópia:

- **`options.txt`:** o YOMBR o copia na primeira abertura, mesmo que o launcher
  já tenha criado um, e grava `options_applied.flag` na instância. Depois disso
  o arquivo do jogador não é mais tocado. Para testar de novo, apague o
  `options_applied.flag`.
- **Os demais arquivos:** são copiados **só se ainda não existirem**.

Quem já joga mantém as próprias escolhas, e quem instala agora começa com os
padrões. Por isso a mudança de um padrão não alcança quem já tem o arquivo. O
`options.txt` precisa da linha `version:` (3955 para a 1.21.1), senão o
Minecraft o descarta.

## Onde cada coisa fica

| Arquivo no pack | Destino na instância |
| --- | --- |
| `pack/config/yosbr/options.txt` | `options.txt` |
| `pack/config/yosbr/config/<arquivo>` | `config/<arquivo>` |
| `pack/config/yosbr/servers.dat` | `servers.dat` (lista de servidores, com o IUNA) |

## Só em `config/yosbr/`

O servidor instala o pack com o packwiz-installer (`-s server`), e o `side`
só vale para os arquivos com `.pw.toml`. Todo arquivo solto do `pack/` vai
também para o servidor. Em `config/yosbr/` isso não faz efeito: só o YOMBR lê
a pasta, e ele não está no servidor. Fora dela, um arquivo em `pack/config/`
sobrescreveria a cada boot a config que vem do `minecraft-config`.

Por isso o `python3 scripts/pack.py soltos` (no Validar e no
`bash scripts/op.sh conferir`) recusa qualquer arquivo solto fora de
`config/yosbr/`, sem exceção. A pasta `config/yosbr/` que aparece
no servidor pode ser ignorada: apagá-la não muda nada, e o próximo boot a recoloca.

## O que o pack define

- **`options.txt`:** gráficos leves (`graphicsMode` rápido, nuvens rápidas,
  `biomeBlendRadius` 1, `entityDistanceScaling` 0,75, `simulationDistance` 8,
  V-Sync desligado), dicas avançadas nos itens, sem tutorial. Volume, FOV, sensibilidade, resource
  packs e idioma ficam por conta do jogador.
- **Sodium:** chuva rápida. **Dynamic FPS:** roda a coleta de lixo quando o jogo
  perde o foco. **ModernFix:** sem o cache de temperatura de bioma (o Lithium já
  faz). Veja [otimização](otimizacao.md).
- **LambDynamicLights:** `mode = "fast"`, com menos atualizações de luz.
- **More Overlays:** `update_interval_frames = 4`, para o scanner de luz.
- **`servers.dat`:** o servidor IUNA (`jogar.iuna.club`) na lista. Como os
  demais arquivos, só é copiado se o jogador ainda não tiver um, então os
  servidores que ele adicionar não somem nas atualizações.

## Teclas

O pack não mexe nas teclas: cada mod usa o padrão dele. A equipe decide depois
se vale um mapa próprio, que entraria no mesmo `options.txt`.

## Como mudar um padrão

1. Jogue uma instância nova, mude a opção e copie a linha (ou o arquivo) para
   o caminho acima.
2. Em config de mod, copie o arquivo inteiro e mude só o valor. Nada de
   segredo, caminho local, waypoint ou favorito.
3. `cd pack && packwiz refresh`.
