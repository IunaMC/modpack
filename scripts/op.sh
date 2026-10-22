#!/usr/bin/env bash
# Atalhos das tarefas de rotina do pack, para quem opera sem o Claude Code.
# Cada alvo só junta os comandos dos guias em docs/guias/; só beta e estavel publicam.
#
# Uso: bash scripts/op.sh <alvo>
#   refresh     packwiz refresh + README + fonte da CurseForge (depois de mexer em mods)
#   corrigir    o mesmo, consertando o file-id da CurseForge (depois de packwiz update)
#   conferir    o que o Validar confere, sem subir o servidor
#   testar      sobe o servidor local com as configs de ../iunamc.minecraft-config
#   versao      versão atual e a próxima beta sugerida pelo SemVer
#   mudancas    mods mudados desde a última estável
#   resumo      o Resumo semanal, na sua máquina
#   beta [versão] [--major]
#               prepara e publica a próxima beta pela devel/devel (para antes do commit se o
#               MUDANCAS.md não tiver o título da versão; depois de escrevê-lo, rode de novo)
#   estavel [versão] [--corpo <arquivo.md>] [--major] [--sem-beta]
#               leva a devel/devel à main: versão, commit, Validar, PR, merge commit, Release e
#               alinhamento da devel/devel. Para no primeiro passo vermelho. O MUDANCAS.md e o
#               corpo do PR (--corpo) são seus; depois, rode o /propagar
#   ci [id]     espera o Validar do commit atual (ou do run <id>) e, se falhar, mostra só o erro
set -euo pipefail
cd "$(dirname "$0")/.."

estavel_tag() { git tag --list 'v*' --sort=-v:refname | grep -v -- -beta | head -1; }

# Valida o commit atual no CI: acha o run, espera e, se falhar, filtra o log.
# Os ~110 ERROR/FATAL do servidor sempre aparecem e não explicam nada: saem do filtro.
ci() {
  local id="${1:-}" sha tentativas=0
  sha="$(git rev-parse HEAD)"
  if [[ -z "$id" ]]; then
    if [[ -n "$(git log --oneline '@{u}..HEAD' 2>/dev/null)" ]]; then
      echo "Há commits sem push: o Validar ainda não viu $(git rev-parse --short HEAD). Faça o push antes." >&2
      return 2
    fi
    until id="$(gh run list --workflow validar.yaml --commit "$sha" --limit 1 \
                  --json databaseId --jq '.[0].databaseId // empty')" && [[ -n "$id" ]]; do
      (( ++tentativas > 12 )) && { echo "Nenhum run do Validar para ${sha:0:7} depois de 1 min." >&2; return 2; }
      sleep 5
    done
  fi
  echo "==> Validar, run $id: $(gh run view "$id" --json url --jq .url)"
  if gh run watch "$id" --exit-status --interval 15 > /dev/null; then
    echo "Validar verde."
    return 0
  fi
  echo "Validar falhou. O que explica:"
  gh run view "$id" --log-failed \
    | sed -E 's/^[^\t]*\t[^\t]*\t[0-9T:.Z-]+ ?//' \
    | awk '
        /\/(ERROR|FATAL)\]/ { next }
        { ultimas[NR % 4] = $0 }
        /##\[error\]/ {
          for (i = NR - 3; i < NR; i++) if (i > 0) print ultimas[i % 4]
          print
          next
        }
        /::error::|^Error:|Exception|Caused by|GraphQL/ { print }' \
    | awk '!visto[$0]++' \
    | sed -E 's/##\[error\]/ERRO: /; s/::error:://'
  return 1
}

# Espera o run de um workflow para um commit, o atual por padrão (até 1 min para ele aparecer).
# Imprime o id; sai com 2 se o run não aparecer.
run_do_commit() {
  local id tentativas=0 sha="${2:-$(git rev-parse HEAD)}"
  until id="$(gh run list --workflow "$1" --commit "$sha" --limit 1 \
                --json databaseId --jq '.[0].databaseId // empty')" && [[ -n "$id" ]]; do
    (( ++tentativas > 12 )) && return 2
    sleep 5
  done
  echo "$id"
}

