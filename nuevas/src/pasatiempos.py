# -*- coding: utf-8 -*-
"""Genera y VERIFICA los pasatiempos de 1o y 2o, y escribe los fragmentos HTML.

    python3 pasatiempos.py

Cada pasatiempo se comprueba con codigo antes de imprimirse: solucion unica y, en los
nonogramas y el bimaru, alcanzable por deduccion pura (sin adivinar).
"""
import json, os, random
from itertools import combinations

D = os.path.dirname(os.path.abspath(__file__))
frag = lambda n, h: open(os.path.join(D, f"frag_{n}.html"), "w").write(h)
SOL = {}

# ══════════════════════════════════════════════════════════ NONOGRAMAS
UNK, FILL, EMPTY = -1, 1, 0

def pistas(linea):
    out, run = [], 0
    for c in linea:
        if c == 1: run += 1
        elif run: out.append(run); run = 0
    if run: out.append(run)
    return out or [0]

def colocaciones(cl, largo, conocido):
    if cl == [0]:
        cand = [tuple([EMPTY] * largo)]
    else:
        k = len(cl); libre = largo - (sum(cl) + k - 1)
        if libre < 0: return []
        cand = []
        for huecos in combinations(range(libre + k), k):
            offs = [huecos[0]] + [huecos[i] - huecos[i-1] - 1 for i in range(1, k)]
            linea = []
            for i, blk in enumerate(cl):
                linea += [EMPTY] * offs[i] + [FILL] * blk
                if i < k - 1: linea += [EMPTY]
            linea += [EMPTY] * (largo - len(linea))
            if len(linea) == largo: cand.append(tuple(linea))
    return [c for c in cand if all(k == UNK or k == v for k, v in zip(conocido, c))]

def resolver(fil, col, n):
    """Solver por logica de lineas. Si deja todo resuelto, la solucion es unica y deducible."""
    tab = [[UNK] * n for _ in range(n)]
    for _ in range(300):
        cambio = False
        for i in range(n):
            ps = colocaciones(fil[i], n, tab[i])
            if not ps: return None
            for j in range(n):
                vals = {p[j] for p in ps}
                if len(vals) == 1 and tab[i][j] == UNK: tab[i][j] = vals.pop(); cambio = True
        for j in range(n):
            columna = [tab[i][j] for i in range(n)]
            ps = colocaciones(col[j], n, columna)
            if not ps: return None
            for i in range(n):
                vals = {p[i] for p in ps}
                if len(vals) == 1 and tab[i][j] == UNK: tab[i][j] = vals.pop(); cambio = True
        if not cambio: break
    return tab

def tabla_nono(fil, col, n, grupo, clase, sol=None):
    """HTML del nonograma. sol=None -> rejilla vacia; sol=matriz -> resuelto."""
    anchoP = max(len(x) for x in fil)      # columnas de pistas a la izquierda
    altoP = max(len(x) for x in col)       # renglones de pistas arriba
    t = [f'<table class="nono {clase}"><colgroup>' + '<col class="cp">' * anchoP
         + '<col class="cc">' * n + "</colgroup>"]
    for r in range(altoP):
        celdas = [f'<td class="esq" colspan="{anchoP}" rowspan="{altoP}"></td>'] if r == 0 else []
        for c in range(n):
            p = col[c]
            v = p[r - (altoP - len(p))] if r >= altoP - len(p) and p != [0] else ""
            g = " g" if c and c % grupo == 0 else ""
            celdas.append(f'<td class="pc{g}">{v}</td>')
        t.append("<tr>" + "".join(celdas) + "</tr>")
    for r in range(n):
        p = fil[r]
        celdas = []
        for k in range(anchoP):
            v = p[k - (anchoP - len(p))] if k >= anchoP - len(p) and p != [0] else ""
            celdas.append(f'<td class="pr">{v}</td>')
        for c in range(n):
            g = " g" if c and c % grupo == 0 else ""
            on = " on" if sol and sol[r][c] == 1 else ""
            celdas.append(f'<td class="{g.strip()}{on}"></td>' if not on else f'<td class="{(g+on).strip()}"></td>')
        cls = ' class="g"' if r and r % grupo == 0 else ""
        t.append(f"<tr{cls}>" + "".join(celdas) + "</tr>")
    t.append("</table>")
    return "".join(t)

