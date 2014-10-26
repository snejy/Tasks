from os import curdir, sep
from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
import string, cgi, time
import socket
import sys
import subprocess
import os
import base64

class MySSLHTTPServer(TCPServer):
    def server_bind(self):
        TCPServer.server_bind(self)
        host, port = self.socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith(".html"):
                f = open(curdir + sep + self.path) 
                self.wfile.write(bytes(f.read(), 'utf-8'))
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                f.close()
                return

            if any(self.path.endswith(x) for x in [".jpeg", ".jpg", ".png"]):
                with open(curdir + sep + self.path, 'rb') as img:
                    encoded_string = base64.b64encode(img.read())
                    self.wfile.write(bytes('<html><body>', 'utf-8'))
                    self.wfile.write(encoded_string)
                    print(self.path[1:])
                    self.wfile.write(bytes('<img alt="Image" src="data:image/png;base64,<{}>" style="width:304px;height:228px">'.format(encoded_string),'utf-8'))
                    self.wfile.write(bytes('</body></html>', 'utf-8'))
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                return

            if self.path.endswith(".txt"):
                p = subprocess.Popen('cat ' + os.getcwd() + "/" + self.path,
                                     shell=True,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)

                for line in p.stdout.readlines():
                    print(line)
                    self.wfile.write(bytes(str(line)[2:len(line)+1], 'utf-8'))

            if any(self.path.endswith(x) for x in [".py",".pl",".rb",".exe",".sh"]):
                binds = {".py" : "python", ".pl" : "perl", ".rb" : "ruby", ".exe" : "exec", ".sh" : "bash"}
                p = subprocess.Popen(binds["." + self.path.split('.', 2)[-1]] + " " + os.getcwd() + self.path,
                                           shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT)

                for line in p.stdout.readlines():
                    print(line)
                    self.wfile.write(bytes(str(line)[2:len(line)+1], 'utf-8'))
                return

            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_POST(self):
        if self.path == "/send": #upload.html -> send
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
            })
            x = form["x"].value
            y = form["y"].value
            print("Your number 1 is: %s" % x)
            print("Your number 2 is: %s" % y)
            self.send_response(200)
            self.end_headers()
            z = int(x) + int(y)
            self.wfile.write(bytes("The result from adding {} and {} is {} !".format(x, y, z), 'utf-8'))
            return


def main():
    if len(sys.argv) > 2:
        PORT = int(sys.argv[2])
        I = sys.argv[1]
    elif len(sys.argv) > 1:
        PORT = int(sys.argv[1])
        I = ""
    else:
        PORT = 8080
        I = ""

    try:
        server = MySSLHTTPServer((I, PORT), MyHandler)
        print('started httpserver...')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()

if __name__ == '__main__':
    main()