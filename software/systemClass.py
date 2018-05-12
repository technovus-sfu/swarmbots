import cv2
import math
import serial

import vision
from robotClass import *

class system:
	distance_between_robots = 250

	target = [650,360]
	goal_post = [65,360]

	robot_positions_prev = [ []*3 ]

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

			ball_position = vision.get_target(frame)

			print " "
			print robot_positions
			carts = []
			# set target of robots
			if len(robot_positions) > 0:
				self.cart1.current_position = robot_positions[0]
				carts.append(self.cart1.current_position)
				# cart1.move()

				if len(robot_positions) > 1:
					self.cart2.current_position = robot_positions[1]
					carts.append(self.cart2.current_position)
					# cart2.move()

				if len(robot_positions) >2:
					self.cart3.current_position = robot_positions[2]
					carts.append(self.cart3.current_position)
					# cart3.move()
			#
			else:
				print " cant see robot"
				self.allstop()
			# set target to be ball
			if ball_position:
				print ball_position
				self.target = ball_position
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
		if target is not None:
			print ball_position
			for i in range(0, min(3,len(robot_positions))):
				# setting x target_pos
				if carts[i].current_position[0] > target[0]:
					carts[i].target_position[0] = target[0]
				else:
					carts[i].target_position[0] = target[0]+200
				# setting y target_pos
				# if (target[1]-100) <= carts[i].current_position[1] <= (target[1]+100):
				# 	carts[i].target_position[1] = target[1]+200
				# else:
				# 	carts[i].target_position[1] = target[1]
				print carts[i].target_position


	# stops all carts
	def allstop(self):
		self.cart1.stop()
		self.cart2.stop()
		self.cart3.stop()


