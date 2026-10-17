#!/usr/bin/env bash
# Sobe um servidor NeoForge de verdade com os mods de servidor do pack e
# espera o "Done (". Falha se o servidor travar, cair ou passar do tempo.
#
# Uso: bash scripts/testar-servidor.sh [pasta-do-servidor]   (padrão: ./servidor-teste)
# Variáveis: MEMORIA (padrão 8G), LIMITE em segundos (padrão 1200).
#
# Instala os mods como o servidor de produção: packwiz-installer com "-s server",
# lendo o pack servido localmente por HTTP.
set -euo pipefail

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
DIR="$(realpath -m "${1:-$RAIZ/servidor-teste}")"
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

echo "==> Subindo o servidor (limite de ${LIMITE}s)"
echo "eula=true" > eula.txt
[[ -f server.properties ]] || printf 'online-mode=false\nlevel-seed=iuna\nview-distance=6\n' > server.properties
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
