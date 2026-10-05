"""Six vector explorations combining the retained rings with folded passages.

The supplied bitmap is a reference only and is not edited. The retained logo
masters remain intact. The vector contact sheet uses outlined type.
"""
from pathlib import Path
import math, html, re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT=Path(__file__).resolve().parent
BRAND=ROOT.parents[1]
INK='#121416';PAPER='#F4F1E9'
NAMES=['Pli discret','Passage croisé','Anneaux entrelacés','Nœud intérieur','Triple pli','Boucle repliée']

def arc(r,c=-56,gap=66):
    a=math.radians(c+gap/2);b=math.radians(c+360-gap/2)
    return f'M{64+r*math.cos(a):.3f} {64+r*math.sin(a):.3f} A{r} {r} 0 1 1 {64+r*math.cos(b):.3f} {64+r*math.sin(b):.3f}'

def path(d):return f'<path d="{d}"/>'
def wrapper(body,w=7):return f'<g fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="butt" stroke-linejoin="round">{body}</g>'

def points_path(p):return 'M'+' L'.join(f'{x:.3f} {y:.3f}' for x,y in p)

def ellipse(cx,cy,rx,ry,angle,start,end,n=300):
    rot=math.radians(angle);p=[]
    for i in range(n):
        t=math.radians(start+(end-start)*i/(n-1))
        x,y=rx*math.cos(t),ry*math.sin(t)
        p.append((cx+x*math.cos(rot)-y*math.sin(rot),cy+x*math.sin(rot)+y*math.cos(rot)))
    return p

def intersections(a,b):
    events=[]
    for i in range(len(a)-1):
        px,py=a[i];rx,ry=a[i+1][0]-px,a[i+1][1]-py
        for j in range(len(b)-1):
            qx,qy=b[j];sx,sy=b[j+1][0]-qx,b[j+1][1]-qy
            den=rx*sy-ry*sx
            if abs(den)<1e-8:continue
            t=((qx-px)*sy-(qy-py)*sx)/den
            u=((qx-px)*ry-(qy-py)*rx)/den
            if 0<=t<1 and 0<=u<1:
                if all(math.hypot(px+t*rx-x,py+t*ry-y)>3 for _,_,x,y in events):
                    events.append((i,j,px+t*rx,py+t*ry))
    return events

def weave_pair(a,b,prefix,extra=''):
    events=intersections(a,b)
    over=[]
    for k,(i,j,x,y) in enumerate(events):
        p,idx=(a,i) if k%2==0 else (b,j)
        over.append(points_path(p[max(0,idx-10):min(len(p),idx+12)]))
    base=path(points_path(a))+path(points_path(b))
    if not over:return wrapper(extra+base)
    mask=f'<defs><mask id="{prefix}" maskUnits="userSpaceOnUse" x="0" y="0" width="128" height="128"><rect width="128" height="128" fill="white"/>'
    mask+=''.join(f'<path d="{d}" fill="none" stroke="black" stroke-width="13"/>' for d in over)+'</mask></defs>'
    return mask+wrapper(extra+f'<g mask="url(#{prefix})">{base}</g>'+''.join(path(d) for d in over))

base=wrapper(path(arc(48))+path(arc(32,-12))+path(arc(16,32)))
variants=[]
variants.append(wrapper(path(arc(48))+path(arc(32,-12))+path('M79.7 61 C76 49 62 44 52 53 C43 62 48 77 60 80 C70 83 79 76 76 68 C74 61 66 60 59 63')))

fold='M79.5 66 C81 53 67 46 55 51 C44 55 42 73 52 78 C63 85 79 77 78 66 C75 54 60 59 50 65 C40 72 31 70 28 62'
over='M42 69 C37 72 31 70 28 62'
mask='<defs><mask id="crossing-02" maskUnits="userSpaceOnUse" x="0" y="0" width="128" height="128"><rect width="128" height="128" fill="white"/>'+f'<path d="{over}" fill="none" stroke="black" stroke-width="13"/></mask></defs>'
variants.append(mask+wrapper(path(arc(48))+f'<g mask="url(#crossing-02)">{path(arc(32,-12))}{path(fold)}</g>'+path(over)))

a=ellipse(61,61,32,23,-35,10,315)
b=ellipse(67,67,26,20,35,-20,270)
variants.append(weave_pair(a,b,'crossing-03',path(arc(48))))

kn=[]
for i in range(420):
    t=math.pi+.14+i/419*(2*math.pi-.28)
    kn.append((64+10.6*(math.sin(t)+2*math.sin(2*t)),64+10.6*(math.cos(t)-2*math.cos(2*t))))
