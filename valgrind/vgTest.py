import socket
import time
import subprocess
import csv
import thread


class valgrindTest:
	def runValgrind(testFile, outFilename)
		testfile = "vc"
		outFilename = "logvg.txt"

	    	subprocess.call("valgrind./", file, stderr=outFilename,shell=True)
		print "name of test file",testFile



	def echo_test(self, data, fileName):
		dataString = ""
    		file = open(fileName,"rb")
		file = csv.reader(file, delimiter = '\t')
		fileContent = ""
		for row in file:
			fileContent += row[0]
		for dataChunk in data['SD1_IO']:
			dataString += dataChunk
		if not fileContent == dataString:
			raise AssertionError("Data sent did not match data received")
		else:
			print "Test passed!"
		