def nonograma(nombre, dibujo, grupo, clase):
    n = len(dibujo)
    assert all(len(f) == n for f in dibujo), f"{nombre}: no es cuadrado"
    g = [[1 if ch == "#" else 0 for ch in f] for f in dibujo]
    fil = [pistas(f) for f in g]
    col = [pistas([g[r][c] for r in range(n)]) for c in range(n)]
    b = resolver(fil, col, n)
    amb = sum(1 for f in (b or []) for c in f if c == UNK)
    ok = b is not None and amb == 0 and b == g
    print(f"  nonograma {nombre:8} {n}x{n}: deducible={ok} ambiguas={amb} "
          f"pistas max fila={max(len(x) for x in fil)} col={max(len(x) for x in col)}")
    assert ok, f"{nombre}: no se resuelve por logica pura"
    SOL[nombre] = dibujo
    frag(nombre, tabla_nono(fil, col, n, grupo, clase))
    frag(nombre + "_sol", tabla_nono(fil, col, n, grupo, "chica", g))
    return fil, col

CARITA = [                      # 1o: una carita, se resuelve por logica pura
    "...####...",
    ".########.",
    "##########",
    "##.####.##",
    "##.####.##",
    "##########",
    "#.######.#",
    "##.####.##",
    ".########.",
    "...####...",
]
PARAGUAS = [                    # 2o: un paraguas, con un renglon de 6 pistas
    "....####....",
    "..########..",
    ".##########.",
    "###########.",
    "#.#.#.#.#.#.",
    ".....##.....",
    ".....##.....",
    ".....##.....",
    ".....##.....",
    "....###.....",
    "...##.##....",
    "....###.....",
]


