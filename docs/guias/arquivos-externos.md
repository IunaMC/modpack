# Arquivos externos

A maioria dos mods vem do Modrinth ou do CurseForge, e o packwiz sabe baixar
de lá. Alguns jars não têm um link fixo em lugar nenhum: o autor só publica
builds de snapshot, ou o arquivo some quando sai uma versão nova. Esses jars
ficam como anexos da pré-release
[`arquivos-servidor`](https://github.com/IunaMC/modpack/releases/tag/arquivos-servidor)
deste repositório, e o `.pw.toml` aponta para a URL do anexo, com o hash.

A release não é uma versão do pack (as versões são as tags `v*`) e não aparece
como "Latest". A descrição dela tem uma tabela com a origem e a licença de
cada anexo.

## Adicionar um arquivo

```sh
python3 scripts/pack.py externo ~/Downloads/NomeDoMod-1.2.3.jar --simular
python3 scripts/pack.py externo ~/Downloads/NomeDoMod-1.2.3.jar
```

O comando:
1. Lê o nome, a versão, o autor, a licença e a origem do próprio jar
   (`fabric.mod.json` ou `META-INF/neoforge.mods.toml`).
2. Anexa o jar à release `arquivos-servidor`.
3. Acrescenta a linha do arquivo na tabela da descrição da release.
4. Cria `pack/mods/<nome>.pw.toml` com a URL do anexo e o hash `sha512`, roda
   `packwiz refresh` e regenera a lista de mods do README.

`--simular` mostra tudo isso sem enviar nem gravar nada. Rode antes, para
conferir os dados.

| Opção | Padrão | Para quê |
| --- | --- | --- |
| `--lado server\|both\|client` | `server` | O `side` do `.pw.toml`. Mod de conteúdo é `both` |
| `--nome`, `--versao`, `--autor`, `--licenca`, `--origem` | o que o jar declara | Corrigir ou completar os metadados do jar |

Depois, como em qualquer mod: suba a versão (MINOR), escreva o
[`MUDANCAS.md`](../../MUDANCAS.md) e faça o commit
(`feat(mods): adiciona <Nome> <versão> no servidor`). O CI sobe o servidor de
teste já com o arquivo novo.

O comando usa o `gh` com a sua conta, que precisa poder editar releases do
repositório.

## Regras

- **O nome do arquivo tem a versão.** Um anexo nunca é substituído: o hash
  mudaria, e as versões antigas do pack, que apontam para a mesma URL,
  deixariam de instalar. O comando recusa um nome sem versão e um nome que já
  existe na release.
- **Para atualizar**, baixe o jar novo com outro nome (a versão nova), apague
  o `.pw.toml` antigo (`packwiz remove <nome>`, dentro de `pack/`) e rode o
  comando de novo. O anexo antigo fica na release para as versões antigas do
  pack.
- **Só entra o que a licença deixa redistribuir.** A release é pública, então
  anexar o jar é distribuir. Mods com URL também entram no índice do `.mrpack`
  da release, mesmo os só de servidor.

## Mod All Rights Reserved ou teste rápido

Não use a release. Coloque o jar direto na pasta `mods/` do servidor. O
packwiz-installer só mexe nos arquivos que ele mesmo instalou, então o jar
fica lá entre os reinícios. A desvantagem é que o arquivo fica fora do pack e
do teste do CI, e precisa ser lembrado a cada servidor novo.
