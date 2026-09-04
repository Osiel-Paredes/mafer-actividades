# -*- coding: utf-8 -*-
"""Piezas de la hoja de soluciones: bimaru resuelto y laberinto con el camino trazado."""
import json, random
from collections import deque

# ---------------- bimaru resuelto ----------------
b = json.load(open("bimaru.json"))
g, fil, col = b["grid"], b["fil"], b["col"]
N = len(g)
t = ['<table class="bim sol"><colgroup>' + "<col>"*(N+1) + "</colgroup>"]
t.append('<tr><td class="esq"></td>' + "".join(f'<td class="pc">{c}</td>' for c in col) + "</tr>")
for r in range(N):
    fila = [f'<td class="pr">{fil[r]}</td>']
    for c in range(N):
        fila.append(f'<td class="cel{" barco" if g[r][c] else " agua"}"></td>')
    t.append("<tr>" + "".join(fila) + "</tr>")
t.append("</table>")
open("frag_bimaru_sol.html", "w").write("".join(t))

# ---------------- laberinto con el camino ----------------
exec(open("laberinto.py").read().split("# elige una semilla")[0])
seed = json.load(open("laberinto.json"))["seed"]
par = generar(seed)
ini, fin = (0, 0), (H-1, W-1)
llaves = [(H//2, 3), (2, W//2 + 4), (H-3, W//2 - 6)]
tramos = [ini] + llaves + [fin]
camino = []
for i in range(len(tramos)-1):
    r = ruta(par, tramos[i], tramos[i+1])
    camino += r if i == 0 else r[1:]
S = 13
o = [f'<svg viewBox="0 0 {W*S+4} {H*S+4}" style="width:100%;height:auto" fill="none" '
     f'stroke="#111" stroke-width="1.5" stroke-linecap="square">']
o.append(f'<rect x="2" y="2" width="{W*S}" height="{H*S}" fill="#fff" stroke="none"/>')
pts = " ".join(f"{2+c*S+S/2:.1f},{2+r*S+S/2:.1f}" for r, c in camino)
o.append(f'<polyline points="{pts}" stroke="#1f4ea8" stroke-width="{S*0.42}" stroke-opacity=".30" '
         f'stroke-linejoin="round" stroke-linecap="round"/>')
for r in range(H):
    for c in range(W):
        x, y = 2 + c*S, 2 + r*S
        p = par[r][c]
        if p["N"] and not (r == 0 and c == 0): o.append(f'<line x1="{x}" y1="{y}" x2="{x+S}" y2="{y}"/>')
        if p["O"] and not (r == 0 and c == 0): o.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+S}"/>')
o.append(f'<line x1="2" y1="{2+H*S}" x2="{2+W*S}" y2="{2+H*S}"/>')
o.append(f'<line x1="{2+W*S}" y1="2" x2="{2+W*S}" y2="{2+H*S}"/>')
for rc, txt in [(ini, "E")] + [(l, str(i)) for i, l in enumerate(llaves, 1)] + [(fin, "S")]:
    r, c = rc; cx, cy = 2 + c*S + S/2, 2 + r*S + S/2
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{S*0.42}" fill="#fff" stroke="#111" stroke-width="1.4"/>')
    o.append(f'<text x="{cx}" y="{cy}" font-family="Montserrat,sans-serif" font-size="{S*0.5}" '
             f'font-weight="800" fill="#111" stroke="none" text-anchor="middle" dominant-baseline="central">{txt}</text>')
o.append("</svg>")
open("frag_laberinto_sol.html", "w").write("\n".join(o))
print("pasos del camino trazado:", len(camino)-1)
