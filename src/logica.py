from itertools import permutations

NOMBRES = ["Ana", "Beto", "Ceci", "Diego", "Emi"]
APPS    = ["TikTok", "Twitch", "Spotify", "YouTube", "Discord"]
HORAS   = [21, 22, 23, 24, 25]          # 24 = 00:00, 25 = 01:00
EXCUSAS = ["luz", "perro", "pila", "lunes", "casa"]

SOL = {
    "Ana":   ("Spotify", 23, "lunes"),
    "Beto":  ("Twitch",  25, "pila"),
    "Ceci":  ("TikTok",  22, "casa"),
    "Diego": ("YouTube", 24, "luz"),
    "Emi":   ("Discord", 21, "perro"),
}

def app(s,n): return s[n][0]
def hora(s,n): return s[n][1]
def exc(s,n): return s[n][2]
def q_app(s,a): return next(n for n in NOMBRES if s[n][0]==a)
def q_exc(s,e): return next(n for n in NOMBRES if s[n][2]==e)

PISTAS = [
 ("Quien usa Discord fue el primero de los cinco en dormirse.",
  lambda s: hora(s,q_app(s,"Discord")) == min(hora(s,n) for n in NOMBRES)),
 ("Ana se durmio exactamente una hora despues que Ceci.",
  lambda s: hora(s,"Ana") == hora(s,"Ceci")+1),
 ("Quien dijo «se me acabo la pila del celular» fue el ultimo en dormirse.",
  lambda s: hora(s,q_exc(s,"pila")) == max(hora(s,n) for n in NOMBRES)),
 ("Quien se quedo viendo YouTube se durmio a las 00:00.",
  lambda s: hora(s,q_app(s,"YouTube")) == 24),
 ("Ceci fue la que dijo que si hizo la tarea, pero que la dejo en su casa.",
  lambda s: exc(s,"Ceci") == "casa"),
 ("Emi no usa TikTok ni Twitch.",
  lambda s: app(s,"Emi") not in ("TikTok","Twitch")),
 ("Quien escucha Spotify dijo que penso que la tarea era para el lunes.",
  lambda s: exc(s,q_app(s,"Spotify")) == "lunes"),
 ("Diego se durmio mas tarde que Ana, pero mas temprano que Beto.",
  lambda s: hora(s,"Ana") < hora(s,"Diego") < hora(s,"Beto")),
 ("Quien dijo que el perro se comio la tarea se durmio antes de las 22:00.",
  lambda s: hora(s,q_exc(s,"perro")) < 22),
 ("Beto no usa Discord ni Spotify.",
  lambda s: app(s,"Beto") not in ("Discord","Spotify")),
 ("Ni Ceci ni Diego usan Twitch.",
  lambda s: app(s,"Ceci") != "Twitch" and app(s,"Diego") != "Twitch"),
 ("Ana no se durmio a las 22:00.",
  lambda s: hora(s,"Ana") != 22),
 ("Diego no fue quien dijo que el perro se comio la tarea.",
  lambda s: exc(s,"Diego") != "perro"),
]

def universo():
    for pa in permutations(APPS):
        for ph in permutations(HORAS):
            for pe in permutations(EXCUSAS):
                yield {n:(pa[i],ph[i],pe[i]) for i,n in enumerate(NOMBRES)}

UNIV = list(universo())

def soluciones(subset):
    return [s for s in UNIV if all(f(s) for _,f in subset)]

if __name__ == "__main__":
    for txt,f in PISTAS:
        assert f(SOL), "La solucion objetivo falla: " + txt
    full = soluciones(PISTAS)
    print("con todas las pistas -> soluciones:", len(full), "| coincide con la objetivo:", full == [SOL])

    # minimizacion greedy: elimina pistas redundantes
    actual = list(PISTAS)
    for p in list(PISTAS):
        prueba = [q for q in actual if q is not p]
        if len(soluciones(prueba)) == 1:
            actual = prueba
    print("\nPISTAS MINIMAS:", len(actual))
    for i,(txt,_) in enumerate(actual,1): print(f"  {i}. {txt}")
    assert soluciones(actual) == [SOL]
    print("\nSOLUCION UNICA VERIFICADA")
    for n in NOMBRES: print(f"  {n:6} {SOL[n][0]:8} {SOL[n][1]} {SOL[n][2]}")