# ══════════════════════════════════════════════════════════ BIMARU
def bimaru(nombre, N, FLOTA, clase, semillas=4000, max_dadas=4, regalar=0):
    from itertools import product
    def vecinos(r, c):
        for dr, dc in product((-1, 0, 1), repeat=2):
            if (dr or dc) and 0 <= r+dr < N and 0 <= c+dc < N: yield r+dr, c+dc
    POS = {}
    for largo in set(FLOTA):
        lst = []
        for r in range(N):
            for c in range(N):
                for hor in (True, False):
                    if largo == 1 and not hor: continue
                    cel = [(r, c+i) if hor else (r+i, c) for i in range(largo)]
                    if any(x >= N or y >= N for x, y in cel): continue
                    som = {v for x, y in cel for v in vecinos(x, y)} - set(cel)
                    lst.append((tuple(cel), frozenset(som)))
        POS[largo] = lst

    def generar(seed):
        rnd = random.Random(seed)
        ocup, som = set(), set()
        for largo in FLOTA:
            opts = [p for p in POS[largo] if not (set(p[0]) & (ocup | som))]
            if not opts: return None
            cel, sm = rnd.choice(opts)
            ocup |= set(cel); som |= sm
        g = [[0]*N for _ in range(N)]
        for r, c in ocup: g[r][c] = 1
        return g

    def contar(fil, col, dadas, tope=2):
        sols = []
        fijo_b = {k for k, v in dadas.items() if v == 1}
        fijo_a = {k for k, v in dadas.items() if v == 0}
        def rec(i, ocup, som, desde):
            if len(sols) >= tope: return
            rf = [fil[r] - sum(1 for c in range(N) if (r, c) in ocup) for r in range(N)]
            rc = [col[c] - sum(1 for r in range(N) if (r, c) in ocup) for c in range(N)]
            if any(x < 0 for x in rf + rc): return
            faltan = sum(FLOTA[i:])
            if sum(rf) != faltan or sum(rc) != faltan: return
            if i == len(FLOTA):
                if fijo_b <= ocup and not (fijo_a & ocup): sols.append(set(ocup))
                return
            largo = FLOTA[i]
            ini = desde if (i > 0 and FLOTA[i-1] == largo) else 0
            for k in range(ini, len(POS[largo])):
                cel, sm = POS[largo][k]
                cs = set(cel)
                if cs & (ocup | som) or cs & fijo_a: continue
                if any(fil[r] - sum(1 for c in range(N) if (r, c) in ocup) < 1 for r, c in cel): continue
                rec(i+1, ocup | cs, som | sm, k+1)
                if len(sols) >= tope: return
        rec(0, set(), set(), 0)
        return sols

    elegido = None
    for seed in range(semillas):
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
        if elegido and len(elegido[4]) <= max_dadas: break
        elegido = None
    assert elegido, f"{nombre}: no encontré tablero con solución única"
    seed, g, fil, col, dadas = elegido
    if regalar:                     # celdas de regalo para la version facil
        n0 = len(dadas)
        rnd = random.Random(seed * 97 + 3)
        libres = [(r, c) for r in range(N) for c in range(N) if (r, c) not in dadas]
        barcos = [x for x in libres if g[x[0]][x[1]] == 1]
        rnd.shuffle(barcos); rnd.shuffle(libres)
        for x in barcos[:max(1, regalar // 2)] + libres:
            if len(dadas) >= regalar + n0: break
            dadas[x] = g[x[0]][x[1]]
    n_sol = len(contar(fil, col, dadas, tope=3))
    print(f"  bimaru {nombre:9} {N}x{N} flota={FLOTA} seed={seed} reveladas={len(dadas)} soluciones={n_sol}")
    assert n_sol == 1

    def tabla(sol):
        t = [f'<table class="bim {clase}"><colgroup>' + "<col>" * (N+1) + "</colgroup>"]
        t.append('<tr><td class="esq"></td>' + "".join(f'<td class="pc">{c}</td>' for c in col) + "</tr>")
        for r in range(N):
            f = [f'<td class="pr">{fil[r]}</td>']
            for c in range(N):
                if sol: cls = "cel barco" if g[r][c] else "cel agua"
                else:
                    v = dadas.get((r, c))
                    cls = "cel" + (" barco" if v == 1 else " agua" if v == 0 else "")
                f.append(f'<td class="{cls}"></td>')
            t.append("<tr>" + "".join(f) + "</tr>")
        t.append("</table>")
        return "".join(t)
    frag(nombre, tabla(False))
    frag(nombre + "_sol", tabla(True))
    SOL[nombre] = ["".join("#" if x else "." for x in f) for f in g]
    # dibujo de la flota que hay que encontrar
    from collections import Counter
    cuenta = Counter(FLOTA)
    f = ['<div class="flota">']
    for largo in sorted(cuenta, reverse=True):
        n = cuenta[largo]
        et = f"{'Uno' if n == 1 else 'Dos' if n == 2 else 'Tres' if n == 3 else n} de {largo}"
        f.append(f'<div class="gr"><span class="et">{et}</span>')
        for _ in range(n): f.append('<span class="barco-mini">' + "<i></i>" * largo + "</span>")
        f.append("</div>")
    f.append("</div>")
    frag(nombre + "_flota", "".join(f))


# ══════════════════════════════════════════════════════════ LABERINTOS
DIRS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}
OPUE = {"N": "S", "S": "N", "E": "O", "O": "E"}

def maze(seed, W, H):
    """Laberinto perfecto por DFS: entre dos celdas hay exactamente un camino."""
    rnd = random.Random(seed)
    vis = [[False]*W for _ in range(H)]
    par = [[{"N": True, "E": True, "S": True, "O": True} for _ in range(W)] for _ in range(H)]
    pila = [(0, 0)]; vis[0][0] = True
    while pila:
        r, c = pila[-1]
        opts = [d for d, (dr, dc) in DIRS.items()
                if 0 <= r+dr < H and 0 <= c+dc < W and not vis[r+dr][c+dc]]
        if not opts: pila.pop(); continue
        d = rnd.choice(opts); dr, dc = DIRS[d]
        par[r][c][d] = False; par[r+dr][c+dc][OPUE[d]] = False
        vis[r+dr][c+dc] = True; pila.append((r+dr, c+dc))
    return par

def vecinos_abiertos(par, W, H, r, c):
    for d, (dr, dc) in DIRS.items():
        if not par[r][c][d] and 0 <= r+dr < H and 0 <= c+dc < W:
            yield r+dr, c+dc

def ruta(par, W, H, a, b):
    from collections import deque
    prev = {a: None}; q = deque([a])
    while q:
        cur = q.popleft()
        if cur == b: break
        for n in vecinos_abiertos(par, W, H, *cur):
            if n not in prev: prev[n] = cur; q.append(n)
    cam, cur = [], b
    while cur is not None: cam.append(cur); cur = prev[cur]
    return cam[::-1]

def svg_maze(par, W, H, S, marcas, tolls=None, extra_clase=""):
    o = [f'<svg viewBox="0 0 {W*S+4} {H*S+4}" style="width:100%;height:auto" class="{extra_clase}" '
         f'fill="none" stroke="#111" stroke-width="2.4" stroke-linecap="square">']
    o.append(f'<rect x="2" y="2" width="{W*S}" height="{H*S}" fill="#fff" stroke="none"/>')
    for r in range(H):
        for c in range(W):
            x, y = 2 + c*S, 2 + r*S
            p = par[r][c]
            if p["N"] and not (r == 0 and c == 0): o.append(f'<line x1="{x}" y1="{y}" x2="{x+S}" y2="{y}"/>')
            if p["O"] and not (r == 0 and c == 0): o.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+S}"/>')
    o.append(f'<line x1="2" y1="{2+H*S}" x2="{2+W*S}" y2="{2+H*S}"/>')
    o.append(f'<line x1="{2+W*S}" y1="2" x2="{2+W*S}" y2="{2+H*S}"/>')
    o.append(f'<line x1="2" y1="2" x2="{2+S}" y2="2" stroke="#fff" stroke-width="4"/>')
    o.append(f'<line x1="{2+(W-1)*S}" y1="{2+H*S}" x2="{2+W*S}" y2="{2+H*S}" stroke="#fff" stroke-width="4"/>')
    if tolls:
        for (r, c), v in tolls.items():
            cx, cy = 2 + c*S + S/2, 2 + r*S + S/2
            o.append(f'<text x="{cx}" y="{cy}" font-family="Montserrat,sans-serif" font-size="{S*0.42:.1f}" '
                     f'font-weight="700" fill="#4a4f57" stroke="none" text-anchor="middle" '
                     f'dominant-baseline="central">{v}</text>')
    for (r, c), (texto, relleno) in marcas.items():
        cx, cy = 2 + c*S + S/2, 2 + r*S + S/2
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{S*0.40:.1f}" fill="{relleno}" stroke="#111" stroke-width="1.8"/>')
        col = "#fff" if relleno == "#111" else "#111"
        o.append(f'<text x="{cx}" y="{cy}" font-family="Montserrat,sans-serif" font-size="{S*0.52:.1f}" '
                 f'font-weight="800" fill="{col}" stroke="none" text-anchor="middle" '
                 f'dominant-baseline="central">{texto}</text>')
    o.append("</svg>")
    return "\n".join(o)

