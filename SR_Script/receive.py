import socket

HOST = ''
PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Receiving data over port', PORT
s.connect((HOST, PORT))
data = s.recv(1025)
print 'Received:', repr(data)
s.close
