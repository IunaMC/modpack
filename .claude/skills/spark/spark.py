#!/usr/bin/env python3
"""Lê um perfil do Spark exportado em .json pelo viewer (botão de download).

Uso:
  python3 spark.py resumo <perfil.json>          # período, MSPT, GC, flags, entidades e as janelas de 1 min
  python3 spark.py mods <perfil.json>            # % do tick por etapa conhecida e por mod
  python3 spark.py pico <perfil.json> <janela>…  # o que cresceu na janela do pico em relação à mediana
  python3 spark.py metodo <perfil.json> <Classe.metodo>  # total de um método e as janelas em que pesou

O Spark guarda só ~60 janelas: perfil longo perde o começo. Janela com menos de
60 s amostrados = a JVM parou (GC ou safepoint), não foi o tick.
"""
import datetime
import json
import statistics as st
import sys
from collections import Counter

ETAPAS = [
    "EntityTickList.forEach", "ServerChunkCache.tickChunks", "NaturalSpawner.spawnForChunk",
    "Level.tickBlockEntities", "LevelTicks.tick", "MinecraftServer.saveEverything", "EventBus.post",
    "ServerGamePacketListenerImpl.tick", "ServerChunkCache$MainThreadExecutor.managedBlock",
    "ChunkSerializer.read", "StructureTemplateManager.readStructure",
]


def hora(ms, fmt="%d/%m %H:%M"):
    return datetime.datetime.fromtimestamp(ms / 1000).strftime(fmt)


class Perfil:
    def __init__(self, arquivo):
        self.d = json.load(open(arquivo))
        self.wins = sorted(self.d["timeWindows"])
        self.tw = self.d["timeWindowStatistics"]
        self.W = len(self.wins)
        t = self.d["threads"][0]
        self.raizes = t["childrenRefs"]
        self.N = t["children"]
        self.cs = self.d["classSources"]
        self.pai = {c: i for i, n in enumerate(self.N) for c in n["childrenRefs"]}

    def nome(self, i):
        n = self.N[i]
        return f'{n["className"].split(".")[-1]}.{n["methodName"]}'

    def mod(self, i):
        c = self.N[i]["className"]
        return self.cs.get(c.split("$")[0]) or self.cs.get(c, "")

    def ancestrais(self, i):
        while i in self.pai:
            i = self.pai[i]
            yield i

    def mais_externos(self, chave):
        """Nós com esse nome que não estão dentro de outro com o mesmo nome."""
        return [i for i in range(len(self.N)) if self.nome(i) == chave
                and not any(self.nome(a) == chave for a in self.ancestrais(i))]

    def tick(self, w=None):
        nos = [i for i in range(len(self.N)) if self.nome(i) == "MinecraftServer.tickServer"]
        return sum(sum(self.N[i]["times"]) if w is None else self.N[i]["times"][w] for i in nos)

    def janela(self, inicio):
        return self.wins.index(int(inicio)), self.tw[str(inicio)]

    def mediana_fora(self, i, w):
        outras = [self.N[i]["times"][k] for k in range(self.W) if k != w]
        return st.median(outras) if outras else 0


def resumo(p):
    m = p.d["metadata"]
    ps, ss = m["platformStatistics"], m["systemStatistics"]
    print(hora(m["startTime"]), "->", hora(m["endTime"]), f'({(m["endTime"] - m["startTime"]) / 60000:.0f} min)',
          "ticks", m.get("numberOfTicks"), "comentário", repr(m.get("comment")))
    print("jogadores", ps.get("playerCount"), "| uptime", round(ps["uptime"] / 3.6e6, 1), "h")
    print("MSPT 5 min", {k: round(v, 1) for k, v in ps["mspt"]["last5m"].items()})
    print("GC", {k: (v["total"], round(v["avgTime"], 1)) for k, v in ps["gc"].items()})
    print("flags", " ".join(a for a in ss["java"]["vmArgs"].split() if a.startswith("-X") or "GC" in a))
    sp = json.loads(m.get("serverConfigurations", {}).get("server.properties", "{}"))
    print("simulation-distance", sp.get("simulation-distance"), "| view-distance", sp.get("view-distance"),
          "(6 = configs do repo; 8 = servidor sem elas)")
    w = ps.get("world", {})
    print("entidades", w.get("totalEntities"), sorted(w.get("entityCounts", {}).items(), key=lambda x: -x[1])[:15])
    amostrado = [sum(p.N[r]["times"][k] for r in p.raizes) for k in range(p.W)]
    print("janelas (* = menos de 60 s amostrados: a JVM parou):")
    for k, ini in enumerate(p.wins):
        x = p.tw[str(ini)]
        marca = "*" if amostrado[k] < 59000 else " "
        print(f' {marca}{ini} {hora(x["startTime"], "%H:%M")} tps {x["tps"]:.1f} mediana {x["msptMedian"]:.0f} '
              f'max {x["msptMax"]:.0f} jog {x["players"]} ent {x["entities"]} chunks {x["chunks"]} '
              f'amostrado {amostrado[k] / 1000:.1f}s')


