import socket
import threading
import pickle
import time
import signal

HOST = 'localhost'
PORT = 8080
ADDR = (HOST, PORT)

def test_with_sequential_connections():
    my_count = 0
    while True:
      client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      print('connecting to %s port %s' % ADDR)
      client.connect((ADDR))
      filename = '/format_string.rb'
      fileobj = client.makefile('rw', 10)
      fileobj.write("GET "+ filename +" HTTP/1.0\n\n")
      buff = fileobj.readlines()
      for line in buff:
          print ("-----------------------")
          print ("I'm Connection : %r" % my_count)
          print ("Received : %s" % line)
          my_count = my_count + 1
      print("closing connection")
      client.close()

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    while 1:
        sock.sendall(message)
        time.sleep(1)
        sock.recv(1024)
    sock.close()

def test_with_parallel_connections(SOCKET_AMOUNT):
  for i in range(SOCKET_AMOUNT):
    filename = '/format_string.rb'
    msg = (bytes("GET "+ filename +" HTTP/1.0\n\n", 'utf-8'))
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    client_thread = threading.Thread(target=client, args=(HOST, PORT, msg))
    client_thread.start()

# http://stackoverflow.com/questions/25779767/python-socket-stress-concurrency
if __name__ == '__main__':
  test_with_parallel_connections(10000)
  # test_with_sequential_connections()

  #parallel connections ~ 270 max
  #mem - 0.2 %
  #cpu - 2.5 % tops