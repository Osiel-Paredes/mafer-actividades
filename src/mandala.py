import math

S = 900; C = S/2
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" fill="none" '
       f'stroke="#111" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">']

def pt(r, deg):
    a = math.radians(deg - 90)
    return C + r*math.cos(a), C + r*math.sin(a)

def circle(r): out.append(f'<circle cx="{C}" cy="{C}" r="{r}"/>')
def radial(r0, r1, n, off=0):
    for i in range(n):
        d = off + i*360/n
        x0,y0 = pt(r0,d); x1,y1 = pt(r1,d)
        out.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')

RADII = [46, 92, 150, 208, 268, 330, 400]
for r in RADII: circle(r)

# zonas por anillo: divisiones radiales
radial(RADII[0], RADII[1], 8, 22.5)
radial(RADII[1], RADII[2], 16, 0)
radial(RADII[2], RADII[3], 16, 11.25)
radial(RADII[3], RADII[4], 24, 0)
radial(RADII[4], RADII[5], 12, 15)
radial(RADII[5], RADII[6], 24, 0)

# petalos de arco en el anillo 150-208
n = 16
for i in range(n):
    d0 = i*360/n; d1 = (i+1)*360/n; dm = (d0+d1)/2
    x0,y0 = pt(RADII[2], d0); x1,y1 = pt(RADII[2], d1); xm,ym = pt(RADII[3]-6, dm)
    out.append(f'<path d="M{x0:.1f},{y0:.1f} Q{xm:.1f},{ym:.1f} {x1:.1f},{y1:.1f}"/>')

# rombos en el anillo 268-330
n = 12
for i in range(n):
    dm = 15 + i*360/n
    a,b = pt(268, dm); c,d = pt(299, dm-12); e,f = pt(330, dm); g,h = pt(299, dm+12)
    out.append(f'<path d="M{a:.1f},{b:.1f} L{c:.1f},{d:.1f} L{e:.1f},{f:.1f} L{g:.1f},{h:.1f} Z"/>')

# flor central
n = 8
for i in range(n):
    dm = i*360/n
    a,b = pt(46, dm); c,d = pt(24, dm+22.5); e,f = pt(46, dm+45)
    out.append(f'<path d="M{a:.1f},{b:.1f} Q{c:.1f},{d:.1f} {e:.1f},{f:.1f}"/>')
circle(16)

# corona exterior: triangulos
n = 24
for i in range(n):
    d0 = i*360/n; d1 = (i+1)*360/n; dm = (d0+d1)/2
    x0,y0 = pt(400, d0); x1,y1 = pt(400, d1); xm,ym = pt(432, dm)
    out.append(f'<path d="M{x0:.1f},{y0:.1f} L{xm:.1f},{ym:.1f} L{x1:.1f},{y1:.1f}"/>')

out.append('</svg>')
open('/home/oscarparedes/Documentos/actividades-secundaria/src/mandala.svg','w').write("\n".join(out))
print("zonas aprox:", 8+16+16+24+12+24+16+12+8, "| bytes:", len("\n".join(out)))
