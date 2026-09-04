# -*- coding: utf-8 -*-
"""Genera los fragmentos SVG/HTML que se insertan en el cuadernillo."""
import math, os
D = os.path.dirname(os.path.abspath(__file__))
def w(name, html): open(os.path.join(D, f"frag_{name}.html"), "w").write(html)

# ---------------------------------------------------------------- reloj 24 h
S, C = 520, 260
R_EXT, R_INT = 205, 74
o = [f'<svg viewBox="0 0 {S} {S}" style="width:100%;height:auto" fill="none" stroke="#111" stroke-width="1.6">']
def p(r, deg):
    a = math.radians(deg - 90)
    return C + r*math.cos(a), C + r*math.sin(a)
for i in range(24):
    d0, d1 = i*15, (i+1)*15
    x0,y0 = p(R_INT,d0); x1,y1 = p(R_EXT,d0); x2,y2 = p(R_EXT,d1); x3,y3 = p(R_INT,d1)
    o.append(f'<path d="M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f} A{R_EXT},{R_EXT} 0 0 1 {x2:.1f},{y2:.1f} '
             f'L{x3:.1f},{y3:.1f} A{R_INT},{R_INT} 0 0 0 {x0:.1f},{y0:.1f} Z" fill="#fff"/>')
    tx,ty = p(R_EXT+19, d0+7.5)
    o.append(f'<text x="{tx:.1f}" y="{ty:.1f}" font-family="Montserrat,sans-serif" font-size="15" font-weight="700" '
             f'fill="#5b6069" stroke="none" text-anchor="middle" dominant-baseline="central">{i}</text>')
o.append(f'<circle cx="{C}" cy="{C}" r="{R_INT}" fill="#fff" stroke="#111" stroke-width="2"/>')
o.append(f'<text x="{C}" y="{C-14}" font-family="Montserrat,sans-serif" font-size="30" font-weight="800" fill="#111" '
         f'stroke="none" text-anchor="middle">24 h</text>')
o.append(f'<text x="{C}" y="{C+12}" font-family="Roboto,sans-serif" font-size="14" fill="#6b7078" stroke="none" '
         f'text-anchor="middle">de un día</text>')
o.append(f'<text x="{C}" y="{C+34}" font-family="Roboto,sans-serif" font-size="13" fill="#6b7078" stroke="none" '
         f'text-anchor="middle">entre semana</text>')
o.append('</svg>')
w("reloj", "\n".join(o))

# ---------------------------------------------------------------- nonograma
GRID = ["....#######....","..###########..",".#############.",".#############.","###############",
        "##....###....##","##.##.###.##.##","##.##.###.##.##","##....###....##","###############",
        "###############","###############","###############","###.###.###.###","##..##...##..##"]
N = 15
g = [[1 if c=='#' else 0 for c in r] for r in GRID]
def clues(line):
    out, run = [], 0
    for c in line:
        if c: run += 1
        elif run: out.append(run); run = 0
    if run: out.append(run)
    return out or [0]
rows = [clues(r) for r in g]
cols = [clues([g[r][c] for r in range(N)]) for c in range(N)]
MAXR, MAXC = max(len(r) for r in rows), max(len(c) for c in cols)

def rejilla(sol=False, cls="nono"):
    t = [f'<table class="{cls}">',
         '<colgroup>' + '<col class="cp">'*MAXR + '<col class="cc">'*N + '</colgroup>']
    for k in range(MAXC):                      # cabeceras de columna
        t.append('<tr>')
        t.append(f'<td class="esq" colspan="{MAXR}"></td>' if k == 0 else '')
        for c in range(N):
            v = cols[c][k - (MAXC - len(cols[c]))] if k >= MAXC - len(cols[c]) else ''
            t.append(f'<td class="pc{" g5" if c%5==0 else ""}">{v}</td>')
        t.append('</tr>')
    for r in range(N):
        t.append(f'<tr class="{"g5" if r%5==0 else ""}">')
        for k in range(MAXR):
            v = rows[r][k - (MAXR - len(rows[r]))] if k >= MAXR - len(rows[r]) else ''
            t.append(f'<td class="pr">{v}</td>')
        for c in range(N):
            f = ' on' if (sol and g[r][c]) else ''
            t.append(f'<td class="cel{" g5" if c%5==0 else ""}{f}"></td>')
        t.append('</tr>')
    t.append('</table>')
    return "".join(t)
# la primera fila lleva el rowspan de la esquina
frag = rejilla().replace(f'<td class="esq" colspan="{MAXR}"></td>',
                         f'<td class="esq" colspan="{MAXR}" rowspan="{MAXC}"></td>', 1)
w("nonograma", frag)
w("nonograma_sol", rejilla(sol=True, cls="nono sol").replace(
    f'<td class="esq" colspan="{MAXR}"></td>', f'<td class="esq" colspan="{MAXR}" rowspan="{MAXC}"></td>', 1))

# mini ejemplo 5x5 resuelto (una flecha)
EJ = ["..#..",".###.","#####","..#..","..#.."]
ge = [[1 if c=='#' else 0 for c in r] for r in EJ]
re_ = [clues(r) for r in ge]; ce = [clues([ge[r][c] for r in range(5)]) for c in range(5)]
MR, MC = max(len(x) for x in re_), max(len(x) for x in ce)
t = ['<table class="nono mini sol">',
     '<colgroup>' + '<col class="cp">'*MR + '<col class="cc">'*5 + '</colgroup>']
for k in range(MC):
    t.append('<tr>')
    if k == 0: t.append(f'<td class="esq" colspan="{MR}" rowspan="{MC}"></td>')
    for c in range(5):
        v = ce[c][k-(MC-len(ce[c]))] if k >= MC-len(ce[c]) else ''
        t.append(f'<td class="pc">{v}</td>')
    t.append('</tr>')
for r in range(5):
    t.append('<tr>')
    for k in range(MR):
        v = re_[r][k-(MR-len(re_[r]))] if k >= MR-len(re_[r]) else ''
        t.append(f'<td class="pr">{v}</td>')
    for c in range(5):
        t.append(f'<td class="cel{" on" if ge[r][c] else ""}"></td>')
    t.append('</tr>')
t.append('</table>')
w("nonograma_mini", "".join(t))

print("piezas: reloj, nonograma, nonograma_sol, nonograma_mini")
