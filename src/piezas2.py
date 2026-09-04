# -*- coding: utf-8 -*-
import os, math
D = os.path.dirname(os.path.abspath(__file__))
def w(n, h): open(os.path.join(D, f"frag_{n}.html"), "w").write(h)

# ------------------------------------------------ rejilla del acertijo de lógica (escalera clásica)
NOM  = ["Ana","Beto","Ceci","Diego","Emi"]
APP  = ["TikTok","Twitch","Spotify","YouTube","Discord"]
HOR  = ["21:00","22:00","23:00","00:00","01:00"]
EXC  = ["Se fue la luz","El perro","Se acabó la pila","Era para el lunes","La dejé en casa"]

def bloques(fila_labels, grupos, titulo_izq):
    """grupos: lista de (titulo, [etiquetas])"""
    ncols = sum(len(g[1]) for g in grupos)
    h = [f'<table class="lg lg{ncols}">',
         '<colgroup><col class="cl">' + '<col class="cc">'*ncols + '</colgroup>']
    # fila de títulos de grupo
    h.append(f'<tr><td class="hueco" rowspan="2"></td>')
    for t,(gt,gl) in enumerate(grupos):
        h.append(f'<td class="gtit" colspan="{len(gl)}">{gt}</td>')
    h.append('</tr>')
    # fila de etiquetas verticales
    h.append('<tr>')
    for gi,(gt,gl) in enumerate(grupos):
        for i,l in enumerate(gl):
            sep = " sep" if i == 0 and gi > 0 else ""
            h.append(f'<td class="vlab{sep}"><span>{l}</span></td>')
    h.append('</tr>')
    for ri,fl in enumerate(fila_labels):
        sepr = " sepr" if ri == 0 else ""
        h.append(f'<tr class="{sepr}"><td class="hlab">{fl}</td>')
        for gi,(gt,gl) in enumerate(grupos):
            for i,l in enumerate(gl):
                sep = " sep" if i == 0 and gi > 0 else ""
                h.append(f'<td class="c{sep}"></td>')
        h.append('</tr>')
    h.append('</table>')
    return "".join(h)

w("logica_a", bloques(NOM, [("Plataforma", APP), ("Se durmió a las", HOR), ("Su excusa", EXC)], "Alumno"))
w("logica_b", bloques(EXC, [("Plataforma", APP), ("Se durmió a las", HOR)], "Excusa"))
w("logica_c", bloques(HOR, [("Plataforma", APP)], "Hora"))

# ------------------------------------------------ triángulo del escape room (acertijo D)
tri = '''<svg viewBox="0 0 200 176" style="width:100%;height:auto" fill="none" stroke="#111"
 stroke-width="2.4" stroke-linejoin="round">
<path d="M100,10 L190,166 L10,166 Z"/>
<path d="M55,88 L145,88"/><path d="M55,88 L100,166"/><path d="M145,88 L100,166"/>
</svg>'''
w("triangulo", tri)

# ------------------------------------------------ verificación del presupuesto (actividad 12)
PRECIOS = {
 "Cómputo":   [("Laptop de uso general", 8400), ("PC de escritorio armada", 10300),
               ("Consola de segunda mano", 4900), ("Tableta con teclado", 3700)],
 "Pantalla":  [("Monitor de 24 pulgadas", 2100), ("Monitor de 27 pulgadas", 3450),
               ("Televisión de 32 pulgadas", 2800), ("No compro pantalla", 0)],
 "Audio":     [("Audífonos con cable", 650), ("Diadema con micrófono", 1150), ("Bocinas de escritorio", 890)],
 "Entrada":   [("Teclado y ratón básicos", 480), ("Teclado mecánico", 1290), ("Control inalámbrico", 920)],
 "Mueble":    [("Silla con respaldo alto", 1750), ("Escritorio de 1.20 m", 1600), ("Tapete y soporte", 390)],
 "Extras":    [("Micrófono de escritorio", 780), ("Cámara web HD", 560), ("Tira de luces LED", 240)],
}
TOPE, IVA = 15000, 0.16
from itertools import product
combos = list(product(*[[(k,n,p) for n,p in v] for k,v in PRECIOS.items()]))
validas = [c for c in combos if sum(x[2] for x in c)*(1+IVA) <= TOPE]
sub_max = max(sum(x[2] for x in c) for c in validas)
print(f"combinaciones totales (una de cada categoría): {len(combos)}")
print(f"válidas dentro de ${TOPE:,} con IVA: {len(validas)}  ({100*len(validas)/len(combos):.0f}%)")
print(f"gasto máximo sin IVA posible: ${TOPE/(1+IVA):,.2f}")
print(f"subtotal más caro que aún cabe: ${sub_max:,.2f} -> total ${sub_max*1.16:,.2f}")
barato = min(combos, key=lambda c: sum(x[2] for x in c))
print(f"opción más barata: ${sum(x[2] for x in barato):,} + IVA = ${sum(x[2] for x in barato)*1.16:,.2f}")
ej = [("Cómputo","Laptop de uso general",8400),("Pantalla","Monitor de 24 pulgadas",2100),
      ("Audio","Audífonos con cable",650),("Entrada","Teclado y ratón básicos",480),
      ("Mueble","Tapete y soporte",390),("Extras","Cámara web HD",560)]
s = sum(x[2] for x in ej)
print(f"\nEJEMPLO PARA EL SOLUCIONARIO: subtotal ${s:,} | IVA ${s*IVA:,.2f} | total ${s*1.16:,.2f} | sobran ${TOPE-s*1.16:,.2f}")
