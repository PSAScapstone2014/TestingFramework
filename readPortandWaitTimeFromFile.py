#!/usr/bin/env python
# Echo client program
# The idea here is that port number and 
# wait intervals are read as part of 
# a data file

import socket
import time



try:
    fname = raw_input("Enter name of data file: ")
    file = open(fname,"r")
except IOError:
    print "File Name " + fname + " not found"
else:
    next(file) #skip line
    next(file) #skip line
	
    s=next(file)
    p=s.split()
    print p[1]
    outPort = int(p[1])
    s=next(file)
    p=s.split()
    print p[1]
    inPort = int(p[1])
    s=next(file)
    p=s.split()
    print p[1]
    timewait=float(p[1])	

    for line in file:
	print line
	time.sleep(timewait)


       
# s.send(line),

#HOST = ''    		  # The remote host
#PORT = 50007              # The same port as used by the server
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((HOST, PORT))
    
 #   data = s.recv(1024)
 #   s.close()
 #   print 'Received', data
