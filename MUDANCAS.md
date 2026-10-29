# Mudanças — v3.10.0-beta.1, otimização do cliente, chat sem assinatura, Saturn sai

Beta: sai como pre-release e o servidor não a instala.

Quem já tem o pack atualiza pelo launcher, sem reinstalar. Os padrões novos de
cliente (Sodium, Dynamic FPS, ModernFix) só valem para instalação nova: o pack
não sobrescreve configuração que o jogador já tem.

## Adicionou
- [Enhanced Block Entities Reloaded](https://modrinth.com/mod/vpenrdOI) 0.13.3 (LGPL-3.0, cliente): renderiza baús, camas, placas e afins como modelos assados no chunk do Sodium, o que alivia o FPS onde há muitos block entities.
- [MatLib](https://modrinth.com/mod/gnefBeV1) 1.0.0 (dependência do anterior, cliente).
- [No Chat Reports](https://modrinth.com/mod/qQyHxfxd) 2.9.1 (WTFPL, cliente e servidor): tira a assinatura das mensagens e o botão de denúncia do chat.
- IUNA Compat 0.1.0 (servidor): ponte do LuckPerms, entrou pelo PR #51.

## Atualizou
Nada.

## Removeu
- [Saturn](https://modrinth.com/mod/2eT495vq) 0.1.5 (servidor): causava conflitos de mixin com o ModernFix e o Lithium, e o ganho nunca foi medido.
