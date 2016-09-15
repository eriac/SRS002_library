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
	def __init__(self, route, direction):
		self.route=route		
		if(self.route=="serial"):
			self.ser = serial.Serial('/dev/ttyUSB0', 1000000)
			self.ser.rtscts=False
			self.ser.dsrdtr=False
			self.ser.rts=False
			self.ser.dtr=False
		elif(self.route=="remote"):
			signal(SIGPIPE,SIG_DFL) 
			self.host = '192.168.1.35'
			self.port = 4000
			self.bufsize = 4096
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
			self.sock.connect((self.host, self.port))
		else:
			self.route="none"
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

## Class of Code for SerialLink
# @code{.py}
#link0=SerialCode()
#original_command="#LINK.LB-COM.1:1234ABCD;"
#link0.decode(original_command)
#print link0.encode()
#sys.exit()
# @endcode
class SerialCode:
	##Initialize variables
	def __init__(self):
		self.enable=False
		self.command=["","","",""]
		self.option=["","","",""]
		self.suboption=["","","",""]
		self.data_max=20
		self.data=[0]*self.data_max
		self.data_size=0

	##Convert data to string
	# @return string code
	def encode(self):
		Output=""
		Output+="#"+self.command[0]
		for i in range(1,4):
			if self.command[i]!="":
				Output+="."+self.command[i]
		for i in range(0,4):
			if self.option[i]!="":
				Output+="-"+self.option[i]
				if self.suboption[i]!="":
					Output+="."+self.suboption[i]
		if self.data_size>0:
			Output+=":"
			for i in range(0,self.data_size):
				Output+="%02X" % self.data[i]
		Output+=";"
		return Output
	
	##Convert string to data
	# @param[in] str_code string code
	def decode(self,str_code):
		if(str_code[0]=="#" and str_code[len(str_code)-1]==";"):
			str_code=str_code[1:len(str_code)-1]
			str_code=str_code.split(":")
			if(len(str_code)>=2):
				self.data_size=len(str_code[1])/2
				for i in range(0,self.data_size):
					self.data[i]=int(str_code[1][i*2:i*2+2],16)
			str_code=str_code[0].split("-")
			com_code=str_code[0].split(".")
			for i in range(0,len(com_code)):
				self.command[i]=com_code[i]
			for i in range(0,len(str_code)-1):
				opt_code=str_code[i+1].split(".")
				if 1<=len(opt_code):
					self.option[i]=opt_code[0]
				if 2<=len(opt_code):
					self.suboption[i]=opt_code[1]
	##Dump data to stdout
	def outprint(self):
		print self.encode()
