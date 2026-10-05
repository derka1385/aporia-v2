"""Color-only study for the retained APORIA emblem. No application changes.

Uses existing logo and particle vector geometry, a common layout, and calculated
contrast so differences between palettes can be judged directly.
"""
from pathlib import Path
import json, re

ROOT=Path(__file__).resolve().parent
BRAND=ROOT.parent
PALETTES=[
  {
    'id':'obsidian','name':'Obsidian & Iris','recommended':True,
    'character':'Philosophical warmth. Precise cognitive color.',
    'judgment':'Best balance of the journal and the instrument. Iris remains a reasoning signal; the identity rests on paper and obsidian.',
    'dark':{'bg':'#121416','surface':'#1B1F23','text':'#F4F1E9','muted':'#B4BBC2','rule':'#353B42','boundary':'#747E88','reasoning':'#B7A2E8','exploration':'#79C5CF','event':'#DDB16B'},
    'light':{'bg':'#F4F1E9','surface':'#E9E5DB','text':'#121416','muted':'#596168','rule':'#D1CDC3','boundary':'#76736C','reasoning':'#65509A','exploration':'#24636C','event':'#805B22'},
  },
  {
    'id':'mineral','name':'Graphite & Mineral','recommended':False,
    'character':'Cooler, clearer, closer to the laboratory.',
    'judgment':'The strongest scientific register. Its colder paper and blue-leaning iris give up some literary warmth.',
    'dark':{'bg':'#10181C','surface':'#18242A','text':'#EDF2F1','muted':'#A3B7BC','rule':'#2F4248','boundary':'#6E8A91','reasoning':'#A1B3E0','exploration':'#6BC6C5','event':'#D7AE73'},
    'light':{'bg':'#EDF2F1','surface':'#DFE7E5','text':'#10181C','muted':'#52666C','rule':'#CCD8D5','boundary':'#64797A','reasoning':'#4D618D','exploration':'#216667','event':'#7B5B2B'},
  },
  {
    'id':'parchment','name':'Ink & Parchment','recommended':False,
    'character':'Warmer, quieter, closer to a philosophical journal.',
    'judgment':'The strongest editorial register. Mauve and copper feel material; the computational character is less immediate.',
    'dark':{'bg':'#1A1715','surface':'#27221E','text':'#F2ECE0','muted':'#BDB2A8','rule':'#453A32','boundary':'#928173','reasoning':'#C0A5CE','exploration':'#9DBFC3','event':'#D7A77D'},
    'light':{'bg':'#F2ECE0','surface':'#E6DED1','text':'#1A1715','muted':'#6B6058','rule':'#D3C8BC','boundary':'#807162','reasoning':'#775782','exploration':'#3E666D','event':'#865634'},
  },
]
STATES={
  'reasoning':{'label':'Reasoning','symbol':'○','role':'reasoning','description':'Iris identifies the active reasoning operation.','a':'reasoning','b':'muted'},
  'exploration':{'label':'Exploration','symbol':'↗','role':'exploration','description':'Cyan identifies a path being explored.','a':'exploration','b':'reasoning'},
  'conflict':{'label':'Conflict','symbol':'≋','role':'event','description':'Amber identifies a conflict that requires inspection.','a':'event','b':'reasoning'},
  'insight':{'label':'Candidate insight','symbol':'◇','role':'event','description':'An amber event is a candidate to examine. A stable region can settle to chalk.','a':'event','b':'text'},
  'concentration':{'label':'Concentration','symbol':'◎','role':'text','description':'Concentration uses neutral coherence rather than an additional hue.','a':'text','b':'muted'},
}

def lum(hexcolor):
    rgb=[int(hexcolor[i:i+2],16)/255 for i in [1,3,5]]
    rgb=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb]
    return sum(x*y for x,y in zip(rgb,[.2126,.7152,.0722]))
def contrast(a,b):
    hi,lo=sorted([lum(a),lum(b)],reverse=True)
    return (hi+.05)/(lo+.05)

