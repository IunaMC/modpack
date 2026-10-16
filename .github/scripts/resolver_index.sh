#!/usr/bin/env bash
# Resolve o arquivo index.lock (sintaxe de .gitignore) na lista de arquivos do ZIP.
#
# Uso: bash ./github/scripts/resolver_index.sh [caminho-do-index]   (padrão: index.lock)
#
# Regras:
#   - cada linha é um arquivo, diretório ou padrão (*, **, ?, [abc], /raiz, dir/);
#   - diretório (com ou sem "/" no fim) inclui todo o conteúdo, recursivamente;
#   - linhas "!padrão" são EXCLUSÕES: depois de resolver todas as inclusões,
#     tudo que casar com alguma exclusão sai da lista, não importa a ordem;
#   - linhas vazias e comentários (#) são ignorados.
#
# A correspondência é feita pelo próprio git (git ls-files), então a semântica
# é exatamente a do .gitignore. Só entram arquivos versionados.
#
# Saída (stdout): um caminho por linha, ordenado e sem repetições.
set -euo pipefail
export LC_ALL=C

INDEX="${1:-index.lock}"
cd "$(git rev-parse --show-toplevel)"
[[ -f "$INDEX" ]] || { echo "ERRO: '$INDEX' não encontrado" >&2; exit 1; }

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
: > "$tmp/inc"
: > "$tmp/exc.padroes"

aviso() {
  if [[ -n "${GITHUB_ACTIONS:-}" ]]; then
    echo "::warning file=$INDEX::$1" >&2
  else
    echo "AVISO: $1" >&2
  fi
}

# Arquivos versionados que casam com os padrões do arquivo $1 (separados por NUL).
resolver() {
  git ls-files -z --cached --ignored --exclude-from="$1"
}

while IFS= read -r linha || [[ -n "$linha" ]]; do
  linha="${linha%$'\r'}"
  [[ -z "${linha//[[:space:]]/}" || "$linha" == \#* ]] && continue

  if [[ "$linha" == '!'* ]]; then
    printf '%s\n' "${linha#!}" >> "$tmp/exc.padroes"
  else
    printf '%s\n' "$linha" > "$tmp/linha"
    resolver "$tmp/linha" > "$tmp/res"
    [[ -s "$tmp/res" ]] || aviso "a entrada '$linha' não corresponde a nenhum arquivo versionado"
    cat "$tmp/res" >> "$tmp/inc"
  fi
done < "$INDEX"

sort -zu "$tmp/inc" > "$tmp/inc.ord"
if [[ -s "$tmp/exc.padroes" ]]; then
  resolver "$tmp/exc.padroes" | sort -zu > "$tmp/exc.ord"
else
  : > "$tmp/exc.ord"
fi

comm -z -23 "$tmp/inc.ord" "$tmp/exc.ord" | tr '\0' '\n'