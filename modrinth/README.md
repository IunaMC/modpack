# IUNA no Modrinth

A página do projeto ([`modrinth.com/project/iuna`](https://modrinth.com/project/iuna),
organização [IUNA](https://modrinth.com/organization/iuna)) e as versões saem
deste repositório. Para mudar a página, mude os arquivos desta pasta e faça
merge na `main`; não edite no site, porque o próximo push desfaz.

| Arquivo | O que vira na página |
| --- | --- |
| [`projeto.toml`](projeto.toml) | Nome, resumo, categorias, licença, links, ícone, galeria e a montagem da descrição |
| [`descricao.en.md`](descricao.en.md) | A descrição (inglês, idioma principal) |
| [`descricao.md`](descricao.md) | A tradução em português, num bloco recolhível no fim |
| [`imagens/`](imagens) | Ícone e galeria. O banner também abre a descrição |
| [`permissoes.md`](permissoes.md) | Referência para a página **Permissions** (preenchida no site) |

## Como funciona

- **Página:** o workflow [`Modrinth`](../.github/workflows/modrinth.yaml) roda
  em todo push que mexe nesta pasta. Fora da `main`, ele confere os arquivos e
  mostra no log o que mudaria; na `main`, aplica. Só envia o que mudou. As
  imagens são reconhecidas pelo conteúdo: trocar um arquivo envia a imagem nova
  e apaga a antiga.
- **Versões:** o workflow [`Release`](../.github/workflows/release.yaml), depois
  de criar a release no GitHub, envia o mesmo `.mrpack` ao Modrinth, com as
  notas da release como changelog. Se a versão já estiver lá, pula. Se o envio
  falhar, rode o workflow de novo pela aba Actions: ele reaproveita a release
  do GitHub e só tenta o Modrinth.
- Sem o secret `MODRINTH_TOKEN`, os dois workflows avisam e não enviam nada.

Para testar localmente, com o token em `MODRINTH_TOKEN` ou em
`~/.config/modrinth/token`:

```sh
python3 scripts/modrinth.py verificar               # confere esta pasta, sem rede
python3 scripts/modrinth.py sincronizar --simular   # mostra o que mudaria na página
```

## O que continua no site

A API não cobre, ou não deve ser automatizado:

- **Permissions:** cada arquivo de fora do Modrinth precisa de origem e
  permissão. Uma versão com arquivo externo novo fica **retida** até alguém
  marcar a permissão. O log do envio diz quantos arquivos externos a versão
  tem. Veja [`permissoes.md`](permissoes.md).
- **Disclosures:** o aviso *Contains AI-generated content* fica marcado, porque
  os textos foram escritos com ajuda de IA (regra 6.1). Ícone e galeria não
  podem ser gerados por IA (regra 6.2.1).
- Status e visibilidade, membros, monetização e o envio para revisão.

## Token

O secret `MODRINTH_TOKEN` é um token pessoal (PAT) criado em
[Settings → Personal access tokens](https://modrinth.com/settings/pats), com
validade de **6 meses** e só estes escopos: **Read projects**, **Write
projects**, **Read versions** e **Create versions**. Para salvar ou renovar:

```sh
gh secret set MODRINTH_TOKEN -R IunaMC/modpack-cliente
```

Token vencido faz os workflows falharem com HTTP 401. Renove o secret e rode de
novo pela aba Actions.

## Limites do Modrinth

O `scripts/modrinth.py verificar` confere estes antes de enviar:

- Nome com 3 a 64 caracteres, sem enchimento como "Modpack" (regra 5.2).
- Resumo com 3 a 255 caracteres, sem formatação e sem repetir o nome (regra 5.3).
- De 1 a 3 categorias principais
  ([lista](https://api.modrinth.com/v2/tag/category), `project_type = modpack`).
- Descrição de até 65.536 caracteres, com tradução em inglês se não for só em
  inglês (regras 2.1 e 2.2). Links só para páginas públicas (regra 5.4).
- Ícone quadrado, 256×256 ou maior, até 256 KiB. Galeria até 5 MiB por imagem.
- Downloads no `.mrpack` só de `cdn.modrinth.com`, `github.com`,
  `raw.githubusercontent.com` e `gitlab.com`.

Regras completas: <https://modrinth.com/legal/rules>.