ratios=[]
for palette in PALETTES:
    for theme in ['dark','light']:
        p=palette[theme]
        for role in ['text','muted','reasoning','exploration','event','boundary']:
            for bg in ['bg','surface']:
                ratio=contrast(p[role],p[bg]);minimum=3 if role=='boundary' else 4.5
                assert ratio>=minimum,(palette['id'],theme,role,bg,ratio)
                ratios.append({'palette':palette['name'],'theme':theme,'foreground':role,'background':bg,'fg':p[role],'bg':p[bg],'ratio':ratio,'minimum':minimum})
(ROOT/'palettes.json').write_text(json.dumps({'logo':'Divergent Apertures / original retained master','status':'color exploration','recommended':'obsidian','palettes':PALETTES,'states':STATES},indent=2)+'\n')
(ROOT/'contrast.json').write_text(json.dumps(ratios,indent=2)+'\n')

for palette in PALETTES:
    css='/* APORIA color study: '+palette['name']+' / proposed */\n'
    for theme in ['dark','light']:
        css+=f'[data-aporia-theme="{theme}"] {{\n'+''.join(f'  --aporia-{k}: {v};\n' for k,v in palette[theme].items())+'}\n'
    (ROOT/'assets'/f'{palette["id"]}-tokens.css').write_text(css)

# Extract, but never edit, the approved logo geometry.
logo=(BRAND/'assets/logos/symbol-dark.svg').read_text()
logo=re.sub(r'^.*?<title>.*?</title>','',logo,flags=re.S).removesuffix('</svg>')
def symbol(color='currentColor',width=128):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="{width}" height="{width}" color="{color}" aria-label="Divergent Apertures, retained original logo" role="img">{logo}</svg>'

# Preserve the particle geometry. Two regional colors are controlled by the
# review interface, so each option is judged on the same object and distribution.
particle=(BRAND/'assets/visuals/particle-exploration.svg').read_text()
particle=particle.replace('width="960" height="660"','class="particle" width="960" height="660"',1)
particle=particle.replace('fill="#121416"','fill="var(--bg)"')
particle=particle.replace('fill="#79C5CF"','fill="var(--particle-a)"').replace('fill="#B7A2E8"','fill="var(--particle-b)"')
particle=particle.replace('APORIA / illustrative exploration particle geometry','APORIA / illustrative particle geometry; color study')

def static_particle(palette):
    p=palette['dark']
    return particle.replace('var(--bg)',p['bg']).replace('var(--particle-a)',p['exploration']).replace('var(--particle-b)',p['reasoning'])
for palette in PALETTES:
    (ROOT/'assets'/f'particle-{palette["id"]}.svg').write_text(static_particle(palette))

def style(p):return ';'.join(f'--{k}:{v}' for k,v in p.items())
cards=[]
for i,palette in enumerate(PALETTES,1):
    d,l=palette['dark'],palette['light'];recommended='Recommended' if palette['recommended'] else 'Alternative'
    chips=''.join(f'<div class="chip"><i style="background:{d[role]}"></i><span>{name}</span><code>{d[role]}</code></div>' for role,name in [('bg','Ground'),('text','Paper'),('reasoning','Reasoning'),('exploration','Exploration'),('event','Event')])
    dark_logo=symbol(d['text'],80);light_logo=symbol(l['text'],38)
    cards.append(f'''<section class="direction" style="{style(d)}"><div class="direction-head"><h3>{palette['name']}</h3><span>{recommended}</span></div><div class="dark-sample"><div class="dark-signature">{dark_logo}<span class="brand">APORIA</span></div><img src="assets/particle-{palette['id']}.svg" alt="Same illustrative particle geometry in {palette['name']} colors"><div class="state-row"><span style="color:{d['reasoning']}">○ Reasoning</span><span style="color:{d['exploration']}">↗ Exploration</span><span style="color:{d['event']}">≋ Conflict</span></div></div><div class="paper-sample" style="background:{l['bg']};color:{l['text']}">{light_logo}<div><strong>Reasoning under uncertainty.</strong><span style="color:{l['muted']}">Paper / {l['bg']}</span></div><span class="light-accent" style="color:{l['reasoning']}">○</span></div><div class="chips">{chips}</div><p class="character">{palette['character']}</p></section>''')

