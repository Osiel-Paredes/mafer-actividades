const $ = (s) => document.querySelector(s);
/* animaciones solo si GSAP cargó y la persona no pidió movimiento reducido */
const MOVER = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const anim = () => window.gsap && MOVER;
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
  animarTarjetas();
}

/* ---------- animaciones (GSAP) ---------- */
let listo = false;
function animarTarjetas() {
  if (!listo || !anim()) return;
  ScrollTrigger.getAll().forEach((t) => t.vars.id === "tarj" && t.kill());
  const els = gsap.utils.toArray("#grid .tarj, #grid .grado-tit, #grid-apoyo .tarj");
  gsap.set(els, { autoAlpha: 0, y: 26 });
  ScrollTrigger.batch(els, {
    id: "tarj", once: true, start: "top 95%",
    onEnter: (b) => gsap.to(b, { autoAlpha: 1, y: 0, duration: .6, stagger: .05, ease: "power3.out", clearProps: "transform,opacity,visibility" }),
  });
  ScrollTrigger.refresh();
}

function inclinar(card) {
  card.addEventListener("mousemove", (e) => {
    if (!anim()) return;
    const r = card.getBoundingClientRect();
    const px = (e.clientX - r.left) / r.width - .5, py = (e.clientY - r.top) / r.height - .5;
    gsap.to(card, { rotationY: px * 7, rotationX: -py * 7, y: -5, transformPerspective: 800, duration: .4, ease: "power2.out" });
  });
  card.addEventListener("mouseleave", () => {
    if (anim()) gsap.to(card, { rotationY: 0, rotationX: 0, y: 0, duration: .6, ease: "elastic.out(1,.6)", clearProps: "transform" });
  });
}

function magnetico(el, f) {
  el.addEventListener("mousemove", (e) => {
    if (!anim()) return;
    const r = el.getBoundingClientRect();
    gsap.to(el, { x: (e.clientX - r.left - r.width / 2) * f, y: (e.clientY - r.top - r.height / 2) * f, duration: .35, ease: "power2.out" });
  });
  el.addEventListener("mouseleave", () => { if (anim()) gsap.to(el, { x: 0, y: 0, duration: .7, ease: "elastic.out(1,.4)" }); });
}

function contar(el) {
  const fin = Number(el.textContent) || 0, o = { v: 0 };
  gsap.to(o, { v: fin, duration: 1.4, ease: "power2.out", delay: .5, onUpdate: () => { el.textContent = Math.round(o.v); } });
}

