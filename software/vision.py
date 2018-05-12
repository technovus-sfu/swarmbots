import numpy as np
import cv2
import math
from copy import deepcopy

# finds coordinates of the circle
def find_location(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    minR = 50;
    maxR = 125;
    # # # # # cv2.HoughCircles(image, method, dp, minDist)
    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT, 2, (2*.9)*minR,
        param1=150, param2=100, minRadius=minR, maxRadius=maxR) #150/100

    if circles is not None:
        circles = np.uint16(np.around(circles))
        # returns circles = [x_Centre y_centre radius]
        return circles

# find contours of color specified
def rangeContours(hsv, colorLower, colorUpper):
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # returns contours of the color speicified
    return cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# finds coordinates of the green orientation block
def find_orientation_block(frame):
    sensitivity = 50
    #bgr
    greenLower = (90, 150, 50)
    greenUpper = (186, 255, 130)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cont_frame, contours, hierarchy = rangeContours(frame,greenLower, greenUpper)
    centers = []
    
    for i, cont in enumerate(contours, start=0):
        M = cv2.moments(cont)
        centers.append( [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])] )
    # returns centres of green block + contours to plot it
    return [centers, contours]

# returns the location (of centre) + orientation of the robot
def find_robots(frame):
    circles                         = find_location(frame);
    (green_centre, green_contours)  = find_orientation_block(frame);
    robots = []
    if circles is not None:
        for i in circles[0,:]:
            cv2.circle(frame, (i[0],i[1]),i[2],(255,0,0),2); # draw the outer circle
            cv2.circle(frame, (i[0],i[1]),2,   (0,0,255),3); # draw the center of the circle
            if len(green_centre) > 0:
                cv2.drawContours(frame, green_contours, -1, (0,255,0), 1) #draw green contours
                for j in green_centre:
                    cv2.circle(frame,(j[0],j[1]),2,(0,0,255),3); # draw the center of the green
                    x_delta = i[0] - j[0];
                    y_delta = i[1] - j[1];
                    distance = math.hypot(x_delta, y_delta);
                    angle = math.atan2(y_delta, x_delta) * 180/math.pi;
                    # only mates the green blocks to close by circle
                    if (distance < i[2]*1.5): 
                        robots.append([i[0], i[1], angle]);

    # returns stats on robots [x_pos; y_pos; angle]
    return robots


class systemClass:

    robot_positions_prev = []

    def match(self, robot_positions):
		
        new_positions = [[660,30]] * len(self.robot_positions_prev)

        for i in range(len(self.robot_positions_prev)):
            for j in range(len(robot_positions)):
                if math.hypot(self.robot_positions_prev[i][0] - robot_positions[j][0], self.robot_positions_prev[i][1] - robot_positions[j][1]) < 50 \
                and abs(self.robot_positions_prev[i][2] - robot_positions[j][2]) < 20:
                    new_positions[i] = robot_positions[j]
                    break

        robot_positions[:] = new_positions[:]