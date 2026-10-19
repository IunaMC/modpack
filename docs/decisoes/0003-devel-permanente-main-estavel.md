# 0003: `devel/devel` permanente e `main` só com estáveis

- **Data:** 18/10/2026; branch permanente em 19/10/2026
- **Estado:** aceita
- **Origem:** `5c5633b` (betas pela `devel/devel`, só estáveis pela `main`) e
  `45d233c` (a `devel/devel` como branch permanente)

## Contexto

O servidor passou a instalar o pack direto da `main`
([IunaMC/docs, decisão 0002](https://github.com/IunaMC/docs/blob/main/decisoes/0002-servidor-instala-da-main.md)).
Uma beta ou uma mudança no pack sem versão nova na `main` chegaria à produção
no próximo reinício.

## Decisão

- O job `versao` do Release decide o que publica:
  - na `main`, recusa versão beta e falha se o `pack/` mudou sem versão nova;
  - na `devel/devel`, publica só betas, como *pre-release*. Versão estável ali
    não publica nada.
- A `devel/devel` é permanente, como a `main`: o repositório não apaga branch
  no merge, e depois de cada estável ela volta a alinhar com
  `git merge --ff-only origin/main`.

## Consequências

- Beta nunca chega ao servidor.
- Toda estável passa por um PR da `devel/devel` para a `main`
  ([guia](../guias/publicar-estavel.md)).
- A proteção da `main` vem do workflow. O GitHub ainda não tem *ruleset* nela.
