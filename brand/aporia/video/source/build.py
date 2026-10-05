#!/usr/bin/env python3
"""Deterministic APORIA film. Existing brand masters; procedural motion and original sound.

Usage: python build.py --stills | --audio | --render | --all
Requires Pillow, NumPy, macOS say and FFmpeg. No inference or external assets.
"""
from __future__ import annotations
import argparse
import functools
import json
import math
import os
from pathlib import Path
import subprocess
import time
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT.parent
ASSETS = ROOT / 'assets'
EXPORTS = ROOT / 'exports'
TIMELINE = json.loads((ROOT / 'source/timeline.json').read_text())
FFMPEG = os.environ.get('APORIA_FFMPEG', '/Applications/ClipGrab.app/Contents/MacOS/ffmpeg')
W, H, FPS = 1920, 1080, 30
BG, PAPER = '#121416', '#F4F1E9'
INK, MUTED, RULE = PAPER, '#B4BBC2', '#353B42'
IRIS, CYAN, AMBER = '#B7A2E8', '#79C5CF', '#DDB16B'
LIGHT_MUTED, LIGHT_RULE = '#596168', '#D1CDC3'
LIGHT_IRIS, LIGHT_CYAN, LIGHT_AMBER = '#65509A', '#24636C', '#805B22'
FONTS = {
    'display':'SourceSerif4Display-Regular.otf',
    'serif':'SourceSerif4-Regular.otf',
    'italic':'SourceSerif4-It.otf',
    'sans':'SourceSans3-Regular.otf',
    'bold':'SourceSans3-Semibold.otf',
    'mono':'IBMPlexMono-Regular.ttf',
}

def rgb(hex_color):
    return tuple(int(hex_color[i:i+2],16) for i in (1,3,5))

def clamp(v, lo=0, hi=1):
    return max(lo,min(hi,v))

def bezier(x, x1=.23, y1=1, x2=.32, y2=1):
    """Brand motion uses Animate's strong ease-out / ease-in-out curves."""
    x=clamp(x); low=0.; high=1.
    for _ in range(18):
        t=(low+high)/2
        bx=3*(1-t)**2*t*x1+3*(1-t)*t*t*x2+t**3
        if bx<x: low=t
        else: high=t
    t=(low+high)/2
    return 3*(1-t)**2*t*y1+3*(1-t)*t*t*y2+t**3

def enter(t, delay=0, duration=.85):
    return bezier((t-delay)/duration)

def ease_io(x):
    return bezier(x,.77,0,.175,1)

@functools.lru_cache(maxsize=200)
def font(family, size):
    return ImageFont.truetype(str(BRAND/'assets/fonts'/FONTS[family]),size)

# A registry lets verification check every rendered text block against the frame.
TEXT_BOUNDS = []
CHECK_BOUNDS = False

@functools.lru_cache(maxsize=1200)
def text_asset(value, family, size, color, tracking):
    f=font(family,size)
    if tracking:
        width=sum(f.getlength(ch) for ch in value)+tracking*max(0,len(value)-1)
    else:
        width=f.getlength(value)
    box=f.getbbox(value)
    img=Image.new('RGBA',(int(math.ceil(width))+6, max(1,box[3]-box[1])+8))
    d=ImageDraw.Draw(img)
    if tracking:
        x=3
        for ch in value:
            d.text((x,4-box[1]),ch,font=f,fill=color)
            x+=f.getlength(ch)+tracking
    else:
        d.text((3,4-box[1]),value,font=f,fill=color)
    return img

def paste_alpha(im, layer, x, y, alpha=1):
    if alpha<.004: return
    if alpha<.999:
        layer=layer.copy()
        layer.putalpha(layer.getchannel('A').point([round(i*clamp(alpha)) for i in range(256)]))
    im.paste(layer,(round(x),round(y)),layer)

def txt(im, value, x, y, size=30, family='sans', color=INK, alpha=1, align='left', tracking=0):
    a=text_asset(value,family,size,color,tracking)
    if align=='center': x-=a.width/2
    elif align=='right': x-=a.width
    if CHECK_BOUNDS and alpha>.5:
        TEXT_BOUNDS.append({'text':value,'x':round(x),'y':round(y),'width':a.width,'height':a.height})
    paste_alpha(im,a,x,y,alpha)

def reveal(im, value, x,y,t,delay=0,size=100,family='display',color=INK,align='left'):
    p=enter(t,delay)
    txt(im,value,x,y+(1-p)*35,size,family,color,p,align)

def lines(im, values, x,y,t,delay=0,size=100,leading=116,color=INK,family='display',align='left'):
    for i,value in enumerate(values):
        reveal(im,value,x,y+i*leading,t,delay+i*.07,size,family,color,align)

