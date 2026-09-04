# -*- coding: utf-8 -*-
"""Criptograma de sustitucion + tabla de frecuencias del espanol."""
import random, json, string

FRASE = "UN PULPO TIENE TRES CORAZONES NUEVE CEREBROS Y SANGRE AZUL"
RETO  = "TAMBIEN PUEDE PROBAR CON LOS BRAZOS"
AB = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def cifrar(seed):
    rnd = random.Random(seed)
    for _ in range(9000):
        perm = list(AB); rnd.shuffle(perm)
        m = dict(zip(AB, perm))
        if all(m[a] != a for a in AB):            # ninguna letra se cifra en si misma
            return m
m = cifrar(2026)
enc = lambda t: "".join(m[ch] if ch in m else ch for ch in t)
c1, c2 = enc(FRASE), enc(RETO)

# letras de regalo: la mas frecuente de la frase y dos que abren palabras cortas
from collections import Counter
frec = Counter(ch for ch in FRASE if ch.isalpha())
regalo = [frec.most_common(1)[0][0], "U", "Z"]
print("frase  :", FRASE)
print("cifrada:", c1)
print("reto   :", c2)
print("regalos:", {m[r]: r for r in regalo})
print("letras distintas en la frase:", len(set(ch for ch in FRASE if ch.isalpha())))
# comprobacion
inv = {v: k for k, v in m.items()}
assert "".join(inv.get(ch, ch) for ch in c1) == FRASE
print("descifrado verificado OK")
json.dump({"frase": FRASE, "cifrada": c1, "reto": RETO, "reto_cifrado": c2,
           "regalos": {m[r]: r for r in regalo},
           "tabla": [["E",13.7],["A",12.5],["O",8.7],["S",8.0],["R",6.9],["N",6.7],
                     ["I",6.2],["D",5.9],["L",5.0],["C",4.7],["T",4.6],["U",3.9]]},
          open("cripto.json","w"), ensure_ascii=False)