def laberinto_llaves(nombre, W, H, S, pos_llaves, objetivo=200, semillas=400):
    """Laberinto con llaves que hay que recoger en orden. Escoge la semilla de recorrido mas largo."""
    mejor = None
    ini, fin = (0, 0), (H-1, W-1)
    for seed in range(semillas):
        par = maze(seed, W, H)
        tramos = [ini] + pos_llaves + [fin]
        total = sum(len(ruta(par, W, H, tramos[i], tramos[i+1])) - 1 for i in range(len(tramos)-1))
        if mejor is None or abs(total - objetivo) < abs(mejor[0] - objetivo): mejor = (total, seed, par)
    total, seed, par = mejor
    directo = len(ruta(par, W, H, ini, fin)) - 1
    print(f"  laberinto {nombre:9} {W}x{H} seed={seed} llaves={len(pos_llaves)} "
          f"recorrido mínimo={total} pasos (sin llaves serían {directo})")
    marcas = {ini: ("E", "#111"), fin: ("S", "#111")}
    for i, l in enumerate(pos_llaves, 1): marcas[l] = (str(i), "#fff")
    frag(nombre, svg_maze(par, W, H, S, marcas))
    cam = []
    tramos = [ini] + pos_llaves + [fin]
    for i in range(len(tramos)-1):
        t = ruta(par, W, H, tramos[i], tramos[i+1])
        cam += t if not cam else t[1:]
    o = [svg_maze(par, W, H, S, marcas)]
    pts = " ".join(f"{2+c*S+S/2:.0f},{2+r*S+S/2:.0f}" for r, c in cam)
    o[0] = o[0].replace("</svg>", f'<polyline points="{pts}" fill="none" stroke="#111" '
                                  f'stroke-width="{S*0.22:.1f}" stroke-opacity=".35" stroke-linejoin="round"/></svg>')
    frag(nombre + "_sol", o[0])
    SOL[nombre] = {"pasos": total, "seed": seed}