def line(im, points, color=RULE, width=2, alpha=1):
    if alpha<.004: return
    if alpha>=.999:
        ImageDraw.Draw(im).line(points,fill=color,width=width,joint='curve')
    else:
        lay=Image.new('RGBA',(W,H)); ImageDraw.Draw(lay).line(points,fill=rgb(color)+(round(alpha*255),),width=width,joint='curve')
        im.paste(lay,(0,0),lay)

def stroke_path(im, points, color=CYAN, width=2, progress=1):
    n=int(len(points)*clamp(progress))
    if n>=2: line(im,points[:n],color,width)

def dotted(im,x1,y1,x2,y2,color=RULE,width=2,dash=10):
    dx,dy=x2-x1,y2-y1; length=math.hypot(dx,dy)
    for pos in np.arange(0,length,dash*2):
        a=pos/max(1,length); b=min(length,pos+dash)/max(1,length)
        line(im,[(x1+dx*a,y1+dy*a),(x1+dx*b,y1+dy*b)],color,width)

def dot(im,x,y,color=CYAN,r=5,outline=False):
    d=ImageDraw.Draw(im); bounds=(x-r,y-r,x+r,y+r)
    if outline: d.ellipse(bounds,outline=color,width=2)
    else: d.ellipse(bounds,fill=color)

def rect(im,x,y,w,h,fill=None,outline=RULE,width=2,radius=4):
    ImageDraw.Draw(im).rounded_rectangle((round(x),round(y),round(x+w),round(y+h)),radius,fill,outline,width)

def cubic(a,b,c,d,n=96):
    q=np.linspace(0,1,n)[:,None]
    return ((1-q)**3*np.array(a)+3*(1-q)**2*q*np.array(b)+3*(1-q)*q*q*np.array(c)+q**3*np.array(d)).tolist()

@functools.lru_cache(maxsize=100)
def master(name,width):
    im=Image.open(ASSETS/(name+'.png')).convert('RGBA')
    if 'wordmark' in name: im=im.crop(im.getbbox())
    return im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS)

def symbol(im,x,y,size=52,light=True,alpha=1):
    paste_alpha(im,master('symbol-light' if light else 'symbol-dark',size),x,y,alpha)

def wordmark(im,x,y,width=140,light=True,alpha=1):
    paste_alpha(im,master('wordmark-light' if light else 'wordmark-dark',width),x,y,alpha)

@functools.lru_cache(maxsize=2)
def base(light=False):
    rng=np.random.default_rng(4026)
    col=np.array(rgb(PAPER if light else BG))
    noise=rng.normal(0,.28,(H,W,1))
    arr=np.clip(col+noise,0,255).astype(np.uint8)
    return Image.fromarray(arr)

def chrome(im,index,t,light=False):
    ink=BG if light else INK; muted=LIGHT_MUTED if light else MUTED; rule=LIGHT_RULE if light else RULE
    symbol(im,88,51,54,not light)
    wordmark(im,161,68,148,not light)
    txt(im,TIMELINE['scenes'][index]['chapter'],1824,71,21,'mono',muted,align='right',tracking=1)
    line(im,[(96,965),(1824,965)],rule,1)
    txt(im,'AI RESEARCH / PHILOSOPHY',96,990,18,'mono',muted,tracking=.4)
    if index in (3,4,5,6):
        txt(im,'WORKFLOW ILLUSTRATION',960,990,18,'mono',muted,align='center',tracking=.5)
    txt(im,f'{index+1:02d} / 08',1824,990,18,'mono',muted,align='right')
    line(im,[(96,1033),(1824,1033)],rule,1)
    line(im,[(96,1033),(96+1728*clamp(t/60),1033)],LIGHT_CYAN if light else CYAN,2)

def sheet(im,x,y,w,h,number,alpha=1):
    lay=Image.new('RGBA',(W,H))
    rect(lay,x,y,w,h,'#1B1F23','#41484F',1)
    txt(lay,'RESEARCH PAPER',x+24,y+26,18,'mono',MUTED)
    txt(lay,number,x+w-24,y+27,18,'mono',MUTED,align='right')
    for k in range(7):
        short=(.9,.73,.86,.91,.6,.85,.74)[k]
        line(lay,[(x+24,y+95+k*28),(x+24+(w-48)*short,y+95+k*28)],'#6A737D' if k<2 else '#3D444C',2)
    paste_alpha(im,lay,0,0,alpha)

def scene0(u,t):
    im=base().copy()
    # Documents continue moving throughout the opening, giving the problem a physical form.
    positions=[(1160,210,380,390),(1440,320,340,420),(1060,490,340,350),(1360,665,340,250),(1580,115,280,280)]
    for i,(x,y,w,h) in enumerate(positions):
        p=enter(u,.12+i*.06,1.3)
        sheet(im,x+(1-p)*190+10*math.sin(t*.32+i),y-(1-p)*30+10*math.cos(t*.23+i),w,h,f'{i+1:02d}',p*(.92-i*.1))
    lines(im,['What should you','write next?'],96,211,u,.05,119,139)
    reveal(im,'A thousand papers.',96,575,u,.65,38,'sans',MUTED)
    reveal(im,'Still no clear research direction.',96,630,u,.72,38,'sans',MUTED)
    line(im,[(99,769),(610,769)],RULE,1)
    reveal(im,'FOR PHILOSOPHY STUDENTS',96,805,u,1.2,21,'mono',CYAN)
    chrome(im,0,t)
    return im

