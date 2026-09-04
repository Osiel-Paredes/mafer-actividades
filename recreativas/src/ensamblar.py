# -*- coding: utf-8 -*-
"""Ensambla base.css + extra.css + cuerpo.html -> HTML final listo para imprimir."""
import re, os
D = os.path.dirname(os.path.abspath(__file__))
p = lambda *a: os.path.join(D, *a)

css = open(p("base.css")).read() + "\n" + open(p("extra.css")).read()
cuerpo = open(p("cuerpo.html")).read()

faltan = []
def sub(m):
    n = m.group(1); f = p(f"frag_{n}.html")
    if not os.path.exists(f): faltan.append(n); return f"<!-- FALTA {n} -->"
    return open(f).read()
cuerpo = re.sub(r"<!--INCLUDE:([a-z_0-9]+)-->", sub, cuerpo)

html = ('<!doctype html>\n<html lang="es-MX"><head><meta charset="utf-8">\n'
        '<title>Actividades recreativas - 3o de secundaria</title>\n'
        f'<style>{css}</style></head><body>\n{cuerpo}\n</body></html>')
out = p(".." , "..", "actividades-recreativas.html")
open(out, "w").write(html)
print("faltantes:", faltan or "ninguno")
print("hojas:", cuerpo.count('class="hoja'), "| bytes:", len(html))
