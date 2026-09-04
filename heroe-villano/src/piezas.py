# -*- coding: utf-8 -*-
"""Piezas graficas de la actividad heroe/villano."""
import os
D = os.path.dirname(os.path.abspath(__file__))
def w(n, h): open(os.path.join(D, f"frag_{n}.html"), "w").write(h)

# ---------------------------------------------- guia de proporciones (8 cabezas)
# Va de fondo en las zonas de dibujo: ayuda a quien no sabe dibujar sin condicionar el diseno.
W, H = 240, 640
MARCAS = [(0,"cabeza"),(1,"mentón"),(1.5,"hombros"),(3.2,"cintura"),(4,"mitad"),(6,"rodillas"),(8,"pies")]
o = [f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%">']
for k, nombre in MARCAS:
    y = H * k / 8
    y = max(y, 0.7)
    o.append(f'<line x1="8" y1="{y:.1f}" x2="{W-8}" y2="{y:.1f}" stroke="#dfe3e8" stroke-width="1.1" '
             f'stroke-dasharray="5 5"/>')

# eje central vertical
o.append(f'<line x1="{(W+26)/2:.0f}" y1="0" x2="{(W+26)/2:.0f}" y2="{H}" stroke="#eaedf1" stroke-width="1.1" stroke-dasharray="3 6"/>')
o.append('</svg>')
w("proporciones", "\n".join(o))

# ---------------------------------------------- guia de proporciones, version ancha (para el cartel)
o = ['<svg viewBox="0 0 300 450" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%">']
for i in range(1, 3):
    x = 300*i/3
    o.append(f'<line x1="{x}" y1="0" x2="{x}" y2="450" stroke="#eef0f3" stroke-width="1" stroke-dasharray="4 6"/>')
for i in range(1, 3):
    y = 450*i/3
    o.append(f'<line x1="0" y1="{y}" x2="300" y2="{y}" stroke="#eef0f3" stroke-width="1" stroke-dasharray="4 6"/>')
o.append('</svg>')
w("tercios", "\n".join(o))
print("piezas: proporciones, tercios")
