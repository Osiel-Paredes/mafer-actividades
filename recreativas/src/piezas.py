# -*- coding: utf-8 -*-
import json, os
D = os.path.dirname(os.path.abspath(__file__))
w = lambda n, h: open(os.path.join(D, f"frag_{n}.html"), "w").write(h)

# ---------------------------------------------------------------- BIMARU
b = json.load(open("bimaru.json"))
g, fil, col = b["grid"], b["fil"], b["col"]
dadas = {(r, c): v for r, c, v in b["dadas"]}
N = len(g)
t = ['<table class="bim"><colgroup>' + '<col>'*(N+1) + '</colgroup>']
t.append('<tr><td class="esq"></td>' + "".join(f'<td class="pc">{c}</td>' for c in col) + "</tr>")
for r in range(N):
    fila = [f'<td class="pr">{fil[r]}</td>']
    for c in range(N):
        v = dadas.get((r, c))
        cls = "cel" + (" barco" if v == 1 else " agua" if v == 0 else "")
        fila.append(f'<td class="{cls}"></td>')
    t.append("<tr>" + "".join(fila) + "</tr>")
t.append("</table>")
w("bimaru", "".join(t))

# flota que hay que encontrar, dibujada
f = ['<div class="flota">']
for etq, largo, cuantos in [("Uno de 3", 3, 1), ("Dos de 2", 2, 2), ("Tres de 1", 1, 3)]:
    f.append('<div class="gr"><span class="et">' + etq + "</span>")
    for _ in range(cuantos):
        f.append('<span class="barco-mini">' + '<i></i>'*largo + "</span>")
    f.append("</div>")
f.append("</div>")
w("flota", "".join(f))

# ---------------------------------------------------------------- SOPA
s = json.load(open("sopa.json"))
t = ['<table class="sopa">']
for fila in s["grid"]:
    t.append("<tr>" + "".join(f"<td>{ch}</td>" for ch in fila) + "</tr>")
t.append("</table>")
w("sopa", "".join(t))
pal = s["palabras"]
cols = [pal]
lst = ['<div class="listapal">']
for col_ in cols:
    lst.append("<ul>" + "".join(f'<li><span class="cb"></span>{p.capitalize()}</li>' for p in col_) + "</ul>")
lst.append("</div>")
w("palabras", "".join(lst))

# ---------------------------------------------------------------- CRIPTOGRAMA
k = json.load(open("cripto.json"))
def bloques(txt, por_linea=26):
    palabras, lineas, cur = txt.split(" "), [], []
    n = 0
    for p in palabras:
        if n + len(p) + 1 > por_linea and cur:
            lineas.append(cur); cur = []; n = 0
        cur.append(p); n += len(p) + 1
    if cur: lineas.append(cur)
    out = []
    for ln in lineas:
        out.append('<div class="crip-linea">')
        for p in ln:
            out.append('<span class="crip-pal">')
            for ch in p:
                dado = k["regalos"].get(ch, "")
                out.append(f'<span class="crip-ch"><b>{dado}</b><i>{ch}</i></span>')
            out.append("</span>")
        out.append("</div>")
    return "".join(out)
w("cripto", bloques(k["cifrada"], 24))
w("cripto_reto", bloques(k["reto_cifrado"], 24))

AB = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
inv = {v: kk for kk, v in k["regalos"].items()}
t = ['<table class="abc-trab">']
for mitad in (AB[:13], AB[13:]):
    t.append("<tr>" + "".join(f'<td class="l">{ch}</td>' for ch in mitad) + "</tr>")
    t.append("<tr>" + "".join(
        f'<td class="v">{k["regalos"].get(ch, "")}</td>' for ch in mitad) + "</tr>")
t.append("</table>")
w("abecedario", "".join(t))
t = ['<table class="frec">']
t.append("<tr>" + "".join(f"<th>{l}</th>" for l, _ in k["tabla"]) + "</tr>")
t.append("<tr>" + "".join(f"<td>{v}</td>" for _, v in k["tabla"]) + "</tr>")
t.append("</table>")
w("frecuencias", "".join(t))
print("piezas: bimaru, flota, sopa, palabras, cripto, cripto_reto, abecedario, frecuencias")
print("laberinto ya generado:", os.path.exists("frag_laberinto.html"))
