#!/usr/bin/env python
# -*- coding: utf8 -*-

## @package ComModule
#  Module for serial and socket communication
#  @date 2016/9/15
#  @version 1.0

import serial
import socket
import threading
from signal import signal, SIGPIPE, SIG_DFL

## Class for communication
# @code{.py}
#com=ComModule.ComModule("serial")
#com.write("#CANLINK;")
#in_data=com.read_all()		
#print in_data
#sys.exit()
# @endcode
class ComModule:
	## Initialize
	#  @param[in] route "serial" for UART, "remote" for socket
	def __init__(self, route):
		self.route=route		
		if(self.route=="serial"):
			self.ser = serial.Serial('/dev/ttyUSB0', 1000000)
			self.ser.rtscts=False
			self.ser.dsrdtr=False
			self.ser.rts=False
			self.ser.dtr=False
		elif(self.route=="remote"):
			signal(SIGPIPE,SIG_DFL) 
			#self.host = '127.0.0.1'
			self.host = '192.168.1.35'
			self.port = 4000
			self.bufsize = 4096
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
			self.sock.connect((self.host, self.port))
		else:
			print "No com route"
	
	## Send data 
	#  @param[in] w0 string send data
	def write(self,w0):
		if(self.route=="serial"):
			self.ser.write(w0)
		elif(self.route=="remote"):
			self.sock.send(w0)
	
	## Read data 
	#  @return read all recieve buffer data
	def read_all(self):
		if(self.route=="serial"):
			if  self.ser.in_waiting!=0:
				return self.ser.read(self.ser.in_waiting)
			else:
				return ""
		elif(self.route=="remote"):
			return "remote"
	
	## Close port did not nessesary
	def close(self):
		if(self.route=="serial"):
			self.ser.close()
		elif(self.route=="remote"):
			self.sock.close()
		