def scene1(u,t):
    im=base(True).copy()
    lines(im,['A convincing answer','can hide a missing step.'],96,186,u,0,105,123,BG)
    p=enter(u,.6,1.5)
    # The edge stops at the unstated premise, then a separate edge reaches the conclusion.
    stroke_path(im,[(x,611) for x in range(275,631)],LIGHT_RULE,3,p)
    stroke_path(im,[(x,611) for x in range(815,1460)],LIGHT_RULE,3,enter(u,1,1.3))
    for x,label,n in [(230,'PREMISE','P'),(1510,'CONCLUSION','C')]:
        dot(im,x,611,BG,26,True)
        txt(im,n,x,592,30,'serif',BG,align='center')
        txt(im,label,x,688,22,'mono',LIGHT_MUTED,align='center')
    q=enter(u,1.2)
    rect(im,666,549,124,124,None,LIGHT_AMBER,2)
    txt(im,'?',728,571,74,'display',LIGHT_AMBER,q,align='center')
    reveal(im,'UNSTATED ASSUMPTION',728,735,u,1.5,22,'mono',LIGHT_AMBER,'center')
    reveal(im,'Or an objection the literature has already answered.',96,884,u,2.4,29,'sans',LIGHT_MUTED)
    chrome(im,1,t,True)
    return im

# Seeded trefoil and deformation are ported from src/Intelligence.jsx.
# It is an explanatory animation, not a replay of measured cognitive state.
N=28000
RNG=np.random.default_rng(9719)
SEEDS=RNG.random((N,3)).astype(np.float32)
U,V,Z=SEEDS[:,0]*math.tau,SEEDS[:,1]*math.tau,SEEDS[:,2]

def centers(u):
    r=1.17+.36*np.cos(3*u)
    return np.stack([r*np.cos(2*u),r*np.sin(2*u),.61*np.sin(3*u)],axis=1)

def norm(a):
    return a/np.maximum(np.linalg.norm(a,axis=1)[:,None],1e-6)

CENTER=centers(U)
TANGENT=norm(centers(U+.005)-centers(U-.005))
NORMAL0=np.stack([np.cos(2*U),np.sin(2*U),np.zeros(N)],axis=1)
BINORMAL=norm(np.cross(TANGENT,NORMAL0))
NORMAL=norm(np.cross(BINORMAL,TANGENT))

def particles(im,t,amount=1,cx=1300,cy=520,scale=380,conflict=0):
    fold=.05*np.sin(V*3+U*5+t*.21)+.025*np.cos(U*9-V*2)
    width=.32+.09*np.sin(U*3+1.4)+fold+.025*np.sin(t*.6+U*3)
    flow=V+t*.07+.07*np.sin(U*5+t*.3)
    p=CENTER+width[:,None]*(NORMAL*np.cos(flow)[:,None]+BINORMAL*np.sin(flow)[:,None])*(.88+.2*Z)[:,None]
    p[:,0]+=np.sin(U*3)*conflict*.45
    p[:,2]+=np.cos(U*3)*conflict*.34
    p+=np.stack([np.sin(U*31+t*.55),np.cos(V*23-t*.7),np.sin(U*17+V*19+t*.6)],axis=1)*(.012+.025*conflict)*Z[:,None]
    ax=.72; ay=-.28+math.sin(t*.045)*.14; az=-.22+math.sin(t*.065)*.045
    rx=np.array([[1,0,0],[0,math.cos(ax),-math.sin(ax)],[0,math.sin(ax),math.cos(ax)]])
    ry=np.array([[math.cos(ay),0,math.sin(ay)],[0,1,0],[-math.sin(ay),0,math.cos(ay)]])
    rz=np.array([[math.cos(az),-math.sin(az),0],[math.sin(az),math.cos(az),0],[0,0,1]])
    p=p@rx.T@ry.T@rz.T
    perspective=5.7/(5.7-p[:,2])
    x=cx+p[:,0]*scale*perspective; y=cy-p[:,1]*scale*perspective
    colfactor=(.5+.5*np.cos(V+U*.8))[:,None]
    color=np.array([65,99,173])*(1-colfactor)+np.array(rgb(CYAN))*colfactor
    violet=(.25*np.maximum(0,np.sin(U*2)))[:,None]
    color=color*(1-violet)+np.array(rgb(IRIS))*violet
    warm=(conflict*np.maximum(0,np.sin(U*3))*.8)[:,None]
    color=color*(1-warm)+np.array(rgb(AMBER))*warm
    intensity=(.25+.45*np.abs(np.sin(V))**.6)*(.45+.4*Z)*amount
    # Bilinear point splats, without an ornamental glow or blur.
    xx=np.floor(x).astype(int); yy=np.floor(y).astype(int)
    fx=x-xx; fy=y-yy
    canvas=np.array(im,dtype=np.float32).reshape(-1,3)
    for dx,dy,weight in [(0,0,(1-fx)*(1-fy)),(1,0,fx*(1-fy)),(0,1,(1-fx)*fy),(1,1,fx*fy)]:
        sx=xx+dx; sy=yy+dy
        keep=(sx>=0)&(sx<W)&(sy>=125)&(sy<940)
        np.add.at(canvas,sy[keep]*W+sx[keep],color[keep]*(intensity[keep]*weight[keep])[:,None]*3.4)
    return Image.fromarray(np.clip(canvas.reshape(H,W,3),0,255).astype(np.uint8))

