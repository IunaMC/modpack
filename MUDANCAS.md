# Mudanças — v3.7.0, lista de servidores preservada e pack só com arquivos do cliente

Quem já tem o pack atualiza pelo launcher, sem reinstalar.

## Adicionou
Nada.

## Atualizou
Nada.

## Removeu
Nada.

## Outras mudanças
- O `servers.dat` com o servidor IUNA passa a vir pelo YOMBR (`config/yosbr/servers.dat`): é copiado para a instância só se o jogador ainda não tiver um, então os servidores que ele adicionar não somem mais nas atualizações.
- O ícone da instância (`icon.png`) sai do pack: a CurseForge usa o ícone do projeto.
- Os arquivos de cliente ficam todos em `config/yosbr/`, que o servidor ignora; o Validar recusa arquivo solto fora dessa pasta.
