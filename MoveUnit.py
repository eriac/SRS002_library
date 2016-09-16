#!/usr/bin/env python
# -*- coding: utf8 -*-

## @package MoveUnit
#  Class for Make Legs motion
#  @date 2016/9/15
#  @version 0.1

import sys
import Tkinter
import math
import time
import threading
import xml.etree.ElementTree as et
import os

## Class for Make Legs motion
#  Read params from MoveUnit.xml
# @code{.py}
#
#sys.exit()
# @endcode
class MoveUnit:
	##Initialize
	#(future: read data from MoveUnit.xml)
	def __init__(self):
		base = os.path.dirname(os.path.abspath(__file__))
		name = os.path.normpath(os.path.join(base, 'MoveUnit.xml'))
		tree = et.parse(name) # 返値はElementTree型
		elem = tree.getroot() # ルート要素を取得(Element型)

		self.l=[UnitLeg(),UnitLeg(),UnitLeg(),UnitLeg(),UnitLeg(),UnitLeg()]
		e=elem.findall("UnitLeg")
		for i in range(6):
			self.l[i].side=         e[i].attrib["Side"]
			self.l[i].number=   int(e[i].attrib["ID"])
			self.l[i].origin[0]=int(e[i].find("Origin").attrib["x"])
			self.l[i].origin[1]=int(e[i].find("Origin").attrib["y"])
			self.l[i].origin[2]=int(e[i].find("Origin").attrib["z"])
			self.l[i].home[0]=  int(e[i].find("Home").attrib["x"])
			self.l[i].home[1]=  int(e[i].find("Home").attrib["y"])
			self.l[i].home[2]=  int(e[i].find("Home").attrib["z"])

		#for tick
		self.mode_current="home"
		self.mode_target="home"
		self.submode=""
		self.count=0
		self.inter=50
		self.axis=[0.0,0.0,0.0,0.0]

		#for walk
		self.a_side=[0,2,4]
		self.b_side=[1,3,5]
		self.f_leg=self.a_side
		self.g_leg=self.b_side
		self.walkscale_x=20
		self.walkscale_y=40
		self.walkscale_rz=0.15
		self.walkscale_zup=40
		self.move_x=0
		self.move_y=0
		self.move_rz=0
		self.move_z=0
		#for slide
		self.walkscale_z=40
	
	##Set inter time		
	def set_inter(self,inter):		
		self.inter=inter
	
	##Culculate step
	def tick(self):
		if(self.mode_current=="home"):
			if(self.mode_target=="walk"):
				self.mode_current="walk"
				self.submode="pre1"
			elif(self.mode_target=="slide"):
				self.mode_current="slide"
			elif(self.mode_target=="rest"):
				self.mode_current="rest"
			for i in range(6):
				self.l[i].set_machinepoint(self.l[i].home)
		elif(self.mode_current=="walk"):
			self.tick_walk()
		elif(self.mode_current=="slide"):
			self.tick_slide()
		elif(self.mode_current=="rest"):
			self.tick_rest()

	## Set mode
	#  @param mode "walk" or "slide" or "rest"
	def set_mode(self,mode):
		if(mode=="walk"):
			self.mode_target="walk"
		elif(mode=="slide"):
			self.mode_target="slide"
		elif(mode=="rest"):
			self.mode_target="rest"	

	## Set params
	#  @param value0~3 float value -1.0~+1.0 
	def set_axis(self,value0,value1,value2,value3):
		self.axis[0]=value0
		self.axis[1]=value1
		self.axis[2]=value2
		self.axis[3]=value3

	##Called from tick etc.
	def convert_towalk(self, home, previous, slide_x, slide_y, rotate_z, pos_z):
		ret=[0.0,0.0,0.0]
		if(math.isnan(slide_x)):slide_x=previous[0]-home[0]
		if(math.isnan(slide_y)):slide_y=previous[1]-home[1]
		ret[0]=home[0]*math.cos(rotate_z)-home[1]*math.sin(rotate_z)+slide_x
		ret[1]=home[0]*math.sin(rotate_z)+home[1]*math.cos(rotate_z)+slide_y
		ret[2]=home[2]+pos_z
		return ret

	##Called from tick
	def tick_walk(self):
		if(self.count<=0):
			NaN=float("nan")
			if(self.submode=="pre1"):
				self.move_z=self.walkscale_zup
				for i in self.f_leg:
					self.walkmotion(i,0,0,0,self.move_z)
					self.l[i].set_command(200)
				self.submode="step2"
				self.count=200
			elif(self.submode=="step1"):
				for i in self.f_leg:
					self.walkmotion(i,-self.move_x,-self.move_y,-self.move_rz,self.move_z)
					self.l[i].set_command(200)
				if(self.mode_target!="walk"):
					self.submode="post1"
					self.count=200
				else:
					self.submode="step2"
					self.count=200
			elif(self.submode=="step2"):		
				self.move_x=self.walkscale_x*self.axis[0]
				self.move_y=self.walkscale_y*self.axis[1]
				self.move_rz=-self.walkscale_rz*self.axis[2]
				for i in self.f_leg:
					self.walkmotion(i,self.move_x,self.move_y,self.move_rz,self.move_z)
					self.l[i].set_command(500)
				for i in self.g_leg:
					self.walkmotion(i,-self.move_x,-self.move_y,-self.move_rz,0)
					self.l[i].set_command(500)
				self.submode="step3"
				self.count=500
			elif(self.submode=="step3"):
				for i in self.f_leg:
					self.walkmotion(i,self.move_x,self.move_y,self.move_rz,0)
					self.l[i].set_command(200)
				if(self.f_leg is self.a_side):
					self.f_leg=self.b_side[:]
					self.g_leg=self.a_side[:]
				else:
					self.f_leg=self.a_side
					self.g_leg=self.b_side
				self.submode="step1"
				self.count=200
			elif(self.submode=="post1"):
				for i in self.f_leg:
					self.walkmotion(i,0,0,0,self.move_z)
					self.l[i].set_command(500)
				for i in self.g_leg:
					self.walkmotion(i,0,0,0,0)
					self.l[i].set_command(500)
				self.submode="post2"
				self.count=500
			elif(self.submode=="post2"):
				for i in self.f_leg:
					self.walkmotion(i,0,0,0,0)
					self.l[i].set_command(200)
				self.mode_current="home"
				self.count=200
		else:
			self.count-=self.inter

	##Called from tick
	def tick_slide(self):
		if(self.count<=0):
			if(self.mode_target!="slide"):
				for i in range(6):
					self.l[i].set_machinepoint(self.l[i].home)
					self.l[i].set_command(500)
				self.mode_current="home"
				self.count=500
			else:
				self.move_x=self.walkscale_x*self.axis[0]
				self.move_y=self.walkscale_y*self.axis[1]
				self.move_z=self.walkscale_z*self.axis[2]
				for i in range(6):
					self.l[i].set_machinepoint(self.l[i].vecadd(self.l[i].home,[self.move_x,self.move_y,self.move_z]))
					self.l[i].set_command(100)
				self.count=100
		else:
			self.count-=self.inter

	##Called from tick
	def tick_rest(self):
		if(self.count<=0):
			if(self.mode_target!="rest"):
				for i in range(6):
					self.l[i].set_machinepoint(self.l[i].home)
					self.l[i].set_command(1000)
				self.mode_current="home"
				self.count=1000
			else:
				for i in range(6):
					self.l[i].set_machinepoint(self.l[i].vecadd(self.l[i].home,[0,0,70]))
					self.l[i].set_command(1000)
				self.count=1000
		else:
			self.count-=self.inter

	##Called from tick or etc
	def walkmotion(self,i,slide_x,slide_y,rotate_z,pos_z):
		self.l[i].set_machinepoint(self.convert_towalk(self.l[i].home,self.l[i].get_machinepoint(),slide_x,slide_y,rotate_z,pos_z))


