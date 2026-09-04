# -*- coding: utf-8 -*-
"""Hoja 0 (banco de 14 problemas) + tabla de datos para la guia. Aplica las correcciones
de los tres verificadores: datos actualizados y los cuatro problemas reescritos por riesgo."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
r = json.load(open("/tmp/claude-1001/hv.json"))
B = {p["key"]: p["data"] for p in r["piezas"]}["banco-problemas"]
P = [dict(x) for x in B["problemas"]]

def fix(i, **kw):
    for k, v in kw.items(): P[i-1][k] = v

# --- correcciones del verificador de DATOS ---
fix(1, dato_estable="México genera más de 130 mil toneladas de basura al día y recicla menos de una décima parte (Diagnóstico Básico para la Gestión Integral de los Residuos, Semarnat).")
fix(2, dato_estable="La Conagua calcula que alrededor de 4 de cada 10 litros de agua potable se pierden antes de llegar a una llave, la mayoría en fugas de la red.")
fix(4, dato_estable="Los últimos diez años han sido los diez más cálidos desde que hay registro y la temperatura media del planeta ya está entre 1.3 y 1.5 °C arriba de la de hace siglo y medio (Organización Meteorológica Mundial).")
fix(6, dato_estable="Alrededor de una tercera parte de los alimentos del mundo se pierde antes de llegar a la tienda o se tira después de llegar (FAO y ONU Medio Ambiente).")
fix(9, dato_estable="Poco más de 1 de cada 10 personas de 5 a 17 años en México está en situación de trabajo infantil: 3.7 millones, y más de 2 millones de ellas en una ocupación no permitida para su edad (Enti, Inegi).")

# --- correcciones del verificador de AULA (riesgo con padres de familia) ---
fix(8, nombre="TRABAJO SIN CONTRATO",
       dato_estable="Más de la mitad de las personas ocupadas en México, alrededor de 55 de cada 100, tiene un empleo informal: nadie le paga seguridad social por ese trabajo (Enoe, Inegi).")
fix(10, nombre="EL TURNO QUE NADIE CUENTA",
        una_linea="Los mandados y las filas de una casa, que se hacen todos los días y no cuentan como trabajo.",
        mecanismo="Mientras alguien lo haga gratis, a nadie le urge repartirlo ni contarlo como trabajo.",
        dato_estable="Las mujeres dedican alrededor de 29 horas a la semana al trabajo del hogar y de cuidados que nadie paga; los hombres, alrededor de 12 (Enut, Inegi).",
        quien_paga="Quien hace ese turno y se queda sin tiempo propio.",
        gancho_villano="Algo que reparte el trabajo por costumbre y le dice «ayuda» a lo que en realidad es la mitad.",
        regla="Esta se escribe desde la calle, no desde tu casa. Lo que se ve es la fila del agua, la cola de la tortillería, quién va por los niños a la salida, quién espera turno en la clínica. No escribas quién hace qué en tu casa.")
fix(11, una_linea="En la esquina de la escuela, lo más barato es lo que aguanta meses en el estante.",
        mecanismo="Lo dulce y lo frito rinde más por peso, no se echa a perder y se vende solo; una fruta hay que venderla hoy.",
        dato_estable="La ley ya prohíbe vender dentro de las escuelas los productos con sellos de advertencia; la banqueta de afuera no está incluida (lineamientos SEP-Secretaría de Salud).",
        quien_paga="Quien solo alcanza a comprar ahí, y quien no tiene otra tienda cerca.")
fix(12, quien_paga="Quien sale en la pantalla sin haber elegido estar ahí.",
        regla="En esta no uses un caso de tu salón ni de tu escuela. Sin nombres, sin apodos, sin iniciales, sin señas. Describes cómo funciona la cadena, no quién salió en la foto. Si solo lo puedes contar contando quién fue, escoge otro problema.")

# ---------------- hoja 0: tabla del alumno (sin datos ni quien_paga) ----------------
t = ['<table class="banco">',
     '<tr><th style="width:7mm">#</th><th style="width:31mm">Problema</th><th style="width:50mm">Lo que se ve</th>'
     '<th style="width:59mm">El acomodo que lo mantiene vivo</th><th>La forma que podría tomar el villano</th></tr>']
for i, p in enumerate(P, 1):
    daga = ' <b>&dagger;</b>' if p.get("regla") else ''
    t.append(f'<tr><td class="n">{i}</td><td class="pb">{p["nombre"]}{daga}</td><td>{p["una_linea"]}</td>'
             f'<td>{p["mecanismo"]}</td><td>{p["gancho_villano"]}</td></tr>')
t.append('</table>')
reglas = [f'<div style="font-size:8pt;margin-top:5px"><b>&dagger; Regla del {i} ({p["nombre"]}).</b> {p["regla"]}</div>'
          for i, p in enumerate(P, 1) if p.get("regla")]
open(os.path.join(D, "frag_banco.html"), "w").write("".join(t) + "".join(reglas))

# ---------------- tabla de datos, solo para la guia de la maestra ----------------
g = ['<table class="banco"><tr><th style="width:7mm">#</th><th style="width:30mm">Problema</th>'
     '<th>El dato, con su fuente (no se imprime en la hoja del alumno)</th><th style="width:42mm">Quién lo paga</th></tr>']
for i, p in enumerate(P, 1):
    g.append(f'<tr><td class="n">{i}</td><td class="pb">{p["nombre"]}</td><td>{p["dato_estable"]}</td>'
             f'<td>{p["quien_paga"]}</td></tr>')
g.append('</table>')
open(os.path.join(D, "frag_datos.html"), "w").write("".join(g))
print("frag_banco + frag_datos |", len(P), "problemas |", sum(1 for p in P if p.get("regla")), "con regla extra")
