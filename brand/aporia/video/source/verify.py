#!/usr/bin/env python3
"""Bounded verification of the final container, decode and captions."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import hashlib
import struct

ROOT=Path(__file__).resolve().parent.parent
VIDEO=ROOT/'exports/APORIA-60s-English-1080p.mp4'
FFMPEG='/Applications/ClipGrab.app/Contents/MacOS/ffmpeg'
meta=subprocess.run([FFMPEG,'-hide_banner','-i',str(VIDEO)],capture_output=True,text=True).stderr
assert '1920x1080' in meta and '30 fps' in meta and 'Video: h264' in meta and 'Audio: aac' in meta
assert 'Subtitle: mov_text' in meta
duration_match=re.search(r'Duration: (\d\d):(\d\d):(\d\d\.\d+)',meta)
hh,mm,ss=duration_match.groups();container_duration=int(hh)*3600+int(mm)*60+float(ss)
# AAC packets may carry up to one extra 1024-sample padding block in the container.
assert 60<=container_duration<=60+1024/48000+.01
decode=subprocess.run([FFMPEG,'-v','error','-i',str(VIDEO),'-map','0:v:0','-map','0:a:0','-progress','pipe:1','-f','null','-'],capture_output=True,text=True,check=True)
assert not decode.stderr.strip(),decode.stderr
frames=int(re.findall(r'frame=(\d+)',decode.stdout)[-1]);assert frames==1800
times=[]
for match in re.finditer(r'(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)',(ROOT/'exports/aporia-en.srt').read_text()):
    a=list(map(int,match.groups()))
    start=a[0]*3600+a[1]*60+a[2]+a[3]/1000;end=a[4]*3600+a[5]*60+a[6]+a[7]/1000
    assert 0<=start<end<=60
    if times:assert start>=times[-1][1]-.002
    times.append((start,end))
audio=json.loads((ROOT/'exports/audio-verification.json').read_text())
assert all(s['start']+s['seconds']<=[7,14,20,28,36,45,54,60][s['scene']-1] for s in audio['sceneVoices'])
layout=json.loads((ROOT/'exports/layout-verification.json').read_text());assert not layout['overflow']
# Verify representative compressed frames, including the Δ transition, by decoding them.
for i,t in enumerate([4,11,17,25,29.7,31.7,33,41,51,58]):
    dest=ROOT/'exports'/f'verified-frame-{i+1:02d}.jpg'
    subprocess.run([FFMPEG,'-y','-v','error','-ss',str(t),'-i',str(VIDEO),'-frames:v','1','-q:v','2',str(dest)],check=True)
result={'durationSeconds':frames/30,'containerDurationSeconds':container_duration,'audioPadding':'at most one AAC block','width':1920,'height':1080,'fps':30,'frames':frames,'videoCodec':'H.264','audioCodec':'AAC stereo','subtitleCodec':'mov_text','language':'English','bytes':VIDEO.stat().st_size,'sha256':hashlib.sha256(VIDEO.read_bytes()).hexdigest(),'fullDecode':'passed','decodeErrors':[],'subtitleCues':len(times),'subtitleEndSeconds':times[-1][1],'shortestCaptionSeconds':round(min(b-a for a,b in times),3),'voiceSegmentsWithinScenes':True,'textBlocksWithinFrame':layout['checkedTextBlocks'],'textOverflow':[],'representativeDecodedFrames':10}
(ROOT/'exports/video-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