# Prepara e publica a próxima beta. Escrever o MUDANCAS.md continua com pessoa:
# o script para antes do commit enquanto o título não for o da versão nova.
beta() {
  local versao="" major=0 motivo arg tmp tmp
  for arg in "$@"; do
    case "$arg" in
      --major) major=1 ;;
      *) versao="$arg" ;;
    esac
  done
  [[ "$(git branch --show-current)" == devel/devel ]] || { echo "Tem que estar na devel/devel." >&2; return 1; }
  # A segunda rodada chega com o que a primeira preparou (versão, índice, README, MUDANCAS.md).
  if [[ -n "$(git status --porcelain | grep -vE ' (pack/pack\.toml|pack/index\.toml|README\.md|MUDANCAS\.md)$' || true)" ]]; then
    echo "A árvore tem mudanças além das que o beta prepara; commite ou descarte antes." >&2
    return 1
  fi
  if [[ -z "$(git status --porcelain)" ]]; then
    git fetch -q --tags
    git merge --ff-only origin/main > /dev/null || { echo "A devel/devel não avança só com a main: resolva antes." >&2; return 1; }
  fi
  if [[ -z "$versao" ]]; then
    if git rev-parse -q --verify "refs/tags/v$(python3 scripts/pack.py versao)" > /dev/null; then
      tmp="$(mktemp)"
      tmp="$(mktemp)"
      versao="$(python3 scripts/pack.py proxima-beta 2> "$tmp")"
      motivo="$(cat "$tmp")"; rm -f "$tmp"
      echo "==> $versao ($motivo)"
      if [[ "$motivo" == MAJOR* && $major -eq 0 ]]; then
        echo "A sugestão é MAJOR: confirme com a equipe e rode de novo com --major." >&2
        return 1
      fi
    else
      versao="$(python3 scripts/pack.py versao)"  # já preparada, ainda sem tag
    fi
  fi
  [[ "$versao" =~ ^[0-9]+\.[0-9]+\.[0-9]+-beta\.[0-9]+$ ]] || { echo "Versão inválida: $versao (esperado X.Y.Z-beta.N)." >&2; return 1; }
  if [[ "$(python3 scripts/pack.py versao)" != "$versao" ]]; then
    sed -i -E "s/^version = \".*\"/version = \"$versao\"/" pack/pack.toml
  fi
  (cd pack && packwiz refresh)
  python3 scripts/pack.py readme
  if ! head -1 MUDANCAS.md | grep -qF "— v$versao,"; then
    echo "O MUDANCAS.md não tem o título da v$versao. Escreva '# Mudanças — v$versao, <resumo>' e rode de novo." >&2
    echo "Mods desde a última tag (python3 scripts/pack.py mudancas ultima):" >&2
    python3 scripts/pack.py mudancas ultima >&2 || true
    return 3
  fi
  git commit -S -s -a -m "build: prepara a versao $versao"
  git push origin devel/devel
  local id
  id="$(run_do_commit release.yaml)" || { echo "O Release não começou para $(git rev-parse --short HEAD)." >&2; return 2; }
  gh run watch "$id" --exit-status --interval 15 > /dev/null || { echo "O Release falhou: gh run view $id --log-failed" >&2; return 1; }
  gh release view "v$versao" --json url,isPrerelease --jq '"Release \(.url) (pre-release: \(.isPrerelease))"'
}

