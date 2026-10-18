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

# Com o bot do Discord ligado (token e IDs de um arquivo seu)
bash scripts/testar-servidor.sh --configs --segredos ~/.config/iuna/segredos.env --manter ~/iuna-copia
```

| Opção | Para quê |
| --- | --- |
| `--configs[=PASTA]` | Copia as configs do [`minecraft-config`](https://github.com/IunaMC/minecraft-config) de uma pasta local, do jeito que estão no disco, inclusive mudanças sem commit. O padrão é `../iunamc.minecraft-config`, ao lado deste repositório |
| `--configs-git REF` | Clona a branch ou tag `REF` do `minecraft-config` no GitHub. O repo é privado: usa o login do `gh` (ou `GH_TOKEN`) |
| `--segredos ARQUIVO` | Preenche o token e os IDs do Discord com um arquivo da sua máquina (veja abaixo). Sem esta opção, a cópia sobe sem bot |
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
  (mundo, dados do LuckPerms) não são tocados. Um arquivo versionado é
  sobrescrito, então não edite o token direto na cópia: use `--segredos`.

## Bot do Discord na cópia (`--segredos`)

Tokens e IDs do Discord ficam no repo de configs como marcadores
(`"{{DISCORD_CANAL_CHAT}}"`), e os valores ficam em secrets do GitHub. Esses
secrets **só podem ser lidos dentro do Actions**: nem o `gh` nem a tela do
GitHub mostram o valor. Por isso a cópia local não usa os secrets.

Sem `--segredos`, os marcadores viram vazio e a cópia sobe **sem bot**. Para
ligar o bot, crie um arquivo fora dos repositórios, com os mesmos nomes dos
secrets, e passe com `--segredos`:

```sh
mkdir -p ~/.config/iuna
touch ~/.config/iuna/segredos.env
chmod 600 ~/.config/iuna/segredos.env
```

```sh
# ~/.config/iuna/segredos.env: NOME=valor, uma linha por marcador
SDLINK_BOT_TOKEN=...
DISCORD_CANAL_CHAT=...
DISCORD_CANAL_EVENTOS=...
```

A lista de marcadores está nos
[segredos do minecraft-config](https://github.com/IunaMC/minecraft-config/blob/main/docs/segredos.md).
Marcador que não estiver no arquivo vira vazio. O script avisa se o arquivo
puder ser lido por outros usuários, e nunca mostra os valores.

Com o token e os canais reais, a cópia posta o início e a parada **nos canais
oficiais**, como a produção. Para não poluir, use os IDs de um canal de teste
nesse arquivo, ou outro bot.

## No CI

O workflow `Validar` sobe o servidor a cada push fora da `main`. Com o secret
`MINECRAFT_CONFIG_TOKEN` (token com leitura do `minecraft-config`), ele usa
`--configs-git main`; sem o secret, sobe só com os mods e mostra um aviso.