initial=PALETTES[0]['dark']
report='<table><thead><tr><th scope="col">Role</th><th scope="col">Hex</th><th scope="col">On background</th><th scope="col">On surface</th></tr></thead><tbody id="contrast-body"></tbody></table>'
diagram='''<div class="trace-diagram" role="group" aria-label="Illustrative reasoning trace"><div class="trace-node"><i class="trace-icon" aria-hidden="true"></i><span>Hypothesis</span></div><div class="trace-node"><i class="trace-icon assumption" aria-hidden="true"></i><span>Assumption</span></div><div class="trace-node active"><i class="trace-icon" aria-hidden="true"></i><span id="trace-state">Exploration</span></div></div>'''
css='''
@font-face{font-family:Interface;src:url(../assets/fonts/SourceSans3-Regular.woff2);font-weight:400}
@font-face{font-family:Interface;src:url(../assets/fonts/SourceSans3-Semibold.woff2);font-weight:600}
@font-face{font-family:Editorial;src:url(../assets/fonts/SourceSerif4Display-Regular.woff2)}
@font-face{font-family:Research;src:url(../assets/fonts/IBMPlexMono-Regular.woff2)}
*{box-sizing:border-box}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}html{scroll-behavior:smooth}body{margin:0;background:#F4F1E9;color:#121416;font-family:Interface,Arial,sans-serif;font-size:18px;line-height:1.55}a{color:inherit;text-underline-offset:4px}h1,h2,h3,p{margin:0}h1,h2{font-family:Editorial,Georgia,serif;font-weight:400;letter-spacing:-.02em}h1{font-size:48px;line-height:1.15}h2{font-size:36px;line-height:1.2}h3{font-size:22px;font-weight:600;line-height:1.4}button,select{font:inherit;color:inherit;cursor:pointer}button{border:1px solid #76736C;background:transparent;border-radius:3px;padding:10px 17px;line-height:1.4}button:hover{background:#E9E5DB}button[aria-pressed=true]{background:#121416;color:#F4F1E9;border-color:#121416}a:focus-visible,button:focus-visible,select:focus-visible,[tabindex]:focus-visible{outline:2px solid #24636C;outline-offset:4px}select{background:#F4F1E9;border:1px solid #76736C;border-radius:3px;padding:10px 16px;max-width:220px}.shell{max-width:1500px;padding:40px 50px 60px;margin:auto}.masthead{display:flex;align-items:center;justify-content:space-between;gap:28px;padding:12px 0 36px;border-bottom:1px solid #D1CDC3}.signature{display:flex;align-items:center;gap:16px;font-size:24px}.signature svg{width:42px;height:42px;display:block}.brand{font-weight:600;letter-spacing:.11em}.micro{font-family:Research,monospace;font-size:13px;line-height:1.6}.muted{color:#596168}.opening{display:flex;align-items:end;justify-content:space-between;gap:40px;padding:52px 0 42px}.opening p{max-width:52ch;margin-top:18px;font-size:18px}.opening>.micro{max-width:230px}.comparison{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}.direction{min-width:0}.direction-head{display:flex;justify-content:space-between;align-items:start;gap:12px;min-height:67px;padding:0 0 18px}.direction-head>span{font-size:13px;white-space:nowrap;border-bottom:1px solid #76736C;padding-bottom:3px;margin-top:5px}.dark-sample{background:var(--bg);color:var(--text);padding:28px 24px 20px}.dark-signature{display:flex;align-items:center;justify-content:center;gap:18px;height:114px}.dark-signature>svg{width:70px;height:70px}.dark-signature>.brand{font-size:29px}.dark-sample>img{width:100%;height:235px;object-fit:contain;display:block}.state-row{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px;font-size:14px;line-height:1.5;padding:16px 0 0;border-top:1px solid var(--rule)}.paper-sample{display:flex;align-items:center;gap:13px;padding:25px 18px;border:1px solid #D1CDC3;border-top:0;min-height:104px}.paper-sample>svg{flex:none;width:38px;height:38px}.paper-sample strong{font-family:Editorial,serif;font-size:20px;font-weight:400;line-height:1.35;display:block}.paper-sample span{font-size:13px;display:block;margin-top:4px}.paper-sample .light-accent{font-size:24px;margin:0 0 0 auto}.chips{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;padding-top:20px}.chip i{display:block;height:44px;border:1px solid #76736C}.chip span{display:block;font-size:13px;margin-top:8px}.chip code{font-family:Research;font-size:12px;display:block;line-height:1.6}.character{font-size:16px;color:#596168;margin-top:18px}.section-heading{display:flex;justify-content:space-between;align-items:baseline;gap:25px;margin:60px 0 24px;padding-top:35px;border-top:1px solid #D1CDC3}.controls{display:flex;gap:28px;align-items:end;flex-wrap:wrap;margin:28px 0 24px}.control-group{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.control-group>span,.control-group>label{display:block;width:100%;font-size:14px;color:#596168}.preview{background:var(--bg);color:var(--text);border:1px solid var(--boundary);--state:var(--exploration);--particle-a:var(--exploration);--particle-b:var(--reasoning)}.preview-top{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:24px 30px;border-bottom:1px solid var(--rule)}.preview-top>.signature{font-size:22px;gap:13px}.preview-top .signature svg{width:32px;height:32px}.preview-top>.micro{color:var(--muted)}.preview-body{display:grid;grid-template-columns:.95fr 1.15fr;gap:40px;padding:42px 38px 32px;align-items:center}.preview-copy h3{font-family:Editorial,serif;font-size:46px;font-weight:400;line-height:1.17;letter-spacing:-.02em;max-width:450px}.preview-copy p{color:var(--muted);font-size:17px;max-width:43ch;margin-top:20px}.sample-action{display:inline-block;padding:12px 20px;border-radius:4px;background:var(--text);color:var(--bg);font-size:16px;font-weight:600;margin-top:25px}.object{position:relative;min-width:0}.particle{display:block;width:100%;height:auto;max-height:335px}.object>.micro{text-align:center;color:var(--muted);font-size:12px;margin-top:8px}.preview-lower{display:grid;grid-template-columns:1.15fr .95fr;gap:40px;background:var(--surface);padding:22px 38px 28px;border-top:1px solid var(--rule)}.trace-diagram{position:relative;display:flex;justify-content:space-between;gap:12px;padding-top:20px;min-height:110px}.trace-diagram:before{content:"";position:absolute;left:38px;right:38px;top:34px;border-top:1.5px solid var(--boundary)}.trace-node{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;gap:14px;color:var(--muted);font-size:14px;line-height:1.5}.trace-icon{display:block;width:28px;height:28px;border:1.5px solid var(--text);background:var(--surface);border-radius:50%}.trace-icon.assumption{border-radius:0;width:23px;height:23px;transform:rotate(45deg);margin:2.5px 0}.trace-node.active{color:var(--state)}.trace-node.active .trace-icon{border:2px solid var(--state)}.state-readout{padding:15px 0;align-self:center}.state-readout .active-state{font-size:22px;line-height:1.4;color:var(--state);display:block;margin-bottom:12px}.state-readout p{font-size:15px;color:var(--muted);max-width:50ch}.details{display:grid;grid-template-columns:1.25fr .75fr;gap:48px;padding-top:38px}.details>section{min-width:0}.details h3{font-size:22px;margin-bottom:15px}.table-scroll{overflow:auto}table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.5;min-width:520px}th,td{text-align:left;padding:13px 18px 13px 0;border-bottom:1px solid #D1CDC3}th{font-weight:600;border-color:#76736C}td:nth-child(2){font-family:Research;font-size:13px}.rules p{font-size:16px;margin-bottom:16px}.rules strong{font-weight:600}.verdict{font-size:15px;color:#596168;margin-top:16px}.exports{display:flex;gap:18px;flex-wrap:wrap;font-size:15px;margin-top:28px}.footer{margin-top:55px;padding-top:25px;border-top:1px solid #D1CDC3;font-size:14px;color:#596168;display:flex;justify-content:space-between;gap:24px}.footer a{font-size:14px}.preview [tabindex]:focus-visible{outline-color:var(--exploration)}
@media(max-width:1100px){.shell{padding:30px}.comparison{gap:14px}.direction-head{display:block;min-height:100px}.direction-head>span{display:inline-block;margin-top:7px}.direction-head h3{font-size:20px}.dark-sample{padding:22px 16px}.dark-signature{gap:10px}.dark-signature>.brand{font-size:23px}.state-row{font-size:13px}.chips{gap:5px}.chip span{font-size:12px}.chip code{font-size:12px}.paper-sample{padding:20px 12px;gap:8px}.paper-sample strong{font-size:18px}.paper-sample>svg{width:30px;height:30px}.preview-body,.preview-lower{gap:25px}.details{gap:30px}}
@media(max-width:800px){.shell{padding:24px}.opening{display:block;padding:38px 0}.opening>.micro{margin-top:20px;max-width:none}.comparison{grid-template-columns:1fr;gap:38px}.direction-head{display:flex;min-height:auto}.direction-head h3{font-size:23px}.dark-sample{padding:28px}.dark-signature>.brand{font-size:30px}.dark-sample>img{height:260px}.paper-sample{padding:25px 20px}.paper-sample strong{font-size:23px}.paper-sample>svg{width:40px;height:40px}.chips{gap:9px}.chip code{font-size:12px}.chip span{font-size:13px}.state-row{font-size:15px}.section-heading{display:block}.section-heading>.micro{margin-top:12px}.preview-body{display:block;padding:30px 25px}.preview-copy h3{font-size:40px}.object{margin-top:25px}.preview-lower{grid-template-columns:1fr;padding:20px 25px;gap:14px}.details{grid-template-columns:1fr}.preview-top{padding:20px 24px}.preview-top>.micro{font-size:12px;max-width:130px;text-align:right}.masthead{gap:20px}.masthead>.micro{text-align:right;font-size:12px;max-width:145px}.signature{font-size:20px;gap:10px}.footer{display:block}.footer>span{display:block;margin-bottom:10px}h1{font-size:40px}h2{font-size:31px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''
header=f'<header class="masthead"><div class="signature">{symbol(width=42)}<span class="brand">APORIA</span></div><span class="micro muted">COLOR STUDY<br>ORIGINAL LOGO RETAINED</span></header>'
opening='<div class="opening"><div><h1>One mark. Three color directions.</h1><p>A restrained foundation, with color reserved for cognitive state. Compare the same logo, geometry and interface in each palette.</p></div><p class="micro muted">Recommendation<br>01 / Obsidian & Iris</p></div>'
controls='<div class="controls"><div class="control-group"><span>Palette</span>'+''.join(f'<button type="button" class="palette-button" data-palette="{p["id"]}" aria-pressed="{str(i==0).lower()}">{i+1:02d} / {p["name"]}</button>' for i,p in enumerate(PALETTES))+'</div><div class="control-group"><span>Surface</span><button type="button" class="theme-button" data-theme="dark" aria-pressed="true">Dark</button><button type="button" class="theme-button" data-theme="light" aria-pressed="false">Paper</button></div><div class="control-group"><label for="state-select">Cognitive state</label><select id="state-select">'+''.join(f'<option value="{k}" {"selected" if k=="exploration" else ""}>{s["label"]}</option>' for k,s in STATES.items())+'</select></div></div>'
preview=f'''<section class="preview" id="preview" aria-label="Interactive color specimen" style="{style(initial)}"><div class="preview-top"><div class="signature">{symbol(width=32)}<span class="brand">APORIA</span></div><span class="micro">COLOR SPECIMEN / ILLUSTRATION</span></div><div class="preview-body"><div class="preview-copy"><h3>Reasoning under uncertainty.</h3><p>A common origin. Different paths.<br>An instrument for inspecting what remains open.</p><span class="sample-action">Inspect the record ↗</span></div><div class="object">{particle}<div class="micro">ILLUSTRATIVE GEOMETRY / SAME OBJECT IN EVERY PALETTE</div></div></div><div class="preview-lower"><div>{diagram}</div><div class="state-readout"><span class="active-state" id="active-state">↗ Exploration</span><p id="state-description">Cyan identifies a path being explored.</p></div></div></section>'''
details=f'''<div class="details"><section><h3>Functional color pairs</h3><div class="table-scroll" tabindex="0" aria-label="Scrollable contrast table">{report}</div><p class="verdict" id="contrast-verdict"></p><div class="exports"><a id="css-download" href="assets/obsidian-tokens.css" download>Download palette CSS</a><a href="palettes.json" download>All palette values</a><a href="CONTRAST.md">Full contrast report</a></div></section><section class="rules"><h3>The color rules</h3><p><strong>Logo:</strong> solid ink or chalk. Its geometry supplies recognition.</p><p><strong>Reasoning:</strong> iris. <strong>Exploration:</strong> cyan. <strong>Conflict / candidate insight:</strong> amber, with a distinct symbol and explicit label.</p><p><strong>Uncertainty and divergence:</strong> geometry and labeled values. They do not require additional hues.</p><p><strong>Proportion:</strong> predominantly neutral surfaces. Use one cognitive accent at a time; a comparison may show a second local state.</p><p id="palette-judgment"></p></section></div>'''
footer='<footer class="footer"><span>Color explorations · all geometry is illustrative.</span><span>Contrast calculations use <a href="https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html">W3C text contrast</a> and <a href="https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html">non-text contrast</a>.</span></footer>'
script='''
const palettes=PALETTES_DATA,states=STATES_DATA;
let activePalette='obsidian',activeTheme='dark',activeState='exploration';
const preview=document.getElementById('preview');
function luminance(hex){const a=[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255).map(c=>c<=.04045?c/12.92:((c+.055)/1.055)**2.4);return a[0]*.2126+a[1]*.7152+a[2]*.0722}
function contrast(a,b){const x=[luminance(a),luminance(b)].sort((a,b)=>b-a);return(x[0]+.05)/(x[1]+.05)}
function render(){
const palette=palettes.find(p=>p.id===activePalette),colors=palette[activeTheme],state=states[activeState];
for(const [name,value] of Object.entries(colors))preview.style.setProperty('--'+name,value);
preview.style.setProperty('--state',colors[state.role]);preview.style.setProperty('--particle-a',colors[state.a]);preview.style.setProperty('--particle-b',colors[state.b]);
document.getElementById('active-state').textContent=state.symbol+' '+state.label;
document.getElementById('state-description').textContent=state.description;
document.getElementById('trace-state').textContent=activeState==='insight'?'Insight':state.label;
document.querySelectorAll('.palette-button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.palette===activePalette)));
document.querySelectorAll('.theme-button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.theme===activeTheme)));
const rows=[['text','Primary text'],['muted','Secondary text'],['reasoning','Reasoning'],['exploration','Exploration'],['event','Conflict / insight'],['boundary','Control boundary']];
document.getElementById('contrast-body').innerHTML=rows.map(([key,name])=>'<tr><td>'+name+'</td><td>'+colors[key]+'</td><td>'+contrast(colors[key],colors.bg).toFixed(2)+':1</td><td>'+contrast(colors[key],colors.surface).toFixed(2)+':1</td></tr>').join('');
document.getElementById('contrast-verdict').textContent=palette.name+' / '+(activeTheme==='dark'?'Dark':'Paper')+' — all displayed pairs pass their prescribed text or control threshold.';
document.getElementById('palette-judgment').textContent=palette.judgment;
document.getElementById('css-download').href='assets/'+palette.id+'-tokens.css';
preview.dataset.palette=activePalette;preview.dataset.theme=activeTheme;preview.dataset.state=activeState;
}
document.querySelectorAll('.palette-button').forEach(b=>b.addEventListener('click',()=>{activePalette=b.dataset.palette;render()}));
document.querySelectorAll('.theme-button').forEach(b=>b.addEventListener('click',()=>{activeTheme=b.dataset.theme;render()}));
document.getElementById('state-select').addEventListener('change',e=>{activeState=e.target.value;render()});
render();
'''.replace('PALETTES_DATA',json.dumps(PALETTES)).replace('STATES_DATA',json.dumps(STATES))
document='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>APORIA — color study</title><link rel="icon" href="../assets/logos/favicon-adaptive.svg"><style>'+css+'</style></head><body><main class="shell">'+header+opening+'<h2 class="sr-only">Three color directions</h2><section class="comparison" id="comparison" aria-label="Three color directions">'+''.join(cards)+'</section><div class="section-heading"><h2>Try the colors in context.</h2><span class="micro muted">PALETTE × SURFACE × STATE</span></div>'+controls+preview+details+footer+'</main><script>'+script+'</script></body></html>'
(ROOT/'index.html').write_text(document)

report_md='# APORIA color comparison — calculated contrast\n\nAll three palettes use the original Divergent Apertures logo. Full-opacity text pairs are checked at 4.5:1 and control boundaries at 3:1. Decorative fine rules and illustrative particle opacity are excluded from functional pair claims.\n\n| Palette | Theme | Foreground | Background | Hex pair | Ratio | Minimum |\n| --- | --- | --- | --- | --- | --- | --- |\n'
for r in ratios:report_md+=f'| {r["palette"]} | {r["theme"]} | {r["foreground"]} | {r["background"]} | {r["fg"]} / {r["bg"]} | {r["ratio"]:.2f}:1 | {r["minimum"]}:1 |\n'
report_md+='\nSources: [W3C text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) and [W3C non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html). These pair checks do not constitute a complete product accessibility audit.\n'
(ROOT/'CONTRAST.md').write_text(report_md)
(ROOT/'README.md').write_text('''# APORIA — color study

The original **Divergent Apertures** logo is the retained reference. This exploration changes color only. The current application and the original brand proposal are separate from this review surface.

Open `index.html` to compare three palettes, two surfaces and five cognitive states. The controls update the logo’s neutral color, particle-region colors, example interface and calculated contrast table together. The particle geometry is identical across palettes and is explicitly labeled illustrative.

**Recommendation: Obsidian & Iris.** It balances warm reading surfaces with precise cognitive accents. Graphite & Mineral is cooler and more technical. Ink & Parchment is warmer and more editorial. These are proposals, rather than a recorded user color choice.

The logo remains a single neutral color. Reasoning uses iris; exploration uses cyan; conflict and candidate insight use amber with different symbols and explicit labels. Uncertainty and divergence use geometry and values rather than extra hues. Avoid assigning those colors to profile identities or graph node types.

`palettes.json` lists exact values. Each palette has a CSS export in `assets/`. `CONTRAST.md` documents all 72 checked pairs. The comparison PNG and individual selected-palette preview PNGs are browser renders of this review surface.

`build.py` reuses existing SVG masters and writes only files in this colors folder. It does not import or execute the original brand builder. No new fonts, dependencies or application changes are required.
''')
print(f'Built 3 color directions / 2 surfaces / 5 state previews. All {len(ratios)} prescribed contrast pairings pass.')
