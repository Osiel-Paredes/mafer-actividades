# -*- coding: utf-8 -*-
"""Catalogo unico de actividades. Lo usan el generador de PDFs y el del sitio."""
import re, os, json
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"

DOCS = {
    "cuad": B + "cuadernillo-actividades.html",
    "hv":   B + "actividad-heroe-y-villano.html",
    "rec":  B + "actividades-recreativas.html",
}

def leer(path):
    h = open(path).read()
    css = "\n".join(re.findall(r"<style>(.*?)</style>", h, re.S))
    secs = re.findall(r'<section class="hoja[^"]*">.*?</section>', h, re.S)
    return css, secs

HOJAS, CSS = {}, {}
for k, p in DOCS.items():
    CSS[k], HOJAS[k] = leer(p)

# ── 4º documento: el lote nuevo (hojas 23-52), organizado por grado ──────────
# Cada hoja vive en su propio fragmento frag_hNN.html; comparten base.css+extra.css.
NUEVAS_SRC = os.path.dirname(os.path.abspath(__file__)).replace("/sitio", "") + "/nuevas/src"
if not os.path.isdir(NUEVAS_SRC):
    NUEVAS_SRC = B + "nuevas/src"

def leer_nuevas():
    css = (open(NUEVAS_SRC + "/base.css").read() + "\n" + open(NUEVAS_SRC + "/extra.css").read())
    # Las hojas de los pasatiempos traen marcadores <!--INCLUDE:x--> que hay que expandir.
    def expandir(txt):
        def sub(m):
            f = NUEVAS_SRC + f"/frag_{m.group(1)}.html"
            return open(f).read() if os.path.exists(f) else ""
        for _ in range(6):
            nuevo = re.sub(r"<!--INCLUDE:([a-z_0-9]+)-->", sub, txt)
            if nuevo == txt:
                break
            txt = nuevo
        return txt
    secs = {}
    for n in range(23, 53):
        p = NUEVAS_SRC + f"/frag_h{n}.html"
        secs[n] = expandir(open(p).read())
    return css, secs

CSS["nuevas"], _NUEVAS = leer_nuevas()
# HOJAS["nuevas"] se indexa por número de hoja (23..52), no por posición.
HOJAS["nuevas"] = _NUEVAS

