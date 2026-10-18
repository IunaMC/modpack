#!/usr/bin/env bash
# Sobe um servidor NeoForge de verdade com os mods de servidor do pack e
# espera o "Done (". Falha se o servidor travar, cair ou passar do tempo.
#
# Uso: bash scripts/testar-servidor.sh [opções] [pasta-do-servidor]   (padrão: ./servidor-teste)
#
# Opções:
#   --configs[=PASTA]   copia as configs do servidor (repo IunaMC/minecraft-config)
#                       de uma pasta local, do jeito que estão no disco. Padrão:
#                       ../iunamc.minecraft-config, ao lado deste repositório.
#   --configs-git REF   o mesmo, mas clona a branch ou tag REF do GitHub. O repo é
#                       privado: usa o login do gh ou a variável GH_TOKEN.
#   --manter            não para o servidor quando ele fica pronto: deixa o console
#                       aberto no terminal para entrar no jogo (localhost) e testar.
#
# Variáveis: MEMORIA (padrão 8G), LIMITE em segundos (padrão 1200).
#
# Instala os mods como o servidor de produção: packwiz-installer com "-s server",
# lendo o pack servido localmente por HTTP. Rodar de novo na mesma pasta atualiza
# os mods e recopia as configs; o mundo e os arquivos que não estão no repo de
# configs (tokens, dados do LuckPerms) ficam.
set -euo pipefail

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
CONFIGS=""
CONFIGS_GIT=""
MANTER=false
DIR=""
while (( $# )); do
  case "$1" in
    --configs) CONFIGS="$RAIZ/../iunamc.minecraft-config" ;;
    --configs=*) CONFIGS="${1#--configs=}" ;;
    --configs-git) CONFIGS_GIT="${2:?--configs-git precisa de uma branch ou tag}"; shift ;;
    --configs-git=*) CONFIGS_GIT="${1#--configs-git=}" ;;
    --manter) MANTER=true ;;
    -h|--help) sed -n '2,/^set -euo/{/^set/d;s/^# \{0,1\}//;p}' "$0"; exit 0 ;;
    -*) echo "Opção desconhecida: $1 (veja --help)" >&2; exit 2 ;;
    *) DIR="$1" ;;
  esac
  shift
done
if [[ -n "$CONFIGS" && -n "$CONFIGS_GIT" ]]; then
  echo "Use --configs ou --configs-git, não os dois." >&2
  exit 2
fi
[[ -z "$CONFIGS" ]] || CONFIGS="$(realpath -m "$CONFIGS")"

DIR="$(realpath -m "${DIR:-$RAIZ/servidor-teste}")"
MEMORIA="${MEMORIA:-8G}"
LIMITE="${LIMITE:-1200}"
NEOFORGE="$(python3 "$RAIZ/scripts/pack.py" neoforge)"
BOOTSTRAP=https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar
PORTA=8765

mkdir -p "$DIR"
cd "$DIR"

echo "==> NeoForge $NEOFORGE"
if [[ ! -f "libraries/net/neoforged/neoforge/$NEOFORGE/unix_args.txt" ]]; then
  curl -fsSL -o neoforge-installer.jar \
    "https://maven.neoforged.net/releases/net/neoforged/neoforge/$NEOFORGE/neoforge-$NEOFORGE-installer.jar"
  java -jar neoforge-installer.jar --installServer > neoforge-installer.log 2>&1 \
    || { tail -50 neoforge-installer.log; exit 1; }
  rm -f neoforge-installer.jar run.bat
fi

echo "==> Mods de servidor (packwiz-installer)"
[[ -f packwiz-installer-bootstrap.jar ]] || curl -fsSL -o packwiz-installer-bootstrap.jar "$BOOTSTRAP"
python3 -m http.server "$PORTA" --bind 127.0.0.1 --directory "$RAIZ/pack" > /dev/null 2>&1 &
HTTP=$!
trap 'kill $HTTP 2>/dev/null || true' EXIT
sleep 1
java -jar packwiz-installer-bootstrap.jar -g -s server "http://127.0.0.1:$PORTA/pack.toml"
kill $HTTP
echo "$(ls mods/*.jar | wc -l) jars em mods/"

