# -*- coding: utf-8 -*-
"""Bimaru (batalla naval solitaria) 8x8 con solucion unica verificada."""
import random, json
from itertools import product

N = 8
FLOTA = [3, 2, 2, 1, 1, 1]          # 10 celdas de 64

def vecinos(r, c):
    for dr, dc in product((-1, 0, 1), repeat=2):
        if (dr or dc) and 0 <= r+dr < N and 0 <= c+dc < N:
            yield r+dr, c+dc

# posiciones posibles por largo, con su sombra (celdas que deben quedar en agua)
POS = {}
for largo in set(FLOTA):
    lst = []
    for r in range(N):
        for c in range(N):
            for hor in (True, False):
                if largo == 1 and not hor: continue
                cel = [(r, c+i) if hor else (r+i, c) for i in range(largo)]
                if any(x >= N or y >= N for x, y in cel): continue
                sombra = {v for x, y in cel for v in vecinos(x, y)} - set(cel)
                lst.append((tuple(cel), frozenset(sombra)))
    POS[largo] = lst

def generar(seed):
    rnd = random.Random(seed)
    ocupadas, sombras = set(), set()
    for largo in FLOTA:
        opts = [p for p in POS[largo]
                if not (set(p[0]) & (ocupadas | sombras))]
        if not opts: return None
        cel, som = rnd.choice(opts)
        ocupadas |= set(cel); sombras |= som
    g = [[0]*N for _ in range(N)]
    for r, c in ocupadas: g[r][c] = 1
    return g

def contar(fil, col, dadas, tope=2):
    """Cuenta hasta `tope` soluciones. dadas: {(r,c): 0|1}."""
    sols = []
    fijo_barco = {k for k, v in dadas.items() if v == 1}
    fijo_agua  = {k for k, v in dadas.items() if v == 0}

    def rec(i, ocup, som, desde):
        if len(sols) >= tope: return
        # poda: lo que falta por colocar no puede exceder lo que piden las pistas
        rf = [fil[r] - sum(1 for c in range(N) if (r, c) in ocup) for r in range(N)]
        rc = [col[c] - sum(1 for r in range(N) if (r, c) in ocup) for c in range(N)]
        if any(x < 0 for x in rf + rc): return
        faltan = sum(FLOTA[i:])
        if sum(rf) != faltan or sum(rc) != faltan: return
        if i == len(FLOTA):
            if fijo_barco <= ocup and not (fijo_agua & ocup):
                sols.append(set(ocup))
            return
        largo = FLOTA[i]
        ini = desde if (i > 0 and FLOTA[i-1] == largo) else 0
        for k in range(ini, len(POS[largo])):
            cel, sm = POS[largo][k]
            cs = set(cel)
            if cs & (ocup | som): continue
            if cs & fijo_agua: continue
            if any(fil[r] - sum(1 for c in range(N) if (r, c) in ocup) < 1 for r, c in cel): continue
            rec(i+1, ocup | cs, som | sm, k+1)
            if len(sols) >= tope: return
    rec(0, set(), set(), 0)
    return sols

elegido = None
for seed in range(3000):
    g = generar(seed)
    if not g: continue
    fil = [sum(r) for r in g]
    col = [sum(g[r][c] for r in range(N)) for c in range(N)]
    dadas, rnd = {}, random.Random(seed * 31 + 7)
    for _ in range(10):
        s = contar(fil, col, dadas, tope=2)
        if len(s) == 1:
            elegido = (seed, g, fil, col, dict(dadas)); break
        if not s: break
        a, b = s[0], s[1]
        difs = [(r, c) for r in range(N) for c in range(N)
                if (((r, c) in a) != ((r, c) in b)) and (r, c) not in dadas]
        if not difs: break
        rc = rnd.choice(difs)
        dadas[rc] = g[rc[0]][rc[1]]
    if elegido and len(elegido[4]) <= 5: break

seed, g, fil, col, dadas = elegido
print("seed:", seed, "| celdas reveladas:", len(dadas), dadas)
print("verificacion:", len(contar(fil, col, dadas, tope=3)), "solucion(es)")
print("   " + " ".join(str(c) for c in col))
for r in range(N):
    print(f"{fil[r]}  " + " ".join("#" if g[r][c] else "." for c in range(N)))
json.dump({"grid": g, "fil": fil, "col": col,
           "dadas": [[r, c, v] for (r, c), v in dadas.items()]}, open("bimaru.json", "w"))
print("flota:", FLOTA, "| total celdas:", sum(FLOTA))
