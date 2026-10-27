# Mudanças — v3.7.0-beta.2, os padrões do cliente passam a funcionar

Beta: sai como pre-release e o servidor não a instala.

Quem já tem o pack atualiza pelo launcher, sem reinstalar. O YOSBR nunca chegou a aplicar os padrões porque o Sinytra Connector não executa o language adapter dele; o YOMBR faz o mesmo trabalho nativo no NeoForge. As mudanças da 3.7.0-beta.1 continuam valendo.

## Adicionou
- [Your Options Must Be Respected](https://www.curseforge.com/minecraft/mc-mods/yombr) 1.0.0 (cliente): copia os padrões de `config/yosbr/` (`options.txt`, LambDynamicLights e More Overlays) na primeira abertura, sem sobrescrever o que o jogador já mudou depois disso. Só existe na CurseForge.

## Atualizou
Nada.

## Removeu
- [Your Options Shall Be Respected (YOSBR)](https://modrinth.com/mod/WwbubTsV) 0.1.2 (cliente), LGPL-3.0: substituído pelo YOMBR.

## Outras mudanças
- Quem já tem um `options.txt` o terá substituído uma única vez pelo padrão do pack; depois o YOMBR não mexe mais nele.
