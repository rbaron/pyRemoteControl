import socket

HOST = ''
PORT = 30667
PACKET_SIZE = 16

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

  # Receive exactly PACKET_SIZE bytes
  def receive(self):

    self.message = bytearray(PACKET_SIZE)

    # A little optimization: try to receive 16 bytes at once,
    # if they're not available, receive the max possible and then
    # receive on at a time until PACKET_SIZE
    n = self.clientsock.recv_into(self.message, PACKET_SIZE)
    bytes_received = n

    if n == 0:
      raise socket.error("Client disconnected")

    while(n<PACKET_SIZE):
      n = self.clientsock.recv_into(self.message, 1)

      if n == 0:
        raise socket.error("Client disconnected.")
      else:
        bytes_received = bytes_received + n

