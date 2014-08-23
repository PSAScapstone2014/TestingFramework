import socket
import time
import subprocess
import csv
import thread
import itertools
import shlex
import threading
from collections import defaultdict

# This is a helper funtion that formats data for the ChibiOS protocol
# @param lld	The name of the low-level driver that the data is being sent to
# @param data	The data to be sent to the driver
# @return	A string formatted for the protocol
def sim_format(lld, data):
	return '%s\t%s\n' % (lld , data.encode('hex'))

# This method reads a TSV file and sends the contents to a socket that
# represents the IO interface for a low-level driver. The TSV file should have the format:
# data<tab>time
# The data is what will be sent to the driver and the time is the time stamp of the data.
# This method will delay its sends to the socket to simulate the time elapse represented
# by the difference of the time stamps.
# @param fileName	The name of the TSV file to be read from
# @param fileDesc	The file descriptor to create the socket from
# @param driver	The name of the low-level driver to send the data to
def send_to_driver(fileName, fileDesc, driver):
	conn = socket.fromfd(fileDesc, socket.AF_INET, socket.SOCK_STREAM)

    	tsvFile = open(fileName,"rb")
	tsvFile = csv.reader(tsvFile, delimiter = '\t')

	lastTime = 0.0	# The time stamp of the last data point

	for row in tsvFile:
		newTime = float(row[1]) # The time stamp of the new data point

		if ((newTime - lastTime) > 0.0): # Delay if there was a tim eelapse between data points
			print "time to wait: ", (newTime - lastTime), " seconds"
			time.sleep(newTime - lastTime)

        	conn.sendall(sim_format(driver, row[0]))
		lastTime = newTime
		print "sent: ", row[0], " to ", driver


#Class that represents keywords usable in the test table.
class SendReceiveLibrary:		

# This method represents a keyword that can be used in the test table. This keyword starts up a
# chibiOS application, sends data to the app, receives data that the app outputs, and finally
# closes the app. The file in dataFiles must have the same index as the driver it needs to be
# sent to in drivers.
# @param simioPort	The port used for ChibiOS input and output simulation
# @param drivers	A list of the drivers used in the application that receive data
# @param dataFiles	A list of data files to be sent to drivers that receive data
# @param arguments	The arguments used to execute the ChibiOs application
# @return	A dictionary that associates the names of low-level drivers to the data they sent
	def send_and_receive(self, simioPort, drivers, dataFiles, arguments):
		args = shlex.split(arguments)
		HOST = ''    		  
		PORT = int(simioPort)
          
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen(1)

		activeApps = []
		data = defaultdict(list)
		dataBuffer = ""
		sendThread = []

		activeApps.append(subprocess.Popen(args, stdout=subprocess.PIPE))

		conn, addr = s.accept()
		print "connection accepted on: ", addr

		for driver, dataFile in itertools.izip(drivers, dataFiles):
			newThread = threading.Thread(target=send_to_driver, args=(dataFile, conn.fileno(), driver))
    			newThread.start()
			sendThread.append(newThread)

		while (1):
			dataBuffer += conn.recv(1024)
			if (threading.activeCount() <= 1):
				break
		
		lines = dataBuffer.split('\n')
		for line in lines:
			try:	
      				header, code = line.strip().split('\t', 1)
			except:
				break
      			dataChunk = code.decode('hex')
			data[header].append(dataChunk)
			print "received: ", dataChunk, " from ", header
			
		for app in activeApps:		
			app.terminate()

		conn.close()
		s.close()
		return data

# This method is the same as send_and_receive except is collects data from an outgoing lwip
# connection as well as that from the drivers.
# @param simioPort	The port used for ChibiOS input and output simulation
# @param drivers	A list of the drivers used in the application that receive data
# @param dataFiles	A list of data files to be sent to drivers that receive data
# @param lwipPort	The port being connected to by the ChibiOS for outgoing lwip data
# @param lwipAddress	The address being connected to by ChibiOS for outgoing lwip data
# @param arguments	The arguments used to execute the ChibiOs application
# @return	A dictionary that associates the names of low-level drivers to the data they sent
	def send_and_receive_with_lwip(self, simioPort, drivers, dataFiles, lwipPort, lwipAddress, arguments):
		args = shlex.split(arguments)
		HOST = ''    		  
		PORT = int(simioPort)
		LWIPPORT = int(lwipPort)
          
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen(1)

		lwipSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		lwipSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		lwipSocket.bind((lwipAddress, LWIPPORT))

		activeApps = []
		data = defaultdict(list)
		dataBuffer = ""
		lwipDataBuffer = ""
		sendThread = []

		activeApps.append(subprocess.Popen(args, stdout=subprocess.PIPE))

		conn, addr = s.accept()
		print "connection accepted on: ", addr

		for driver, dataFile in itertools.izip(drivers, dataFiles):
			newThread = threading.Thread(target=send_to_driver, args=(dataFile, conn.fileno(), driver))
    			newThread.start()
			sendThread.append(newThread)

		while (1):
			dataBuffer += conn.recv(1024)
			lwipDataBuffer += lwipSocket.recv(1024) + "\n"
			if (threading.activeCount() <= 1):
				break
		
		lines = dataBuffer.split('\n')
		for line in lines:
			try:	
      				header, code = line.strip().split('\t', 1)
			except:
				break
      			dataChunk = code.decode('hex')
			data[header].append(dataChunk)
			print "received: ", dataChunk, " from ", header

		lines = lwipDataBuffer.split('\n')
		for line in lines:
			data['lwip'].append(line)
			print "received: ", line, " from lwip"
			
		for app in activeApps:		
			app.terminate()

		conn.close()
		s.close()
		return data

# *** USER DEFINED TESTS DEFINED BELOW ***
# Here you can define keywords to be used to test the data returned from 
# the send_and_receive keyword.

# An example user defined test is provided.
# The keyword echo_test will take the dictionary returned from send_and_received and check that the
# data sent from the serial driver matches the data in a provided TSV data file.
	def echo_test(self, data, fileName):
		dataString = ""
    		tsvFile = open(fileName,"rb")
		tsvFile = csv.reader(tsvFile, delimiter = '\t')
		fileContent = ""

		for row in tsvFile:
			fileContent += row[0]

		for dataChunk in data['SD1_IO']:
			dataString += dataChunk

		if not fileContent == dataString:
			raise AssertionError("Data sent did not match data received")
		else:
			print "Test passed!"

