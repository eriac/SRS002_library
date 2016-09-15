#!/usr/bin/env python
# -*- coding: utf8 -*-

## @package SerialCode
#  Code class for SerialLink
#  @date 2016/9/15
#  @version 0.1

import sys
import Tkinter
import math
import time
import threading

## Class of Code for SerialLink
# @code{.py}
#gui=GuiModule.GuiModule()
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

