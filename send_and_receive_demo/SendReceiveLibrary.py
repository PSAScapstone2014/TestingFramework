import socket
import time
import subprocess
import csv

class SendReceiveLibrary:

	def send_and_receive(self, port1, port2, fileName, *apps):
		HOST = ''    		  
		PORT1 = int(port1)
		PORT2 = int(port2)
		data = ""              
		s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s1.bind((HOST, PORT1))
		s1.listen(1)
		if not PORT1 == PORT2:
			s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s2.bind((HOST, PORT2))
			s2.listen(1)
		activeApps = []
		for appName in apps:
			activeApps.append(subprocess.Popen(appName))
		conn1, addr1 = s1.accept()
		if not PORT1 == PORT2:
			conn2, addr2 = s2.accept()
		else:
			conn2 = conn1
			addr2 = addr1
		print "connection 1 accepted on: ", addr1
		print "connection 2 accepted on: ", addr2
		try:
		    	file = open(fileName,"rb")
			file = csv.reader(file, delimiter = '\t')
		except IOError:
    			print "File Name " + fileName + " not found"
		else:

    			for row in file:
        			conn1.send(row[0])
				print "sent: ", row[0]
				dataChunk = conn2.recv(1024)
				print "received: ", dataChunk
				data += dataChunk
		for app in activeApps:		
			app.terminate()
		conn1.close()
		s1.close()
		if not PORT1 == PORT2:
			conn2.close()
			s2.close()
		return data

	def echo_test(self, data, fileName):
		try:
    			file = open(fileName,"rb")
			file = csv.reader(file, delimiter = '\t')
		except IOError:
    			print "File Name " + fileName + " not found"
		else:
			fileContent = ""
			for row in file:
				fileContent += row[0]
			if not fileContent == data:
				raise AssertionError("Data sent did not match data received")
			else:
				print "Test passed!"

