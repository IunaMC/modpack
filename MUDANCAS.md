# Mudanças — v3.0.0, pack em .mrpack e fonte única

## Mudou
- O modpack agora é distribuído como **`.mrpack`**, no lugar do zip com as pastas `Obrigatorios` e `Opcionais`. O arquivo tem cerca de 79 MB, contra 1,1 GB do zip. O launcher baixa os mods do Modrinth na instalação e instala o NeoForge **21.1.253** sozinho.
- Os mods opcionais viraram escolhas na tela de instalação do launcher. Todos vêm marcados por padrão.
- O pack passa a ser a fonte única do jogador e do servidor. Os mods só de servidor (administração, desempenho e geração de mundo) estão no mesmo pack, e o launcher do jogador os ignora.

## Atualizou
- [ModernFix](https://modrinth.com/mod/nmDcB62a) `5.27.24` → `5.27.26`, a mesma versão do servidor
- [Mezz Config](https://modrinth.com/mod/7tEfOcA7) `0.6.6` → `0.6.8`, a mesma versão do servidor

## Como migrar
- **Crie uma instância nova.** Importe o `IUNA-3.0.0.mrpack` no Prism Launcher (*Add Instance → Import*) ou no Modrinth App (*Import from file*). A pasta `mods` da instância antiga não serve.
- Para manter mundos, prints e configurações, copie `saves`, `screenshots` e `config` da instância antiga para a nova.
