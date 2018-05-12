import serial
import string
import math

class robot:

	address = "/dev/cu.HC-05-DevB"
	speed = 0;
	current_position = [0,0,0]
	target_position = [0, 0]
	distance = 0;
	angle_diff = 0;
	compliment = 0;

	# def __init__ (self):
	# 	pass
	#
	def __init__ (self, address = None, target = None):
		self.address = address
		self.target_position = target
	#
	port = serial.Serial(address, 9600)


	# set address and target
	def initialize(self, address, target):
		self.address = address
		self.target_position = target

	# method to move the robot
	def move(self):
		self.calc_dist_angle()

		print "angle ", self.angle_diff, "distance", self.distance, "compliment", self.compliment

		if 20 <= abs(self.compliment) <= 160 and self.distance > 100:
			print "orientating"
			self.orient()

		elif self.distance > 170:
			print "moving"
			if 160 <= abs(self.angle_diff) <= 200:
				print "should go forward"
				self.forward()
			elif math.floor(abs(self.angle_diff)) in range (0,20)+range(340,360):
				print "should go backward"
				self.backward()
		#
		else:
			self.stop();

	# method to move the robot forward
	def forward(self):
		if abs(self.speed) == 0.5:
			self.speed = 0
		#
		ratio = int(math.ceil((self.distance*8)/1000))
		if self.speed < 2:
			# for i in range(0,ratio):
			print "forward ", ratio, self.speed
			self.port.write("w")
			self.speed = self.speed+1;

	# method to move the robot backward
	def backward(self):
		ratio = int(math.ceil((self.distance*8)/1000))
		if self.speed > -2:
			print "backward", ratio, self.speed
			# for i in range(0,ratio):
			self.port.write("s")
			self.speed = self.speed-1;

	# method to stop the robot
	def stop(self):
		print "stopped"
		self.port.write("q")
		self.speed = 0

	# method to find the required orientation
	def orient(self):
		if abs(self.speed) > 0.5:
			self.speed = 0
		#
		left_turn_conditions = range(-90,0)+range(90,180)+range(-270,-180)+range(270,360)
		right_turn_conditions = range(0,90)+range(-180,-90)+range(180, 270)+range(-360,-270)
		if math.floor(self.angle_diff) in left_turn_conditions and (self.speed > -0.5):
			print "left"
			self.port.write("a")
			self.speed = self.speed - 0.5
		elif math.floor(self.angle_diff) in right_turn_conditions and (self.speed < 0.5):
			print "right"
			self.port.write("d")
			self.speed = self.speed + 0.5

	# method to calculate the distance between robot and target and orientation difference
	def calc_dist_angle(self):
		x_delta = self.target_position[0] - self.current_position[0]
		y_delta = self.target_position[1] - self.current_position[1]
		self.distance = math.hypot(x_delta, y_delta)

		required_orientation = math.atan2(y_delta, x_delta) * 180/math.pi 
		current_orientation = self.current_position[2]
		
		self.angle_diff = (required_orientation - current_orientation)

		#calculates the compliment of angle [0, 90] in each quadrant
		self.compliment = abs(self.angle_diff) - math.floor( abs(self.angle_diff)/180 )*180

	def match(self, robot_positions, self.robot_positions_prev):
		for newpos in newPositions:
			for i in range(len(oldPositions)):
				if math.hypot(newpos[0] - oldPositions[i][0], newpos[1] - oldPositions[i][1]) < 50 and abs(newpos[2] - oldPositions[i][2]) < 20:
					oldPositions[i] = newpos
					break
		return oldPositions