def sub_nueva(n):
    m = re.search(r'<div class="sub">(.*?)</div>', HOJAS["nuevas"][n], re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""

def sub_de(doc, i):
    m = re.search(r'<div class="sub">(.*?)</div>', HOJAS[doc][i], re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""

# id, num, titulo, min, materias, tipo, doc, indices de hoja, nombre de archivo, grado
CRUDO = [
 ("a02","02","Diseña tu app",55,["Tecnología","Español"],"diseño","cuad",[4],"02-disena-tu-app",3),
 ("a03","03","Cazafakes",45,["Español","Cívica"],"crítico","cuad",[5],"03-cazafakes",3),
 ("a05","05","Ficha de personaje",50,["Español","Artes"],"dibujo","cuad",[7],"05-ficha-de-personaje",3),
 ("a06","06","Cómic de seis viñetas",55,["Español","Artes"],"dibujo","cuad",[8],"06-comic-de-seis-vinetas",3),
 ("a07","07","Poema tachado",40,["Español"],"escritura","cuad",[9],"07-poema-tachado",3),
 ("a08","08","El objeto de 2050",50,["Ciencias","Tecnología"],"diseño","cuad",[10],"08-el-objeto-de-2050",3),
 ("a09","09","Pixel lógica",50,["Matemáticas"],"pasatiempo","cuad",[11],"09-pixel-logica",3),
 ("a10","10","La tarea perdida",40,["Matemáticas"],"pasatiempo","cuad",[12],"10-la-tarea-perdida",3),
 ("a11","11","Escape room de papel",45,["Matemáticas"],"pasatiempo","cuad",[13],"11-escape-room-de-papel",3),
 ("a12","12","Arma tu setup con $15,000",50,["Matemáticas"],"mate","cuad",[14],"12-arma-tu-setup",3),
 ("a13","13","Mandala geométrico",None,["Artes"],"arte","cuad",[15],"13-mandala-geometrico",3),
 ("a14","14","Tu héroe y tu villano",50,["Cívica","Español","Artes"],"dibujo","hv",[0],"14-tu-heroe-y-tu-villano",3),
 ("a15","15","Batalla naval de un solo jugador",45,["Matemáticas"],"pasatiempo","rec",[0],"15-batalla-naval",3),
 ("a16","16","El laberinto de las tres llaves",45,["Matemáticas"],"pasatiempo","rec",[1],"16-laberinto-tres-llaves",3),
 ("a17","17","Palabras que suenan inventadas",45,["Español"],"pasatiempo","rec",[2],"17-palabras-inventadas",3),
 ("a18","18","Mensaje cifrado",50,["Matemáticas","Español"],"pasatiempo","rec",[3],"18-mensaje-cifrado",3),
 ("a19","19","La historia rellenada",50,["Español"],"escritura","rec",[4],"19-la-historia-rellenada",3),
 ("a20","20","Diseña tu nivel",50,["Tecnología","Artes"],"diseño","rec",[5],"20-disena-tu-nivel",3),
 ("a21","21","Inventa un deporte",50,["Educación física","Matemáticas"],"diseño","rec",[6],"21-inventa-un-deporte",3),
 ("a22","22","La caja de cereal",50,["Artes","Matemáticas"],"diseño","rec",[7],"22-la-caja-de-cereal",3),
 # ── Primero de secundaria (23-34) ──
 ("a23","23","El noticiero de mi calle",45,["Español","Cívica"],"escritura","nuevas",[23],"23-noticiero-de-mi-calle",1),
 ("a24","24","Instructivo para un extraterrestre",45,["Español"],"escritura","nuevas",[24],"24-instructivo-extraterrestre",1),
 ("a25","25","El mapa de mi camino a la escuela",50,["Geografía","Matemáticas"],"diseño","nuevas",[25],"25-mapa-camino-escuela",1),
 ("a26","26","Bestiario del patio",50,["Ciencias","Artes"],"dibujo","nuevas",[26],"26-bestiario-del-patio",1),
 ("a27","27","La receta para siete",45,["Matemáticas"],"mate","nuevas",[27],"27-la-receta-para-siete",1),
 ("a28","28","Mis 24 horas de ayer",45,["Matemáticas"],"mate","nuevas",[28],"28-mis-24-horas",1),
 ("a29","29","La leyenda de mi colonia",50,["Español"],"escritura","nuevas",[29],"29-leyenda-de-mi-colonia",1),
 ("a30","30","El dibujo escondido",40,["Matemáticas"],"pasatiempo","nuevas",[30],"30-el-dibujo-escondido",1),
 ("a31","31","Barcos en la niebla",40,["Matemáticas"],"pasatiempo","nuevas",[31],"31-barcos-en-la-niebla",1),
 ("a32","32","El laberinto de las dos llaves",35,["Matemáticas"],"pasatiempo","nuevas",[32],"32-laberinto-dos-llaves",1),
 ("a33","33","La sopa con recado",40,["Español"],"pasatiempo","nuevas",[33],"33-la-sopa-con-recado",1),
 ("a34","34","Mensaje en clave",45,["Matemáticas","Español"],"pasatiempo","nuevas",[34],"34-mensaje-en-clave",1),
 # ── Segundo de secundaria (35-46) ──
 ("a35","35","Noticiero 2045",50,["Español","Ciencias"],"escritura","nuevas",[35],"35-noticiero-2045",2),
 ("a36","36","El anuncio que miente sin mentir",50,["Español","Cívica"],"crítico","nuevas",[36],"36-anuncio-que-miente",2),
 ("a37","37","La máquina de seis pasos",50,["Ciencias","Tecnología"],"diseño","nuevas",[37],"37-maquina-seis-pasos",2),
 ("a38","38","Un día en el año que te toque",50,["Historia","Español"],"escritura","nuevas",[38],"38-un-dia-en-el-ano",2),
 ("a39","39","El puesto del recreo",50,["Matemáticas"],"mate","nuevas",[39],"39-el-puesto-del-recreo",2),
 ("a40","40","La rifa amañada",45,["Matemáticas"],"mate","nuevas",[40],"40-la-rifa-amanada",2),
 ("a41","41","Expediente de un objeto roto",50,["Artes","Tecnología"],"dibujo","nuevas",[41],"41-expediente-objeto-roto",2),
 ("a42","42","Pixel lógica de doce",45,["Matemáticas"],"pasatiempo","nuevas",[42],"42-pixel-logica-de-doce",2),
 ("a43","43","Batalla naval de bolsillo",40,["Matemáticas"],"pasatiempo","nuevas",[43],"43-batalla-naval-bolsillo",2),
 ("a44","44","El laberinto del peaje",45,["Matemáticas"],"pasatiempo","nuevas",[44],"44-laberinto-del-peaje",2),
 ("a45","45","Sopa de física",40,["Ciencias"],"pasatiempo","nuevas",[45],"45-sopa-de-fisica",2),
 ("a46","46","El mensaje del sol",50,["Matemáticas","Ciencias"],"pasatiempo","nuevas",[46],"46-el-mensaje-del-sol",2),
 # ── Tercero de secundaria (47-52) ──
 ("a47","47","La misma noticia en dos canales",50,["Español","Cívica"],"crítico","nuevas",[47],"47-misma-noticia-dos-canales",3),
 ("a48","48","El experimento de la cocina",50,["Ciencias"],"diseño","nuevas",[48],"48-experimento-de-la-cocina",3),
 ("a49","49","El dilema de la beca",50,["Cívica","Matemáticas"],"crítico","nuevas",[49],"49-el-dilema-de-la-beca",3),
 ("a50","50","Medir lo que no puedes tocar",50,["Matemáticas"],"mate","nuevas",[50],"50-medir-lo-que-no-tocas",3),
 ("a51","51","La carta que sí se manda",45,["Español","Cívica"],"escritura","nuevas",[51],"51-la-carta-que-si-se-manda",3),
 ("a52","52","Ingeniería inversa",45,["Matemáticas"],"mate","nuevas",[52],"52-ingenieria-inversa",3),
]

def _sub(d, hs):
    return sub_nueva(hs[0]) if d == "nuevas" else sub_de(d, hs[0])

ACTIVIDADES = [dict(id=i, num=n, titulo=t, sub=_sub(d, hs), min=m, materias=ma,
                    tipo=tp, doc=d, hojas=hs, archivo=ar, grado=g)
               for i, n, t, m, ma, tp, d, hs, ar, g in CRUDO]

APOYO = [
 dict(id="g-cuad", num="Guía", titulo="Guía de las actividades", min=None, materias=["Para ti"], grado=0,
      tipo="guia", doc="cuad", hojas=[1, 2], archivo="guia-actividades",
      sub="Tiempos, con qué materia empata cada una, la rúbrica única de 10 puntos y cómo cachar una hoja hecha con IA. "
          "La tabla todavía lista las dos actividades que se quitaron por pedir celular."),
 dict(id="g-sol", num="Claves", titulo="Solucionario", min=None, materias=["Para ti"], grado=0,
      tipo="guia", doc="cuad", hojas=[16], archivo="solucionario",
      sub="Respuestas del nonograma, del acertijo de lógica, del escape room y del presupuesto, con el camino de deducción."),
 dict(id="g-rec", num="Claves", titulo="Soluciones de los pasatiempos", min=None, materias=["Para ti"], grado=0,
      tipo="guia", doc="rec", hojas=[8], archivo="soluciones-pasatiempos",
      sub="La batalla naval resuelta, el mensaje cifrado, el mensaje escondido de la sopa y los pasos del laberinto."),
]

if __name__ == "__main__":
    for a in ACTIVIDADES: print(f"  {a['num']:>6}  {a['titulo'][:42]:44} {a['doc']:5} {a['archivo']}")
    print("\nactividades:", len(ACTIVIDADES), "| apoyo:", len(APOYO))
    print("hojas por doc:", {k: len(v) for k, v in HOJAS.items()})