def scene2(u,t):
    im=base().copy()
    im=particles(im,t,enter(u,.05,1.3),1325,515,235,.25*(1-enter(u,1.4,2.5)))
    lines(im,['Meet','APORIA.'],96,215,u,0,112,125)
    reveal(im,'An experimental AI lab',96,556,u,.65,37,'sans',MUTED)
    reveal(im,'for philosophical research.',96,611,u,.72,37,'sans',MUTED)
    symbol(im,94,730,108,True,enter(u,.8))
    reveal(im,'From uncertainty to inquiry.',228,768,u,1.1,27,'italic',CYAN)
    txt(im,'FOLDED PARTICLE TOPOLOGY',1300,899,19,'mono',MUTED,enter(u,1.1),align='center')
    chrome(im,2,t)
    return im

def graph_node(im,x,y,w,title,subtitle,color=LIGHT_CYAN,p=1):
    if p<.001:return
    dy=(1-p)*22
    rect(im,x,y+dy,w,98,PAPER,LIGHT_RULE,1)
    line(im,[(x,y+dy),(x,y+dy+98)],color,4)
    txt(im,title,x+22,y+17+dy,22,'mono',color,p)
    txt(im,subtitle,x+22,y+54+dy,29,'sans',BG,p)

def scene3(u,t):
    im=base(True).copy()
    reveal(im,'Read. Rebuild. Reveal.',96,181,u,0,109,'display',BG)
    reveal(im,'Make the argument inspectable.',96,330,u,.3,33,'sans',LIGHT_MUTED)
    rect(im,96,453,380,389,None,LIGHT_RULE,1)
    txt(im,'SOURCE PAPER',124,479,22,'mono',LIGHT_MUTED,enter(u,.45))
    txt(im,'“',124,512,115,'display',LIGHT_IRIS,enter(u,.45))
    for k,f in enumerate([.85,.93,.72,.87]):
        stroke_path(im,[(x,621+k*33) for x in range(128,int(128+314*f))],LIGHT_RULE,3,enter(u,.7+k*.08,1))
    txt(im,'Verbatim source quotes',124,782,28,'sans',BG,enter(u,.8))
    edges=[cubic((476,590),(570,590),(550,506),(680,506)),cubic((476,654),(570,654),(550,650),(680,650)),
           cubic((1060,506),(1200,506),(1180,577),(1340,577)),cubic((1060,650),(1200,650),(1180,577),(1340,577)),
           cubic((1060,803),(1200,803),(1270,640),(1340,610))]
    for i,edge in enumerate(edges): stroke_path(im,edge,LIGHT_AMBER if i==4 else LIGHT_RULE,2,enter(u,.9+i*.1,1.2))
    graph_node(im,680,457,380,'PREMISE 01','An explicit claim',LIGHT_CYAN,enter(u,.65))
    graph_node(im,680,601,380,'PREMISE 02','A supporting claim',LIGHT_CYAN,enter(u,.72))
    graph_node(im,1340,529,380,'CONCLUSION','What the paper argues',LIGHT_CYAN,enter(u,1.15))
    p=enter(u,2.1)
    graph_node(im,680,754,380,'HIDDEN PREMISE','What must also be true?',LIGHT_AMBER,p)
    txt(im,'FORMAL CHECK',1340,756,22,'mono',LIGHT_IRIS,enter(u,2.35))
    txt(im,'Does the conclusion follow?',1340,804,29,'sans',BG,enter(u,2.5))
    chrome(im,3,t,True)
    return im

