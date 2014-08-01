#!/usr/bin/env python
# Echo server program
import socket

HOST = ''		# Symbolic name meaning the local host.
PORT = 50009		# Arbitrary non privileged port.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Sending data over port', PORT
s.connect((HOST, PORT))
s.send('This is a string.')
s.close()
