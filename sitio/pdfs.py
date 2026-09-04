# -*- coding: utf-8 -*-
"""Genera un PDF por actividad en hojas/."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogo import ACTIVIDADES, APOYO, HOJAS, CSS, B

TMP = "/tmp/claude-1001/pdfind"
os.makedirs(TMP, exist_ok=True)
os.makedirs(B + "hojas", exist_ok=True)

def construir(a):
    secs = "\n".join(HOJAS[a["doc"]][i] for i in a["hojas"])
    doc = ('<!doctype html><html lang="es-MX"><head><meta charset="utf-8">'
           f'<title>{a["num"]} · {a["titulo"]}</title><style>{CSS[a["doc"]]}</style>'
           "</head><body>" + secs + "</body></html>")
    p = f"{TMP}/{a['archivo']}.html"
    open(p, "w").write(doc)
    return p

pend = []
for a in ACTIVIDADES + APOYO:
    src = construir(a)
    dst = f"{B}hojas/{a['archivo']}.pdf"
    pend.append((a, src, dst))

for a, src, dst in pend:
    subprocess.run(["timeout", "90", "google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--virtual-time-budget=12000",
                    f"--print-to-pdf={dst}", f"file://{src}"], capture_output=True)
    r = subprocess.run(["pdfinfo", dst], capture_output=True, text=True)
    pgs = [l for l in r.stdout.splitlines() if l.startswith("Pages")]
    tam = os.path.getsize(dst) // 1024 if os.path.exists(dst) else 0
    ok = "OK " if len(a["hojas"]) == int(pgs[0].split()[1]) else "REVISAR"
    print(f"  {ok} {a['archivo']:32} {pgs[0] if pgs else '-':14} {tam:5} KB")
print("\nPDFs individuales:", len(pend))