window.addEventListener("DOMContentLoaded", () => {
  if (!anim()) return;
  gsap.registerPlugin(ScrollTrigger);
  listo = true;
  const tl = gsap.timeline({ defaults: { ease: "power3.out" } });
  tl.from(".nav", { y: -30, autoAlpha: 0, duration: .7 })
    .from(".hero", { y: 30, autoAlpha: 0, scale: .98, duration: .8 }, "-=.4")
    .from(".hero-txt > *", { y: 22, autoAlpha: 0, stagger: .08, duration: .6 }, "-=.5")
    .from(".h-hoja", { y: 60, rotation: (i) => [-14, 10, 4][i] || 0, autoAlpha: 0, stagger: .12, duration: .9, ease: "back.out(1.5)", transformOrigin: "50% 100%" }, "-=.6")
    .from(".h-sol", { scale: 0, transformOrigin: "50% 50%", duration: .9, ease: "elastic.out(1,.5)" }, "-=.7")
    .from(".h-lapiz", { x: 80, y: -40, autoAlpha: 0, duration: .8, ease: "back.out(1.6)" }, "-=.6")
    .from(".h-check", { autoAlpha: 0, scale: 0, transformOrigin: "50% 50%", duration: .5, ease: "back.out(3)" }, "-=.3")
    .from(".h-est", { scale: 0, autoAlpha: 0, transformOrigin: "50% 50%", stagger: .1, duration: .5, ease: "back.out(3)" }, "-=.4")
    .from(".filtros", { y: 24, autoAlpha: 0, duration: .6 }, "-=1")
    .from(".filtros .chip, .filtros .busca", { y: 10, autoAlpha: 0, stagger: .025, duration: .4, clearProps: "transform,opacity,visibility" }, "-=.4")
    .from(".corazon-btn", { scale: 0, rotation: -90, duration: .8, ease: "back.out(2)" }, "-=.6")
    .from(".h-dino", { y: 70, autoAlpha: 0, duration: .9, ease: "back.out(1.8)" }, "-=1.1")
    .from(".h-globo", { scale: 0, autoAlpha: 0, svgOrigin: "0 80", duration: .6, ease: "back.out(2.5)" }, "-=.4");
  contar($("#c-act")); contar($("#c-usadas"));

  // el dinosaurito saluda con la manita, rebota y de vez en cuando parpadea su globo
  gsap.to(".h-mano", { rotation: -28, svgOrigin: "40 -62", duration: .32, yoyo: true, repeat: -1, repeatDelay: .05, ease: "sine.inOut" });
  gsap.to(".h-dino", { y: -6, scaleY: 1.02, svgOrigin: "-6 252", duration: .9, yoyo: true, repeat: -1, ease: "sine.inOut", delay: 1.5 });
  gsap.to(".h-globo", { y: -5, duration: 1.6, yoyo: true, repeat: -1, ease: "sine.inOut", delay: 2 });
  // foto propia (img/nailong1.png): entra rebotando y se balancea como saludando
  gsap.from(".h-foto", { y: 80, autoAlpha: 0, duration: 1, delay: 1.2, ease: "back.out(1.8)" });
  gsap.to(".h-foto", { rotation: 5, duration: .5, yoyo: true, repeat: -1, ease: "sine.inOut", delay: 2.2 });
  gsap.to(".h-foto", { y: -8, duration: .9, yoyo: true, repeat: -1, ease: "sine.inOut", delay: 2.2 });

  // movimiento continuo y suave en la ilustración y las manchas del fondo
  gsap.to(".h-h1", { y: -8, duration: 2.6, yoyo: true, repeat: -1, ease: "sine.inOut", delay: 1.6 });
  gsap.to(".h-lapiz", { y: -10, rotation: 4, duration: 3, yoyo: true, repeat: -1, ease: "sine.inOut", delay: 1.6 });
  gsap.to(".h-sol", { scale: 1.06, transformOrigin: "50% 50%", duration: 3.4, yoyo: true, repeat: -1, ease: "sine.inOut" });
  gsap.to(".h-est", { y: -6, rotation: 12, transformOrigin: "50% 50%", duration: 1.8, yoyo: true, repeat: -1, stagger: .4, ease: "sine.inOut" });
  gsap.utils.toArray(".fondo i").forEach((b, i) => gsap.to(b, {
    x: [80, -90, 60][i], y: [60, 80, -70][i], scale: [1.15, .9, 1.2][i], duration: 12 + i * 3, yoyo: true, repeat: -1, ease: "sine.inOut" }));
  gsap.to(".hero-arte", { yPercent: 18, ease: "none", scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true } });

  document.querySelectorAll(".btn, .corazon-btn, .cerrar-carta").forEach((b) => magnetico(b, .25));
  // tarjetas: inclinación 3D al pasar el mouse (delegado, porque se re-pintan)
  const vistas = new WeakSet();
  document.addEventListener("mouseover", (e) => {
    const c = e.target.closest && e.target.closest(".tarj");
    if (c && !vistas.has(c)) { vistas.add(c); inclinar(c); }
  });
  animarTarjetas();
});

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
  if (anim()) {
    gsap.fromTo("#visor", { autoAlpha: 0 }, { autoAlpha: 1, duration: .3, clearProps: "opacity,visibility" });
    gsap.from(".vbar .env", { y: -24, autoAlpha: 0, duration: .5, ease: "power3.out", clearProps: "transform,opacity,visibility" });
    gsap.from("#pila .marco", { y: 50, autoAlpha: 0, duration: .7, stagger: .12, delay: .1, ease: "power3.out", clearProps: "transform,opacity,visibility" });
  }
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