events=[]
for i in range(len(kn)-1):
    for j in range(i+22,len(kn)-1):
        hit=intersections(kn[i:i+2],kn[j:j+2])
        for _,_,x,y in hit:
            if all(math.hypot(x-xx,y-yy)>4 for _,_,xx,yy in events):events.append((i,j,x,y))
over=[]
for i,j,x,y in events:
    t1=math.pi+.14+i/419*(2*math.pi-.28);t2=math.pi+.14+j/419*(2*math.pi-.28)
    idx=i if math.sin(3*t1)>math.sin(3*t2) else j
    over.append(points_path(kn[max(0,idx-9):min(len(kn),idx+11)]))
mask='<defs><mask id="crossing-04" maskUnits="userSpaceOnUse" x="0" y="0" width="128" height="128"><rect width="128" height="128" fill="white"/>'+''.join(f'<path d="{d}" fill="none" stroke="black" stroke-width="12.5"/>' for d in over)+'</mask></defs>'
variants.append(mask+wrapper(path(arc(48))+f'<g mask="url(#crossing-04)">{path(points_path(kn))}</g>'+''.join(path(d) for d in over),6.5))

# Three open curved passages repeat the reference's three-fold rhythm.
triple=[]
d='M64 17 C91 16 110 39 102 62 C96 81 72 91 56 79 C42 68 44 48 58 43'
for angle in [0,120,240]:triple.append(f'<g transform="rotate({angle} 64 64)">{path(d)}</g>')
variants.append(wrapper(''.join(triple),7))

# Two open return curves suggest a folded band with an explicit overpass.
a=ellipse(64,64,47,38,-28,-57,267)
b=ellipse(64,64,27,40,34,20,320)
variants.append(weave_pair(a,b,'crossing-06'))

