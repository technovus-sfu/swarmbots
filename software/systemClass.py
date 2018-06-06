import cv2
import math
import serial

import vision
import imgsample as imgsamp 
from robotClass import *

# 1 = carts wont move
gathering_data = 0

# robot 1
whiteLower  = (230, 230, 230)
whiteUpper  = (255, 255, 255)
# robot 2
blueLower  = (170, 180, 130)
blueUpper  = (255, 255, 180)
# robot 3
brownLower  = (80, 130, 180)
brownUpper  = (120, 170, 230)

number_of_robots = 3

#sensitivity
sensitivity = 10


class system:
	distance_between_robots = 250

	target = [650,360]
	goal_post = [65,360]

	robot_positions_prev = [[0,0,0]] * number_of_robots

	cart1 = robot(whiteLower, 	whiteUpper	, 1)
	cart2 = robot(blueLower	, 	blueUpper	, 2)
	cart3 = robot(brownLower, 	brownUpper	, 3)

	carts = [cart1, cart2, cart3]

	cart_color_ranges = [ ]
	#
	def __init__ (self, address1, address2, address3):
		self.cart1.initialize_port(address1, self.target)
		self.cart2.initialize_port(address2, self.target)
		self.cart3.initialize_port(address3, self.target)
			
	#play function
	def play(self, cam):

		robot_positions = [[0,0,0]]*number_of_robots
		
		colorpicker = imgsamp.activeFrame(cam,imgsamp.MODE_PICKCOLOR)

		for i in range(number_of_robots):
			midval = colorpicker.analizeframe("Select Robot "+str(i))
			if midval is not None:
				self.carts[i].colorLower = (int(midval[0]-sensitivity),int(midval[1]-sensitivity),int(midval[2]-sensitivity))
				self.carts[i].colorUpper = (int(midval[0]+sensitivity),int(midval[1]+sensitivity),int(midval[2]+sensitivity))

		print(type(self.carts[0].colorLower),type(self.carts[0].colorLower[0]),type(self.carts[1].colorLower),type(self.carts[1].colorLower[0]))
		while 1:
			(got_frame, frame) = cam.read()
			
			# find robots
			for i in range(number_of_robots):
				robot_positions[i] =  vision.find_robots(frame, self.carts[i].colorLower,\
				 self.carts[i].colorUpper, self.carts[i].ID)

			#get new ball position
			ball_position = vision.get_target(frame)

			print (" ")
			print (robot_positions)
			for i, cart in enumerate(self.carts):
				print("cart",i,"lower:",cart.colorLower)
				print("cart",i,"upper:",cart.colorUpper)

			# set robot current positions and manuever them
			for i, value in enumerate(robot_positions):
				if value != [0,0,0]:
					self.carts[i].current_position = robot_positions[i]
					if gathering_data == 0:
						self.carts[i].move()
				else:
					self.carts[i].stop()

			# set target to be ball
			if ball_position:
				self.target = ball_position
			else:
				self.target = [650,360]

			# set robot targets 
			self.set_robot_target()
			#
			self.robot_positions_prev = robot_positions

			cv2.circle(frame,(self.target[0], self.target[1]),2,(0,255,0),3);
			cv2.imshow('frame', frame)
			
			if cv2.waitKey(1) == 27:
				for i, cart in enumerate(self.carts):
					cart.stop()
					print("stopped cart ",i)
				break

	# set target of all robots
	def set_robot_target(self):
		for i in range(0, number_of_robots):
			# setting x target_pos
			if self.carts[i].current_position[0] > self.target[0]+50:
				self.carts[i].target_position = [self.target[0]+150, self.target[1]]
			else:
				self.carts[i].target_position[0] = self.target[0]
				# setting y target_pos
				if self.carts[i].current_position[1] < self.target[1]-50:
					self.carts[i].target_position[1] = self.target[1]-150
				else:
					self.carts[i].target_position[1] = self.target[1]+150
			print (self.carts[i].ID, self.carts[i].target_position)

