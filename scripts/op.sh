#!/usr/bin/env bash
# Atalhos das tarefas de rotina do pack, para quem opera sem o Claude Code.
# Cada alvo só junta os comandos dos guias em docs/guias/; só beta, estavel e propagar publicam.
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
#   propagar <versão>
#               leva a estável à moderação (pack base, commit reassinado, PR, merge, devel/devel)
#               e ao MODPACK do minecraft-config. Os clones ficam ao lado do modpack
#               (MODERACAO_DIR e CONFIGS_DIR trocam o caminho)
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

# Espera o check obrigatório conferir (Entrada na main) de um PR e os demais checks.
# O conferir demora a aparecer depois do gh pr create: sem esperar por ele, o
# gh pr checks --watch termina com os outros checks e o merge é recusado.
espera_conferir() {
  local pr="$1" tentativas=0 estado
  until [[ -n "$(gh pr checks "$pr" --required --json name --jq '.[] | select(.name == "conferir") | .name' 2>/dev/null || true)" ]]; do
    (( ++tentativas > 24 )) && { echo "O check conferir não apareceu no PR $pr depois de 2 min: gh pr checks $pr" >&2; return 2; }
    sleep 5
  done
  gh pr checks "$pr" --watch --interval 15 > /dev/null || { echo "O PR $pr tem check vermelho: gh pr checks $pr" >&2; return 1; }
  estado="$(gh pr checks "$pr" --required --json name,bucket --jq '.[] | select(.name == "conferir") | .bucket' || true)"
  [[ "$estado" == pass ]] || { echo "O conferir (Entrada na main) do PR $pr terminou como '$estado': gh pr checks $pr" >&2; return 1; }
  echo "==> conferir verde."
}

# Faz o merge commit de um PR e confere que ele entrou (gh pr merge recusado não pode passar).
merge_pr() {
  local pr="$1"
  gh pr merge "$pr" --merge || { echo "O merge do PR $pr foi recusado: gh pr view $pr" >&2; return 1; }
  [[ "$(gh pr view "$pr" --json state --jq .state)" == MERGED ]] \
    || { echo "O PR $pr não ficou MERGED depois do gh pr merge: gh pr view $pr" >&2; return 1; }
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
  espera_conferir "$pr" || return 1

  # 4. merge commit; nunca rebase, nunca apagar a devel/devel
  merge_pr "$pr" || return 1
  git fetch -q
  sha="$(git rev-parse origin/main)"

  # 5. Release da main (GitHub e CurseForge)
  id="$(run_do_commit release.yaml "$sha")" || { echo "O Release da main não começou para ${sha:0:7}." >&2; return 2; }
  echo "==> Release, run $id"
  local falhou=0
  gh run watch "$id" --exit-status --interval 15 > /dev/null || falhou=1
  gh run view "$id" --json jobs --jq '.jobs[].steps[] | select(.name | test("CurseForge")) | "  \(.name): \(.conclusion)"'

  # 6. devel/devel igual à main, mesmo se o Release falhou (o merge já aconteceu)
  git merge --ff-only origin/main > /dev/null || { echo "A devel/devel não avança só com a main: resolva e faça o push." >&2; return 1; }
  git push origin devel/devel || return 1
  if (( falhou )); then
    echo "O Release falhou: gh run view $id --log-failed. A release do GitHub vale se existir; a devel/devel já está alinhada." >&2
    return 1
  fi
  gh release view "v$versao" --json url --jq '"Release \(.url)"'
  echo "Falta propagar: o /propagar leva a v$versao à moderação e às configs."
}

