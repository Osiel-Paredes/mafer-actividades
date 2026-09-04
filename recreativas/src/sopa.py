# -*- coding: utf-8 -*-
"""Sopa de letras 15x15: las letras que sobran, leidas en orden, forman un mensaje."""
import random, json

N = 15
PALABRAS = ["APAPACHAR","ACHICHINCLE","CHIPICHIPI","ZANGOLOTEAR","ESDRUJULA","CACOFONIA",
            "ORNITORRINCO","JIPIJAPA","TLACUACHE","CHAMAGOSO","MOLCAJETE","TIANGUIS",
            "PETATE","CHAPULIN","METATE","AGUACERO","TECOLOTE","CHINAMPA","MECATE","JICARA"]
DIRS = [(0,1),(1,0),(1,1),(-1,1),(0,-1),(-1,0),(-1,-1),(1,-1)]

def intentar(seed, cuantas):
    rnd = random.Random(seed)
    pals = PALABRAS[:cuantas]
    g = [[None]*N for _ in range(N)]
    puestas = []
    for p in sorted(pals, key=len, reverse=True):
        opts = []
        for r in range(N):
            for c in range(N):
                for dr, dc in DIRS:
                    fr, fc = r + dr*(len(p)-1), c + dc*(len(p)-1)
                    if not (0 <= fr < N and 0 <= fc < N): continue
                    ok = True
                    for i, ch in enumerate(p):
                        v = g[r+dr*i][c+dc*i]
                        if v is not None and v != ch: ok = False; break
                    if ok: opts.append((r, c, dr, dc))
        if not opts: return None
        r, c, dr, dc = rnd.choice(opts)
        for i, ch in enumerate(p): g[r+dr*i][c+dc*i] = ch
        puestas.append((p, r, c, dr, dc))
    libres = [(r, c) for r in range(N) for c in range(N) if g[r][c] is None]
    return g, puestas, libres

# ¿que longitudes de mensaje son alcanzables?
alcanzables = {}
for cuantas in range(14, 21):
    for seed in range(120):
        t = intentar(seed, cuantas)
        if not t: continue
        L = len(t[2])
        alcanzables.setdefault(L, (seed, cuantas))
print("longitudes de mensaje posibles (largo -> seed, nº palabras):")
for L in sorted(alcanzables)[:40]:
    print(f"   {L:3}  {alcanzables[L]}")
json.dump({str(k): v for k, v in alcanzables.items()}, open("sopa_opciones.json","w"))