def laberinto_peaje(nombre, W, H, S, semillas=3000):
    """Laberinto con ciclos y un peaje por celda: el camino mas barato es unico y NO es el mas corto."""
    import heapq
    ini, fin = (0, 0), (H-1, W-1)
    for seed in range(semillas):
        rnd = random.Random(seed)
        par = maze(seed, W, H)
        # abrimos paredes extra para que haya varios caminos posibles
        for r in range(H):
            for c in range(W):
                for d, (dr, dc) in DIRS.items():
                    if par[r][c][d] and 0 <= r+dr < H and 0 <= c+dc < W and rnd.random() < .16:
                        par[r][c][d] = False; par[r+dr][c+dc][OPUE[d]] = False
        peaje = {(r, c): rnd.randint(1, 9) for r in range(H) for c in range(W)}
        peaje[ini] = 0
        # dijkstra contando caminos minimos
        INF = float("inf")
        dist = {ini: 0}; cuantos = {ini: 1}; pq = [(0, ini)]; hecho = set()
        while pq:
            d0, u = heapq.heappop(pq)
            if u in hecho: continue
            hecho.add(u)
            for v in vecinos_abiertos(par, W, H, *u):
                nd = d0 + peaje[v]
                if nd < dist.get(v, INF):
                    dist[v] = nd; cuantos[v] = cuantos[u]; heapq.heappush(pq, (nd, v))
                elif nd == dist.get(v, INF) and v not in hecho:
                    cuantos[v] = cuantos.get(v, 0) + cuantos[u]
        if fin not in dist or cuantos.get(fin, 0) != 1: continue
        # el camino mas corto en pasos y lo que cuesta
        corto = ruta(par, W, H, ini, fin)
        costo_corto = sum(peaje[x] for x in corto[1:])
        # reconstruimos el mas barato
        barato, cur = [fin], fin
        while cur != ini:
            for v in vecinos_abiertos(par, W, H, *cur):
                if dist.get(v, INF) + peaje[cur] == dist[cur]: barato.append(v); cur = v; break
            else: break
        barato = barato[::-1]
        if barato[0] != ini: continue
        if not (dist[fin] < costo_corto - 6 and len(barato) > len(corto) + 2): continue
        print(f"  laberinto {nombre:9} {W}x{H} seed={seed} más barato={dist[fin]} pesos en {len(barato)-1} pasos "
              f"| el más corto son {len(corto)-1} pasos y cuesta {costo_corto} (caminos mínimos: {cuantos[fin]})")
        marcas = {ini: ("E", "#111"), fin: ("S", "#111")}
        frag(nombre, svg_maze(par, W, H, S, marcas, tolls={k: v for k, v in peaje.items() if k not in marcas}))
        base = svg_maze(par, W, H, S, marcas, tolls={k: v for k, v in peaje.items() if k not in marcas})
        pts = " ".join(f"{2+c*S+S/2:.0f},{2+r*S+S/2:.0f}" for r, c in barato)
        frag(nombre + "_sol", base.replace("</svg>", f'<polyline points="{pts}" fill="none" stroke="#111" '
             f'stroke-width="{S*0.20:.1f}" stroke-opacity=".35" stroke-linejoin="round"/></svg>'))
        SOL[nombre] = {"barato": dist[fin], "pasos_barato": len(barato)-1,
                       "pasos_corto": len(corto)-1, "costo_corto": costo_corto}
        return
    raise SystemExit(f"{nombre}: no encontré laberinto que cumpla")

# ══════════════════════════════════════════════════════════ SOPA DE LETRAS
DIRS8 = [(0,1),(1,0),(1,1),(-1,1),(0,-1),(-1,0),(-1,-1),(1,-1)]