def scene4(u,t):
    im=base().copy()
    lines(im,['One question.','Five ways to investigate.'],96,179,u,0,96,111)
    delta=ease_io((u-1.2)/3.6)
    txt(im,'Δ',1280,187,78,'serif',INK,enter(u,.3))
    txt(im,f'{delta:.2f}',1384,216,31,'mono',CYAN,enter(u,.3))
    line(im,[(1279,288),(1748,288)],RULE,3)
    line(im,[(1279,288),(1279+469*delta,288)],CYAN,3)
    dot(im,1279+469*delta,288,CYAN,7)
    txt(im,'POLICY DIFFERENTIATION',1279,326,20,'mono',MUTED,enter(u,.6))
    rect(im,96,557,365,158,'#1B1F23',RULE,1)
    txt(im,'SHARED QUESTION',120,579,20,'mono',MUTED)
    txt(im,'Where does an',120,624,34,'serif',INK)
    txt(im,'argument fail?',120,669,34,'serif',INK)
    profiles=['Explorer','Formalist','Skeptic','Synthesizer','Minimalist']
    operations=['imagine','formalize','doubt','connect','introspect']
    for i,(name,op) in enumerate(zip(profiles,operations)):
        target=478+i*91
        end=641+(target-641)*delta
        path=cubic((461,641),(740,641),(1110,end),(1513,end),140)
        stroke_path(im,path,CYAN,2,enter(u,.42+i*.06,1.2))
        dot(im,1513,end,INK,6,True)
        label_alpha=clamp((delta-.42)/.3)*enter(u,.9+i*.06)
        txt(im,name,1540,end-17,31,'sans',INK,label_alpha)
        if delta>.42:
            point=path[int((.35+((u*.09+i*.17)% .48))*(len(path)-1))]
            dot(im,*point,IRIS,5)
            txt(im,op,1058,end-33,20,'mono',MUTED,label_alpha)
    reveal(im,'Different policies. Measured diversity.',96,910,u,1.8,29,'sans',MUTED)
    chrome(im,4,t)
    return im

def dark_node(im,x,y,w,h,title,body,t,delay=0,color=CYAN):
    p=enter(t,delay)
    if p<.001:return
    y+=(1-p)*20
    rect(im,x,y,w,h,'#1B1F23',RULE,1)
    txt(im,title,x+24,y+25,21,'mono',color,p)
    for i,text in enumerate(body): txt(im,text,x+24,y+76+i*39,30,'sans',INK,p)

def scene5(u,t):
    im=base().copy()
    reveal(im,'Pressure-test the idea.',96,183,u,0,109)
    reveal(im,'Search what is known. Challenge what survives.',96,326,u,.35,34,'sans',MUTED)
    dark_node(im,96,512,255,171,'OBJECTION',['A specific','premise to test'],u,.5,IRIS)
    dark_node(im,446,512,320,171,'PRIOR-ART CHECK',['Already in','the literature?'],u,.75,CYAN)
    dark_node(im,951,423,320,153,'DEFENDER A',['Independent reply'],u,1.2,INK)
    dark_node(im,951,670,320,153,'DEFENDER B',['Independent reply'],u,1.4,INK)
    dark_node(im,1455,512,369,195,'REFEREE',['Label the outcome.','Verify citations.'],u,2,AMBER)
    connections=[cubic((351,597),(392,597),(401,597),(446,597)),
                 cubic((766,597),(861,597),(847,499),(951,499)),
                 cubic((766,597),(861,597),(847,746),(951,746)),
                 cubic((1271,499),(1370,499),(1340,597),(1455,597)),
                 cubic((1271,746),(1370,746),(1340,636),(1455,636))]
    for i,path in enumerate(connections):
        pp=enter(u,.9+i*.3,1.2)
        stroke_path(im,path,RULE if i<3 else AMBER,2,pp)
        if pp>.95:
            pos=((u*.21-i*.16)%1)
            px,py=path[int(pos*(len(path)-1))]
            dot(im,px,py,CYAN if i<3 else AMBER,4)
    txt(im,'SEPARATE MODEL FAMILIES',1111,878,20,'mono',MUTED,enter(u,1.8),align='center')
    reveal(im,'Human review remains essential.',96,902,u,3.2,28,'italic',MUTED)
    chrome(im,5,t)
    return im

def scene6(u,t):
    im=base(True).copy()
    lines(im,['A direction you can','actually investigate.'],96,187,u,0,85,101,BG)
    items=[('01','A question to pursue'),('02','The closest prior work'),('03','The strongest replies'),('04','What your paper must show')]
    for i,(n,value) in enumerate(items):
        p=enter(u,.5+i*.16)
        txt(im,n,98,463+i*66,25,'mono',LIGHT_IRIS,p)
        txt(im,value,160+(1-p)*24,462+i*66,34,'sans',BG,p)
    p=enter(u,.5,1.1); bx=1001+(1-p)*100
    rect(im,bx,198,773,668,'#FCFAF4',LIGHT_RULE,1)
    txt(im,'APORIA / RESEARCH BRIEF',bx+42,232,21,'mono',LIGHT_MUTED,p)
    line(im,[(bx+42,287),(bx+731,287)],LIGHT_RULE,1)
    txt(im,'What would change',bx+42,320,63,'display',BG,p)
    txt(im,'this conclusion?',bx+42,394,63,'display',BG,p)
    sections=[('CHALLENGED PREMISE','A precise point of disagreement.'),('STRONGEST RESPONSE','The best reply, with source references.'),('A PAPER HERE WOULD…','Defend or revise the disputed premise.')]
    for i,(title,body) in enumerate(sections):
        a=enter(u,1+i*.3)
        txt(im,title,bx+42,526+i*94,19,'mono',LIGHT_IRIS,a)
        txt(im,body,bx+42,562+i*94,27,'sans',BG,a)
    reveal(im,'THE DIRECTOR',96,781,u,2.3,22,'mono',LIGHT_CYAN)
    reveal(im,'Observe → choose → test → learn',96,831,u,2.4,30,'sans',BG)
    # A completed loop communicates learning, rather than invented performance numbers.
    path=cubic((730,850),(822,912),(109,924),(106,878),180)
    stroke_path(im,path,LIGHT_CYAN,2,enter(u,3.2,1.8))
    txt(im,'Ranked leads. Novelty estimates. Human assessment.',1001,912,24,'sans',LIGHT_MUTED,enter(u,2.9))
    chrome(im,6,t,True)
    return im

