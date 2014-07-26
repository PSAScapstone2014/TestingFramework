# Receives data from an input socket, and then
# sends that data out through an output socket
# 
# Input Arguments:
#   arg1 = Input port
#   arg2 = Output port

import sys, socket

# Check input arguments
if len(sys.argv) < 3:
  print 'Error: Not enough arguments.'
  exit(0)
elif len(sys.argv) > 3:
  print 'Error: Too many arguments.'
  exit(0)

# Set port variables
HOST = ''
PORT1 = int(sys.argv[1]) # arg1
PORT2 = int(sys.argv[2]) # arg2

# Recieve data from port 1(input)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT1))
data = s.recv(1024)
s.close
print 'Received', repr(data)

# Send recieved data to port 2(output)
o = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#o.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
o.bind((HOST, PORT2))
o.listen(1)
conn, addr = o.accept()
print 'Connected by', addr
# Send data over socket
conn.send(data)
conn.close()
o.close()
addr.close()
