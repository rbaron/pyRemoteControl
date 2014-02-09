import socket

HOST = ''
PORT = 30667
BUFFERSIZE = 17 

class Server:
  def __init__(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind(('', 30667))
    self.sock.listen(1)

    self.localaddr = socket.gethostbyname_ex(socket.gethostname())[2][0]

  # This blocks until a new client connects
  def accept(self):
    (self.clientsock, self.clientaddr) = self.sock.accept()

  def receive(self):
    self.message = self.clientsock.recv(BUFFERSIZE)
