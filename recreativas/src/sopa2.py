# -*- coding: utf-8 -*-
import random, json, unicodedata
exec(open("sopa.py").read().split("# ¿que longitudes")[0])

MENSAJE = "EL QUE ACABE PRIMERO INVENTA UNA PALABRA QUE NO EXISTA PERO QUE SUENE REAL Y ESCRIBE SU DEFINICION"
letras = "".join(ch for ch in MENSAJE if ch.isalpha())
print("mensaje:", len(letras), "letras")

t = intentar(23, 17)
g, puestas, libres = t
assert len(libres) == len(letras), f"no calza: {len(libres)} libres vs {len(letras)} letras"
for (r, c), ch in zip(libres, letras): g[r][c] = ch

# comprobacion: leer las celdas que no son de ninguna palabra debe devolver el mensaje
ocupadas = set()
for p, r, c, dr, dc in puestas:
    for i in range(len(p)): ocupadas.add((r+dr*i, c+dc*i))
leido = "".join(g[r][c] for r in range(N) for c in range(N) if (r, c) not in ocupadas)
print("se lee de vuelta:", leido == letras, "|", leido[:52], "...")

filas = ["".join(g[r]) for r in range(N)]
for f in filas: print("  " + " ".join(f))
pal = sorted([p for p, *_ in puestas])
json.dump({"grid": filas, "palabras": pal, "mensaje": MENSAJE, "letras": len(letras)},
          open("sopa.json", "w"), ensure_ascii=False)
print("\npalabras:", len(pal), "->", ", ".join(pal))
