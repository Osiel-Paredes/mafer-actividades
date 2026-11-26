# -*- coding: utf-8 -*-
"""Genera un PDF por actividad en hojas/."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogo import ACTIVIDADES, APOYO, HOJAS, CSS, B

import tempfile, pathlib, shutil
TMP = os.path.join(tempfile.gettempdir(), "pdfind")
os.makedirs(TMP, exist_ok=True)
CHROME = shutil.which("google-chrome") or shutil.which("chrome") or next(
    (p for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                 r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe") if os.path.exists(p)), None)
os.makedirs(B + "hojas", exist_ok=True)

def construir(a):
    secs = "\n".join(HOJAS[a["doc"]][i] for i in a["hojas"])
    doc = ('<!doctype html><html lang="es-MX"><head><meta charset="utf-8">'
           f'<title>{a["num"]} · {a["titulo"]}</title><style>{CSS[a["doc"]]}</style>'
           "</head><body>" + secs + "</body></html>")
    p = f"{TMP}/{a['archivo']}.html"
    open(p, "w", encoding="utf-8").write(doc)
    return p

pend = []
for a in ACTIVIDADES + APOYO:
    src = construir(a)
    dst = f"{B}hojas/{a['archivo']}.pdf"
    pend.append((a, src, dst))

for a, src, dst in pend:
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--virtual-time-budget=12000",
                    f"--print-to-pdf={dst}", pathlib.Path(src).as_uri()],
                   capture_output=True, timeout=90)
    r = subprocess.run(["pdfinfo", dst], capture_output=True, text=True, errors="replace")
    pgs = [l for l in r.stdout.splitlines() if l.startswith("Pages")]
    tam = os.path.getsize(dst) // 1024 if os.path.exists(dst) else 0
    ok = "OK " if pgs and len(a["hojas"]) == int(pgs[0].split()[1]) else "REVISAR"
    print(f"  {ok} {a['archivo']:32} {pgs[0] if pgs else '-':14} {tam:5} KB")
print("\nPDFs individuales:", len(pend))
