#!/usr/bin/env python
# Echo client program
#import socket
import time
i=[]

try:
    fname = raw_input("Enter name of data file: ")
    file = open(fname,"r")
except IOError:
    print "File Name " + fname + " not found"
else:

    for line in file:
	l=line        
	i= l.split("\t")
	print i[0]
	print i[1]
        time.sleep(.05)
 #       s.send(line),
    



#HOST = ''    		  # The remote host
#PORT = 50007              # The same port as used by the server
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((HOST, PORT))





 #   data = s.recv(1024)
  #  s.close()
#    print 'Received', data
