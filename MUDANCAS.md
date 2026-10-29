# Mudanças — v3.11.0-beta.1, otimização do servidor e do cliente, NeoForge 21.1.265

Beta: sai como pre-release só no GitHub. O servidor não a instala.

Quem já tem o pack atualiza pelo launcher, sem reinstalar; o launcher troca o
NeoForge para a 21.1.265 sozinho. Os padrões novos de cliente (Sodium, Dynamic
FPS, ModernFix) só valem para instalação nova: o pack não sobrescreve
configuração que o jogador já tem.

## NeoForge
- NeoForge 21.1.253 → 21.1.265: Mixin 0.16.4 e MixinExtras 0.5.5, e limites de tamanho e de decodificação de pacotes que protegem o servidor de pacotes malformados. Exigido pelo Almanac e pelo Let Me Despawn novos.

## Adicionou
- [Neruina](https://modrinth.com/mod/1s5x833P) 3.3.5 (MIT, servidor): evita que um erro no tick de uma entidade ou de um bloco derrube o servidor; o item defeituoso é congelado e os operadores são avisados.
- [Configurable](https://modrinth.com/mod/lGffrQ3O) 3.5.3 (MIT, servidor): dependência do Neruina.
- [Structure Layout Optimizer](https://modrinth.com/mod/ayPU0OHc) 1.0.12 (MIT, servidor): gera estruturas jigsaw mais rápido, sem mudar o resultado.
- [Enhanced Block Entities Reloaded](https://modrinth.com/mod/vpenrdOI) 0.13.3 (LGPL-3.0, cliente): renderiza baús, camas, placas e afins como modelos assados no chunk do Sodium, o que alivia o FPS onde há muitos block entities.
- [MatLib](https://modrinth.com/mod/gnefBeV1) 1.0.0 (MIT, cliente): dependência do anterior.
- [No Chat Reports](https://modrinth.com/mod/qQyHxfxd) 2.9.1 (WTFPL, cliente e servidor): tira a assinatura das mensagens e o botão de denúncia do chat.

## Atualizou
- [Almanac](https://modrinth.com/mod/Gi02250Z) 1.26.10.3 (LGPL-3.0, servidor): o conserto de NBT vazio fica bem mais leve (custava 2,9% do tick no servidor).
- [Let Me Despawn](https://modrinth.com/mod/vE2FN5qn) 1.26.10.2 (LGPL-3.0, servidor): mobs de estrutura e com nome não perdem a persistência ao pegar item, Endermen largam o bloco ao sumir e o desafio do trial spawner não se completa mais só esperando os mobs sumirem.
- [Sophisticated Core](https://modrinth.com/mod/nmoqTijg) 1.5.19, [Sophisticated Backpacks](https://modrinth.com/mod/TyCTlI4b) 3.26.17 e [Sophisticated Storage](https://modrinth.com/mod/hMlaZH8f) 1.6.10 (All Rights Reserved, cliente e servidor): corrigem perda de itens em controladores e baús duplos, um cache que crescia sem parar, consultas que carregavam chunks e ações que ignoravam claims.
- [Supplementaries](https://modrinth.com/mod/fFEIiSDQ) 4.0.2 (licença própria, cliente e servidor): corrige um dupe com a polia e traz a Pigñata e o Grouper.
- [Amendments](https://modrinth.com/mod/6iTJugQR) 2.2.4 (licença própria, cliente e servidor): animais acompanham teletransportes, muros, cercas e painéis se conectam, e deixa de brigar com o Enhanced Block Entities em placas e sinos.
- [Moonlight Lib](https://modrinth.com/mod/twkfQtEc) 3.7.2 (cliente e servidor): biblioteca dos dois anteriores.
- [Accessories](https://modrinth.com/mod/jtmvUHXj) 1.1.0-beta.54 (MIT, cliente e servidor): menos trabalho em toda leitura de componente de item.
- [Simple Voice Chat](https://modrinth.com/mod/9eGKb6K1) 2.6.27 (All Rights Reserved, cliente e servidor): o servidor não desconecta mais quem manda dados de voz inválidos.
- [Cataclysm: Spellbooks](https://modrinth.com/mod/3FEg0A8D) 1.1.15 (LGPL-2.1, cliente e servidor): corrige um crash ligado ao Monolith.
- [Twilight Forest - Dungeons & Villages](https://modrinth.com/mod/eDeSn4Ds) 2.0.3 republicado (All Rights Reserved, cliente e servidor): as mesas de lenhador, micologista, alquimia e açougueiro e a composteira voltam a ter receita.
- [Krypton Reno](https://modrinth.com/mod/JkxWVYwU) 0.2.28.1 (LGPL-3.0, cliente e servidor): passa a ser instalado também no cliente. Mesma versão.

## Removeu
- [Saturn](https://modrinth.com/mod/2eT495vq) 0.1.5 (servidor): causava conflitos de mixin com o ModernFix e o Lithium, e o ganho nunca foi medido.
- [Fast Async World Save](https://www.curseforge.com/projects/951499) 2.6 (servidor): gravava dados salvos e o level.dat numa thread que não é esperada ao desligar, então a última gravação podia se perder; o Smooth Chunk Save e o ServerCore já cuidam do salvamento.
