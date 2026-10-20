# Contribuir

Bugs e sugestões de mods vão para o
[IunaMC/issues](https://github.com/IunaMC/issues). Este guia é para quem mexe
no pack.
O trabalho planejado, com prioridade e situação de cada item, está no projeto
[IUNA · Roadmap](https://github.com/orgs/IunaMC/projects/1).

## Preparar a máquina

- `git` com assinatura GPG configurada e [`gh`](https://cli.github.com/) logado.
- [`packwiz`](https://packwiz.infra.link/) e Python 3.
- Java 21, só para o [teste local do servidor](docs/guias/servidor-local.md).

```sh
git switch devel/devel
```

```sh
bash scripts/op.sh
```

O segundo comando lista os atalhos de rotina. Nenhum publica.

## Como trabalhar

- Pack, scripts e CI: na `devel/devel`, ou numa `devel/<tarefa>` com PR para ela.
  Documentação que não depende de código: na `docs/docs`, ou numa
  `docs/<assunto>` com PR para ela. A `main` só recebe PR dessas duas, e um
  job confere a versão antes do merge
  ([regras](docs/referencia/versionamento.md#o-que-entra-na-main)).
- Um commit por mod, assinado (`git commit -S -s`), em Conventional Commits em
  português. As regras completas estão em
  [versionamento](docs/referencia/versionamento.md).
- Cada tarefa tem um [guia](docs/README.md#guias). No Claude Code, a skill de
  mesmo nome faz os mesmos passos.
- Depois de mexer em mods, rode `bash scripts/op.sh refresh` e
  `bash scripts/op.sh conferir`.

## Documentação

- Mudou skill, workflow ou script? Atualize o guia ou a referência em `docs/`
  no mesmo commit.
- O que atravessa repositórios vai para o
  [IunaMC/docs](https://github.com/IunaMC/docs), não para cá.
- Siga o
  [padrão de escrita](https://github.com/IunaMC/docs/blob/main/referencia/padrao-de-escrita.md).
  O workflow [Docs](.github/workflows/docs.yaml) confere links e estilo.
