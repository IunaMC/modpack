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
set -euo pipefail
cd "$(dirname "$0")/.."

estavel() { git tag --list 'v*' --sort=-v:refname | grep -v -- -beta | head -1; }

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
  *)
    sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
    exit 1 ;;
esac