def scene7(u,t):
    im=base().copy()
    p=enter(u,0,1.05)
    symbol(im,861,173+(1-p)*20,198,True,p)
    wordmark(im,697,411+(1-p)*20,526,True,p)
    lines(im,['From uncertainty','to a research direction.'],960,555,u,.5,86,101,INK,align='center')
    reveal(im,'EXPLORE APORIA',960,817,u,1.1,23,'mono',CYAN,'center')
    txt(im,'derka1385.github.io/APORIA/docs/',960,863,26,'mono',MUTED,enter(u,1.3),align='center')
    txt(im,'Experimental AI research. The final judgment stays yours.',960,927,25,'sans',MUTED,enter(u,1.5),align='center')
    # Let the final logo and invitation breathe: no instrument chrome at the end.
    return im

SCENES=[scene0,scene1,scene2,scene3,scene4,scene5,scene6,scene7]

def frame(t):
    idx=max(i for i,s in enumerate(TIMELINE['scenes']) if s['start']<=t)
    s=TIMELINE['scenes'][idx]
    out=SCENES[idx](t-s['start'],t)
    # A short editorial crossfade preserves continuity at chapter boundaries.
    if idx and t-s['start']<.32:
        old=TIMELINE['scenes'][idx-1]
        previous=SCENES[idx-1](old['end']-old['start']-.001,t)
        out=Image.blend(previous,out,ease_io((t-s['start'])/.32))
    if t<.35: out=Image.blend(base(),out,enter(t,0,.35))
    return out