def mods(p):
    tick = p.tick()
    print(f"tick total {tick / 1000:.0f} s")
    for k in ETAPAS:
        tot = sum(sum(p.N[i]["times"]) for i in p.mais_externos(k))
        print(f"  {k:55s} {100 * tot / tick:5.1f}%")
    agg = Counter()
    for i in range(len(p.N)):
        m = p.mod(i)
        if m and not any(p.mod(a) == m for a in p.ancestrais(i)):
            agg[m] += sum(p.N[i]["times"])
    print("mods (inclusivo, sem contar o mesmo mod aninhado; self atribuído a mixin pode ser artefato):")
    for m, v in agg.most_common(25):
        print(f"  {m:30s} {100 * v / tick:5.1f}%")


def pico(p, janelas):
    for ini in janelas:
        w, x = p.janela(ini)
        print(f'\n=== {hora(x["startTime"], "%H:%M")} msptMax {x["msptMax"]:.0f}')
        cresceu = lambda i: (p.N[i]["times"][w] >= 800
                             and p.mediana_fora(i, w) <= p.N[i]["times"][w] * 0.2)
        topo = [i for i in range(len(p.N)) if cresceu(i) and not (i in p.pai and cresceu(p.pai[i]))]
        for i in sorted(topo, key=lambda i: -p.N[i]["times"][w])[:4]:
            caminho = [p.nome(a) for a in p.ancestrais(i)][::-1]
            print(" caminho:", " > ".join(caminho[-6:]))
            j, prof = i, 0
            while prof <= 60:
                v = p.N[j]["times"][w]
                print(f'   {"  " * min(prof, 12)}{p.nome(j)} [{p.mod(j)}] {v / 1000:.1f}s')
                prof += 1
                filhos = sorted(p.N[j]["childrenRefs"], key=lambda c: -p.N[c]["times"][w])
                grandes = [c for c in filhos[:3] if p.N[c]["times"][w] >= v * 0.35]
                if not grandes:
                    break
                for c in grandes[1:]:
                    print(f'   {"  " * min(prof, 12)}(+) {p.nome(c)} [{p.mod(c)}] {p.N[c]["times"][w] / 1000:.1f}s')
                j = grandes[0]


def metodo(p, chave):
    nos = p.mais_externos(chave)
    tot = [sum(p.N[i]["times"][k] for i in nos) for k in range(p.W)]
    tick = p.tick()
    print(chave, f"{sum(tot) / 1000:.1f} s de {tick / 1000:.0f} s de tick = {100 * sum(tot) / max(1, tick):.1f}%")
    print("  janelas com 0,3 s ou mais:", " ".join(
        f'{hora(p.tw[str(p.wins[k])]["startTime"], "%H:%M")}={tot[k] / 1000:.1f}' for k in range(p.W) if tot[k] >= 300))


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("resumo", "mods", "pico", "metodo"):
        sys.exit(__doc__)
    p = Perfil(sys.argv[2])
    {"resumo": lambda: resumo(p), "mods": lambda: mods(p),
     "pico": lambda: pico(p, sys.argv[3:]), "metodo": lambda: metodo(p, sys.argv[3])}[sys.argv[1]]()


if __name__ == "__main__":
    main()
