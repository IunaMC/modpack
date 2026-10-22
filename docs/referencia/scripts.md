# Scripts e skills

O uso completo de cada script está no topo do próprio arquivo. Esta página diz
para que serve cada um e liga as skills do Claude Code aos comandos que elas
rodam.

## Scripts

| Script | Para quê |
| --- | --- |
| [`scripts/op.sh`](../../scripts/op.sh) | Atalhos de rotina (`refresh`, `corrigir`, `conferir`, `testar`, `versao`, `mudancas`, `resumo`, `ci`). Nenhum publica |
| [`scripts/pack.py`](../../scripts/pack.py) | Lista de mods do README, versão, próxima beta, mods mudados desde uma tag, `lado` de cada mod pelo Modrinth, dependências `orfas`, [arquivos externos](../guias/arquivos-externos.md) e as [regras da `main`](versionamento.md#o-que-entra-na-main) (`conferir`) |
| [`scripts/curseforge.py`](../../scripts/curseforge.py) | Fonte da CurseForge de cada mod (`verificar`, `ligar`), envio (`publicar`), `status` e `descricao` |
| [`scripts/modrinth.py`](../../scripts/modrinth.py) | Página do Modrinth a partir de `modrinth/` (`verificar`, `sincronizar`) e envio de versões (`publicar`) |
| [`scripts/resumo.py`](../../scripts/resumo.py) | O Resumo semanal, em Markdown |
| [`scripts/testar-servidor.sh`](../../scripts/testar-servidor.sh) | Sobe um servidor NeoForge com o pack ([servidor local](../guias/servidor-local.md)) |

Os que publicam (`publicar`, `sincronizar`) aceitam `--simular`.

## Skills

Cada skill em `.claude/skills/` é um atalho para um guia. Se o Claude Code não
estiver disponível, o guia basta.

| Skill | Guia | Comandos principais | O que só a skill faz |
| --- | --- | --- | --- |
| `/add-mod` | [Adicionar um mod](../guias/adicionar-mod.md) | `packwiz modrinth add`, `pack.py lado`, `curseforge.py ligar`, `op.sh refresh` | Acha o Project ID da CurseForge; o lado e a licença vêm do `pack.py lado` |
| `/remover-mod` | [Remover um mod](../guias/remover-mod.md) | `pack.py orfas`, `packwiz remove`, `op.sh refresh` | Decide se a dependência é mesmo órfã e se o conteúdo pode sair |
| `/beta` | [Publicar uma beta](../guias/publicar-beta.md) | `op.sh versao`, `pack.py mudancas ultima` | Escreve o `MUDANCAS.md`; o resto vira `op.sh beta` ([#19](https://github.com/IunaMC/modpack/issues/19)) |
| `/estavel` | [Publicar a estável](../guias/publicar-estavel.md) | `pack.py mudancas estavel`, `gh pr create`, `gh pr merge --merge` | Escreve o `MUDANCAS.md` e o corpo do PR; o resto vira `op.sh estavel` ([#20](https://github.com/IunaMC/modpack/issues/20)) |
| `/propagar` | [Propagar](https://github.com/IunaMC/docs/blob/main/processo/propagar.md) | `gh workflow run acompanhar-base.yaml`, `git commit --amend -S -s` | Tudo vira `op.sh propagar` ([#21](https://github.com/IunaMC/modpack/issues/21)) |
| `/testar` | [Servidor local](../guias/servidor-local.md) | `op.sh ci`, `testar-servidor.sh` | Escolhe entre o CI e a máquina local pelo disco e pela memória livres |
| `/spark` | — | `.claude/skills/spark/spark.py` | Análise dos perfis do Spark |

A coluna "O que só a skill faz" lista o que ainda depende de julgamento ou de
IA. O que é mecânico vai virar script, com uma issue por script (etiqueta
[`processo`](https://github.com/IunaMC/modpack/issues?q=label%3Aprocesso)).
Quando um script existir, a skill passa a chamá-lo, e o guia mostra o comando
no mesmo commit.

O mapa entre repositórios do que roda sozinho e do que é feito à mão, com o
porquê de cada item, está no IunaMC/docs:
[processos automáticos](https://github.com/IunaMC/docs/blob/main/processo/automatico.md)
e [processos manuais](https://github.com/IunaMC/docs/blob/main/processo/manual.md).