def stills():
    global CHECK_BOUNDS
    CHECK_BOUNDS=True
    times=[4,11,17,25,33,41,51,58]
    thumbnails=[]
    for idx,t in enumerate(times):
        im=frame(t)
        im.save(EXPORTS/f'scene-{idx+1:02d}.jpg',quality=94)
        thumb=im.resize((640,360),Image.Resampling.LANCZOS)
        thumbnails.append(thumb)
    contact=Image.new('RGB',(1280,1440),BG)
    for idx,thumb in enumerate(thumbnails):contact.paste(thumb,((idx%2)*640,(idx//2)*360))
    contact.save(EXPORTS/'storyboard.jpg',quality=94)
    frame(17).save(EXPORTS/'poster.jpg',quality=95)
    # Check useful settled frames and early/later animation positions.
    for t in [1.2,8.5,15.4,21.4,29.1,34.9,37.4,43.8,46.4,53,55.4,59.9]:frame(t)
    bad=[b for b in TEXT_BOUNDS if b['x']<0 or b['y']<0 or b['x']+b['width']>W or b['y']+b['height']>H]
    (EXPORTS/'layout-verification.json').write_text(json.dumps({'checkedTextBlocks':len(TEXT_BOUNDS),'overflow':bad,'frame':[W,H]},indent=2)+'\n')
    if bad:raise RuntimeError(f'Text overflow: {bad}')
    CHECK_BOUNDS=False
    print('Eight storyboard frames and poster rendered; all text remains inside the 1920 × 1080 frame.',flush=True)

def command(args):
    subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

def wav_read(path):
    with wave.open(str(path),'rb') as f:
        if f.getsampwidth()!=2:raise ValueError('Expected 16-bit PCM')
        rate=f.getframerate(); channels=f.getnchannels()
        v=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(np.float32)/32768
        if channels>1:v=v.reshape(-1,channels).mean(axis=1)
        return v,rate

def wav_write(path,data,sr=48000):
    with wave.open(str(path),'wb') as f:
        f.setnchannels(2 if data.ndim==2 else 1);f.setsampwidth(2);f.setframerate(sr)
        f.writeframes((np.clip(data,-1,1)*32767).astype('<i2').tobytes())

def stamp(seconds,sep=','):
    ms=round(seconds*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}'

def caption_chunks(text,max_chars=68):
    # Balance chunks so a final word never flashes alone for a fraction of a second.
    result=[]
    count=math.ceil(len(text)/max_chars)
    for n in range(count,1,-1):
        target=len(text)/n
        choices=[i for i,ch in enumerate(text) if ch==' ' and 16<=i<=max_chars]
        cut=min(choices,key=lambda i:abs(i-target)-(7 if text[i-1] in ',.;' else 0))
        result.append(text[:cut]);text=text[cut+1:]
    result.append(text)
    return result

def audio():
    sr=48000;duration=60;size=sr*duration
    voice=np.zeros(size,dtype=np.float32);captions=[];measurements=[]
    for idx,scene in enumerate(TIMELINE['scenes']):
        aiff=ASSETS/f'voice-{idx+1:02d}.aiff';wav=ASSETS/f'voice-{idx+1:02d}.wav'
        if not aiff.exists() or aiff.stat().st_size<6000:
            command(['/usr/bin/say','-v',TIMELINE['voice'],'-r',str(TIMELINE['voiceRate']),'-o',str(aiff),scene['narration']])
        command([FFMPEG,'-y','-i',str(aiff),'-ar',str(sr),'-ac','1','-c:a','pcm_s16le',str(wav)])
        samples,_=wav_read(wav)
        active=np.where(np.abs(samples)>.005)[0]
        if not len(active):raise RuntimeError(f'Empty synthesized voice in scene {idx+1}')
        samples=samples[max(0,active[0]-round(.07*sr)):min(len(samples),active[-1]+round(.13*sr))]
        available=scene['end']-scene['voiceStart']-.24
        length=len(samples)/sr;tempo=max(1,length/available)
        if tempo>1.005:
            trimmed=ASSETS/f'voice-{idx+1:02d}-trim.wav';fitted=ASSETS/f'voice-{idx+1:02d}-fit.wav'
            wav_write(trimmed,samples,sr)
            command([FFMPEG,'-y','-i',str(trimmed),'-af',f'atempo={tempo:.6f}','-c:a','pcm_s16le',str(fitted)])
            samples,_=wav_read(fitted)
        start=round(scene['voiceStart']*sr);end=min(size,start+len(samples))
        voice[start:end]+=samples[:end-start]
        length=len(samples)/sr
        chunks=caption_chunks(scene['narration'])
        total=sum(len(c) for c in chunks);at=scene['voiceStart']
        for chunk in chunks:
            d=length*len(chunk)/total
            captions.append((at,at+d,chunk));at+=d
        measurements.append({'scene':idx+1,'start':scene['voiceStart'],'seconds':round(length,3),'tempo':round(tempo,3)})
        print(f'Voice {idx+1}/8: {length:.2f}s, tempo {tempo:.3f}',flush=True)
    # Original restrained ambient score. No samples, copyrighted recordings or stock music.
    music=np.zeros((size,2),dtype=np.float32)
    chords=[(110,164.81,246.94,329.63),(130.81,196,246.94,293.66),(87.31,130.81,220,329.63),(146.83,220,293.66,329.63)]
    for index,start in enumerate(range(0,60,7)):
        length=min(11,60-start);q=np.arange(round(length*sr),dtype=np.float32)/sr
        envelope=np.minimum(1,q/2.0)*np.minimum(1,(length-q)/3.8)
        chord=chords[index%len(chords)]
        for j,freq in enumerate(chord):
            a=np.sin(math.tau*freq*q+.11*np.sin(q*.23))*envelope*.009
            b=np.sin(math.tau*(freq*1.0012)*q+.11*np.sin(q*.21))*envelope*.009
            begin=start*sr;music[begin:begin+len(q),0]+=a;music[begin:begin+len(q),1]+=b
    # Muted pulses establish a 96 BPM pace; soft chimes mark each narrative turn.
    for k,start in enumerate(np.arange(.2,60,.625)):
        length=.22;q=np.arange(round(length*sr),dtype=np.float32)/sr
        pulse=np.sin(math.tau*(48*q+14*.032*(1-np.exp(-q/.032))))*np.exp(-q*28)*.015
        a=round(start*sr);n=min(len(pulse),size-a)
        if n>0:music[a:a+n]+=pulse[:n,None]
    for i,scene in enumerate(TIMELINE['scenes']):
        start=scene['start']+.18;length=2.3;q=np.arange(round(length*sr),dtype=np.float32)/sr
        f=[659.25,587.33,880,783.99][i%4]
        ping=(np.sin(math.tau*f*q)+.22*np.sin(math.tau*f*2.003*q))*np.minimum(1,q/.03)*np.exp(-q*2.7)*.02
        a=round(start*sr);n=min(len(ping),size-a);music[a:a+n]+=ping[:n,None]
    # Duck the score under the narration, with smooth control blocks.
    block=2400;peak=np.array([np.max(np.abs(voice[i:i+block])) for i in range(0,size,block)])
    envelope=np.interp(np.arange(size),np.arange(len(peak))*block,peak)
    duck=1-.44*np.minimum(1,envelope/.07)
    music*=duck[:,None]
    fade=np.minimum(1,np.arange(size)/(sr*.7))*np.minimum(1,(size-np.arange(size))/(sr*1.4))
    music*=fade[:,None]
    voice*=.64/max(.001,np.max(np.abs(voice)))
    mixed=music+voice[:,None]
    wav_write(ASSETS/'voiceover.wav',voice,sr)
    wav_write(ASSETS/'original-score.wav',music,sr)
    wav_write(ASSETS/'mix.wav',mixed,sr)
    command([FFMPEG,'-y','-i',str(ASSETS/'mix.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=7','-ar',str(sr),'-c:a','pcm_s16le',str(EXPORTS/'soundtrack.wav')])
    srt=[];vtt=['WEBVTT','']
    for n,(a,b,c) in enumerate(captions,1):
        srt += [str(n),f'{stamp(a)} --> {stamp(b)}',c,'']
        vtt += [str(n),f'{stamp(a,".")} --> {stamp(b,".")}',c,'']
    (EXPORTS/'aporia-en.srt').write_text('\n'.join(srt))
    (EXPORTS/'aporia-en.vtt').write_text('\n'.join(vtt))
    (EXPORTS/'audio-verification.json').write_text(json.dumps({'duration':60,'sampleRate':sr,'voice':'macOS Daniel / synthetic English UK','sceneVoices':measurements,'originalComposition':True,'mixedPeak':float(np.max(np.abs(mixed)))},indent=2)+'\n')
    (ROOT/'narration.txt').write_text('\n\n'.join(s['narration'] for s in TIMELINE['scenes'])+'\n')
    print('60-second stereo soundtrack and English subtitle tracks exported.',flush=True)

def render():
    if not (EXPORTS/'soundtrack.wav').exists():raise RuntimeError('Build audio before rendering.')
    silent=ASSETS/'picture.mp4'
    args=[FFMPEG,'-y','-hide_banner','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24',
          '-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18',
          '-pix_fmt','yuv420p','-threads','4','-movflags','+faststart',str(silent)]
    proc=subprocess.Popen(args,stdin=subprocess.PIPE)
    start=time.monotonic()
    try:
        for index in range(60*FPS):
            proc.stdin.write(frame(index/FPS).tobytes())
            if index%150==0:print(f'Picture: {index//FPS:02d}/60 seconds; elapsed {time.monotonic()-start:.1f}s',flush=True)
        proc.stdin.close()
        if proc.wait()!=0:raise RuntimeError('FFmpeg picture encode failed.')
    except BaseException:
        proc.kill();raise
    mux()

def mux():
    silent=ASSETS/'picture.mp4'
    output=EXPORTS/'APORIA-60s-English-1080p.mp4'
    command([FFMPEG,'-y','-i',str(silent),'-i',str(EXPORTS/'soundtrack.wav'),'-i',str(EXPORTS/'aporia-en.srt'),
             '-map','0:v:0','-map','1:a:0','-map','2:0',
             '-c:v','copy','-c:a','aac','-b:a','192k','-c:s','mov_text','-t','60','-movflags','+faststart',
             '-metadata:s:a:0','language=eng','-metadata:s:s:0','language=eng','-metadata:s:s:0','title=English captions',
             '-disposition:s:0','0',
             '-metadata','title=APORIA — From uncertainty to a research direction',
             '-metadata','comment=Illustrative workflow. Synthetic English voice. Original procedural score. Human review required.',str(output)])
    print(f'Exported {output} ({output.stat().st_size/1048576:.1f} MiB)',flush=True)

def music_only():
    """Preserve the finished picture and use only the separately composed music stem."""
    score=EXPORTS/'soundtrack-music-only.wav'
    command([FFMPEG,'-y','-i',str(ASSETS/'original-score.wav'),
             '-af','loudnorm=I=-27:TP=-7:LRA=9','-ar','48000','-c:a','pcm_s16le',str(score)])
    output=EXPORTS/'APORIA-60s-No-Voice-1080p.mp4'
    command([FFMPEG,'-y','-i',str(ASSETS/'picture.mp4'),'-i',str(score),
             '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k',
             '-t','60','-movflags','+faststart',
             '-metadata','title=APORIA — Music only / ready for live narration',
             '-metadata','comment=No voiceover. Original ambient score only. Illustrative workflow.',str(output)])
    print(f'Exported music-only film: {output} ({output.stat().st_size/1048576:.1f} MiB)',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--stills',action='store_true');parser.add_argument('--audio',action='store_true');parser.add_argument('--render',action='store_true');parser.add_argument('--mux',action='store_true');parser.add_argument('--music-only',action='store_true');parser.add_argument('--all',action='store_true')
    args=parser.parse_args();ASSETS.mkdir(exist_ok=True);EXPORTS.mkdir(exist_ok=True)
    if args.stills or args.all:stills()
    if args.audio or args.all:audio()
    if args.render or args.all:render()
    elif args.mux:mux()
    if args.music_only:music_only()
