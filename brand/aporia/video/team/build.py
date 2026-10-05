"""Brand the existing team film, retaining its edit and original sound.

Run with the bundled Python runtime (Pillow). Add team.json with three objects
in speaking order, each with a confirmed name and optional role, then rerun.
Without that file the export is explicitly a branding-only draft.
"""
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
BRAND = ROOT.parents[1]
FFMPEG = '/Applications/ClipGrab.app/Contents/MacOS/ffmpeg'
SOURCE = Path('/Users/petrinolann/Movies/team presentation .mov')
W, H, FPS = 1920, 1080, 24
FRAMES = 1439
DURATION = FRAMES / FPS
PAPER = '#F4F1E9'
IRIS = '#B7A2E8'
MUTED = '#B4BBC2'
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)

def font(filename, size):
    return ImageFont.truetype(str(BRAND / 'assets/fonts' / filename), size)

def text(im, value, xy, size, family='SourceSans3-Regular.otf', fill=PAPER, anchor=None):
    ImageDraw.Draw(im).text(xy, value, font=font(family, size), fill=fill, anchor=anchor)

def logo(im, xy, scale=1):
    x, y = xy
    for filename, bx, by, width in [('symbol-light.png', x, y, 54), ('wordmark-light.png', x+76*scale, y+16*scale, 164)]:
        source = Image.open(ROOT.parent / 'assets' / filename).convert('RGBA')
        source = source.crop(source.getbbox())
        size = round(width*scale)
        source = source.resize((size, round(source.height*size/source.width)), Image.Resampling.LANCZOS)
        im.alpha_composite(source, (round(bx), round(by)))

def gradient(im, y, height, reverse=False, maximum=210):
    d = ImageDraw.Draw(im)
    for row in range(height):
        fraction = (1-row/max(1,height-1)) if reverse else row/max(1,height-1)
        d.line((0, y+row, im.width, y+row), fill=(18,20,22,round(maximum*fraction*fraction)))

header = Image.new('RGBA', (W,170))
gradient(header,0,170,True,225)
logo(header,(1608,49))
text(header,'TEAM PRESENTATION', (74,64), 24, 'IBMPlexMono-Regular.ttf')
ImageDraw.Draw(header).line((74,106,132,106), fill=IRIS, width=3)
header.save(ASSETS/'header.png')

team_path = ROOT/'team.json'
team = json.loads(team_path.read_text()) if team_path.exists() else None
if team is not None:
    assert len(team) == 3 and all(person.get('name','').strip() for person in team), 'Three confirmed names are required.'

overlays = [('header.png',0,0,0,DURATION,0)]
if team:
    starts = [0.65, 16.5416666667+0.45, 34.5+0.45]
    for i,(person,start) in enumerate(zip(team, starts)):
        name = person['name'].strip()
        role = person.get('role','').strip()
        name_font = font('SourceSerif4Display-Regular.otf',58)
        width = max(530, min(850, round(name_font.getlength(name))+100))
        panel = Image.new('RGBA',(width,158),(18,20,22,237))
        d = ImageDraw.Draw(panel)
        d.rectangle((0,0,4,157), fill=IRIS)
        text(panel,name,(32,18),58,'SourceSerif4Display-Regular.otf')
        text(panel,role or 'APORIA / TEAM',(34,105),24,'SourceSans3-Regular.otf',MUTED)
        filename = f'speaker-{i+1}.png'
        panel.save(ASSETS/filename)
        overlays.append((filename,74,846,start,start+6.5,.25))
    group = Image.new('RGBA',(W,248))
    gradient(group,0,248,maximum=248)
    # The final shot places speakers 1, 3, 2 from left to right.
    for index,center in [(0,510),(2,948),(1,1460)]:
        person=team[index]
        name_size=44
        while font('SourceSerif4Display-Regular.otf',name_size).getlength(person['name'])>400:
            name_size-=1
        text(group,person['name'],(center,145),name_size,'SourceSerif4Display-Regular.otf',anchor='mt')
        text(group,person.get('role','') or 'APORIA / TEAM',(center,208),21,fill=MUTED,anchor='mt')
        ImageDraw.Draw(group).line((center-20,132,center+20,132),fill=IRIS,width=3)
    group.save(ASSETS/'group.png')
    overlays.append(('group.png',0,832,49.2916666667+.4,DURATION,.3))

command=[FFMPEG,'-hide_banner','-y','-i',str(SOURCE)]
for filename,*_ in overlays:
    command += ['-loop','1','-framerate',str(FPS),'-i',str(ASSETS/filename)]
filters=[]
base='0:v'
for i,(filename,x,y,start,end,fade) in enumerate(overlays,1):
    tag=f'asset{i}'
    chain=f'[{i}:v]format=rgba'
    if fade:
        chain+=f',fade=t=in:st={start}:d={fade}:alpha=1'
        if end<DURATION:
            chain+=f',fade=t=out:st={end-fade}:d={fade}:alpha=1'
    chain+=f'[{tag}]'
    filters.append(chain)
    result=f'video{i}'
    filters.append(f'[{base}][{tag}]overlay=x={x}:y={y}:enable=\'between(t,{start},{end})\':shortest=1[{result}]')
    base=result
filters.append(f'[0:a]atrim=end={DURATION},asetpts=PTS-STARTPTS[audio]')
(ROOT/'filter.txt').write_text(';\n'.join(filters))
filename='APORIA-Team-Hackathon-59.96s-1080p.mp4' if team else 'APORIA-Team-Branding-Draft-59.96s-1080p.mp4'
output=ROOT/filename
command += ['-filter_complex_script',str(ROOT/'filter.txt'),'-map',f'[{base}]','-map','[audio]',
            '-frames:v',str(FRAMES),'-t',str(DURATION),'-r',str(FPS),'-c:v','libx264',
            '-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k',
            '-movflags','+faststart','-map_metadata','-1','-metadata','title=APORIA — Team presentation',
            '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(output)]
subprocess.run(command,check=True)
(ROOT/'edit.json').write_text(json.dumps({
    'source':str(SOURCE),'output':str(output),'status':'complete' if team else 'awaiting confirmed names',
    'fps':FPS,'frames':FRAMES,'duration_seconds':DURATION,'team':team,
    'cuts_seconds':[16.5416666667,34.5,49.2916666667],
    'identity':'Existing APORIA / Divergent Apertures masters; Obsidian & Iris; Source fonts',
    'audio':'Original source sound, no added music or synthetic voice',
    'edit':'Original cuts preserved; final video frame omitted to remain below 60 seconds',
},ensure_ascii=False,indent=2))
print(output)