def _sopa_intento(seed, N, pals):
    rnd = random.Random(seed)
    g = [[None]*N for _ in range(N)]
    puestas = []
    for pal in sorted(pals, key=len, reverse=True):
        opts = []
        for r in range(N):
            for c in range(N):
                for dr, dc in DIRS8:
                    fr, fc = r + dr*(len(pal)-1), c + dc*(len(pal)-1)
                    if not (0 <= fr < N and 0 <= fc < N): continue
                    if all(g[r+dr*i][c+dc*i] in (None, ch) for i, ch in enumerate(pal)):
                        opts.append((r, c, dr, dc))
        if not opts: return None
        r, c, dr, dc = rnd.choice(opts)
        for i, ch in enumerate(pal): g[r+dr*i][c+dc*i] = ch
        puestas.append((pal, r, c, dr, dc))
    libres = [(r, c) for r in range(N) for c in range(N) if g[r][c] is None]
    return g, puestas, libres

def sopa(nombre, N, palabras, mensaje, clase, semillas=900):
    letras = "".join(ch for ch in mensaje.upper() if ch.isalpha())
    L = len(letras)
    hallado, cercanos = None, set()
    for cuantas in range(len(palabras), 7, -1):
        for seed in range(semillas):
            t = _sopa_intento(seed, N, palabras[:cuantas])
            if not t: continue
            if len(t[2]) == L: hallado = (seed, cuantas, t); break
            if abs(len(t[2]) - L) <= 8: cercanos.add(len(t[2]))
        if hallado: break
    if not hallado:
        raise SystemExit(f"{nombre}: el mensaje tiene {L} letras y no calza. Huecos posibles cerca: "
                         f"{sorted(cercanos)}")
    seed, cuantas, (g, puestas, libres) = hallado
    for (r, c), ch in zip(libres, letras): g[r][c] = ch
    ocup = set()
    for pal, r, c, dr, dc in puestas:
        for i in range(len(pal)): ocup.add((r+dr*i, c+dc*i))
    leido = "".join(g[r][c] for r in range(N) for c in range(N) if (r, c) not in ocup)
    print(f"  sopa {nombre:11} {N}x{N} palabras={cuantas} seed={seed} huecos={L} "
          f"se lee de vuelta={leido == letras}")
    assert leido == letras
    filas = ["".join(g[r]) for r in range(N)]
    frag(nombre, f'<table class="sopa {clase}">' +
         "".join("<tr>" + "".join(f"<td>{ch}</td>" for ch in f) + "</tr>" for f in filas) + "</table>")
    pal = sorted(p for p, *_ in puestas)
    mitad = (len(pal) + 1) // 2
    cols = [pal[:mitad], pal[mitad:]]
    frag(nombre + "_lista", '<div class="listapal">' + "".join(
        "<ul>" + "".join(f'<li><span class="cb"></span>{x}</li>' for x in col) + "</ul>" for col in cols) + "</div>")
    frag(nombre + "_sol", f'<table class="sopa {clase} chica">' + "".join(
        "<tr>" + "".join(f'<td{" style=\"background:#e3e5e9\"" if (r,c) in ocup else ""}>{g[r][c]}</td>'
                          for c in range(N)) + "</tr>" for r in range(N)) + "</table>")
    SOL[nombre] = {"mensaje": mensaje, "palabras": pal, "filas": filas}

# ══════════════════════════════════════════════════════════ CLAVES
AB = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def cajas_cifradas(texto_claro, mapa, regalos=(), grande=True):
    """Renglones de casillas vacias con la letra cifrada debajo; los regalos vienen puestos."""
    o = ['<div class="crip-linea' + (" g" if grande else "") + '">']
    for palabra in texto_claro.split():
        o.append('<div class="crip-pal">')
        for ch in palabra:
            cif = mapa[ch]
            dado = ch if ch in regalos else ""
            o.append(f'<div class="crip-ch"><b>{dado}</b><i>{cif}</i></div>')
        o.append("</div>")
    o.append("</div>")
    return "".join(o)

def cripto_cesar(nombre, frase, reto, desp):
    mapa = {a: AB[(AB.index(a) + desp) % 26] for a in AB}
    inv = {v: k for k, v in mapa.items()}
    cif = "".join(mapa.get(ch, ch) for ch in frase)
    assert "".join(inv.get(ch, ch) for ch in cif) == frase
    print(f"  clave {nombre:11} corrimiento=+{desp} | «{frase}» -> «{cif}»")
    frag(nombre, cajas_cifradas(frase, mapa, regalos=("E", "L")))
    frag(nombre + "_reto", cajas_cifradas(reto, mapa))
    fila1 = "".join(f'<td class="l">{a}</td>' for a in AB)
    frag(nombre + "_abc", '<table class="abc-trab alta"><tr>' + fila1 + "</tr><tr>" +
         '<td class="v"></td>' * 26 + "</tr></table>")
    SOL[nombre] = {"frase": frase, "reto": reto, "corrimiento": desp, "cifrada": cif}

