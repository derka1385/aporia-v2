"""Build the APORIA proposal assets. Uses fontTools for outlined type / WOFF2.

Run with fontTools + Brotli available. All geometry is authored here; examples
are illustrations, never model-generated research records.
"""
from pathlib import Path
import math, json, re, html, random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
LOGOS = ASSETS / 'logos'
VISUALS = ASSETS / 'visuals'
FONTDIR = ASSETS / 'fonts'
PALETTE = {
    'obsidian':'#121416','paper':'#F4F1E9','surface-dark':'#1B1F23',
    'surface-light':'#E9E5DB','graphite':'#383D43',
    'text-secondary-dark':'#B4BBC2','text-secondary-light':'#596168',
    'rule-dark':'#353B42','rule-light':'#D1CDC3',
    'boundary-dark':'#747E88','boundary-light':'#76736C',
    'iris-dark':'#B7A2E8','iris-light':'#65509A',
    'cyan-dark':'#79C5CF','cyan-light':'#24636C',
    'amber-dark':'#DDB16B','amber-light':'#805B22',
}
NAMES = ['Shared Aperture','Divergent Apertures','Displaced Orbits','Counter-Orbits',
         'Forked Trajectory','Segmented Inquiry','Common Tangent','Delta Cut',
         'Discrete Field','Return Trace']

def point(cx,cy,r,a):
    a=math.radians(a)
    return cx+r*math.cos(a),cy+r*math.sin(a)

def arc(cx,cy,r,a,b):
    x1,y1=point(cx,cy,r,a); x2,y2=point(cx,cy,r,b)
    return f'<path d="M{x1:.3f} {y1:.3f} A{r} {r} 0 {int(b-a>180)} 1 {x2:.3f} {y2:.3f}"/>'

def opened(cx,cy,r,center,width):
    return arc(cx,cy,r,center+width/2,center+360-width/2)

def mark(index,micro=False):
    w=7
    if index==1:
        body=''.join(opened(64,64,r,0,58) for r in [48,32,16])
    elif index==2:
        if micro:
            w=10
            body=opened(64,64,46,-40,88)+opened(64,64,23,20,88)
        else:
            body=''.join(opened(64,64,r,c,66) for r,c in zip([48,32,16],[-56,-12,32]))
    elif index==3:
        body=''.join(opened(cx,cy,r,c,72) for cx,cy,r,c in [(60,64,47,-42),(66,66,31,4),(72,68,15,45)])
    elif index==4:
        w=9
        body=opened(64,64,47,0,78)+opened(64,64,25,180,78)
    elif index==5:
        body=arc(64,64,46,80,300)+arc(64,64,27,80,300)
        body+='<path d="M87 24.16 C95 17 104 18 112 25 M87 24.16 C100 34 102 48 97 57"/>'
    elif index==6:
        body=''.join(arc(64,64,r,a,b) for r,segs in [(48,[(25,155),(185,335)]),(32,[(65,210),(240,385)]),(16,[(10,135),(180,305)])] for a,b in segs)
    elif index==7:
        body=''.join(opened(16+r,70,r,-65,92) for r in [45,31,17])
    elif index==8:
        # Interrupt all bands with a diagonal strip defined in the symbol coordinates.
        body='<defs><clipPath id="delta-cut"><path d="M0 0 H128 V128 H0 Z M65 0 H75 L102 128 H92 Z" clip-rule="evenodd" fill-rule="evenodd"/></clipPath></defs>'
        body+='<g clip-path="url(#delta-cut)">'+''.join(f'<circle cx="64" cy="64" r="{r}"/>' for r in [48,32,16])+'</g>'
    elif index==9:
        dots=[]
        for r,n,c in [(48,27,-56),(32,19,-12),(16,10,32)]:
            for k in range(n):
                a=k*360/n
                diff=abs((a-c+180)%360-180)
                if diff<38: continue
                x,y=point(64,64,r,a)
                dots.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.25" fill="currentColor" stroke="none"/>')
        body=''.join(dots)
    elif index==10:
        pts=[]
        for k in range(420):
            a=math.radians(-55+k/419*790); r=49-k/419*37
            pts.append((64+r*math.cos(a),64+r*math.sin(a)))
        body='<path d="M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in pts)+'"/>'
    return f'<g fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="butt" stroke-linejoin="round">{body}</g>'

