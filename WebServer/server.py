from os import curdir, sep
from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer, ForkingMixIn
import string, cgi, time
import socket
import sys
import subprocess
import os
import base64
import os.path
import threading
from copy import deepcopy
import logging
from logger import Logger

class ForkingHTTPServer(ForkingMixIn, TCPServer):

    def __init__(self, server_address, request_handler, logger):
        self.logger = logger
        super(ForkingHTTPServer, self).__init__(server_address, request_handler)

    def server_bind(self):
        TCPServer.server_bind(self)
        host, port = self.socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        self.logger.log([str(self.server_name), "started on", str(self.server_port)])

    def get_request(self):
        try:
            request, client_address = super(ForkingHTTPServer, self).get_request()
            self.logger.log([str(request), str(client_address)])
        except Exception as e:
            self.logger.log(str(e))
        return super(ForkingHTTPServer, self).get_request()

    def serve_forever(self):
        super(ForkingHTTPServer, self).serve_forever()

class MyHandler(BaseHTTPRequestHandler):

    handler_logger = Logger('handlerlog.log', "handler logger")

    def log_message(self, format, *args):
        self.handler_logger.log("%s - - [%s] %s\n" %
                         (self.client_address[0],
                          self.log_date_time_string(),
                          format%args))
        super(MyHandler, self).log_message(format, *args)

    def handle_text_files(self, path, wfile):
        if any(path.endswith(x) for x in [".html", ".txt", ".docs", ".doc"]):
            if not os.path.isfile(path[1:]):
                super(MyHandler, self).send_error(404,'File Not Found: %s' % path)
                return
            f = open(curdir + sep + path) 
            wfile.write(bytes(f.read(), 'utf-8'))
            self.send_response(200)
            f.close()
            return

    def handle_images(self, path, wfile):
        if any(path.endswith(x) for x in [".jpeg", ".jpg", ".png"]):
            if not os.path.isfile(path[1:]):
                super(MyHandler, self).send_error(404,'File Not Found: %s' % path)
                return
            path_to_image = os.getcwd() + path
            with open(path_to_image, 'rb') as image:
                wfile.write(image.read())
            self.send_response(200)
            return

    def handle_scripts(self, path, wfile, values = []):
        if any(path.endswith(x) for x in [".py",".pl",".rb",".exe",".sh"]):
            binds = {".py" : "python3", ".pl" : "perl", ".rb" : "ruby", ".exe" : "exec", ".sh" : "bash"}

            if not os.path.isfile(path[1:]):
                super(MyHandler, self).send_error(404,'File Not Found: %s' % path)
                return

            if len(values) == 0: 
                p = subprocess.Popen(binds["." + path.split('.', 2)[-1]] + " " + os.getcwd() + path,
                                           shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT)

            else:
                p = subprocess.Popen(binds["." + path.split('.', 2)[-1]] + " " + os.getcwd() + path +  " "  + " ".join(values),
                                           shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT)

            for line in p.stdout.readlines():
                print(line)
                wfile.write(bytes(str(line)[2:len(line)+1], 'utf-8'))
            self.send_response(200)
            return

    def handle_other(self, path):
        if not os.path.isfile(path[1:]):
            super(MyHandler, self).send_error(404,'File Not Found: %s' % path)

    def add(self, x, y):
        return int(x) + int(y)

    def do_GET(self):
        try:
            parts = self.path.split("?")
            self.path = deepcopy(parts[0])
            arguments = []
            values = []
            if len(parts) > 1:
                arguments = parts[1].split("&")
                names = list(map(lambda s: s.split("="), arguments))
                values = [x[1] for x in names]
            if self.path.startswith("/test"):
                self.send_response(200)
                return

            if self.path.startswith("/add") and len(values) > 1:
                sumarize = self.add(values[0], values[1])
                self.wfile.write(bytes(str(sumarize), 'utf-8'))
                self.send_response(200)
                return

            self.handle_text_files(self.path, self.wfile)
            self.handle_images(self.path, self.wfile)
            self.handle_scripts(self.path, self.wfile, values)
            self.handle_other(self.path)
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            arguments = []
            values = []
            ctype, pdict = cgi.parse_header(self.headers['Content-type'])

            if ctype == 'multipart/form-data':
                content_type = self.headers['Content-type']
                content_length = int(self.headers['Content-Length'])
                content = self.rfile.read(content_length)
                data_list = []
                content_list = content.decode("utf-8").split("\r\n\r\n")

                for i in range(len(content_list) - 1):
                    data_list.append("")
                data_list[0] += content_list[0].split("name=")[1].split(";")[0].replace('"','') + "="

                for i,c in enumerate(content_list[1:-1]):
                    key = c.split("name=")[1].split(";")[0].replace('"','')
                    data_list[i+1] += key + "="
                    value = c.split("\r\n")
                    data_list[i] += value[0]
                data_list[-1] += content_list[-1].split("\r\n")[0]
                arguments = data_list
                names = list(map(lambda x: x.split("="), data_list))
                values = [x[1] for x in names]

            elif ctype == 'application/x-www-form-urlencoded':
                content_length = int(self.headers['Content-Length'])
                content = self.rfile.read(content_length)
                arguments =  content.decode("utf-8").split("&")
                names = list(map(lambda x: x.split("="), arguments))
                values = [x[1] for x in names]

            self.handle_text_files(self.path, self.wfile)
            self.handle_scripts(self.path, self.wfile, values)
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


def main():
    if len(sys.argv) > 2:
        PORT = int(sys.argv[2])
        IP = sys.argv[1]
    elif len(sys.argv) > 1:
        PORT = int(sys.argv[1])
        IP = ""
    else:
        PORT = 8080
        IP = ""

    try:
        logger = Logger('serverlog.log', "server logger")
        server = ForkingHTTPServer((IP, PORT), MyHandler, logger)
        print(ForkingHTTPServer.mro())
        print('started httpserver...')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()

if __name__ == '__main__':
    main()