#!/usr/bin/env python
# -*- coding: utf8 -*-

## @package GuiModule
#  class for GUI
#  @date 2016/9/15
#  @version 0.1

import sys
import Tkinter
import math
import time
import threading

## Class for GUI
# @code{.py}
#link0=SerialLink()
#gui.mainloop()
#sys.exit()
# @endcode
class GuiModule:
	def __init__(self):
		self.root = Tkinter.Tk()
		self.root.geometry("800x600")
		
		self.canvas = Tkinter.Canvas(self.root, width = 600, height = 600, bg = "white")
		self.canvas.place(x=0,y=0)
		self.width=3
		self.fill="black"
		self.scale=1.0
		self.cx=300
		self.cy=300

		#GUIsetting
		self.lv0 = Tkinter.StringVar()
		self.l0=Tkinter.Label(text='label0', textvariable = self.lv0)
		self.l0.place(x=600,y=0)
		self.lv1 = Tkinter.StringVar()
		self.l1=Tkinter.Label(text='label1', textvariable = self.lv1)
		self.l1.place(x=600,y=30)
		self.lv2 = Tkinter.StringVar()
		self.l2=Tkinter.Label(text='label2', textvariable = self.lv2)
		self.l2.place(x=600,y=60)
		self.lv3 = Tkinter.StringVar()
		self.l3=Tkinter.Label(text='label3', textvariable = self.lv3)
		self.l3.place(x=600,y=90)
		
		self.cv0 = Tkinter.BooleanVar()
		self.c0 = Tkinter.Checkbutton(text="check0", variable = self.cv0)
		self.c0.place(x=600,y=120)
		self.cv1 = Tkinter.BooleanVar()
		self.c1 = Tkinter.Checkbutton(text="check1", variable = self.cv1)
		self.c1.place(x=700,y=120)
		self.cv2 = Tkinter.BooleanVar()
		self.c2 = Tkinter.Checkbutton(text="check2", variable = self.cv2)
		self.c2.place(x=600,y=150)
		self.cv3 = Tkinter.BooleanVar()
		self.c3 = Tkinter.Checkbutton(text="check3", variable = self.cv3)
		self.c3.place(x=700,y=150)
		
		self.ev0 = Tkinter.StringVar()
		self.e0 = Tkinter.Entry(textvariable=self.ev0)
		self.e0.place(x=600,y=200)
		
		self.t0 = Tkinter.Text(self.root,width=30, height=13)
		self.t0.place(x=600,y=240)
				

		self.s0 = Tkinter.Scale(self.root, label = 'scale0', orient = 'h', from_ = -100, to = 100)
		self.s0.place(x=600,y=450)
		self.s1 = Tkinter.Scale(self.root, label = 'scale1', orient = 'h', from_ = -100, to = 100)
		self.s1.place(x=700,y=450)
		self.s2 = Tkinter.Scale(self.root, label = 'scale2', orient = 'h', from_ = -100, to = 100)
		self.s2.place(x=600,y=520)
		self.s3 = Tkinter.Scale(self.root, label = 'scale3', orient = 'h', from_ = -100, to = 100)
		self.s3.place(x=700,y=520)
		
	def paraset(self,width,fill):
		self.width=width
		self.fill=fill
	def clear(self):
		self.canvas.delete("all")

	def drawline(self, x1, y1, x2, y2):
		self.canvas.create_line(x1*self.scale+self.cx, -y1*self.scale+self.cy, \
		x2*self.scale+self.cx, -y2*self.scale+self.cy, width=self.width, fill=self.fill)
	def drawcircle(self, x1, y1, radius):
		self.canvas.create_oval((x1-radius)*self.scale+self.cx, -(y1-radius)*self.scale+self.cy, \
		(x1+radius)*self.scale+self.cx, -(y1+radius)*self.scale+self.cy, \
		width=0, fill=self.fill)
	def drawleglines(self,lines):
		#lines
		self.drawline(lines[0][0],lines[0][1],lines[1][0],lines[1][1])
		self.drawline(lines[1][0],lines[1][1],lines[2][0],lines[2][1])
		self.drawline(lines[2][0],lines[2][1],lines[3][0],lines[3][1])
		self.drawline(lines[3][0],lines[3][1],lines[4][0],lines[4][1])
		self.drawline(lines[4][0],lines[4][1],lines[5][0],lines[5][1])
		#circles
		self.drawcircle(lines[0][0],lines[0][1],6)
		self.drawcircle(lines[1][0],lines[1][1],6)
		self.drawcircle(lines[2][0],lines[2][1],6)
		self.drawcircle(lines[3][0],lines[3][1],6)
		self.drawcircle(lines[4][0],lines[4][1],6)
		self.drawcircle(lines[5][0],lines[5][1],14)
		#Z-draw
		self.drawline(lines[0][0],lines[0][1],lines[0][0],lines[0][1]+lines[5][2])
		self.drawcircle(lines[0][0],lines[0][1]+lines[5][2],10)
		
	#def read_volume


	def mainloop(self):
		self.root.mainloop()

