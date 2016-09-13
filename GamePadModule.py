#!/usr/bin/env python
# -*- coding: utf8 -*-
import serial
import pygame
from pygame.locals import *

class GamePadModule:
	def __init__(self):
		self.mode=""
		self.axis=[0.0,0.0,0.0,0.0]
		self.button=[0,0,0,0,0,0,0,0,0,0,0,0]
		self.press=[0,0,0,0,0,0,0,0,0,0,0,0]
		self.hat=[0,0]
		
		pygame.init()
		pygame.joystick.init()
		if pygame.joystick.get_count() == 0:
			print "GamePad is not detected."
			self.mode="none"
		else:
			self.mode="pad"	
			# 最初の一個だけ初期化
			self.joystick = pygame.joystick.Joystick(0)
			self.joystick.init()
		
	def read_status(self):
		if(self.mode=="pad"):
			#disable out
			self.press=[0,0,0,0,0,0,0,0,0,0,0,0]
			for e in pygame.event.get(): # イベントチェック
				if e.type == pygame.locals.JOYAXISMOTION:
					self.dummy=0				
					if(e.axis==0):
						self.axis[e.axis]=self.joystick.get_axis(e.axis)
						print "\x1b[1A\x1b[2K\x1b[1A"	#cancel debug message
					elif(e.axis==1):
						self.axis[e.axis]=-self.joystick.get_axis(e.axis)
						print "\x1b[1A\x1b[2K\x1b[1A"	#cancel debug message
					elif(e.axis==3):
						self.axis[e.axis-1]=self.joystick.get_axis(e.axis)
						print "\x1b[1A\x1b[2K\x1b[1A"
					elif(e.axis==4):
						self.axis[e.axis-1]=-self.joystick.get_axis(e.axis)
						print "\x1b[1A\x1b[2K\x1b[1A"		
				elif e.type == pygame.locals.JOYHATMOTION:
					self.hat[0],self.hat[1]=self.joystick.get_hat(0)
					print "\x1b[1A\x1b[2K\x1b[1A"
					print "\x1b[1A\x1b[2K\x1b[1A"
				elif e.type == pygame.locals.JOYBUTTONDOWN:
					self.button[e.button]=1
					self.press[e.button]=1
				elif e.type == pygame.locals.JOYBUTTONUP:
					self.button[e.button]=0
