# -*- coding: utf-8 -*-
"""Genera index.html: sitio estatico autocontenido con las 20 actividades."""
import os, sys, json, re
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from catalogo import ACTIVIDADES, APOYO, HOJAS, CSS, B

def namespace(css, ns):
    fuera, i = [], 0
    def pre(sel):
        out = []
        for s in sel.split(","):
            s = s.strip()
            if not s: continue
            if s in ("html", ":root", "body"): out.append(f".{ns}")
            elif s == "*": out.append(f".{ns}, .{ns} *")
            else: out.append(f".{ns} {s}")
        return ", ".join(out)
    while i < len(css):
        if css[i] == "@":
            j = css.index("{", i); regla = css[i:j].strip()
            prof, k = 0, j
            while k < len(css):
                if css[k] == "{": prof += 1
                elif css[k] == "}":
                    prof -= 1
                    if prof == 0: break
                k += 1
            cuerpo = css[j+1:k]
            fuera.append(css[i:k+1] if regla.startswith("@page") else regla + "{" + namespace(cuerpo, ns) + "}")
            i = k + 1
        else:
            j = css.find("{", i)
            if j < 0: break
            k = css.find("}", j)
            sel, cu = css[i:j].strip(), css[j+1:k]
            if sel: fuera.append(pre(sel) + "{" + cu + "}")
            i = k + 1
    return "\n".join(fuera)

NS = {"cuad": "doc-a", "hv": "doc-b", "rec": "doc-c", "nuevas": "doc-d"}
GRADOS = {1: "1º de secundaria", 2: "2º de secundaria", 3: "3º de secundaria"}
GRUPOS = {"g-pasa": ["pasatiempo"], "g-dib": ["dibujo", "diseño", "arte"], "g-esc": ["escritura", "crítico"]}

def js(a):
    return dict(id=a["id"], etiqueta=a["num"], titulo=a["titulo"], sub=a["sub"], min=a["min"],
                materias=a["materias"], tipo=a["tipo"], archivo=a["archivo"], grado=a["grado"],
                hojas=[f'{a["doc"]}{i}' for i in a["hojas"]],
                rotulos=(["Guía · 1 de 2", "Guía · 2 de 2"] if a["id"] == "g-cuad" else None))

usados = set()
for a in ACTIVIDADES + APOYO:
    for i in a["hojas"]: usados.add((a["doc"], i))
papeles = ['<div id="papeles" hidden aria-hidden="true">']
for doc, i in sorted(usados):
    papeles.append(f'<div class="papel {NS[doc]}" id="h-{doc}{i}" data-off="1">{HOJAS[doc][i]}</div>')
papeles.append("</div>")

datos = ("const ACTIVIDADES=" + json.dumps([js(a) for a in ACTIVIDADES], ensure_ascii=False) +
         ";\nconst APOYO=" + json.dumps([js(a) for a in APOYO], ensure_ascii=False) +
         ";\nconst TODAS=ACTIVIDADES.concat(APOYO);" +
         "\nconst GRADOS=" + json.dumps(GRADOS, ensure_ascii=False) +
         ";\nconst GRUPOS=" + json.dumps(GRUPOS, ensure_ascii=False) + ";")

hojas_css = "\n".join(f"/* ===== {k} ===== */\n" + namespace(v, NS[k]) for k, v in CSS.items())

doc = f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>El cajón de Mafer</title>
<meta name="description" content="Cincuenta actividades individuales e imprimibles para secundaria, divididas por grado (1º, 2º y 3º). Sin celular, sin equipos, sin material extra.">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🗂️</text></svg>">
<style>[hidden]{{display:none!important}} img{{max-width:100%}}</style>
{open(os.path.join(D, "ui.html")).read()}
<style>
{hojas_css}
@media print{{
  .pila .papel .hoja{{page-break-after:auto!important;break-after:auto!important}}
  .pila .marco:not(:last-child) .papel{{page-break-after:always;break-after:page}}
}}
</style>
</head>
<body>
{open(os.path.join(D, "cuerpo-ui.html")).read()}
{chr(10).join(papeles)}
<script>
{datos}
{open(os.path.join(D, "logica.js")).read()}
</script>
</body>
</html>"""
open(B + "index.html", "w").write(doc)
print("index.html:", len(doc), "bytes |", len(ACTIVIDADES), "actividades,", len(APOYO), "de apoyo,", len(usados), "hojas embebidas")