def cripto_sust(nombre, frase, reto, n_regalos, seed=2026):
    rnd = random.Random(seed)
    for _ in range(9000):
        perm = list(AB); rnd.shuffle(perm)
        m = dict(zip(AB, perm))
        if all(m[a] != a for a in AB): break
    from collections import Counter
    frec = Counter(ch for ch in frase if ch.isalpha())
    regalos = [x for x, _ in frec.most_common()][:n_regalos]
    inv = {v: k for k, v in m.items()}
    cif = "".join(m.get(ch, ch) for ch in frase)
    assert "".join(inv.get(ch, ch) for ch in cif) == frase
    print(f"  clave {nombre:11} sustitución | regalos={regalos} | distintas={len(frec)} | «{cif[:34]}…»")
    frag(nombre, cajas_cifradas(frase, m, regalos=tuple(regalos)))
    frag(nombre + "_reto", cajas_cifradas(reto, m))
    usadas = sorted({m[ch] for ch in frase if ch.isalpha()})
    frag(nombre + "_conteo",
         '<table class="abc-trab alta"><tr>'
         + "".join(f'<td class="l">{x}</td>' for x in usadas) + "</tr><tr>"
         + '<td></td>' * len(usadas) + "</tr><tr>"
         + '<td class="v"></td>' * len(usadas) + "</tr></table>")
    SOL[nombre] = {"frase": frase, "reto": reto, "clave": {m[k]: k for k in AB}, "regalos": regalos}

ANIMALES = ["ARMADILLO", "MURCIELAGO", "CENZONTLE", "LAGARTIJA", "ZOPILOTE", "MAPACHE",
            "AJOLOTE", "TORTUGA", "COLIBRI", "COYOTE", "IGUANA", "JAGUAR", "VENADO",
            "LECHUZA", "TEJON", "GARZA"]
FISICA = ["VELOCIDAD", "ELECTRICO", "CORRIENTE", "FRICCION", "PALANCA", "RESORTE", "INERCIA",
          "ENERGIA", "VOLTAJE", "CIRCUITO", "FUERZA", "POLEA", "CALOR", "MASA", "ONDA", "IMAN"]

# ══════════════════════════════════════════════════════════ MAIN
if __name__ == "__main__":
    print("NONOGRAMAS")
    nonograma("nono10", CARITA, 5, "n10")
    nonograma("nono12", PARAGUAS, 4, "n12")
    print("BIMARUS")
    bimaru("bim6", 6, [3, 2, 2, 1, 1], "b6", regalar=4)
    bimaru("bim7", 7, [3, 3, 2, 2, 1, 1], "b7", regalar=2)
    print("LABERINTOS")
    laberinto_llaves("lab1", 19, 13, 24, [(6, 3), (2, 13)], objetivo=200)
    laberinto_peaje("lab2", 13, 9, 34)
    print("SOPAS")
    sopa("sopa12", 12, ANIMALES, "EL QUE ACABE ANTES DIBUJA AL REVERSO EL ANIMAL QUE NO CONOZCA", "s12")
    sopa("sopa13", 13, FISICA, "EL QUE ACABE ANTES ESCOGE UNA PALABRA DE LA LISTA Y ESCRIBE AL REVERSO DONDE LA VIO HOY", "s13")
    print("CLAVES")
    cripto_cesar("ces1", "EL COLIBRI PUEDE VOLAR HACIA ATRAS", "TAMBIEN LATE MIL VECES POR MINUTO", 7)
    cripto_sust("sus2", "LA LUZ DEL SOL TARDA OCHO MINUTOS EN LLEGAR A LA TIERRA", "Y LA DE LA LUNA SOLO UN SEGUNDO", 6)
    json.dump(SOL, open(os.path.join(D, "soluciones.json"), "w"), ensure_ascii=False, indent=1)
    print("\nsoluciones.json:", list(SOL))