# Leva a devel/devel à main por PR. Texto do MUDANCAS.md e do PR continua com pessoa.
estavel() {
  local versao="" corpo="" major=0 sem_beta=0 atual titulo pr id sha
  while (( $# )); do
    case "$1" in
      --corpo) corpo="${2:?--corpo pede um arquivo}"; shift ;;
      --major) major=1 ;;
      --sem-beta) sem_beta=1 ;;
      *) versao="$1" ;;
    esac
    shift
  done
  [[ "$(git branch --show-current)" == devel/devel ]] || { echo "Tem que estar na devel/devel." >&2; return 1; }
  if [[ -n "$(git status --porcelain | grep -vE ' (pack/pack\.toml|pack/index\.toml|README\.md|MUDANCAS\.md)$' || true)" ]]; then
    echo "A árvore tem mudanças além das que a estável prepara; commite ou descarte antes." >&2
    return 1
  fi
  atual="$(python3 scripts/pack.py versao)"
  versao="${versao:-${atual%-beta.*}}"
  [[ "$versao" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "Versão inválida: $versao (esperado X.Y.Z)." >&2; return 1; }
  git fetch -q --tags
  if (( ! sem_beta )) && [[ -z "$(git tag --list "v$versao-beta.*")" ]]; then
    echo "Nenhuma beta de $versao saiu. Se pode ir sem beta, rode de novo com --sem-beta." >&2
    return 1
  fi
  if [[ "${versao%%.*}" != "$(estavel_tag | sed 's/^v//; s/\..*//')" && $major -eq 0 ]]; then
    echo "É MAJOR: confirme com a equipe e rode de novo com --major." >&2
    return 1
  fi

  # 1. versão e MUDANCAS.md (o texto é seu)
  if [[ "$atual" != "$versao" ]]; then
    sed -i -E "s/^version = \".*\"/version = \"$versao\"/" pack/pack.toml
  fi
  (cd pack && packwiz refresh)
  python3 scripts/pack.py readme
  if ! head -1 MUDANCAS.md | grep -qF "— v$versao,"; then
    echo "O MUDANCAS.md não tem o título da v$versao. Escreva '# Mudanças — v$versao, <resumo>' (sem a linha 'Beta: …'), comparando com a última estável, e rode de novo." >&2
    python3 scripts/pack.py mudancas estavel >&2 || true
    return 3
  fi
  if grep -q '^Beta:' MUDANCAS.md; then
    echo "O MUDANCAS.md ainda tem a linha 'Beta: …'. Tire e rode de novo." >&2
    return 3
  fi

  # 2. commit, push e Validar
  if [[ -n "$(git status --porcelain)" ]]; then
    git commit -S -s -a -m "build: prepara a versao $versao"
  fi
  git push origin devel/devel
  ci || return 1

  # 3. PR
  titulo="Versão $versao: $(head -1 MUDANCAS.md | sed -E 's/^[^,]*, //')"
  pr="$(gh pr list --head devel/devel --base main --state open --json number --jq '.[0].number // empty')"
  if [[ -z "$pr" ]]; then
    [[ -f "$corpo" ]] || { echo "Sem PR aberto: escreva o corpo (Resumo, Mods, outras mudanças, Testes) e passe com --corpo <arquivo.md>." >&2; return 3; }
    (( major )) && ! grep -q 'MAJOR confirmado' "$corpo" && printf '\nMAJOR confirmado\n' >> "$corpo"
    python3 scripts/pack.py conferir origin/main HEAD --ramo devel/devel > /dev/null \
      || CORPO_PR="$(cat "$corpo")" python3 scripts/pack.py conferir origin/main HEAD --ramo devel/devel
    pr="$(gh pr create --base main --head devel/devel --title "$titulo" --body-file "$corpo" | grep -oE '[0-9]+$')"
  fi
  echo "==> PR $pr: $(gh pr view "$pr" --json url --jq .url)"
  gh pr checks "$pr" --watch --interval 15 || { echo "O PR tem check vermelho: gh pr checks $pr" >&2; return 1; }

  # 4. merge commit; nunca rebase, nunca apagar a devel/devel
  gh pr merge "$pr" --merge
  git fetch -q
  sha="$(git rev-parse origin/main)"

  # 5. Release da main (GitHub, Modrinth e CurseForge)
  id="$(run_do_commit release.yaml "$sha")" || { echo "O Release da main não começou para ${sha:0:7}." >&2; return 2; }
  echo "==> Release, run $id"
  local falhou=0
  gh run watch "$id" --exit-status --interval 15 > /dev/null || falhou=1
  gh run view "$id" --json jobs --jq '.jobs[].steps[] | select(.name | test("Modrinth|CurseForge")) | "  \(.name): \(.conclusion)"'

  # 6. devel/devel igual à main, mesmo se o Release falhou (o merge já aconteceu)
  git merge --ff-only origin/main > /dev/null
  git push origin devel/devel
  if (( falhou )); then
    echo "O Release falhou: gh run view $id --log-failed. A release do GitHub vale se existir; a devel/devel já está alinhada." >&2
    return 1
  fi
  gh release view "v$versao" --json url --jq '"Release \(.url)"'
  echo "Falta propagar: o /propagar leva a v$versao à moderação e às configs."
}

case "${1:-}" in
  refresh)
    (cd pack && packwiz refresh)
    python3 scripts/pack.py readme
    python3 scripts/curseforge.py verificar ;;
  corrigir)
    python3 scripts/curseforge.py verificar --corrigir
    (cd pack && packwiz refresh)
    python3 scripts/pack.py readme ;;
  conferir)
    python3 scripts/pack.py readme --check
    python3 scripts/curseforge.py verificar
    python3 scripts/modrinth.py verificar ;;
  testar)
    bash scripts/testar-servidor.sh --configs "${@:2}" ;;
  versao)
    echo "atual: $(python3 scripts/pack.py versao)"
    echo "próxima beta: $(python3 scripts/pack.py proxima-beta)" ;;
  mudancas)
    python3 scripts/pack.py mudancas "$(estavel_tag)" ;;
  resumo)
    python3 scripts/resumo.py ;;
  beta)
    beta "${@:2}" ;;
  ci)
    ci "${2:-}" ;;
  estavel)
    estavel "${@:2}" ;;
  *)
    sed -n '2,21p' "$0" | sed 's/^# \{0,1\}//'
    exit 1 ;;
esac
