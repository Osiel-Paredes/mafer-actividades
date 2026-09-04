import re, os
D = os.path.dirname(os.path.abspath(__file__))
html = open(os.path.join(D,"cuadernillo.html")).read()
faltan = []
def sub(m):
    n = m.group(1); p = os.path.join(D, f"frag_{n}.html")
    if not os.path.exists(p): faltan.append(n); return f"<!-- FALTA {n} -->"
    return open(p).read()
out = re.sub(r"<!--INCLUDE:([a-z_0-9]+)-->", sub, html)
usados = re.findall(r"<!--INCLUDE:([a-z_0-9]+)-->", html)
open(os.path.join(D,"..","cuadernillo-actividades.html"),"w").write(out)
print("marcadores sustituidos:", len(usados), "->", usados)
print("faltantes:", faltan or "ninguno")
print("bytes finales:", len(out))