# Leva a versão estável do modpack à moderação e às configs. Mexe em dois outros
# clones, ao lado deste (mesmo a partir de um worktree). Nunca apaga branch.
propagar() {
  local versao="${1:-}" mod cfg raiz base branch sha id pr issue
  [[ "$versao" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "Uso: op.sh propagar X.Y.Z" >&2; return 1; }
  raiz="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"
  mod="${MODERACAO_DIR:-$(dirname "$raiz")/iunamc.modpack-moderacao}"
  cfg="${CONFIGS_DIR:-$(dirname "$raiz")/iunamc.minecraft-config}"
  [[ -d "$mod/.git" && -d "$cfg/.git" ]] || { echo "Não achei os clones $mod e $cfg." >&2; return 1; }
  gh release view "v$versao" --json isPrerelease --jq 'select(.isPrerelease | not)' > /dev/null \
    || { echo "v$versao não é uma release estável do modpack." >&2; return 1; }
  for dir in "$mod" "$cfg"; do
    [[ -z "$(git -C "$dir" status --porcelain)" ]] || { echo "A árvore de $dir não está limpa." >&2; return 1; }
  done

  # 1. Moderação
  git -C "$mod" fetch -q --prune
  base="$(git -C "$mod" show origin/main:base.toml | sed -nE 's/^tag = "(.*)"/\1/p')"
  if [[ "$base" == "v$versao" ]]; then
    echo "==> Moderação já está na v$versao."
  else
    branch="base/v$versao"
    if [[ -z "$(git -C "$mod" ls-remote --heads origin "$branch")" ]]; then
      echo "==> Disparando o Acompanhar pack base"
      GH_REPO=IunaMC/modpack-moderacao gh workflow run acompanhar-base.yaml
      sleep 10
      id="$(GH_REPO=IunaMC/modpack-moderacao gh run list --workflow acompanhar-base.yaml --limit 1 --json databaseId --jq '.[0].databaseId')"
      GH_REPO=IunaMC/modpack-moderacao gh run watch "$id" --exit-status --interval 15 > /dev/null \
        || { echo "O Acompanhar pack base falhou: gh run view $id -R IunaMC/modpack-moderacao --log-failed" >&2; return 1; }
      git -C "$mod" fetch -q --prune
      [[ -n "$(git -C "$mod" ls-remote --heads origin "$branch")" ]] \
        || { echo "O workflow não criou a $branch (veja as issues de Pack base na moderação)." >&2; return 1; }
    fi
    git -C "$mod" checkout -q -B "$branch" "origin/$branch"
    # O bot não tem a chave de quem mantém: refaz o commit com a sua.
    if [[ "$(git -C "$mod" log -1 --format=%G?)" == N ]]; then
      git -C "$mod" commit --amend --no-edit --reset-author -S -s
      git -C "$mod" push --force-with-lease origin "$branch"
    fi
    sha="$(git -C "$mod" rev-parse HEAD)"
    pr="$(GH_REPO=IunaMC/modpack-moderacao gh pr list --head "$branch" --state open --json number --jq '.[0].number // empty')"
    if [[ -z "$pr" ]]; then
      issue="$(GH_REPO=IunaMC/modpack-moderacao gh issue list --state open --search "Pack base v$versao in:title" --json number --jq '.[0].number // empty')"
      pr="$(GH_REPO=IunaMC/modpack-moderacao gh pr create --base main --head "$branch" --title "Pack base v$versao" \
              --body "${issue:+Closes #$issue}" | grep -oE '[0-9]+$')"
    fi
    echo "==> PR da moderação: $(GH_REPO=IunaMC/modpack-moderacao gh pr view "$pr" --json url --jq .url)"
    id="$(GH_REPO=IunaMC/modpack-moderacao run_do_commit validar.yaml "$sha")" \
      || { echo "O Validar da moderação não começou para ${sha:0:7}." >&2; return 2; }
    GH_REPO=IunaMC/modpack-moderacao gh run watch "$id" --exit-status --interval 15 > /dev/null \
      || { echo "O Validar da moderação falhou: gh run view $id -R IunaMC/modpack-moderacao --log-failed" >&2; return 1; }
    echo "--- MUDANCAS.md da moderação:"; git -C "$mod" show "HEAD:MUDANCAS.md" | sed -n 1,20p
    GH_REPO=IunaMC/modpack-moderacao merge_pr "$pr" || return 1
    git -C "$mod" fetch -q
    sha="$(git -C "$mod" rev-parse origin/main)"
    id="$(GH_REPO=IunaMC/modpack-moderacao run_do_commit release.yaml "$sha")" \
      || { echo "O Release da moderação não começou." >&2; return 2; }
    GH_REPO=IunaMC/modpack-moderacao gh run watch "$id" --exit-status --interval 15 > /dev/null \
      || { echo "O Release da moderação falhou: gh run view $id -R IunaMC/modpack-moderacao --log-failed" >&2; return 1; }
    # A devel/devel de lá pode ter commits que a main ainda não tem: aí vai merge assinado.
    git -C "$mod" checkout -q devel/devel || return 1
    git -C "$mod" merge -q --ff-only "origin/devel/devel" 2> /dev/null || true
    if ! git -C "$mod" merge -q --ff-only origin/main 2> /dev/null; then
      git -C "$mod" merge -q -S --signoff --no-edit origin/main \
        || { git -C "$mod" merge --abort 2> /dev/null; echo "A main da moderação não entra na devel/devel de lá sem conflito: resolva em $mod." >&2; return 1; }
    fi
    git -C "$mod" push origin devel/devel || { echo "O push da devel/devel da moderação falhou." >&2; return 1; }
    echo "==> Moderação na v$versao."
  fi

  # 2. Configs
  if [[ "$(git -C "$cfg" branch --show-current)" != devel/devel ]]; then
    echo "O minecraft-config tem que estar na devel/devel." >&2; return 1
  fi
  if [[ "$(cat "$cfg/MODPACK")" == "$versao" ]]; then
    echo "==> Configs já testam com o modpack $versao."
  else
    echo "$versao" > "$cfg/MODPACK"
    git -C "$cfg" commit -S -s -a -m "build: testa com o modpack $versao" || return 1
    git -C "$cfg" push origin devel/devel || return 1
    echo "==> MODPACK das configs em $versao."
  fi
  echo "Falta: o /versao do minecraft-config (testa o servidor com o pack novo) e o envio pelo FileZilla."
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
    python3 scripts/pack.py soltos
    python3 scripts/curseforge.py verificar ;;
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
  propagar)
    propagar "${2:-}" ;;
  *)
    sed -n '2,25p' "$0" | sed 's/^# \{0,1\}//'
    exit 1 ;;
esac
