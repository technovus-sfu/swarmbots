import cv2
import math
import serial

import vision
from robotClass import *

class system:
	distance_between_robots = 250

	target = [650,360]
	goal_post = [65,360]

	carts = []

	def __init__ (self, address1, address2, address3):
		self.carts.append(robot(address1, self.target))
		self.carts.append(robot(address2, self.target))
		self.carts.append(robot(address3, self.target))

	#play function
	def play(self, cam):
		while 1:
			(got_frame, frame) = cam.read()

			#get new position of robots
			new_positions = vision.find_robots(frame)

			#get new ball position
			ball_position = vision.get_target(frame)

			#assign new positions to appropriate robot.
			#returns binary list indicating which robots got new position
			gotnewpos = self.assign_new_positions(new_positions)

			print (" ")
			print (robot_positions)

			# either stop or move bot depending if it recieved new position this frame
			for val in gotnewpos:
				if val == 0:
					cart[val].stop()
				else:
					cart[val].move()
			
			# set target to be ball
			if ball_position:
				self.target = ball_position
			else:
				self.target = [650,360]
			
			self.set_target(robot_positions)
			
			# self.robot_positions_prev = robot_positions

			cv2.circle(frame,(self.target[0], self.target[1]),2,(0,255,0),3);
			cv2.imshow('frame', frame)
			cv2.waitKey(0)

	# set target of all robots
	def set_target(self, robot_positions):
		# print i in robot_positions
		print (self.target)
		for i in range(0, min(3,len(robot_positions))):
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
			# print carts[i].target_position

	# stops all carts
	def allstop(self):
		for cart in carts:
			cart.stop()

	#assign new positions to appropriate robot.
	#return indicates which robots got new position
	def assign_new_positions(self, new_positions):
		
		#binary list indicating if cart changed
		gotnew = [0] * len(carts)

		for i, cart in enumerate(self.carts):
			
			#shitty method of initializing positions, will only work reliably for one bot
			#replace once multiple bots is properly implimented
			if cart.current_position == None:
				cart.current_position = new_positions.pop(0)
				gotnew[i] = 1
			else:

				for pos in new_positions:
					if math.hypot(cart.current_position[0] - pos[0], cart.current_position[1] - pos[1]) < 50 \
					and abs(cart.current_position[2] - robot_positions[2]) < 20:
						cart.current_position = pos
						gotnew[i] = 1
						break
			
		return gotnew