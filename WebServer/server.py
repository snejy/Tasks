from os import curdir, sep
from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
import string, cgi, time
import socket
import sys
import subprocess
import os
import base64
import os.path
from copy import deepcopy

class MySSLHTTPServer(TCPServer):
    
    def server_bind(self):
        TCPServer.server_bind(self)
        host, port = self.socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port


class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        try:
            parts = self.path.split("?")
            self.path = deepcopy(parts[0])
            arguments = []
            if len(parts) > 1:
                arguments = parts[1].split("&")
                # print(arguments)

            if self.path.endswith(".html"):
                f = open(curdir + sep + self.path) 
                self.wfile.write(bytes(f.read(), 'utf-8'))
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                f.close()
                return

            if any(self.path.endswith(x) for x in [".jpeg", ".jpg", ".png"]):

                path_to_image = os.getcwd() + self.path
                with open(path_to_image, 'rb') as image:
                    self.wfile.write(image.read())

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
                binds = {".py" : "python3", ".pl" : "perl", ".rb" : "ruby", ".exe" : "exec", ".sh" : "bash"}

                if len(arguments) == 0: 
                    p = subprocess.Popen(binds["." + self.path.split('.', 2)[-1]] + " " + os.getcwd() + self.path,
                                               shell=True,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.STDOUT)

                else:
                    names = list(map(lambda s: s.split("="), arguments))
                    values = [x[1] for x in names]
                    p = subprocess.Popen(binds["." + self.path.split('.', 2)[-1]] + " " + os.getcwd() + self.path +  " "  + " ".join(values),
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
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(post_data)

    # def do_POST(self):
    #     if self.path == "/send": #sum.html -> send
    #         form = cgi.FieldStorage(
    #             fp=self.rfile, 
    #             headers=self.headers,
    #             environ={'REQUEST_METHOD':'POST',
    #                      'CONTENT_TYPE':self.headers['Content-Type'],
    #         })
    #         x = form["x"].value
    #         y = form["y"].value
    #         print("Your number 1 is: %s" % x)
    #         print("Your number 2 is: %s" % y)
    #         self.send_response(200)
    #         self.end_headers()
    #         z = int(x) + int(y)
    #         self.wfile.write(bytes("The result from adding {} and {} is {} !".format(x, y, z), 'utf-8'))
    #         return


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