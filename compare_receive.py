#!/usr/bin/env python
#
#  Receive arbitrary text data and compare it to text in a file.

import socket # Needed to receive text over a tcp socket...
import sys # For exiting out of the main function to avoid looping...



#===============================================================================
# Send text string text to a tcp port and exit on exception or return 'Success'
def socket_send_program(text):

    HOST = ''
    PORT = 50000



    try:
          sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          sock.connect((HOST,PORT))
          sock.send(text)
    except Exception as e:
          return e

    return 'Success'
#===============================================================================



#===============================================================================
# Receive text data on a tcp port and return as a text string...
def socket_recv_program():
    HOST = ''
    port = 50000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST,port))
    sock.listen(1)
    conn, addr = sock.accept()

    while 1:
        data = conn.recv(1024)
        if not data: break 

    conn.close()

    return data;
#===============================================================================



#===============================================================================
# Purpose is to strip the last newline off of a string...
def chomp(s):
    if  s.endswith('\n'):
         return s[:-1]
    else:
         return s
#===============================================================================



#===============================================================================
def main():

    workfile = 'test.txt'

    # Open the file to be read and encode it's text content into a string...
    lcl_file = open(workfile,'r')

    lines = []

    for line in lcl_file:
        lines += line

    text = ''.join(lines)
    text = chomp(text)
    # Text content of file encoded as a string...


    # Now send the text string representation of the file over a socket...
    msg = socket_send_program(text)

    if ( msg != 'Success' ):
         print msg
         sys.exit(-1)


    # Now listen for and receive the string via a socket...
    text2 = socket_recv_program()


    # Compare the string received to the content of the file...
    if text == text2:
        print 'Matched!!!'
    else:
        print 'Different :-('


    # Clean up...
    lcl_file.close()


    # Avoid infintely looping on main...
    sys.exit(0)
#===============================================================================



main()

