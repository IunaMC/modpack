# Scripts e skills

O uso completo de cada script está no topo do próprio arquivo. Esta página diz
para que serve cada um e liga as skills do Claude Code aos comandos que elas
rodam.

## Scripts

| Script | Para quê |
| --- | --- |
| [`scripts/op.sh`](../../scripts/op.sh) | Atalhos de rotina (`refresh`, `corrigir`, `conferir`, `testar`, `versao`, `mudancas`, `resumo`, `ci`, `beta`, `estavel`, `propagar`). Só `beta`, `estavel` e `propagar` publicam |
| [`scripts/pack.py`](../../scripts/pack.py) | Lista de mods do README, versão, próxima beta, mods mudados desde uma tag, `lado` (só informa o que o Modrinth declara e a licença, não grava), dependências `orfas`, [arquivos externos](../guias/arquivos-externos.md) e as [regras da `main`](versionamento.md#o-que-entra-na-main) (`conferir`) |
| [`scripts/curseforge.py`](../../scripts/curseforge.py) | Fonte da CurseForge de cada mod (`verificar`, `ligar`), envio (`publicar`), `status` e `descricao` (imprime o `curseforge/descricao.md`) |
| [`scripts/resumo.py`](../../scripts/resumo.py) | O Resumo semanal, em Markdown |
| [`scripts/testar-servidor.sh`](../../scripts/testar-servidor.sh) | Sobe um servidor NeoForge com o pack ([servidor local](../guias/servidor-local.md)) |

Os que publicam (`publicar`, `sincronizar`) aceitam `--simular`.

## Skills

Cada skill em `.claude/skills/` é um atalho para um guia. Se o Claude Code não
estiver disponível, o guia basta.

| Skill | Guia | Comandos principais | O que só a skill faz |
| --- | --- | --- | --- |
| `/add-mod` | [Adicionar um mod](../guias/adicionar-mod.md) | `packwiz modrinth add`, `pack.py lado`, `curseforge.py ligar`, `op.sh refresh` | Acha o Project ID da CurseForge; o lado é escolha do usuário; o `pack.py lado` só mostra o que o Modrinth declara e a licença |
| `/remover-mod` | [Remover um mod](../guias/remover-mod.md) | `pack.py orfas`, `packwiz remove`, `op.sh refresh` | Decide se a dependência é mesmo órfã e se o conteúdo pode sair |
| `/beta` | [Publicar uma beta](../guias/publicar-beta.md) | `op.sh beta`, `pack.py mudancas ultima` | Escreve o `MUDANCAS.md`; o resto é do `op.sh beta` |
| `/estavel` | [Publicar a estável](../guias/publicar-estavel.md) | `op.sh estavel`, `pack.py mudancas estavel` | Escreve o `MUDANCAS.md` e o corpo do PR; o resto é do `op.sh estavel` |
| `/propagar` | [Propagar](../guias/propagar.md) | `op.sh propagar` | Nada: é só o script |
| `/testar` | [Servidor local](../guias/servidor-local.md) | `op.sh ci`, `testar-servidor.sh` | Escolhe entre o CI e a máquina local pelo disco e pela memória livres |
| `/spark` | — | `.claude/skills/spark/spark.py` | Análise dos perfis do Spark |

A coluna "O que só a skill faz" lista o que ainda depende de julgamento ou de
IA; o mecânico é script. Quando um passo novo virar script, a skill passa a
chamá-lo, e o guia mostra o comando no mesmo commit. As ideias que ainda não
viraram script ficam nas issues com a etiqueta
[`processo`](https://github.com/IunaMC/modpack/issues?q=label%3Aprocesso).

### Modelo e esforço

Cada skill fixa no próprio cabeçalho (`model` e `effort`) o modelo que a roda,
para não gastar o limite do plano com tarefa mecânica. A regra vale também
para o que se faz sem skill.

A tabela de tarefa, modelo e esforço vale para todos os repositórios e está
nas [regras do Claude Code](https://github.com/IunaMC/docs/blob/main/referencia/claude.md).
Para este repositório: packwiz, commit, `MUDANCAS.md` e conferir o CI são
mecânicos; análise de crash ou do Spark é decisão.

Na conversa principal, o modelo e o esforço se escolhem pelo `/model` e pelo
seletor de esforço. Em subagentes, passe o `model` da tabela. Uma tarefa sem
relação com a anterior abre uma sessão nova, porque o histórico é reenviado a
cada mensagem.

O mapa entre repositórios do que roda sozinho e do que é feito à mão, com o
porquê de cada item, está no IunaMC/docs:
[processos automáticos](https://github.com/IunaMC/docs/blob/main/processo/automatico.md)
e [processos manuais](https://github.com/IunaMC/docs/blob/main/processo/manual.md).
