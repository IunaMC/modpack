# Servidor local

O [`scripts/testar-servidor.sh`](../scripts/testar-servidor.sh) monta um
servidor NeoForge com os mods de servidor do pack, instalados pelo
packwiz-installer (`-s server`), igual à produção. O CI usa o script para
conferir se o pack sobe. Com as opções abaixo, ele também serve para ter uma
cópia do servidor na sua máquina.

```sh
# Teste do CI: sobe, espera o "Done" e para
bash scripts/testar-servidor.sh

# Cópia do servidor: mods + configs da pasta local, console aberto
bash scripts/testar-servidor.sh --configs --manter ~/iuna-copia

# O mesmo, com as configs de uma branch do GitHub
bash scripts/testar-servidor.sh --configs-git main --manter ~/iuna-copia
```

| Opção | Para quê |
| --- | --- |
| `--configs[=PASTA]` | Copia as configs do [`minecraft-config`](https://github.com/IunaMC/minecraft-config) de uma pasta local, do jeito que estão no disco, inclusive mudanças sem commit. O padrão é `../iunamc.minecraft-config`, ao lado deste repositório |
| `--configs-git REF` | Clona a branch ou tag `REF` do `minecraft-config` no GitHub. O repo é privado: usa o login do `gh` (ou `GH_TOKEN`) |
| `--manter` | Não para o servidor quando ele fica pronto. O console fica no terminal; entre pelo jogo em `localhost:<server-port>` e saia com `stop` |

Variáveis: `MEMORIA` (padrão `8G`) e `LIMITE` em segundos (padrão `1200`, só
sem `--manter`).

## De onde vem cada coisa

- **Mods:** o pack é servido por HTTP a partir da pasta `pack/` local. Então
  o servidor sobe com o que está no disco, inclusive uma branch que ainda não
  foi para a `main`.
- **Configs:** o pack não tem configs. Sem `--configs`/`--configs-git`, o
  servidor sobe "pelado", com as configs padrão dos mods e um
  `server.properties` mínimo.
- **Mundo:** não vem de lugar nenhum. Para testar no mundo real, copie um
  backup para `<pasta>/world` antes de subir.

## Rodar de novo na mesma pasta

- O packwiz-installer atualiza os mods. Um jar que você colocou à mão em
  `mods/` com nome novo fica; um jar do pack que você trocou é baixado de
  novo.
- As configs são copiadas por cima. Arquivos que não estão no repo de configs
  (mundo, dados do LuckPerms) não são tocados. Mas um arquivo versionado é
  sobrescrito: se você pôs o token do bot no `simple-discord-link.toml` da
  cópia, ele volta vazio.
- Tokens e IDs do Discord ficam no repo de configs como marcadores
  (`"{{DISCORD_CANAL_CHAT}}"`). Na cópia, eles viram vazio, então ela não
  conecta no Discord. Veja os
  [segredos do minecraft-config](https://github.com/IunaMC/minecraft-config/blob/main/docs/segredos.md).

## No CI

O workflow `Validar` sobe o servidor a cada push fora da `main`. Com o secret
`MINECRAFT_CONFIG_TOKEN` (token com leitura do `minecraft-config`), ele usa
`--configs-git main`; sem o secret, sobe só com os mods e mostra um aviso.
