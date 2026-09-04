# -*- coding: utf-8 -*-
"""Laberinto perfecto con tres llaves que hay que recoger en orden."""
import random, json
from collections import deque

W, H = 29, 19          # celdas
def generar(seed):
    rnd = random.Random(seed)
    # paredes: cada celda guarda si tiene pared al N/E/S/O
    vis = [[False]*W for _ in range(H)]
    par = [[{"N": True, "E": True, "S": True, "O": True} for _ in range(W)] for _ in range(H)]
    OP = {"N": "S", "S": "N", "E": "O", "O": "E"}
    D = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}
    pila = [(0, 0)]; vis[0][0] = True
    while pila:
        r, c = pila[-1]
        opts = [d for d, (dr, dc) in D.items()
                if 0 <= r+dr < H and 0 <= c+dc < W and not vis[r+dr][c+dc]]
        if not opts:
            pila.pop(); continue
        d = rnd.choice(opts); dr, dc = D[d]
        par[r][c][d] = False
        par[r+dr][c+dc][OP[d]] = False
        vis[r+dr][c+dc] = True
        pila.append((r+dr, c+dc))
    return par

def ruta(par, a, b):
    D = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}
    prev = {a: None}; q = deque([a])
    while q:
        cur = q.popleft()
        if cur == b: break
        r, c = cur
        for d, (dr, dc) in D.items():
            n = (r+dr, c+dc)
            if not par[r][c][d] and 0 <= n[0] < H and 0 <= n[1] < W and n not in prev:
                prev[n] = cur; q.append(n)
    camino, cur = [], b
    while cur is not None: camino.append(cur); cur = prev[cur]
    return camino[::-1]

# elige una semilla donde el recorrido total sea largo y las llaves queden repartidas
mejor = None
for seed in range(300):
    par = generar(seed)
    ini, fin = (0, 0), (H-1, W-1)
    llaves = [(H//2, 3), (2, W//2 + 4), (H-3, W//2 - 6)]
    tramos = [ini] + llaves + [fin]
    total = sum(len(ruta(par, tramos[i], tramos[i+1])) - 1 for i in range(len(tramos)-1))
    if mejor is None or total > mejor[0]:
        mejor = (total, seed, par, ini, fin, llaves)
total, seed, par, ini, fin, llaves = mejor
print(f"seed {seed} | recorrido mínimo recogiendo las 3 llaves en orden: {total} pasos")

# ---------------- SVG ----------------
S = 22                          # px por celda
o = [f'<svg viewBox="0 0 {W*S+4} {H*S+4}" style="width:100%;height:auto" '
     f'fill="none" stroke="#111" stroke-width="2.4" stroke-linecap="square">']
o.append(f'<rect x="2" y="2" width="{W*S}" height="{H*S}" fill="#fff" stroke="none"/>')
for r in range(H):
    for c in range(W):
        x, y = 2 + c*S, 2 + r*S
        p = par[r][c]
        if p["N"] and not (r == 0 and c == 0):
            o.append(f'<line x1="{x}" y1="{y}" x2="{x+S}" y2="{y}"/>')
        if p["O"] and not (r == 0 and c == 0):
            o.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+S}"/>')
o.append(f'<line x1="2" y1="{2+H*S}" x2="{2+W*S}" y2="{2+H*S}"/>')
o.append(f'<line x1="{2+W*S}" y1="2" x2="{2+W*S}" y2="{2+H*S}"/>')
# entrada arriba-izquierda y salida abajo-derecha, abiertas al exterior
o.append(f'<line x1="2" y1="2" x2="{2+S}" y2="2" stroke="#fff" stroke-width="4"/>')
o.append(f'<line x1="{2+(W-1)*S}" y1="{2+H*S}" x2="{2+W*S}" y2="{2+H*S}" stroke="#fff" stroke-width="4"/>')

def marca(rc, texto, relleno):
    r, c = rc; cx, cy = 2 + c*S + S/2, 2 + r*S + S/2
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{S*0.40}" fill="{relleno}" stroke="#111" stroke-width="1.8"/>')
    col = "#fff" if relleno == "#111" else "#111"
    o.append(f'<text x="{cx}" y="{cy}" font-family="Montserrat,sans-serif" font-size="{S*0.52}" '
             f'font-weight="800" fill="{col}" stroke="none" text-anchor="middle" '
             f'dominant-baseline="central">{texto}</text>')
marca(ini, "E", "#111")
for i, l in enumerate(llaves, 1): marca(l, str(i), "#fff")
marca(fin, "S", "#111")
o.append("</svg>")
open("frag_laberinto.html", "w").write("\n".join(o))
json.dump({"seed": seed, "pasos": total}, open("laberinto.json", "w"))
print("svg listo:", len("\n".join(o)), "bytes |", W, "x", H, "celdas")
