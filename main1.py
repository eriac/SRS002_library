#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import Tkinter
import math
import time
import threading
import GuiModule
import ComModule
import GamePadModule
import MoveUnit

def interval():
	global gui
	while 1:
		if(gui.cv0.get()):
			move.set_mode("walk")
			gui.cv0.set(False)
		elif(gui.cv1.get()):
			move.set_mode("slide")
			gui.cv1.set(False)
		elif(gui.cv2.get()):
			move.set_mode("rest")
			gui.cv2.set(False)
		else:
			gui.lv0.set("none")
		
		gamepad.read_status()
		#print gamepad.button
		#print gamepad.axis
		#print gamepad.hat
		if(gamepad.mode=="pad"):
			if(gamepad.press[0]==1):
				move.set_mode("walk")
			elif(gamepad.press[1]==1):
				move.set_mode("slide")
			elif(gamepad.press[2]==1):
				move.set_mode("rest")

		if(gamepad.mode=="pad"):
			move.set_axis(gamepad.axis[0],gamepad.axis[1],gamepad.axis[2],gamepad.axis[3])
		else:
			move.set_axis(gui.s0.get()/100.0,gui.s1.get()/100.0,gui.s2.get()/100.0,gui.s3.get()/100.0)
		move.set_inter(50)
		move.tick()
		
		gui.clear()
		for i in range(6):
			gui.drawleglines(move.l[i].get_leglines())		
		
		
		for i in range(6):
			if(move.l[i].ready):
				move.l[i].ready=False
				value1=-move.l[i].angle1*16000/3.0/math.pi+7500
				value2=-move.l[i].angle2*16000/3.0/math.pi+7500
				value3=-move.l[i].angle3*16000/3.0/math.pi+7500
				comout="#CANLINK.A-ID.%d-COM.1:%04X%04X%04X01%02X;" % (move.l[i].number,value1, value2, value3,move.l[i].delaytime/10)				
				com.write(comout)
				
				link0=ComModule.SerialCode()
				link0.command[0]="CANLINK"
				link0.command[1]="A"
				link0.option[0]="ID"
				link0.suboption[0]="%d" % move.l[i].number
				link0.option[1]="COM"
				link0.suboption[1]="1"
				link0.data[0]=(int(value1)>>8)&0xFF
				link0.data[1]=(int(value1)>>0)&0xFF
				link0.data[2]=(int(value2)>>8)&0xFF
				link0.data[3]=(int(value2)>>0)&0xFF
				link0.data[4]=(int(value3)>>8)&0xFF
				link0.data[5]=(int(value3)>>0)&0xFF
				link0.data[6]=0x01
				link0.data[7]=move.l[i].delaytime/10
				link0.data_size=8
				print link0.encode()


		outprint=str(move.l[1].get_machinepoint())
		gui.lv0.set(outprint)

		
		#gui.t0.insert(Tkinter.END, com.read_all())
		#gui.t0.insert(Tkinter.END, "rec\n")
		
		#com.write("#FUNC.A-ID.1-COM.1:%04X%04X%04X0108;" % (value1, value2, value3))
		#gui.lv1.set("#FUNC.A-ID.1-COM.1\n:%04X%04X%04X0108;" % (value1, value2, value3))
		
		time.sleep(0.05)

gui=GuiModule.GuiModule()
com=ComModule.ComModule("serial","")#serial or remote
gamepad=GamePadModule.GamePadModule()
move=MoveUnit.MoveUnit()

t=threading.Thread(target=interval)
t.setDaemon(True)
t.start()

gui.mainloop()
sys.exit()
time.sleep(2)
tflag=False
t.join()
print "END"
sys.exit()
