import socket
import time
import subprocess
import threading

class SendReceiveLibrary:

	def send_and_receive(self, port, fileName, appName):
		HOST = ''    		  
		PORT = int(port)
		data = ""              
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen(1)
		app = subprocess.Popen("./" + appName)
		conn, addr = s.accept()
		print "connection accepted on: ", addr
		try:
    			file = open(fileName,"r")
		except IOError:
    			print "File Name " + fileName + " not found"
		else:

    			for line in file:
        			conn.send(line)
				print "sent: ", line
				dataChunk = conn.recv(1024)
				print "received: ", dataChunk
				data += dataChunk
		app.terminate()
		conn.close()
		s.close()
		file.seek(0)
		fileContent = file.read()
		if not fileContent == data:
			raise AssertionError("Data sent did not match data received")
		

