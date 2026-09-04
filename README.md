# El cajón de Mafer.

Veinte hojas de trabajo imprimibles para un grupo de **tercero de secundaria** en México, más las
guías para quien las aplica. Todas cumplen las mismas cuatro condiciones:

- **Trabajo individual en la banca.** Nadie se levanta, no hay equipos, no hay exposiciones.
- **Sin celular.** Ninguna necesita internet ni teléfono para resolverse.
- **Sin material extra.** Lápiz, colores si hay, y la hoja.
- **Una cara, tamaño carta, blanco y negro.** Pensadas para fotocopiarse.

Cada hoja lleva al pie un **Reto extra** para quien termina antes de tiempo, que es lo que evita el
clásico «ya acabé» a los quince minutos.

## Cómo se usa

Abre `index.html` en cualquier navegador, o publícalo con GitHub Pages. Es un solo archivo sin
dependencias ni servidor: trae las veinte hojas maquetadas dentro.

- **Ver e imprimir.** Haz clic en una actividad y sale la vista previa a tamaño real. El botón
  *Imprimir esta hoja* abre el PDF suelto, que es el que está maquetado al milímetro.
- **Contador de copias.** Escribe cuántos alumnos son y te dice cuántas fotocopias necesitas.
- **«Ya la apliqué».** Marca las que ya usaste; se guarda en tu navegador, no en el repositorio.
- **Filtros.** Por pasatiempo, dibujo, escritura, materia, duración, o las que aún no has aplicado.
- **Sugerencia del día.** Propone una que no hayas aplicado y no cambia durante el día.

Si solo quieres el papel, están todos en `hojas/`, un PDF por actividad.

## Qué hay

| # | Actividad | Min | Qué se hace |
|---|---|---|---|
| 02 | Diseña tu app | 55 | Tres pantallas dibujadas para un problema real, con su lado oscuro |
| 03 | Cazafakes | 45 | Ocho preguntas de verificación sobre una noticia falsa que viene impresa |
| 05 | Ficha de personaje | 50 | Un avatar con 30 puntos que hay que repartir entre seis atributos |
| 06 | Cómic de seis viñetas | 55 | Marco listo, arranque dado, final libre |
| 07 | Poema tachado | 40 | Se tacha un texto impreso hasta que lo que sobra es un poema |
| 08 | El objeto de 2050 | 50 | Ficha de patente con dibujo y llamadas numeradas |
| 09 | Pixel lógica | 50 | Nonograma de 15 × 15 |
| 10 | La tarea perdida | 40 | Acertijo de rejilla con nueve pistas |
| 11 | Escape room de papel | 45 | Cuatro acertijos que abren un candado de cuatro dígitos |
| 12 | Arma tu setup con $15,000 | 50 | Presupuesto con IVA y porcentajes |
| 13 | Mandala geométrico | abierta | 136 zonas y la regla de que dos vecinas no repiten patrón |
| 14 | Tu héroe y tu villano | 50 | Dibujan a los dos; el villano encarna un problema real de su colonia |
| 15 | Batalla naval de un solo jugador | 45 | Bimaru de 8 × 8 |
| 16 | El laberinto de las tres llaves | 45 | 1072 pasos, y hay que recoger las llaves en orden |
| 17 | Palabras que suenan inventadas | 45 | Sopa cuyas letras sobrantes forman un mensaje de 81 letras |
| 18 | Mensaje cifrado | 50 | Criptograma de sustitución con tabla de frecuencias |
| 19 | La historia rellenada | 50 | Doce palabras a ciegas; el relato viene impreso de cabeza |
| 20 | Diseña tu nivel | 50 | Mapa de un nivel de plataformas y su curva de dificultad |
| 21 | Inventa un deporte | 50 | Cancha con medidas, reglas, y la jugada que rompería el juego |
| 22 | La caja de cereal | 50 | Empaque completo y las cuentas que deciden cuántos sellos le tocan |

Más tres documentos que **no se fotocopian para el grupo**: la guía de aplicación con la rúbrica de 10
puntos, el solucionario y las soluciones de los pasatiempos.

## Los pasatiempos están verificados

Los seis puzzles con respuesta no se armaron a ojo: se generaron y se comprobaron con código antes de
imprimirse.

- **Nonograma (09)** y **Bimaru (15)**: solución única, y se llega a ella por deducción pura.
- **La tarea perdida (10)**: fuerza bruta sobre las 1 728 000 combinaciones posibles. Una sola
  solución, con nueve pistas mínimas.
- **Sopa de letras (17)**: las letras que sobran se leen de vuelta y dan el mensaje exacto.
- **Mensaje cifrado (18)**: el descifrado se verifica contra la frase original.
- **Laberinto (16)**: el recorrido mínimo pasando por las tres llaves en orden mide 1072 pasos.
- **Arma tu setup (12)**: de las 1296 combinaciones de compra, 735 caben en el presupuesto con IVA.

## Antes de repartir

- La actividad **14** pide inventar un villano que encarne un problema real. La hoja impone que el
  villano sea **una costumbre o un acomodo, nunca una persona**: ni políticos reales, ni empresas con
  nombre, ni grupos de gente. Si alguien dibuja a alguien real, la corrección es una frase: «cámbialo
  por la regla que esa persona sigue».
- Las hojas **03** y **19** traen textos falsos o absurdos **puestos a propósito** (una noticia falsa y
  un relato para rellenar). No se usan como material de repaso.
- La **19** trae el relato impreso de cabeza. No es un error de imprenta: es para que no lo lean antes
  de elegir sus palabras.

## Estructura

```
index.html      el sitio, autocontenido
hojas/          un PDF por actividad
```

Nada más. No hay build, no hay dependencias.
