from itertools import combinations

# Fantasma pixel-art 15x15 (1 = celda pintada)
GRID = [
    "....#######....",
    "..###########..",
    ".#############.",
    ".#############.",
    "###############",
    "##....###....##",
    "##.##.###.##.##",
    "##.##.###.##.##",
    "##....###....##",
    "###############",
    "###############",
    "###############",
    "###############",
    "###.###.###.###",
    "##..##...##..##",
]
N = 15
g = [[1 if c == '#' else 0 for c in row] for row in GRID]
assert all(len(r) == N for r in g) and len(g) == N

def clues(line):
    out, run = [], 0
    for c in line:
        if c == 1: run += 1
        elif run: out.append(run); run = 0
    if run: out.append(run)
    return out or [0]

rows = [clues(r) for r in g]
cols = [clues([g[r][c] for r in range(N)]) for c in range(N)]

# ---- solver por lógica de líneas: si resuelve todo, la solución es única y deducible ----
UNK, FILL, EMPTY = -1, 1, 0

def placements(cl, length, known):
    if cl == [0]:
        cand = [tuple([EMPTY]*length)]
    else:
        k = len(cl)
        free = length - (sum(cl) + k - 1)
        if free < 0: return []
        cand = []
        for gaps in combinations(range(free + k), k):
            line, pos, prev = [], 0, 0
            offs = [gaps[0]] + [gaps[i] - gaps[i-1] - 1 for i in range(1, k)]
            line = []
            for i, blk in enumerate(cl):
                line += [EMPTY]*offs[i] + [FILL]*blk
                if i < k-1: line += [EMPTY]
            line += [EMPTY]*(length - len(line))
            if len(line) == length: cand.append(tuple(line))
    return [c for c in cand if all(k == UNK or k == v for k, v in zip(known, c))]

def solve(rows, cols, n):
    board = [[UNK]*n for _ in range(n)]
    for _ in range(200):
        changed = False
        for i in range(n):
            ps = placements(rows[i], n, board[i])
            if not ps: return None
            for j in range(n):
                vals = {p[j] for p in ps}
                if len(vals) == 1 and board[i][j] == UNK:
                    board[i][j] = vals.pop(); changed = True
        for j in range(n):
            col = [board[i][j] for i in range(n)]
            ps = placements(cols[j], n, col)
            if not ps: return None
            for i in range(n):
                vals = {p[i] for p in ps}
                if len(vals) == 1 and board[i][j] == UNK:
                    board[i][j] = vals.pop(); changed = True
        if not changed: break
    return board

b = solve(rows, cols, N)
unknown = sum(1 for r in b for c in r if c == UNK) if b else -1
print("resuelto por logica pura:", b is not None and unknown == 0, "| celdas ambiguas:", unknown)
print("coincide con el dibujo :", b == g)
print("max pistas por fila:", max(len(r) for r in rows), "| por columna:", max(len(c) for c in cols))
print("ROWS =", rows)
print("COLS =", cols)
