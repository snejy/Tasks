import socket


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

if __name__ == '__main__':
    test_with_sequential_connections()