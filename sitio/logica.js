const $ = (s) => document.querySelector(s);
const LS = "cajon-mafer-v2";
const estado = { filtro: "todo", grado: "todos", busca: "", usadas: {}, abierta: null };

try { estado.usadas = (JSON.parse(localStorage.getItem(LS) || "{}").usadas) || {}; } catch (e) {}
const guardar = () => { try { localStorage.setItem(LS, JSON.stringify({ usadas: estado.usadas })); } catch (e) {} };

/* saludo según la hora, y nada más: la hoja la elige ella */
function saludar() {
  const d = new Date(), h = d.getHours();
  const franja = h < 12 ? "Buenos días" : h < 19 ? "Buenas tardes" : "Buenas noches";
  $("#saludo").innerHTML = franja + ', <em>Mafer</em>';
  $("#fecha").textContent = d.toLocaleDateString("es-MX",
    { weekday: "long", day: "numeric", month: "long", year: "numeric" });
}

const CLASE_MAT = { "Matemáticas": "m-mat", "Español": "m-esp", "Artes": "m-art", "Ciencias": "m-cie",
  "Tecnología": "m-tec", "Cívica": "m-civ", "Educación física": "m-efi" };

function tarjeta(a) {
  const b = document.createElement("button");
  b.type = "button";
  b.className = "tarj" + (estado.usadas[a.id] ? " usada" : "");
  b.onclick = () => abrir(a.id);
  const dur = a.min ? a.min + " min" : "sin límite";
  const marca = estado.usadas[a.id];
  const gr = a.grado ? '<span class="grado g' + a.grado + '">' + a.grado + "º</span>" : "";
  b.innerHTML =
    '<div class="fila1"><span class="n">' + a.etiqueta + '</span>' + gr + '<span class="dur">' + dur + "</span></div>" +
    "<h3>" + a.titulo + "</h3><p>" + a.sub + "</p>" +
    '<div class="pies">' +
      '<span class="sello">' + (marca ? "Aplicada el " + marca : "Aplicada") + "</span>" +
      a.materias.map((m) => '<span class="mat ' + (CLASE_MAT[m] || "") + '">' + m + "</span>").join("") +
      '<span class="mat m-hoja">' + a.hojas.length + (a.hojas.length === 1 ? " hoja" : " hojas") + "</span></div>";
  const dl = document.createElement("a");
  dl.className = "dl"; dl.href = "hojas/" + a.archivo + ".pdf"; dl.target = "_blank";
  dl.rel = "noopener"; dl.textContent = "PDF"; dl.title = "Abrir el PDF de esta hoja";
  dl.onclick = (e) => e.stopPropagation();
  b.querySelector(".pies").appendChild(dl);
  return b;
}

function pinta() {
  const cont = $("#grid"); cont.innerHTML = "";
  const q = estado.busca.trim().toLowerCase();
  const visibles = ACTIVIDADES.filter((a) => {
    if (estado.grado !== "todos" && String(a.grado) !== estado.grado) return false;
    if (q && !(a.titulo + " " + a.sub + " " + a.materias.join(" ")).toLowerCase().includes(q)) return false;
    if (estado.filtro === "todo") return true;
    if (estado.filtro === "pendiente") return !estado.usadas[a.id];
    if (GRUPOS[estado.filtro]) return GRUPOS[estado.filtro].includes(a.tipo);
    return a.materias.some((m) => m.startsWith(estado.filtro));
  });

  // Con un grado concreto elegido: una sola rejilla. Con "todos": una sección por grado.
  const grados = estado.grado === "todos" ? [1, 2, 3] : [Number(estado.grado)];
  grados.forEach((g) => {
    const delGrado = visibles.filter((a) => a.grado === g);
    if (!delGrado.length) return;
    if (estado.grado === "todos") {
      const h = document.createElement("div");
      h.className = "seccion grado-tit g" + g;
      h.innerHTML = (GRADOS[g] || g + "º de secundaria") +
        '<span class="cta">' + delGrado.length + (delGrado.length === 1 ? " actividad" : " actividades") + "</span>";
      cont.appendChild(h);
    }
    const grid = document.createElement("div");
    grid.className = "grid";
    delGrado.forEach((a) => grid.appendChild(tarjeta(a)));
    cont.appendChild(grid);
  });

  $("#vacio").hidden = visibles.length > 0;
  const ga = $("#grid-apoyo"); ga.innerHTML = "";
  APOYO.forEach((a) => ga.appendChild(tarjeta(a)));
  $("#c-usadas").textContent = ACTIVIDADES.filter((a) => estado.usadas[a.id]).length;
}

