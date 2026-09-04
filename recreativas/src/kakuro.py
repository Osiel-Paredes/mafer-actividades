# -*- coding: utf-8 -*-
"""Kakuro con solucion unica verificada. Rejilla 9x9 (fila y columna 0 = pistas)."""
import random, json
from itertools import combinations

N = 8
COMB = {}
for l in range(2, 10):
    for c in combinations(range(1, 10), l):
        COMB.setdefault((sum(c), l), []).append(set(c))

def runs(pat):
    H, V = [], []
    for r in range(N):
        c = 0
        while c < N:
            if pat[r][c]:
                ini = c
                while c < N and pat[r][c]: c += 1
                if c - ini >= 2: H.append([(r, x) for x in range(ini, c)])
                elif c - ini == 1: return None, None
            else: c += 1
    for c in range(N):
        r = 0
        while r < N:
            if pat[r][c]:
                ini = r
                while r < N and pat[r][c]: r += 1
                if r - ini >= 2: V.append([(x, c) for x in range(ini, r)])
                elif r - ini == 1: return None, None
            else: r += 1
    return H, V

def patron(seed):
    rnd = random.Random(seed)
    pat = [[0]*N for _ in range(N)]
    for r in range(1, N):
        for c in range(1, N):
            pat[r][c] = 0 if rnd.random() < .34 else 1
    # arregla los runs de longitud 1 volviendolos negros
    for _ in range(40):
        H, V = runs(pat)
        if H is not None: return pat, H, V
        cambio = False
        for r in range(N):
            for c in range(N):
                if not pat[r][c]: continue
                hor = ((c == 0 or not pat[r][c-1]) and (c == N-1 or not pat[r][c+1]))
                ver = ((r == 0 or not pat[r-1][c]) and (r == N-1 or not pat[r+1][c]))
                if hor and ver: pat[r][c] = 0; cambio = True
        if not cambio: return None, None, None
    return None, None, None

def llenar(H, V, celdas, seed):
    rnd = random.Random(seed)
    porcelda = {}
    for g in H + V:
        for x in g: porcelda.setdefault(x, []).append(tuple(g))
    orden = sorted(celdas)
    val = {}
    def rec(i):
        if i == len(orden): return True
        x = orden[i]
        ds = list(range(1, 10)); rnd.shuffle(ds)
        for d in ds:
            if all(all(val.get(y) != d for y in g if y != x) for g in porcelda[x]):
                val[x] = d
                if rec(i+1): return True
                del val[x]
        return False
    return val if rec(0) else None

def unica(H, V, sumas, celdas, tope=2):
    porcelda = {}
    for g in H + V:
        for x in g: porcelda.setdefault(x, []).append(tuple(g))
    orden = sorted(celdas, key=lambda x: -len(porcelda[x]))
    val, sols = {}, []
    def posibles(x):
        opts = set(range(1, 10))
        for g in porcelda[x]:
            s = sumas[g]
            usados = {val[y] for y in g if y in val}
            libres = [y for y in g if y not in val]
            ok = set()
            for comb in COMB.get((s, len(g)), []):
                if usados <= comb:
                    ok |= (comb - usados)
            opts &= ok
            opts -= usados
            # si esta es la ultima libre del run, el valor queda forzado
            if len(libres) == 1 and libres[0] == x:
                opts &= {s - sum(usados)}
        return opts
    def rec(i):
        if len(sols) >= tope: return
        if i == len(orden): sols.append(dict(val)); return
        x = orden[i]
        for d in sorted(posibles(x)):
            val[x] = d
            rec(i+1)
            del val[x]
            if len(sols) >= tope: return
    rec(0)
    return sols

elegido = None
for seed in range(60000):
    pat, H, V = patron(seed)
    if not pat: continue
    celdas = [(r, c) for r in range(N) for c in range(N) if pat[r][c]]
    if not (20 <= len(celdas) <= 30): continue
    val = llenar(H, V, celdas, seed)
    if not val: continue
    sumas = {}
    for g in H + V: sumas[tuple(g)] = sum(val[x] for x in g)
    s = unica(H, V, sumas, celdas, tope=2)
    if len(s) == 1:
        elegido = (seed, pat, H, V, sumas, val, celdas); break

if not elegido:
    print("no se encontro; ampliar rango"); raise SystemExit(1)
seed, pat, H, V, sumas, val, celdas = elegido
print("seed:", seed, "| celdas blancas:", len(celdas), "| runs:", len(H), "horizontales,", len(V), "verticales")
print("verificacion:", len(unica(H, V, sumas, celdas, tope=3)), "solucion(es)")
for r in range(N):
    print("  " + " ".join(str(val[(r, c)]) if pat[r][c] else "#" for c in range(N)))
json.dump({"pat": pat, "sol": {f"{r},{c}": val[(r, c)] for r, c in celdas},
           "H": [[list(x) for x in g] for g in H], "V": [[list(x) for x in g] for g in V],
           "sumasH": [sumas[tuple(g)] for g in H], "sumasV": [sumas[tuple(g)] for g in V]},
          open("kakuro.json", "w"))