if [[ -n "$CONFIGS_GIT" ]]; then
  CONFIGS="$DIR/.minecraft-config"
  echo "==> Configs: IunaMC/minecraft-config@$CONFIGS_GIT (GitHub)"
  rm -rf "$CONFIGS"
  gh repo clone IunaMC/minecraft-config "$CONFIGS" -- --quiet --depth 1 --branch "$CONFIGS_GIT"
elif [[ -n "$CONFIGS" ]]; then
  echo "==> Configs: $CONFIGS (pasta local)"
  [[ -d "$CONFIGS/config" ]] || { echo "::error::$CONFIGS não parece o repo minecraft-config (falta config/)."; exit 1; }
fi
if [[ -n "$CONFIGS" ]]; then
  # Copia por cima tudo o que o repo de configs versiona, menos os arquivos do
  # próprio git/GitHub. O que não está no repo (mundo, tokens) não é tocado.
  tar -C "$CONFIGS" --exclude=./.git --exclude=./.github --exclude=./.claude \
    --exclude=./docs --exclude=./.gitignore --exclude='./README*' -cf - . | tar -xf -
  echo "$(find "$CONFIGS/config" -type f | wc -l) arquivos de config copiados"
fi

echo "eula=true" > eula.txt
[[ -f server.properties ]] || printf 'online-mode=false\nlevel-seed=iuna\nview-distance=6\n' > server.properties

if $MANTER; then
  echo "==> Subindo o servidor (console aberto; 'stop' para sair)"
  echo "    Porta: $(grep -oP '^server-port=\K.*' server.properties || echo 25565)"
  exec java "-Xms$MEMORIA" "-Xmx$MEMORIA" "@libraries/net/neoforged/neoforge/$NEOFORGE/unix_args.txt" nogui
fi

echo "==> Subindo o servidor (limite de ${LIMITE}s)"
rm -f entrada && mkfifo entrada
tail -f entrada | java "-Xms$MEMORIA" "-Xmx$MEMORIA" \
  "@libraries/net/neoforged/neoforge/$NEOFORGE/unix_args.txt" nogui > servidor.log 2>&1 &
JAVA=$!
exec 3> entrada

inicio=$SECONDS
resultado=tempo
while (( SECONDS - inicio < LIMITE )); do
  if grep -qE 'Done \([0-9.]+s\)!' servidor.log; then resultado=ok; break; fi
  if ! kill -0 "$JAVA" 2>/dev/null; then resultado=caiu; break; fi
  sleep 5
done

if [[ "$resultado" == ok ]]; then
  echo "==> Servidor pronto em $((SECONDS - inicio))s: $(grep -oE 'Done \([0-9.]+s\)!' servidor.log)"
  echo stop >&3
  for _ in $(seq 60); do kill -0 "$JAVA" 2>/dev/null || break; sleep 2; done
fi
exec 3>&-
kill "$JAVA" 2>/dev/null || true
pkill -f "tail -f entrada" 2>/dev/null || true

if [[ "$resultado" != ok ]]; then
  [[ "$resultado" == tempo ]] && echo "::error::O servidor não ficou pronto em ${LIMITE}s." \
                             || echo "::error::O servidor caiu antes de ficar pronto."
  ls crash-reports/* 2>/dev/null && tail -80 crash-reports/* || true
  echo "==> Últimas linhas do log"
  tail -150 servidor.log
  exit 1
fi

if grep -E '/(ERROR|FATAL)\]' logs/latest.log > erros.log 2>/dev/null && [[ -s erros.log ]]; then
  echo "::warning::O servidor subiu, mas registrou $(wc -l < erros.log) linhas de ERROR/FATAL (veja erros.log nos artefatos)."
fi
