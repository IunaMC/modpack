#!/usr/bin/env bash
# Atalhos das tarefas de rotina do pack, para quem opera sem o Claude Code.
# Cada alvo só junta os comandos dos guias em docs/guias/; nada aqui publica.
#
# Uso: bash scripts/op.sh <alvo>
#   refresh     packwiz refresh + README + fonte da CurseForge (depois de mexer em mods)
#   corrigir    o mesmo, consertando o file-id da CurseForge (depois de packwiz update)
#   conferir    o que o Validar confere, sem subir o servidor
#   testar      sobe o servidor local com as configs de ../iunamc.minecraft-config
#   versao      versão atual e a próxima beta sugerida pelo SemVer
#   mudancas    mods mudados desde a última estável
#   resumo      o Resumo semanal, na sua máquina
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
  ci)
    ci "${2:-}" ;;
  *)
    sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'
    exit 1 ;;
esac
