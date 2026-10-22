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
#   ci [id]     espera o Validar do commit atual (ou do run <id>) e, se falhar, mostra só o erro
set -euo pipefail
cd "$(dirname "$0")/.."

estavel() { git tag --list 'v*' --sort=-v:refname | grep -v -- -beta | head -1; }

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

# Espera o run de um workflow para o commit atual (até 1 min para ele aparecer).
# Imprime o id; sai com 2 se o run não aparecer.
run_do_commit() {
  local id tentativas=0
  until id="$(gh run list --workflow "$1" --commit "$(git rev-parse HEAD)" --limit 1 \
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
    python3 scripts/pack.py mudancas "$(estavel)" ;;
  resumo)
    python3 scripts/resumo.py ;;
  beta)
    beta "${@:2}" ;;
  ci)
    ci "${2:-}" ;;
  *)
    sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'
    exit 1 ;;
esac