class UnitLeg:
	def __init__(self):
		self.local=[0,0,0]#point from origin_point in local dir
		self.origin=[0,0,0]
		self.home=[0,0,0]#in machine dir
		self.side="R"#"R"or"L"
		self.arm1=30
		self.angle1=0
		self.arm2=50
		self.angle2=0
		self.arm3=70
		self.angle3=0
		self.arm4=34
		self.arm5=90
		self.ready=False
		self.delaytime=0
		self.number=0
	def set_localpoint(self,local):
		try:
			armv = math.sqrt(self.arm4**2 + self.arm5**2);
			armvangleoffset = math.atan2(self.arm5, self.arm4);
			pl=math.sqrt((local[0]-self.arm1)**2+local[1]**2)-self.arm2
			self.angle1=math.atan2(local[1],local[0]-self.arm1)
			self.angle2=self.anticulc1(self.arm3,armv,pl,local[2])
			self.angle3=self.anticulc2(self.arm3,armv,pl,local[2])+armvangleoffset
			self.local=local
		except:
			print "EEROR legdata.setloclpont"
	def set_machinepoint(self,machine):
		if(self.side=="R"):
			self.set_localpoint(self.vecsub(machine,self.origin))
		elif(self.side=="L"):
			self.set_localpoint(self.z_invert(self.vecsub(machine,self.origin)))
	def get_machinepoint(self):
		ret=[0.0,0.0,0.0]
		if(self.side=="R"):
			ret=self.vecadd(self.origin,self.local)
		elif(self.side=="L"):
			ret=self.vecadd(self.origin,self.z_invert(self.local))
		return ret
	def get_leglines(self):
		a1=[self.arm1,0,0]
		a2=[self.arm2*math.cos(self.angle1),self.arm2*math.sin(self.angle1),0]
		a3=[self.arm3*math.cos(self.angle2)*math.cos(self.angle1),
		    self.arm3*math.cos(self.angle2)*math.sin(self.angle1),
		    self.arm3*math.sin(self.angle2)]
		a4=[self.arm4*math.cos(self.angle2+self.angle3)*math.cos(self.angle1),
		    self.arm4*math.cos(self.angle2+self.angle3)*math.sin(self.angle1),
		    self.arm4*math.sin(self.angle2+self.angle3)]
		a5=[self.arm5*math.cos(self.angle2+self.angle3-math.pi/2.0)*math.cos(self.angle1),
		    self.arm5*math.cos(self.angle2+self.angle3-math.pi/2.0)*math.sin(self.angle1),
		    self.arm5*math.sin(self.angle2+self.angle3-math.pi/2.0)]
		if(self.side=="R"):
			p0=self.origin
			p1=self.vecadd(p0,a1)
			p2=self.vecadd(p1,a2)
			p3=self.vecadd(p2,a3)
			p4=self.vecadd(p3,a4)
			p5=self.vecadd(p4,a5)
		elif(self.side=="L"):
			p0=self.origin
			p1=self.vecadd(p0,self.z_invert(a1))
			p2=self.vecadd(p1,self.z_invert(a2))
			p3=self.vecadd(p2,self.z_invert(a3))
			p4=self.vecadd(p3,self.z_invert(a4))
			p5=self.vecadd(p4,self.z_invert(a5))
		return [p0,p1,p2,p3,p4,p5]
	def vecadd(self,x1, x2):
		if(len(x1)==len(x2)):
			ret=[]
			for i in range(len(x1)):
				ret.append(x1[i]+x2[i])
			return ret
		else:
			print "ERROR legdata.vecadd"
			return []
	def vecsub(self,x1, x2):
		if(len(x1)==len(x2)):
			ret=[]
			for i in range(len(x1)):
				ret.append(x1[i]-x2[i])
			return ret
		else:
			print "ERROR legdata.vecadd"
			return []
	def z_invert(self, x):
		x[0]=-x[0]
		x[1]=-x[1]
		return x
	def anticulc1(self,rod1,rod2,pl,pz,):
		try:
			ret=math.acos((rod1 * rod1 + pl * pl + pz * pz - rod2 * rod2) /  \
			(2 * rod1 * math.sqrt(pl * pl + pz * pz))) + math.atan2(pz, pl);
		except:
			raise
		return ret

	def anticulc2(self,rod1,rod2,pl,pz,):
		try:
			ret=math.acos((rod1 * rod1 + rod2 * rod2 - (pl * pl + pz * pz)) / (2 * rod1 * rod2)) - math.pi;
		except:
			raise
		return ret
	def set_command(self,delaytime):
		self.ready=True
		self.delaytime=delaytime
