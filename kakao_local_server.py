from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import subprocess,tempfile
from pathlib import Path
class Handler(SimpleHTTPRequestHandler):
 def do_POST(self):
  if self.path!='/convert-heic': return self.send_error(404)
  size=int(self.headers.get('Content-Length','0'))
  if not 0<size<40*1024*1024:return self.send_error(413)
  with tempfile.TemporaryDirectory() as folder:
   src=Path(folder)/'input.heic';dst=Path(folder)/'output.jpg';src.write_bytes(self.rfile.read(size))
   result=subprocess.run(['sips','-s','format','jpeg',str(src),'--out',str(dst)],capture_output=True)
   if result.returncode or not dst.exists():return self.send_error(422,'Unable to convert image')
   body=dst.read_bytes();self.send_response(200);self.send_header('Content-Type','image/jpeg');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
if __name__=='__main__':
 import os
 os.chdir(Path(__file__).resolve().parent)
 ThreadingHTTPServer(('127.0.0.1',8766),Handler).serve_forever()