function escalar() {
  document.querySelectorAll("#pila .marco").forEach((m) => {
    const p = m.querySelector(".papel");
    const z = Math.min(1, Math.min(m.parentElement.clientWidth, 1100) / p.offsetWidth);
    p.style.transform = "scale(" + z + ")";
    m.style.width = p.offsetWidth * z + "px";
    m.style.height = p.offsetHeight * z + "px";
  });
}

function abrir(id) {
  const a = TODAS.find((x) => x.id === id);
  if (!a) return;
  estado.abierta = a;
  $("#v-t").textContent = a.titulo;
  $("#v-s").textContent = (a.min ? a.min + " minutos" : "sin límite de tiempo") + " · " +
    a.hojas.length + (a.hojas.length === 1 ? " hoja" : " hojas") + " · " + a.materias.join(", ");
  const pila = $("#pila"); pila.innerHTML = "";
  a.hojas.forEach((ref, i) => {
    const orig = document.getElementById("h-" + ref);
    if (!orig) return;
    const m = document.createElement("div");
    m.className = "marco";
    const r = document.createElement("div");
    r.className = "etiq";
    r.textContent = a.rotulos && a.rotulos[i] ? a.rotulos[i]
      : (a.hojas.length > 1 ? "Hoja " + (i + 1) + " de " + a.hojas.length : "");
    const clon = orig.cloneNode(true);
    clon.id = ""; clon.dataset.off = "0";
    m.appendChild(r); m.appendChild(clon); pila.appendChild(m);
  });
  marcaBoton(a);
  $("#pdf").href = "hojas/" + a.archivo + ".pdf";
  $("#visor").classList.add("on");
  document.body.style.overflow = "hidden";
  requestAnimationFrame(escalar);
  $("#visor").scrollTop = 0;
}

function marcaBoton(a) {
  const f = estado.usadas[a.id];
  $("#usada").setAttribute("aria-pressed", f ? "true" : "false");
  $("#usada").textContent = f ? "Aplicada el " + f : "Ya la apliqué";
}

function cerrar() {
  $("#visor").classList.remove("on");
  document.body.style.overflow = "";
  estado.abierta = null;
  pinta();
}

document.querySelectorAll(".chip.gr").forEach((c) => {
  c.onclick = () => {
    estado.grado = c.dataset.g;
    document.querySelectorAll(".chip.gr").forEach((o) => o.setAttribute("aria-pressed", o === c ? "true" : "false"));
    pinta();
  };
});
document.querySelectorAll(".chip:not(.gr)").forEach((c) => {
  c.onclick = () => {
    estado.filtro = c.dataset.f;
    document.querySelectorAll(".chip:not(.gr)").forEach((o) => o.setAttribute("aria-pressed", o === c ? "true" : "false"));
    pinta();
  };
});
$("#busca").oninput = (e) => { estado.busca = e.target.value; pinta(); };
$("#volver").onclick = cerrar;
$("#usada").onclick = () => {
  const a = estado.abierta; if (!a) return;
  if (estado.usadas[a.id]) delete estado.usadas[a.id];
  else estado.usadas[a.id] = new Date().toLocaleDateString("es-MX", { day: "numeric", month: "short" });
  guardar(); marcaBoton(a);
};
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && estado.abierta) cerrar();
  if ((e.key === "p" || e.key === "P") && (e.metaKey || e.ctrlKey) && estado.abierta) {
    e.preventDefault(); window.open($("#pdf").href, "_blank", "noopener");
  }
});
window.addEventListener("resize", () => { if (estado.abierta) escalar(); });

saludar(); pinta();
$("#c-act").textContent = ACTIVIDADES.length;
