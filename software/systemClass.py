import cv2
import math
import serial

import vision
from robotClass import *

class system:
	distance_between_robots = 250

	target = [650,360]
	goal_post = [65,360]

	robot_positions_prev = [None] * 3

	cart1 = robot()
	cart2 = robot()
	cart3 = robot()

	def __init__ (self, address1, address2, address3):
		self.cart1.initialize(address1, self.target)
		self.cart2.initialize(address2, self.target)
		self.cart3.initialize(address3, self.target)

	#play function
	def play(self, cam):
		while 1:
			(got_frame, frame) = cam.read()

			robot_positions = vision.find_robots(frame)

			robot_positions = self.match(robot_positions)

			ball_position = vision.get_target(frame)

			print (" ")
			print (robot_positions)
			carts = []
			# set target of robots
			if len(robot_positions) > 0:
				self.cart1.current_position = robot_positions[0]
				carts.append(self.cart1.current_position)
				# self.cart1.move()

			if len(robot_positions) > 1:
				self.cart2.current_position = robot_positions[1]
				carts.append(self.cart2.current_position)
				# self.cart2.move()

			if len(robot_positions) >2:
				self.cart3.current_position = robot_positions[2]
				carts.append(self.cart3.current_position)
				# self.cart3.move()
			
			else:
				print (" cant see robot")
				self.allstop()
			# set target to be ball
			if ball_position:
				self.target = ball_position
			else:
				self.target = [650,360]
			#
			self.set_target(self.target, robot_positions)
			self.robot_positions_prev = robot_positions

			cv2.circle(frame,(self.target[0], self.target[1]),2,(0,255,0),3);
			cv2.imshow('frame', frame)
			cv2.waitKey(0)

	# set target of all robots
	def set_target(self, target, robot_positions):
		# print i in robot_positions
		carts = [self.cart1, self.cart2, self.cart3]
		print (target)
		for i in range(0, min(3,len(robot_positions))):
			# setting x target_pos
			if carts[i].current_position[0] > target[0]+50:
				carts[i].target_position = [target[0]+150, target[1]]
			else:
				carts[i].target_position[0] = target[0]
				# setting y target_pos
				if carts[i].current_position[1] < target[1]-50:
					carts[i].target_position[1] = target[1]-150
				else:
					carts[i].target_position[1] = target[1]+150
			# print carts[i].target_position

	# stops all carts
	def allstop(self):
		self.cart1.stop()
		self.cart2.stop()
		self.cart3.stop()

	# main consistency on array of new robot positions
	def match(self, robot_positions):
		 
		new_positions = [None] * len(self.robot_positions_prev)

		# keeps track of which new positions have been matched to an old value
		matched = [0] * len(robot_positions)	

		for i in range(len(self.robot_positions_prev)):
			
			if self.robot_positions_prev[i] != None:
				for j in range(len(robot_positions)):
					
					if math.hypot(self.robot_positions_prev[i][0] - robot_positions[j][0], self.robot_positions_prev[i][1] - robot_positions[j][1]) < 50 \
					and abs(self.robot_positions_prev[i][2] - robot_positions[j][2]) < 20:
						
						new_positions[i] = robot_positions[j]
						matched[j] = 1
						break
				else:
					new_positions[i] = self.robot_positions_prev[i]

		for pos in new_positions:
			if pos == None:
				for i in matched:
					if i == 0:
						pos = robot_positions[i]
						i = 1
		
		robot_positions[:] = new_positions[:]
