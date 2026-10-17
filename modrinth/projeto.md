# Projeto no Modrinth: checklist

Tudo o que precisa estar pronto para criar o projeto do IUNA no Modrinth. Nada
aqui foi criado no site: os cliques e o envio são feitos pela conta do
mantenedor. Os itens marcados com **Decisão** dependem de uma escolha sua.

Estado conferido em 17/10/2026, versão do pack **3.0.0** (Minecraft 1.21.1,
NeoForge 21.1.253).

## 1. Requisitos do Modrinth para modpacks

O que as regras e a documentação oficiais exigem hoje, com a fonte de cada
item.

| Item | Requisito | Fonte |
| --- | --- | --- |
| Tipo do projeto | `modpack`. A versão é um arquivo `.mrpack`. | [API: Create a project](https://docs.modrinth.com/api/operations/createproject/), [API: Create a version](https://docs.modrinth.com/api/operations/createversion/) |
| Nome | Só o nome do projeto, "sem dados de enchimento". 3 a 64 caracteres. | [Regras, 5.2](https://modrinth.com/legal/rules); limite: espelho da documentação do código ([mintlify](https://mintlify.wiki/modrinth/code/creators/creating-projects)) |
| Slug | 3 a 64 caracteres, único no site. Slugs que são IDs base62 válidos são recusados. | [API: Create a project](https://docs.modrinth.com/api/operations/createproject/) (regex `^[\w!@$()`.+,"\-']{3,64}$`) |
| Resumo | Curto, sem formatação e sem repetir o nome. 3 a 255 caracteres. | [Regras, 5.3](https://modrinth.com/legal/rules); limite: [mintlify](https://mintlify.wiki/modrinth/code/creators/creating-projects) |
| Descrição | Diz claramente o que o projeto faz e por que baixar, com toda informação crítica antes do download. Precisa de versão em texto simples, não pode usar títulos como corpo de texto e precisa de **tradução em inglês**, a não ser que o projeto seja só para um idioma. Até 65.536 caracteres. | [Regras, 2, 2.1 e 2.2](https://modrinth.com/legal/rules) |
| Links | Todo link externo leva a um recurso **público** e relevante. | [Regras, 5.4](https://modrinth.com/legal/rules) |
| Créditos | Esforço real para creditar cada fonte original. Conteúdo de terceiros só com permissão. | [Regras, 4](https://modrinth.com/legal/rules) |
| IA | O aviso **"Contains AI-generated content"** é obrigatório quando qualquer parte da página, como a descrição, depende de IA generativa. Ícone e galeria **não podem** vir de IA. | [Regras, 6.1 e 6.2.1](https://modrinth.com/legal/rules) |
| Ícone | PNG ou JPEG, quadrado, 256×256 ou maior, até 256 KiB. Exibido em 96×96. | [mintlify](https://mintlify.wiki/modrinth/code/creators/creating-projects) (a API oficial aceita png, jpg, webp, gif, svg etc. e não diz o limite) |
| Galeria | Até 5 MiB por imagem (PNG, JPEG, WebP). Uma imagem pode ser a destacada. As imagens precisam ser do próprio pack e não podem dar falsa impressão do conteúdo. | [API: Add a gallery image](https://docs.modrinth.com/api/operations/addgalleryimage/), [Regras, 5.5](https://modrinth.com/legal/rules) |
| Licença | Identificador SPDX obrigatório (o padrão é ARR), com URL opcional. | [API: Create a project](https://docs.modrinth.com/api/operations/createproject/) |
| Categorias | 1 a 3 categorias principais. As de modpack são: `adventure`, `challenging`, `combat`, `kitchen-sink`, `lightweight`, `magic`, `multiplayer`, `optimization`, `quests`, `technology`. | `GET https://api.modrinth.com/v2/tag/category`; limite: [mintlify](https://mintlify.wiki/modrinth/code/creators/creating-projects) |
| Ambiente (lados) | `client_side`/`server_side` estão obsoletos. Agora é o **Environment**, configurado na página *Environments* das configurações do projeto e por versão (`environment` na criação da versão). | [Notícia: New environments (28/08/2025)](https://modrinth.com/news/article/new-environments), [OpenAPI](https://docs.modrinth.com/openapi.yaml) (`EnvironmentInputEnum`) |
| Arquivos externos | Desde **23/06/2026**, toda versão com arquivo fora do Modrinth fica retida até cada arquivo ter origem e permissão na página **Permissions**. Veja [`permissoes.md`](permissoes.md). | [Notícia: Modpack permissions](https://modrinth.com/news/article/modpack-permissions), [Obtaining modpack permissions](https://support.modrinth.com/en/articles/8797527) |
| Downloads no `.mrpack` | Só `cdn.modrinth.com`, `github.com`, `raw.githubusercontent.com` e `gitlab.com`. Por isso os mods do CurseForge vão embutidos em `overrides/`. | [Formato .mrpack](https://support.modrinth.com/en/articles/8802351-modrinth-modpack-format-mrpack) |
| Revisão | O projeto vai para a fila de moderação. A maioria é aprovada em 24 a 48 horas. Para enviar, precisa de pelo menos uma versão. | [mintlify](https://mintlify.wiki/modrinth/code/creators/creating-projects) |

> As linhas que citam o mintlify vêm de um espelho gerado a partir do código do
> Modrinth, não da ajuda oficial. Confira os limites na tela de criação.

## 2. Dados do projeto

| Campo | Valor sugerido | Observação |
| --- | --- | --- |
| Tipo | Modpack | |
| Nome | `IUNA` | **Decidido.** A regra 5.2 desencoraja enchimento como "Modpack" no nome; o tipo já aparece na página. O nome interno do `.mrpack` (`pack.toml`) continua "IUNA Modpack". |
| Slug | `iuna` | **Decidido.** Livre em 17/10/2026 (`GET /v2/project/iuna` → 404). |
| URL final | `https://modrinth.com/modpack/iuna` | |
| Resumo | `A Brazilian Minecraft community made for friends — and yes, we ‘don’t have a name’.` | **Decidido**, texto do mantenedor, em inglês (a mesma frase da bio da conta IUNA). Sem formatação e sem repetir o nome (regra 5.3). |
| Categorias principais (até 3) | `technology`, `magic`, `adventure` | Create, Mekanism e AE2; Ars Nouveau, Iron's Spells e Occultism; Twilight Forest, Aether, BetterEnd e Alex's Caves. |
| Categorias adicionais | `kitchen-sink`, `multiplayer`, `combat` | 285 mods de todos os temas, servidor da comunidade, Better Combat, Cataclysm e Apotheosis. |
| Loader e versão | NeoForge, 1.21.1 | Vêm da versão (o Modrinth lê do `.mrpack`). |
| Environment | **Client and server, required on both** (`client_and_server`) | Os mods de conteúdo precisam estar nos dois lados para entrar no servidor. O `.mrpack` também lista os mods `side = server` baixados do Modrinth; os jars só de servidor do CurseForge não vão no arquivo, porque o servidor IUNA instala pelo packwiz-installer. |
| Licença | `MIT`, URL `https://github.com/IunaMC/modpack-cliente/blob/main/LICENSE` | **Decidido.** Veja a seção 3. |
| Aviso de IA | Marcar **Contains AI-generated content** (texto) | **Decidido.** A descrição foi escrita com ajuda de IA; a regra 6.1 exige o aviso. |
| Descrição | [`descricao.en.md`](descricao.en.md), com o português de [`descricao.md`](descricao.md) num bloco recolhível e o banner no topo | Veja como juntar os dois em [`publicar.md`](publicar.md). |

### Links

| Campo | Valor |
| --- | --- |
| Source | `https://github.com/IunaMC/modpack-cliente` |
| Issues | `https://github.com/IunaMC/issues` |
| Wiki | `<link-da-wiki>` (deixe vazio se não houver) |
| Discord | `<convite-do-discord>`. Só preencha com um **convite público** que não expire; a regra 5.4 exige links públicos. Se o Discord for só por convite pessoal, deixe vazio. |
| Doações | `<link-de-doação>` ou vazio |

## 3. Licença do pack

O `.mrpack` contém o que o IunaMC escreveu (o manifesto `modrinth.index.json`
com a seleção de mods e, no futuro, configs) e os jars embutidos de terceiros,
que continuam com a licença de cada autor. A licença do projeto cobre só a
primeira parte. Escolhida: **MIT**, no [`LICENSE`](../LICENSE) da raiz.

| Opção | SPDX | Prós | Contras |
| --- | --- | --- | --- |
| **MIT** (sugerida) | `MIT` | O repositório já é público. Deixa outros servidores reaproveitarem a lista e as configs, só pedindo o aviso de copyright. É a licença mais comum em packs do Modrinth. | Permite uso comercial e forks sem devolver mudanças. |
| CC BY-SA 4.0 | `CC-BY-SA-4.0` | Pensada para conteúdo, não código. Obriga quem derivar a manter a mesma licença. | Menos comum em modpacks; não é ideal para scripts. |
| Todos os direitos reservados | `LicenseRef-All-Rights-Reserved` | Ninguém pode redistribuir o pack. | Contradiz um repositório público feito para ser lido e copiado. |

**Sugestão:** MIT, com um `LICENSE` na raiz do repositório e esta frase no
README e na descrição: "A licença vale para os arquivos do IunaMC. Cada mod
mantém a licença do autor." No Modrinth, `License URL` =
`https://github.com/IunaMC/modpack-cliente/blob/main/LICENSE`.

## 4. Ícone e galeria (você precisa produzir)

Nada disso pode ser gerado por IA (regra 6.2.1).

- **Ícone do projeto:** PNG quadrado, 512×512 (mínimo 256×256), até 256 KiB.
  Precisa ficar legível em 96×96: logo do IUNA com pouco texto.
- **Ícone da organização IunaMC:** o mesmo logo ou uma variação, mesmo formato.
- **Galeria:** de 4 a 8 capturas reais do jogo com o pack, em 1920×1080 (16:9),
  PNG ou JPEG, até 5 MiB cada. Sugestões, uma por tema:
  1. Base com Create funcionando (destacada: vira o banner da página).
  2. Máquinas do Mekanism ou rede do AE2.
  3. Magia: altar do Ars Nouveau ou um feitiço do Iron's Spells.
  4. Uma dimensão: Twilight Forest, Aether ou BetterEnd.
  5. Um dragão do Ice and Fire ou um chefe do Cataclysm.
  6. Cozinha com Farmer's Delight e os addons.
  7. Uma vila ou construção com Chipped, Handcrafted e Supplementaries.
- Use shaders só se a captura não enganar: diga no título da imagem que foi com
  Iris e qual shader, já que o pack não traz shader.
- Cada imagem pode ter título e descrição. Não mostre o IP do servidor nem
  nomes de jogadores sem autorização.

## 5. Organização e projeto

Já existem: a organização **IUNA** (`https://modrinth.com/organization/iuna`,
ID `T8IxJ4hk`) e, dentro dela, o projeto `iuna` (ID `vfStiAFv`). Em 17/10/2026
o projeto recebeu pela API a descrição, as categorias, os links, a URL da
licença, o banner na galeria e a versão 3.0.0 (`h30ZlPSP`), e continua em
rascunho. O aviso de IA e a página **Permissions** só existem no site.

## 6. Antes de enviar para revisão

- [ ] Organização IunaMC criada, com ícone.
- [ ] Projeto criado na organização, com nome, slug, resumo e categorias.
- [x] Licença escolhida (MIT, com `LICENSE` no repositório).
- [ ] Environment configurado como *client and server*.
- [ ] Descrição em PT com a tradução em inglês colada.
- [x] Aviso de IA decidido (marcar).
- [ ] Ícone e galeria enviados.
- [ ] Links preenchidos (sem placeholders `<...>`).
- [ ] Primeira versão enviada e todos os arquivos externos resolvidos na
      página **Permissions** ([`permissoes.md`](permissoes.md)).
- [ ] README do repositório com o link real do Modrinth.