def svg(body, width=128, height=128, color='#121416', title='APORIA'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" color="{color}" role="img"><title>{html.escape(title)}</title>{body}</svg>'

def inline(index=2,cls='',micro=False):
    return f'<svg viewBox="0 0 128 128" class="{cls}" role="img" aria-label="{NAMES[index-1]}">{mark(index,micro)}</svg>'

fonts={}
for path in FONTDIR.glob('*'):
    if path.suffix in ['.otf','.ttf']:
        f=TTFont(path)
        fonts[path.stem]=f
        f.flavor='woff2'; f.save(path.with_suffix('.woff2')); f.flavor=None

def typepath(text,size=18,x=0,y=20,font='SourceSans3-Regular',tracking=0):
    f=fonts[font]; gs=f.getGlyphSet(); cmap=f.getBestCmap()
    scale=size/f['head'].unitsPerEm; cursor=x; parts=[]
    for c in text:
        name=cmap.get(ord(c))
        if name is None: continue
        pen=SVGPathPen(gs)
        trans=TransformPen(pen,(scale,0,0,-scale,cursor,y))
        gs[name].draw(trans)
        parts.append(pen.getCommands())
        cursor += f['hmtx'][name][0]*scale+tracking
    return '<path d="'+' '.join(parts)+'" fill="currentColor"/>', cursor-x-tracking

for i,name in enumerate(NAMES,1):
    slug=re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-')
    (LOGOS/f'concept-{i:02d}-{slug}.svg').write_text(svg(mark(i),title=f'APORIA / {name}'))
for variant,color in [('dark',PALETTE['obsidian']),('light',PALETTE['paper'])]:
    (LOGOS/f'symbol-{variant}.svg').write_text(svg(mark(2),color=color,title='APORIA / standard symbol'))
    (LOGOS/f'symbol-micro-{variant}.svg').write_text(svg(mark(2,True),color=color,title='APORIA / micro symbol'))
    word,width=typepath('APORIA',56,166,85,'SourceSans3-Semibold',6.16)
    (LOGOS/f'lockup-horizontal-{variant}.svg').write_text(svg(mark(2)+word,int(width+166+24),128,color,'APORIA / horizontal lockup'))
    word,width=typepath('APORIA',46,0,0,'SourceSans3-Semibold',5.06)
    stack=f'<g transform="translate(96 8)">{mark(2)}</g><g transform="translate({(320-width)/2:.3f} 205)">{word}</g>'
    (LOGOS/f'lockup-stacked-{variant}.svg').write_text(svg(stack,320,240,color,'APORIA / stacked lockup'))
    word,width=typepath('APORIA',56,20,67,'SourceSans3-Semibold',6.16)
    (LOGOS/f'wordmark-{variant}.svg').write_text(svg(word,int(width+40),92,color,'APORIA / wordmark'))

icon_scale=640/103
icon_offset=(1024-128*icon_scale)/2
icon=f'<rect width="1024" height="1024" fill="{PALETTE["obsidian"]}"/><g transform="translate({icon_offset:.3f} {icon_offset:.3f}) scale({icon_scale:.5f})">{mark(2)}</g>'
(LOGOS/'app-icon.svg').write_text(svg(icon,1024,1024,PALETTE['paper'],'APORIA / app icon'))
for size in [16,32,48]:
    body=f'<rect width="128" height="128" fill="{PALETTE["obsidian"]}"/>'+mark(2,size==16)
    content=svg(body,color=PALETTE['paper'],title='APORIA favicon').replace('width="128" height="128"','width="'+str(size)+'" height="'+str(size)+'"',1)
    (LOGOS/f'favicon-{size}.svg').write_text(content)
adaptive='<style>:root{color:#121416}.field{fill:#F4F1E9}@media(prefers-color-scheme:dark){:root{color:#F4F1E9}.field{fill:#121416}}</style><rect class="field" width="128" height="128"/>'+mark(2,True)
(LOGOS/'favicon-adaptive.svg').write_text(svg(adaptive,title='APORIA adaptive favicon'))

# A vector contact sheet: every letter is outlined, so it is portable.
sheet=['<rect width="1600" height="850" fill="#F4F1E9"/>']
title,_=typepath('APORIA',24,50,53,'SourceSans3-Semibold',2.64); sheet.append(title)
sub,_=typepath('Ten constructions. One open question.',21,50,91,'SourceSerif4-Regular'); sheet.append(sub)
for i,name in enumerate(NAMES,1):
    col=(i-1)%5; row=(i-1)//5; x=50+col*303; y=140+row*333
    sheet.append(f'<path d="M{x} {y}H{x+282}" stroke="#D1CDC3"/>')
    num,_=typepath(f'{i:02d}',13,x,y+31,'IBMPlexMono-Regular'); sheet.append(num)
    if i==2:
        label,_=typepath('RECOMMENDED',11,x+120,y+31,'IBMPlexMono-Regular');sheet.append(f'<g color="#65509A">{label}</g>')
    sheet.append(f'<g transform="translate({x+68} {y+58}) scale(1.1)">{mark(i)}</g>')
    namepath,_=typepath(name,19,x,y+240,'SourceSans3-Semibold');sheet.append(namepath)
    captions=['Aligned gaps','Staggered gaps','Offset centers','Opposing arcs','One path, two branches','Phased segments','Shared contact','Diagonal interruption','Sampled point rings','One continuous path']
    cap,_=typepath(captions[i-1],14,x,y+266);sheet.append(cap)
foot,_=typepath('Vector concept studies / monochrome / 04 October 2026',13,50,812,'IBMPlexMono-Regular');sheet.append(foot)
(VISUALS/'logo-contact-sheet.svg').write_text(svg(''.join(sheet),1600,850,title='APORIA / ten logo directions'))

# Deterministic surface of a folded trefoil, derived from the product's geometric
# family. Colors illustrate regional states; there is no research-data binding.
def particle_svg(mode='exploration',width=960,height=660):
    rand=random.Random(9719)
    pts=[]
    def center(u):
        r=1.17+.36*math.cos(3*u)
        return (r*math.cos(2*u),r*math.sin(2*u),.61*math.sin(3*u))
    def norm(v):
        m=math.sqrt(sum(x*x for x in v));return tuple(x/m for x in v)
    def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
    for a in range(275):
        u=2*math.pi*(a+rand.random()*.6)/275
        c=center(u);cn=center(u+.005)
        t=norm(tuple(cn[k]-c[k] for k in range(3)))
        n=norm((math.cos(2*u),math.sin(2*u),0));b=norm(cross(t,n));n=norm(cross(b,t))
        for j in range(31):
            v=(j+rand.random()*.6)/31*2*math.pi
            tube=.32+.09*math.sin(u*3+1.4)+.04*math.sin(v*3+u*5)
            if mode=='concentration':tube*=.78
            p=[c[k]+tube*(n[k]*math.cos(v)+b[k]*math.sin(v)) for k in range(3)]
            region=max(0,math.cos(u-1))**12
            if mode=='conflict':p[0]+=.38*math.sin(3*u);p[2]+=.24*math.cos(3*u)
            if mode=='uncertainty':p=[z+(rand.random()-.5)*.13 for z in p]
            if mode=='rejection' and region>.3 and j%3==0:continue
            # Camera rotations keep the object folded and asymmetrical.
            x,y,z=p
            rx=.72;ry=-.28;rz=-.22
            y,z=y*math.cos(rx)-z*math.sin(rx),y*math.sin(rx)+z*math.cos(rx)
            x,z=x*math.cos(ry)+z*math.sin(ry),-x*math.sin(ry)+z*math.cos(ry)
            x,y=x*math.cos(rz)-y*math.sin(rz),x*math.sin(rz)+y*math.cos(rz)
            scale=min(width*.245,height*.36)*(5.7/(5.7-z))
            px=width/2+x*scale;py=height/2-y*scale
            col=PALETTE['cyan-dark'] if math.sin(u*2)>.3 else PALETTE['iris-dark']
            if mode=='concentration':col=PALETTE['paper']
            if mode=='conflict' and math.sin(3*u)>.4:col=PALETTE['amber-dark']
            if mode=='insight' and region>.1:col=PALETTE['amber-dark'] if region<.5 else PALETTE['paper']
            if mode=='uncertainty':col=PALETTE['text-secondary-dark']
            if mode=='rejection' and region>.2:col=PALETTE['text-secondary-dark']
            opacity=.32+.55*rand.random(); radius=.55+.36*rand.random()
            pts.append((z,f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{radius:.2f}" fill="{col}" opacity="{opacity:.2f}"/>'))
    body=f'<rect width="{width}" height="{height}" fill="#121416"/>'+''.join(p[1] for p in sorted(pts))
    return svg(body,width,height,title=f'APORIA / illustrative {mode} particle geometry')
for state in ['exploration','concentration','conflict','uncertainty','insight','rejection']:
    (VISUALS/f'particle-{state}.svg').write_text(particle_svg(state))

def luminance(hexcolor):
    rgb=[int(hexcolor[i:i+2],16)/255 for i in [1,3,5]]
    rgb=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in rgb]
    return sum(c*k for c,k in zip(rgb,[.2126,.7152,.0722]))
def contrast(a,b):
    x,y=sorted([luminance(a),luminance(b)],reverse=True)
    return (x+.05)/(y+.05)
rows=[]
for name,fg,bg,threshold in [
    ('Primary dark','paper','obsidian',4.5),('Primary light','obsidian','paper',4.5),
    ('Secondary dark','text-secondary-dark','obsidian',4.5),('Secondary light','text-secondary-light','paper',4.5),
    ('Secondary dark surface','text-secondary-dark','surface-dark',4.5),('Secondary paper surface','text-secondary-light','surface-light',4.5),
    *[(f'{s} / dark',s+'-dark','obsidian',4.5) for s in ['iris','cyan','amber']],
    *[(f'{s} / paper',s+'-light','paper',4.5) for s in ['iris','cyan','amber']],
    *[(f'{s} / instrument surface',s+'-dark','surface-dark',4.5) for s in ['iris','cyan','amber']],
    *[(f'{s} / paper surface',s+'-light','surface-light',4.5) for s in ['iris','cyan','amber']],
    ('Boundary dark','boundary-dark','obsidian',3),('Boundary dark surface','boundary-dark','surface-dark',3),
    ('Boundary paper','boundary-light','paper',3),('Boundary paper surface','boundary-light','surface-light',3),
]:
    ratio=contrast(PALETTE[fg],PALETTE[bg]);assert ratio>=threshold,(name,ratio)
    rows.append((name,PALETTE[fg],PALETTE[bg],ratio,threshold))
report='# APORIA contrast report\n\nComputed from final hexadecimal sRGB values using WCAG relative luminance. Rounded ratios are displayed; pass/fail uses the unrounded value.\n\n| Pairing | Foreground | Background | Ratio | Minimum |\n| --- | --- | --- | --- | --- |\n'
for name,fg,bg,ratio,threshold in rows:report+=f'| {name} | {fg} | {bg} | {ratio:.2f}:1 | {threshold}:1 |\n'
report+='\nAll prescribed pairs pass their stated threshold at full opacity. Fine decorative rules are deliberately excluded; they must not serve as interactive boundaries or the sole indication of a state. Recheck composed components, imagery, hover states and opacity during product integration. These calculations do not claim a complete accessibility audit.\n\nSources: [W3C text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) and [W3C non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).\n'
(ROOT/'CONTRAST.md').write_text(report)

tokens={
  'name':'APORIA / Divergent Apertures','status':'proposed','primitive':PALETTE,
  'semantic':{
    'dark':{'background':'{obsidian}','surface':'{surface-dark}','text':'{paper}','textSecondary':'{text-secondary-dark}','rule':'{rule-dark}','boundary':'{boundary-dark}','reasoning':'{iris-dark}','exploration':'{cyan-dark}','event':'{amber-dark}','focus':'{cyan-dark}'},
    'light':{'background':'{paper}','surface':'{surface-light}','text':'{obsidian}','textSecondary':'{text-secondary-light}','rule':'{rule-light}','boundary':'{boundary-light}','reasoning':'{iris-light}','exploration':'{cyan-light}','event':'{amber-light}','focus':'{cyan-light}'},
  },
  'typography':{'editorial':'Source Serif 4','interface':'Source Sans 3','research':'IBM Plex Mono'},
  'spacing':[4,8,12,16,24,32,48,64,96,128],
  'radius':{'control':4,'containedSpecimen':8},
  'logo':{'center':[64,64],'radii':[48,32,16],'stroke':7,'gapDegrees':66,'gapCentersDegrees':[-56,-12,32],'clearSpace':24},
}
(ROOT/'tokens.json').write_text(json.dumps(tokens,indent=2)+'\n')
css=':root {\n'+''.join(f'  --aporia-{k}: {v};\n' for k,v in PALETTE.items())+'}\n'
for theme,mapping in tokens['semantic'].items():
    css+=f'[data-aporia-theme="{theme}"] {{\n'+''.join(f'  --{k}: var(--aporia-{v[1:-1]});\n' for k,v in mapping.items())+'}\n'
(ROOT/'tokens.css').write_text(css)

# A deliberately small Markdown renderer keeps the saved proposal authoritative.
def fmt(s):
    s=html.escape(s)
    s=re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',r'<a href="\2">\1</a>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    return s
def markdown(s):
    lines=s.strip().splitlines();out=[];i=0
    while i<len(lines):
        line=lines[i]
        if not line.strip():i+=1;continue
        if line.startswith('|'):
            table=[]
            while i<len(lines) and lines[i].startswith('|'):
                row=[x.strip() for x in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r'[- :]+',x) for x in row):table.append(row)
                i+=1
            out.append('<div class="table-scroll" tabindex="0"><table><thead><tr>'+''.join('<th scope="col">'+fmt(x)+'</th>' for x in table[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+fmt(x)+'</td>' for x in row)+'</tr>' for row in table[1:])+'</tbody></table></div>')
            continue
        if re.match(r'^\d+\. ',line):
            vals=[]
            while i<len(lines) and re.match(r'^\d+\. ',lines[i]):
                vals.append(re.sub(r'^\d+\. ','',lines[i]));i+=1
            out.append('<ol>'+''.join('<li>'+fmt(x)+'</li>' for x in vals)+'</ol>');continue
        if line.startswith('### '):out.append('<h3>'+fmt(line[4:])+'</h3>');i+=1;continue
        if line.startswith('#'):i+=1;continue
        para=[]
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('|','#')):
            para.append(lines[i]);i+=1
        out.append('<p>'+fmt(' '.join(para))+'</p>')
    return '\n'.join(out)