/* ---- corazoncito secreto 💜 ---- */
const MENSAJES_AMOR = [
  {t:"¡Suerte, mi niña! 🍀", m:"Eres la mejor maestra, por ende te mereces todo…", e:"…pero primero, un asado del Bosco. 🥩🔥"},
  {t:"Oye, Mafer…", m:"Recuerda que tu novio te ama con todo su corazón y siempre va a estar ahí para apoyarte en todo lo que te propongas. 💪", e:"Eres increíblemente capaz, inteligente y dedicada. Cada hoja que preparas para tus alumnos demuestra lo mucho que te importa hacer las cosas bien. No lo olvides nunca. 🌻"},
  {t:"¡Hola, bonita! 🌸", m:"Solo pasaba a recordarte que eres la mejor maestra del mundo mundial y que estoy muy orgulloso de ti.", e:"Todo el esfuerzo que pones en tus clases vale muchísimo. Tus alumnos tienen mucha suerte de tenerte. Y yo, más. 💜"},
  {t:"Psst… un secreto:", m:"Hay alguien que piensa en ti todo el día y que te admira un montón. Pista: es tu novio. 😏", e:"Sigue brillando, Mafer. Cada día te vuelves más fuerte, más sabia y más increíble. Yo solo te echo porras desde aquí. 📣"},
  {t:"Recordatorio importante 📌", m:"Hoy, mañana y siempre: tu novio te ama, te apoya y cree en ti más que nadie en el mundo.", e:"Cuando sientas que algo se pone difícil, respira hondo y recuerda que no estás sola. Yo estoy contigo en cada paso. 💜"},
  {t:"Dato curioso 🧪", m:"Estudios confirman que Mafer es la persona más maravillosa del universo conocido. Fuente: su novio.", e:"También se descubrió que su dedicación y su corazón gigante la hacen imparable. Ningún lunes puede contra ella. 🚀"},
  {t:"Parte meteorológico ☀️", m:"Pronóstico para hoy: lluvia de besos, cielos despejados de problemas, y un 100% de probabilidad de que te amo.", e:"Temperatura emocional: cálida. Recomendación: seguir siendo la persona tan chida que eres. 🌈"},
  {t:"Mafer, mi amor 🌙", m:"Si estás leyendo esto en un día pesado: ya casi acabas, lo estás haciendo genial y al rato descansas.", e:"Y si estás leyendo esto en un día bueno: ¡qué bueno! Te mereces puros días así. Te quiero mucho. 💛"},
  {t:"Noticia de último minuto 📰", m:"Se reporta que cierta maestra increíble está haciendo un trabajo extraordinario. Vecinos aplauden. Su novio llora de orgullo.", e:"La afectada declaró: \"solo estoy haciendo mi trabajo\". Los expertos responden: \"ese es exactamente el punto\". 😂💜"},
];
(function(){
  const btn = $("#corazon"), ov = $("#carta-overlay"), cerrar = $("#cerrar-carta");
  const tit = $("#carta-titulo"), msg = $("#carta-msg"), ext = $("#carta-extra");
  let veces = 0;
  function chispas(){
    if (!window.gsap || !MOVER) return;
    const r = btn.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    const em = ["💜","✨","💖","🌸","⭐"];
    for (let i = 0; i < 16; i++) {
      const s = document.createElement("span");
      s.className = "chispa"; s.textContent = em[i % em.length];
      document.body.appendChild(s);
      const ang = Math.random() * Math.PI * 2, dist = 70 + Math.random() * 120;
      gsap.fromTo(s, { x: cx - 10, y: cy - 10, scale: .3, opacity: 1 },
        { x: cx - 10 + Math.cos(ang) * dist, y: cy - 10 + Math.sin(ang) * dist - 40, scale: 1 + Math.random() * .6,
          rotation: (Math.random() - .5) * 120, opacity: 0, duration: 1 + Math.random() * .5, ease: "power2.out",
          onComplete: () => s.remove() });
    }
  }
  function abrir(){
    // la primera vez siempre sale la nota nueva; después, al azar
    const m = veces++ === 0 ? MENSAJES_AMOR[0] : MENSAJES_AMOR[Math.floor(Math.random()*MENSAJES_AMOR.length)];
    tit.textContent = m.t; msg.textContent = m.m; ext.textContent = m.e;
    chispas();
    ov.classList.add("on"); ov.setAttribute("aria-hidden","false");
    if (window.gsap && MOVER) gsap.fromTo(".carta > *", { y: 14, opacity: 0 },
      { y: 0, opacity: 1, duration: .45, stagger: .07, delay: .1, ease: "power3.out", clearProps: "all" });
    if (window.gsap && MOVER) gsap.fromTo(".carta-dino", { y: 60, rotation: -20, scale: .6 },
      { y: 0, rotation: 0, scale: 1, duration: .8, delay: .25, ease: "elastic.out(1,.5)",
        onComplete: () => gsap.to(".carta-dino", { rotation: 6, duration: .45, yoyo: true, repeat: 5, ease: "sine.inOut" }) });
    cerrar.focus();
  }
  function cerrarModal(){ ov.classList.remove("on"); ov.setAttribute("aria-hidden","true"); btn.focus(); }
  btn.addEventListener("click", abrir);
  cerrar.addEventListener("click", cerrarModal);
  ov.addEventListener("click", e=>{ if(e.target===ov) cerrarModal(); });
  document.addEventListener("keydown", e=>{ if(e.key==="Escape" && ov.classList.contains("on")){ e.stopPropagation(); cerrarModal(); }}, true);
})();
