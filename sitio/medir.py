# -*- coding: utf-8 -*-
"""Mide cada hoja de un documento con height:auto y avisa si se pasa de 279 mm (se recortaria al imprimir).

    python3 sitio/medir.py actividades-nuevas.html
"""
import os, re, subprocess, sys, tempfile

MAX_MM = 279.0
PX_MM = 96 / 25.4

src = os.path.abspath(sys.argv[1])
html = open(src).read()
sonda = """
<style>.hoja{height:auto!important;min-height:0!important;overflow:visible!important}</style>
<script>
window.addEventListener('load', function(){
  var o = [];
  document.querySelectorAll('.hoja').forEach(function(h, i){
    var t = h.querySelector('.tira h1');
    o.push(i + '\\t' + h.offsetHeight + '\\t' + (t ? t.textContent.trim() : '?'));
  });
  var pre = document.createElement('pre');
  pre.id = 'MEDIDAS';
  pre.textContent = o.join('\\n');
  document.body.appendChild(pre);
});
</script>
"""
html = html.replace("</head>", sonda + "</head>", 1)
tmp = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=os.path.dirname(src))
tmp.write(html); tmp.close()
try:
    r = subprocess.run(["timeout", "120", "google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
                        "--virtual-time-budget=8000", "--dump-dom", f"file://{tmp.name}"],
                       capture_output=True, text=True)
    dom = r.stdout
finally:
    os.unlink(tmp.name)

m = re.search(r'<pre id="MEDIDAS">(.*?)</pre>', dom, re.S)
if not m:
    print("no se pudo medir; revisa que google-chrome corra"); sys.exit(1)

malas = 0
for linea in m.group(1).strip().splitlines():
    i, px, tit = linea.split("\t")
    mm = int(px) / PX_MM
    flag = "SE PASA" if mm > MAX_MM + 0.5 else "ok     "
    if mm > MAX_MM + 0.5: malas += 1
    print(f"  {flag} {mm:6.1f} mm  hoja {int(i)+1:>2}  {tit[:52]}")
print(f"\n{malas} hoja(s) se pasan de {MAX_MM:.0f} mm" if malas else f"\ntodas caben en {MAX_MM:.0f} mm")