COMMON_CSS='''
@font-face{font-family:Serif;src:url(assets/fonts/SourceSerif4-Regular.woff2)}
@font-face{font-family:Display;src:url(assets/fonts/SourceSerif4Display-Regular.woff2)}
@font-face{font-family:Serif;src:url(assets/fonts/SourceSerif4-It.woff2);font-style:italic}
@font-face{font-family:Sans;src:url(assets/fonts/SourceSans3-Regular.woff2);font-weight:400}
@font-face{font-family:Sans;src:url(assets/fonts/SourceSans3-Semibold.woff2);font-weight:600}
@font-face{font-family:Mono;src:url(assets/fonts/IBMPlexMono-Regular.woff2)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#F4F1E9;color:#121416;font-family:Sans,Arial,sans-serif;font-size:18px;line-height:1.55}
a{color:inherit;text-underline-offset:4px}button{font:inherit;cursor:pointer}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,[tabindex]:focus-visible{outline:2px solid #24636C;outline-offset:4px}
.mono{font-family:Mono,monospace;font-size:12px;letter-spacing:.025em}.word{font-weight:600;letter-spacing:.11em}.rule{border-top:1px solid #D1CDC3}.muted{color:#596168}.tag{font-family:Mono,monospace;font-size:12px;letter-spacing:.03em}.dark{background:#121416;color:#F4F1E9}.dark .muted{color:#B4BBC2}.dark a:focus-visible,.dark button:focus-visible{outline-color:#79C5CF}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:22px 4vw;border-bottom:1px solid #D1CDC3}.mini-lockup{display:flex;align-items:center;gap:14px;font-size:21px}.mini-lockup svg{width:36px;height:36px}.topbar .mono{color:#596168}
h1,h2,h3{font-weight:400}h1,h2{font-family:Display,Georgia,serif}p{margin:0 0 18px}svg{display:block}img{max-width:100%;display:block} @media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''
BOOK_CSS='''
.cover{display:grid;grid-template-columns:1.25fr 1fr;padding:100px 6vw 84px;gap:70px;align-items:center;min-height:760px}.cover .eyebrow{color:#596168;margin-bottom:30px}.cover h1{font-size:clamp(58px,5.4vw,86px);line-height:1.05;letter-spacing:-.035em;margin:0 0 30px;max-width:750px}.cover p{font-size:20px;max-width:500px}.cover .signature{width:300px;margin:auto}.cover .signature-note{margin-top:28px;text-align:center;font-family:Mono;font-size:12px;color:#596168}.cover-bottom{grid-column:1/-1;display:flex;justify-content:space-between;margin-top:24px;padding-top:26px;border-top:1px solid #D1CDC3}
.book{display:grid;grid-template-columns:230px minmax(0,1fr);max-width:1440px;margin:auto;padding:0 48px;gap:60px}.toc{position:sticky;top:20px;align-self:start;font-size:15px;padding:20px 0 30px;max-height:96vh;overflow:auto}.toc strong{display:block;margin-bottom:15px}.toc a{display:block;text-decoration:none;color:#596168;line-height:1.4;padding:6px 0}.toc a:hover{color:#121416}.toc .num{font-family:Mono;font-size:12px;display:inline-block;width:25px}.chapter{padding:72px 0;border-top:1px solid #D1CDC3;scroll-margin-top:24px}.chapter>.index{color:#596168;margin-bottom:15px}.chapter h2{font-size:44px;line-height:1.13;letter-spacing:-.02em;margin:0 0 32px}.chapter h3{font-family:Serif;font-size:26px;line-height:1.3;margin:32px 0 16px}.chapter strong{font-weight:600}.chapter p{max-width:76ch}.chapter ol{padding-left:24px}.chapter li{padding:0 0 16px 8px}.table-scroll{overflow:auto;margin:28px 0 32px}table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.5;min-width:600px}th{text-align:left;font-weight:600;border-bottom:1px solid #76736C;padding:12px 15px 12px 0}td{vertical-align:top;border-bottom:1px solid #D1CDC3;padding:14px 15px 14px 0}td:first-child{min-width:138px}
.visual-panel{margin:30px 0 38px}.concept{display:grid;grid-template-columns:230px minmax(0,1fr);gap:30px;border-top:1px solid #D1CDC3;padding-top:30px;margin-top:36px}.concept .symbol{background:#E9E5DB;display:flex;align-items:center;justify-content:center;height:230px}.concept .symbol svg{width:150px;height:150px}.concept h3{font-family:Sans;font-weight:600;font-size:22px;margin:0 0 14px}.concept p{font-size:16px;line-height:1.55}.recommend .symbol{background:#121416;color:#F4F1E9}.logo-tools{display:flex;align-items:center;gap:16px;flex-wrap:wrap;padding:20px 0}.logo-tools button,.logo-tools select{background:transparent;color:#121416;border:1px solid #76736C;border-radius:3px;padding:8px 14px;font-family:Sans;font-size:14px}.scale-strip{display:flex;gap:32px;align-items:center;margin:20px 0 38px;padding:28px;border:1px solid #D1CDC3;overflow:auto}.scale-strip svg{flex:none}.scale-strip span{font-size:12px}.concepts[data-mode="dark"] .symbol{background:#121416;color:#F4F1E9}.concepts[data-mode="light"] .symbol{background:#E9E5DB;color:#121416}.concepts .symbol svg{width:var(--preview-size,150px);height:var(--preview-size,150px)}
.swatches{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:28px 0}.swatch-color{height:100px;border:1px solid #76736C}.swatch p{font-size:14px;margin:10px 0 0}.swatch code{font-family:Mono;font-size:12px}.particle-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:28px 0}.particle-grid figure{margin:0;background:#121416;color:#F4F1E9}.particle-grid figcaption{font-family:Mono;font-size:12px;padding:10px 15px;border-top:1px solid #353B42}.specimen{padding:50px;margin:28px 0;background:#E9E5DB}.specimen .serif{font-family:Display;font-size:52px;line-height:1.15;letter-spacing:-.02em}.specimen .sans{font-family:Sans;font-size:24px;margin-top:30px}.specimen .data{font-family:Mono;font-size:14px;margin-top:22px;color:#596168}.app-row{display:flex;flex-wrap:wrap;gap:28px;align-items:center;margin:32px 0}.app-row img{width:150px}.app-row svg{width:120px}.caption{font-family:Mono;font-size:12px;color:#596168;margin-top:12px}.footer{padding:50px 4vw;border-top:1px solid #D1CDC3;display:flex;justify-content:space-between;font-size:14px}.download{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}.download a{border:1px solid #76736C;border-radius:3px;text-decoration:none;padding:10px 16px;font-size:14px}
@media(max-width:1100px){.book{grid-template-columns:170px minmax(0,1fr);gap:32px;padding:0 30px}.concept{grid-template-columns:160px minmax(0,1fr);gap:20px}.concept .symbol{height:180px}.cover{gap:20px;padding:70px 5vw}.cover .signature{width:220px}}
@media(max-width:760px){.topbar{padding:18px 22px}.topbar>.mono{font-size:12px;max-width:160px;text-align:right}.topbar .mini-lockup{flex:none}.cover{display:block;min-height:auto;padding:55px 24px 40px}.cover h1{font-size:56px}.cover p{font-size:18px}.cover .signature{width:160px;margin:50px auto 20px}.cover .signature-note{margin-bottom:40px}.cover-bottom{display:block;font-size:12px}.cover-bottom>span{display:block;margin-top:12px}.book{display:block;padding:0 24px}.toc{position:static;max-height:none;display:grid;grid-template-columns:1fr 1fr;column-gap:16px;border-top:1px solid #D1CDC3;padding:25px 0}.toc strong{grid-column:1/-1}.toc a{font-size:14px}.chapter{padding:45px 0}.chapter h2{font-size:36px}.concept{display:block}.concept .symbol{height:230px;margin-bottom:24px}.swatches{grid-template-columns:repeat(2,1fr)}.particle-grid{grid-template-columns:repeat(2,1fr)}.specimen{padding:25px}.specimen .serif{font-size:38px}.footer{display:block;padding:30px 24px}.footer>span{display:block;margin-bottom:10px}}
@media print{.topbar,.toc,.logo-tools,.download{display:none}.cover{min-height:0;padding:25px;break-after:page}.cover h1{font-size:55px}.cover .signature{width:180px}.book{display:block;padding:0}.chapter{padding:25px 0;break-before:page}.chapter h2{font-size:32px}.chapter p,.chapter li{font-size:11pt}.concept{break-inside:avoid}.table-scroll{overflow:visible}table{min-width:0;font-size:9pt}.concept p{font-size:10pt}.particle-grid,.swatches{break-inside:avoid}.footer{display:none}}
'''

def head(title,extra=''):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="icon" href="assets/logos/favicon-adaptive.svg" type="image/svg+xml"><style>{COMMON_CSS}{extra}</style></head>'

top=f'<header class="topbar"><div class="mini-lockup">{inline()}<span class="word">APORIA</span></div><span class="mono">IDENTITY PROPOSAL · 01 / 2026</span></header>'
overview_css='''
body{padding:36px;background:#DAD6CC}.board{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:1536px;margin:auto}.panel{padding:36px;position:relative;min-height:310px;background:#F4F1E9;overflow:hidden}.panel.dark{background:#121416;color:#F4F1E9}.panel>.tag{color:#596168}.panel.dark>.tag{color:#B4BBC2}.panel h2{font-size:46px;line-height:1.1;letter-spacing:-.025em;margin:24px 0 20px}.panel h3{font-family:Serif;font-size:28px;line-height:1.25;margin:20px 0}.panel p{font-size:15px;line-height:1.5;max-width:36ch}.p1{grid-column:span 2;display:flex;align-items:center;justify-content:space-between;min-height:350px}.p1 .brand{font-size:42px;letter-spacing:.12em;margin-bottom:26px}.p1 h2{font-size:60px;max-width:390px;margin:0}.p1>svg{width:220px;flex:none;margin:0 12px}.p2{min-height:350px;background:#E9E5DB}.p2>svg{width:155px;margin:24px auto 18px}.p2 .construction{position:relative}.p2 p{font-size:14px;color:#596168}.p3 img{position:absolute;inset:65px 0 38px;width:100%;height:230px;object-fit:contain}.p3 .particle-label{position:absolute;bottom:20px}.p4 h2{font-size:45px;max-width:370px}.p4 .ui-bar{display:flex;gap:8px;border-top:1px solid #353B42;padding-top:15px;font-size:12px}.p4 .state{color:#79C5CF}.p5 .reading{font-family:Serif;font-size:40px;line-height:1.25;margin:26px 0 20px}.p5 .samples{margin-top:28px}.p5 .samples p{font-size:14px;margin:10px 0}.p6 .palette{display:flex;margin:26px 0 22px;height:82px}.p6 .palette>div{flex:1}.p6 .colors{display:flex;gap:10px;font-size:12px;justify-content:space-between}.p6 .colors span{display:block;font-family:Mono}.p7 .mini-app{width:106px;height:106px;float:left;margin:27px 25px 15px 0}.p7 .mini-app img{width:100%}.p7 .badge{margin-top:33px;border-top:1px solid #76736C;padding-top:18px;font-size:14px;line-height:1.5}.p7 .badge .word{font-size:23px}.p8 h2{font-size:43px}.p8 .state-list{display:flex;gap:20px;flex-wrap:wrap;margin-top:25px;font-size:12px;font-family:Mono}.footer-board{max-width:1536px;display:flex;justify-content:space-between;font-family:Mono;font-size:12px;margin:22px auto 0;color:#383D43}.p8 a{font-size:14px}.p8 .tag{color:#B4BBC2}@media(max-width:900px){body{padding:16px}.board{grid-template-columns:repeat(2,1fr)}.p1{grid-column:span 2}.panel{padding:26px}.p1 h2{font-size:45px}.p1 .brand{font-size:32px}.p1>svg{width:160px}.footer-board{display:block}}@media(max-width:570px){.board{grid-template-columns:1fr}.p1{grid-column:auto;display:block}.p1>svg{margin:40px auto 0;width:140px}.panel{min-height:290px}.footer-board>span{display:block;margin:10px 0}}
'''
palette_html=''.join(f'<div style="background:{PALETTE[n]}"></div>' for n in ['obsidian','paper','iris-dark','cyan-dark','amber-dark'])
board=f'''<main class="board" aria-label="APORIA brand overview">
<section class="panel p1"><div><div class="tag">EXPERIMENTAL REASONING LABORATORY</div><div class="brand word">APORIA</div><h2>The productive<br>impasse.</h2></div>{inline()}</section>
<section class="panel p2"><div class="tag">01 / DIVERGENT APERTURES</div>{inline()}<p>One center. Three open paths.<br>Shared conditions; different limits.</p><div class="mono">r = 48 / 32 / 16 &nbsp; · &nbsp; gap = 66°</div></section>
<section class="panel dark p3"><div class="tag">02 / THE PARTICLE FIELD</div><img src="assets/visuals/particle-exploration.svg" alt="Folded trefoil point surface in iris and cyan"><div class="tag particle-label">ILLUSTRATIVE GEOMETRY</div></section>
<section class="panel dark p4"><div class="tag">03 / OBSERVATORY STUDY</div><h2>What survives<br>an objection?</h2><p class="muted">A common model. Differentiated policies.<br>An inspectable research record.</p><div class="ui-bar"><span>Δ / configured differentiation</span><span class="state">○ Exploration</span></div></section>
<section class="panel p5"><div class="tag">04 / PHILOSOPHY × COMPUTATION</div><div class="reading">An open question.</div><div class="samples"><p>Source Serif 4 · questions &amp; reading</p><p>Source Sans 3 · interface &amp; explanation</p><p class="mono">IBM Plex Mono · Δ / run / operation</p></div></section>
<section class="panel p6"><div class="tag">05 / COLOR AS COGNITIVE STATE</div><div class="palette">{palette_html}</div><div class="colors"><div>Obsidian<span>#121416</span></div><div>Paper<span>#F4F1E9</span></div><div>Iris<span>Reasoning</span></div><div>Cyan<span>Exploration</span></div><div>Amber<span>Event</span></div></div><p style="margin-top:24px">Color has a defined role.<br>Geometry and labels preserve meaning.</p></section>
<section class="panel p7"><div class="tag">06 / SMALL, FIXED, RECOGNIZABLE</div><div class="mini-app"><img src="assets/logos/app-icon.svg" alt="APORIA app icon"></div><div class="badge"><span class="word">APORIA</span><br>Research instrument<br><span class="mono">Divergent Apertures / 02</span></div><p style="clear:both;padding-top:15px">A standard mark for the instrument.<br>A separate micro mark for 16 px.</p></section>
<section class="panel dark p8"><div class="tag">07 / THE EDITORIAL LINE</div><h2>Where reasoning<br>reaches uncertainty,<br>inquiry begins.</h2><a href="index.html">Read the complete proposal →</a></section>
</main><footer class="footer-board"><span>APORIA / STRUCTURED DIVERGENCE</span><span>PROPOSED IDENTITY · 04 OCTOBER 2026 · ALL APPLICATIONS ARE STUDIES</span></footer>'''
(ROOT/'overview.html').write_text(head('APORIA — identity overview',overview_css)+'<body>'+board+'</body></html>')

text=(ROOT/'PROPOSAL.md').read_text()
chunks=re.split(r'^## (\d{2}) — (.+)$',text,flags=re.M)
nav=[];chapters=[]
for k in range(1,len(chunks),3):
    number,title,body=chunks[k:k+3]
    nav.append(f'<a href="#s{number}"><span class="num">{number}</span>{html.escape(title)}</a>')
    rendered=markdown(body)
    if number=='05':rendered='<div class="visual-panel"><img src="assets/logos/lockup-horizontal-dark.svg" alt="Outlined APORIA horizontal lockup" style="width:430px;max-width:100%;margin:45px 0"></div>'+rendered
    if number=='06':
        parts=re.split(r'^### (\d{2})\. (.+)$',body,flags=re.M)
        intro=markdown(parts[0]);concepts=[]
        for j in range(1,len(parts),3):
            num,name,details=parts[j:j+3]
            tail=''
            if '### Decision' in details:details,tail=details.split('### Decision',1)
            slug=re.sub(r'[^a-z0-9]+','-',NAMES[int(num)-1].lower()).strip('-')
            concepts.append(f'<div class="concept {"recommend" if num=="02" else ""}"><div class="symbol">{inline(int(num))}</div><div><h3>{num}. {html.escape(name)}</h3>{markdown(details)}<a class="mono" href="assets/logos/concept-{num}-{slug}.svg" download>Download SVG</a></div></div>')
            if tail:concepts.append('<h3>Decision</h3>'+markdown(tail))
        rendered=intro+'<div class="visual-panel"><img src="assets/visuals/logo-contact-sheet.svg" alt="Contact sheet of all ten ring constructions"></div><div class="logo-tools"><button type="button" id="theme-toggle" aria-pressed="false">View on obsidian</button><label for="preview-size" class="mono">Symbol size</label><select id="preview-size"><option value="150">150 px</option><option value="64">64 px</option><option value="24">24 px</option><option value="16">16 px (standard concepts)</option></select></div><div class="concepts" id="concepts">'+''.join(concepts)+'</div>'
    if number=='07':rendered='<div class="specimen"><div class="serif">Can an objection<br>change the path?</div><div class="sans">Begin inquiry · Inspect the record</div><div class="data">Δ / differentiation &nbsp; → &nbsp; trace / operation</div></div>'+rendered
    if number=='08':
        swatches=''.join(f'<div class="swatch"><div class="swatch-color" style="background:{PALETTE[c]}"></div><p>{n}<br><code>{PALETTE[c]}</code></p></div>' for n,c in [('Obsidian','obsidian'),('Paper','paper'),('Iris','iris-dark'),('Cyan','cyan-dark'),('Amber','amber-dark')])
        rendered='<div class="swatches">'+swatches+'</div>'+rendered+'<p><a href="CONTRAST.md">Open the calculated contrast report →</a></p>'
    if number=='09':
        rendered='<div class="particle-grid">'+''.join(f'<figure><img src="assets/visuals/particle-{s}.svg" alt="Illustrative {s} folded point surface"><figcaption>{s.upper()} / ILLUSTRATION</figcaption></figure>' for s in ['exploration','concentration','conflict','uncertainty','insight','rejection'])+'</div>'+rendered
    if number=='16':rendered='<div class="visual-panel"><img src="assets/visuals/presentation-study.png" alt="APORIA presentation opening study on paper"></div>'+rendered
    if number=='13':rendered='<div class="visual-panel"><img src="assets/visuals/website-study.png" alt="Paper-first APORIA public website identity study"></div>'+rendered
    if number=='14':rendered='<div class="visual-panel"><img src="assets/visuals/dashboard-study.png" alt="Obsidian APORIA observatory identity study with configured and observed states separated"></div>'+rendered
    if number=='15':
        previews=[]
        for size in [16,24,32,48,96]:
            symbol=inline(2,micro=size==16).replace('<svg ',f'<svg width="{size}" height="{size}" ',1)
            previews.append(f'<div>{symbol}<span>{size} px</span></div>')
        strip='<div class="scale-strip">'+''.join(previews)+'</div>'
        rendered='<div class="app-row"><img src="assets/logos/app-icon.svg" alt="APORIA square app icon"><img src="assets/logos/lockup-stacked-dark.svg" alt="APORIA stacked lockup" style="width:220px"></div>'+strip+rendered
    if number=='18':rendered+='<div class="download"><a href="PROPOSAL.md">Written proposal</a><a href="overview.html">Overview board</a><a href="assets/visuals/logo-contact-sheet.svg">10 logo concepts</a><a href="tokens.json">Design tokens</a><a href="aporia-brand-proposal.zip">Complete asset pack</a></div>'
    chapters.append(f'<section class="chapter" id="s{number}"><div class="mono index">{number} / APORIA IDENTITY</div><h2>{html.escape(title)}</h2>{rendered}</section>')

cover=f'''<section class="cover"><div><div class="mono eyebrow">A RESEARCH INSTRUMENT FOR UNRESOLVED QUESTIONS</div><h1>The productive<br>impasse.</h1><p>One shared origin. Deliberately open paths.<br>A coherent identity for an experimental reasoning laboratory.</p><div class="download"><a href="overview.html">View the overview</a><a href="#s06">Explore 10 logos</a></div></div><div>{inline(2,'signature')}<div class="signature-note">DIVERGENT APERTURES / RECOMMENDED</div></div><div class="cover-bottom"><span class="mono">STRATEGY · SYMBOL · TYPE · STATE · INSTRUMENT</span><span class="mono">PROPOSAL / 04 OCTOBER 2026</span></div></section>'''
script='''<script>const toggle=document.getElementById('theme-toggle'),concepts=document.getElementById('concepts');toggle.addEventListener('click',()=>{const dark=toggle.getAttribute('aria-pressed')!=='true';toggle.setAttribute('aria-pressed',String(dark));toggle.textContent=dark?'View on paper':'View on obsidian';concepts.dataset.mode=dark?'dark':'light'});document.getElementById('preview-size').addEventListener('change',e=>concepts.style.setProperty('--preview-size',e.target.value+'px'));</script>'''
footer='<footer class="footer"><span class="word">APORIA</span><span>Proposed identity · Applications are studies · Research limits remain explicit.</span><a href="#">Back to the opening ↑</a></footer>'
(ROOT/'index.html').write_text(head('APORIA — complete identity proposal',BOOK_CSS)+'<body>'+top+cover+'<div class="book"><nav class="toc" aria-label="Proposal chapters"><strong class="mono">THE IDENTITY / 18 CHAPTERS</strong>'+''.join(nav)+'</nav><main>'+''.join(chapters)+'</main></div>'+footer+script+'</body></html>')

print(f'Built {len(NAMES)} vector concepts, lockups, icons, 6 particle specimens, brand book, overview and tokens.')
print(f'Contrast: {len(rows)} prescribed pairings pass. Lowest text ratio: {min(x[3] for x in rows if x[4]==4.5):.2f}:1')
