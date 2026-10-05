#!/usr/bin/env python3
"""Local film preview with byte ranges, so browsers can seek the MP4."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
import re

ROOT=Path(__file__).resolve().parent.parent

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
    def send_head(self):
        self.remaining=None
        path=self.translate_path(self.path)
        if os.path.isdir(path):return super().send_head()
        try:source=open(path,'rb')
        except OSError:
            self.send_error(404,'File not found');return None
        total=os.fstat(source.fileno()).st_size
        start=0;end=total-1
        requested=self.headers.get('Range')
        if requested:
            match=re.fullmatch(r'bytes=(\d*)-(\d*)',requested.strip())
            if not match or not any(match.groups()):
                source.close();self.send_error(416,'Invalid range');return None
            a,b=match.groups()
            if a:
                start=int(a);end=min(total-1,int(b)) if b else total-1
            else:start=max(0,total-int(b))
            if start>=total or start>end:
                source.close();self.send_response(416);self.send_header('Content-Range',f'bytes */{total}');self.end_headers();return None
            self.send_response(206)
            self.send_header('Content-Range',f'bytes {start}-{end}/{total}')
            source.seek(start)
        else:self.send_response(200)
        self.send_header('Content-Type',self.guess_type(path))
        self.send_header('Content-Length',str(end-start+1))
        self.send_header('Accept-Ranges','bytes')
        self.send_header('Last-Modified',self.date_time_string(os.fstat(source.fileno()).st_mtime))
        self.end_headers();self.remaining=end-start+1
        return source
    def copyfile(self,source,output):
        if self.remaining is None:return super().copyfile(source,output)
        try:
            while self.remaining>0:
                chunk=source.read(min(self.remaining,65536))
                if not chunk:break
                output.write(chunk);self.remaining-=len(chunk)
        except (BrokenPipeError,ConnectionResetError):pass
    def log_message(self,*args):pass

if __name__=='__main__':
    server=ThreadingHTTPServer(('127.0.0.1',8767),Handler)
    print('APORIA film preview: http://127.0.0.1:8767/',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:server.server_close()