def svg(body,w=128,h=128,color=INK,title='APORIA'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" color="{color}" role="img"><title>{html.escape(title)}</title>{body}</svg>'
for i,(name,body) in enumerate(zip(NAMES,variants),1):
    for suffix,color in [('dark',INK),('light',PAPER)]:
        (ROOT/'assets'/f'variante-{i:02d}-{suffix}.svg').write_text(svg(body,color=color,title=f'APORIA — {name}'))
(ROOT/'assets'/'reference-retenue.svg').write_text(svg(base,title='APORIA — Divergent Apertures / référence retenue'))

font=TTFont(BRAND/'assets/fonts/SourceSans3-Regular.otf')
bold=TTFont(BRAND/'assets/fonts/SourceSans3-Semibold.otf')
def lettering(text,size,x,y,strong=False):
    f=bold if strong else font;gs=f.getGlyphSet();cmap=f.getBestCmap();scale=size/f['head'].unitsPerEm;cursor=x;parts=[]
    for c in text:
        name=cmap.get(ord(c))
        if not name:continue
        pen=SVGPathPen(gs);gs[name].draw(TransformPen(pen,(scale,0,0,-scale,cursor,y)));parts.append(pen.getCommands());cursor+=f['hmtx'][name][0]*scale
    return '<path d="'+' '.join(parts)+'" fill="currentColor"/>'

sheet=[f'<rect width="1600" height="1110" fill="{PAPER}"/>']
sheet.append(lettering('APORIA / ANNEAUX × PLIS',28,55,64,True))
sheet.append(lettering('Six variantes minimalistes. Le logo actuel reste la référence.',21,55,102))
sheet.append(f'<g transform="translate(1205 26) scale(.72)">{base}</g>')
sheet.append(lettering('Référence retenue',17,1315,73,True))
sheet.append(lettering('Divergent Apertures',16,1315,97))
for i,(name,body) in enumerate(zip(NAMES,variants)):
    x=55+(i%3)*513;y=152+(i//3)*457
    sheet.append(f'<path d="M{x} {y}H{x+464}" stroke="#D1CDC3"/>')
    sheet.append(lettering(f'{i+1:02d}',18,x,y+38))
    sheet.append(f'<g transform="translate({x+112} {y+59}) scale(1.85)">{body}</g>')
    sheet.append(lettering(name,24,x,y+362,True))
    notes=['Anneaux conservés · pli intérieur','Anneaux conservés · un passage','Deux boucles entrelacées','Un anneau · une boucle nouée','Trois chemins repliés','Deux anneaux · inversion de plan']
    sheet.append(lettering(notes[i],18,x,y+396))
sheet.append(lettering('Exploration de symbole / monochrome / 4 octobre 2026',16,55,1080))
(ROOT/'variantes.svg').write_text(svg(''.join(sheet),1600,1110,title='APORIA — six variantes anneaux × plis'))

# The review surface shows symbols only, with no additional brand material.
cards=[]
for i,(name,body) in enumerate(zip(NAMES,variants),1):
    icon=svg(body,title=name).replace('color="#121416"','class="symbol"')
    cards.append(f'<figure><div class="drawing">{icon}</div><figcaption><span>{i:02d}</span> {html.escape(name)}<a href="assets/variante-{i:02d}-dark.svg" download aria-label="Télécharger {html.escape(name)} en SVG">SVG ↗</a></figcaption></figure>')
css='''
@font-face{font-family:Source Sans;src:url(../../assets/fonts/SourceSans3-Regular.woff2)}
@font-face{font-family:Source Sans;src:url(../../assets/fonts/SourceSans3-Semibold.woff2);font-weight:600}
*{box-sizing:border-box}body{margin:0;padding:40px;background:#F4F1E9;color:#121416;font-family:Source Sans,sans-serif;font-size:16px;line-height:1.5}main{max-width:1440px;margin:auto}header{display:flex;justify-content:space-between;align-items:center;gap:32px;padding:12px 0 30px;border-bottom:1px solid #76736C}h1{font-size:28px;font-weight:600;margin:0 0 8px}p{margin:0}.reference{display:flex;align-items:center;gap:18px;font-size:15px}.reference img{width:78px;height:78px}.reference strong{font-weight:600}.tools{display:flex;gap:14px;align-items:center;flex-wrap:wrap;padding:26px 0}button,select{font:inherit;border:1px solid #76736C;padding:9px 16px;border-radius:3px;background:transparent;color:inherit}button{cursor:pointer}select{max-width:170px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}figure{margin:0;border-top:1px solid #D1CDC3;padding:16px 0 26px}.drawing{height:285px;display:flex;align-items:center;justify-content:center}.symbol{width:var(--symbol-size,200px);height:var(--symbol-size,200px);max-width:100%;display:block}figcaption{display:flex;gap:15px;align-items:center;font-size:18px;padding:12px 0}figcaption span{font-size:14px;color:#596168}figcaption a{margin-left:auto;font-size:14px;color:inherit;text-underline-offset:3px}footer{border-top:1px solid #D1CDC3;padding:25px 0;font-size:14px;display:flex;justify-content:space-between;gap:20px}footer a{color:inherit;text-underline-offset:3px}a:focus-visible,button:focus-visible,select:focus-visible{outline:2px solid #24636C;outline-offset:4px}body[data-theme="dark"]{background:#121416;color:#F4F1E9}body[data-theme="dark"] figure,body[data-theme="dark"] footer{border-color:#353B42}body[data-theme="dark"] button,body[data-theme="dark"] select{border-color:#747E88}body[data-theme="dark"] select option{background:#121416;color:#F4F1E9}body[data-theme="dark"] figcaption span{color:#B4BBC2}body[data-theme="dark"] .reference img{filter:invert(1)}@media(max-width:800px){body{padding:24px}.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.drawing{height:235px}.symbol{width:var(--symbol-size,150px);height:var(--symbol-size,150px)}header{align-items:flex-start;flex-direction:column;gap:20px}figcaption{flex-wrap:wrap;font-size:16px}footer{flex-direction:column}}@media(max-width:450px){.grid{grid-template-columns:1fr}.drawing{height:250px}}
'''
script='''<script>document.getElementById('theme').addEventListener('click',e=>{const dark=document.body.dataset.theme!=='dark';document.body.dataset.theme=dark?'dark':'light';e.target.setAttribute('aria-pressed',String(dark));e.target.textContent=dark?'Fond papier':'Fond obsidienne'});document.getElementById('size').addEventListener('change',e=>document.documentElement.style.setProperty('--symbol-size',e.target.value+'px'));</script>'''
doc=f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>APORIA — variantes anneaux × plis</title><style>{css}</style></head><body><main><header><div><h1>Anneaux × plis</h1><p>Six variantes minimalistes.</p></div><div class="reference"><img src="assets/reference-retenue.svg" alt="Logo actuel Divergent Apertures"><div><strong>Référence retenue</strong><br>Divergent Apertures</div></div></header><div class="tools"><button type="button" id="theme" aria-pressed="false">Fond obsidienne</button><label for="size">Taille du symbole</label><select id="size"><option value="200">200 px</option><option value="64">64 px</option><option value="24">24 px</option></select></div><div class="grid">'+''.join(cards)+'</div><footer><span>Explorations de symbole · le logo retenu est conservé.</span><a href="variantes.svg" download>Planche SVG ↗</a></footer></main>'+script+'</body></html>'
(ROOT/'index.html').write_text(doc)
print('Six variantes SVG et une planche comparative créées.')
