import numpy as np
import cv2
import math

#ball color
redLower    = (0, 0, 130)
redUpper    = (100, 100, 255)
# robot alignment color
greenLower  = (80, 140, 50)
greenUpper  = (190, 255, 160)

def show_all(frame):
    mask1 = cv2.inRange(frame, whiteLower, whiteUpper)
    mask2 = cv2.inRange(frame, redLower, redUpper)
    mask3 = cv2.inRange(frame, greenLower, greenUpper)

    cv2.imshow('white', mask1)
    cv2.imshow('red', mask2)
    cv2.imshow('green', mask3)


# finds coordinates of the circle
def find_location(frame, colorLower, colorUpper):
    cont_frame, contours, hierarchy = rangeContours(frame, colorLower, colorUpper)

    circles = []
    minR = 20;
    maxR = 80;

    for i, cnt in enumerate(contours, start=0):
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        centre = (int(x), int(y))
        radius = int(radius)
        a = cv2.contourArea(cnt)
        if math.pi*minR*minR < a < math.pi*maxR*maxR:
            circles.append([centre[0], centre[1], radius])
    # returns stats (centre, area) of green block + contours to plot it
    return circles

# find contours of color specified
def rangeContours(frame, colorLower, colorUpper):
    mask = cv2.inRange(frame, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # returns contours of the color speicified
    return cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# returns the location (of centre) + orientation of the robot
def get_target(frame):
    sensitivity = 50
    
    minR = 15
    maxR = 80

    cont_frame, contours, hierarchy = rangeContours(frame, redLower, redUpper)
    
    # cv2.drawContours(frame, contours, -1, (0,255,0), 1)
    # centers = [] 
    
    for i, cnt in enumerate(contours, start=0):
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        centre = (int(x), int(y))
        radius = int(radius)
        a = cv2.contourArea(cnt)

        if math.pi*minR*minR < a < math.pi*maxR*maxR:
            return [centre[0], centre[1]]

# finds coordinates of the green orientation block
def find_orientation_block(frame):
    sensitivity = 50

    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    centers = []
    
    for i, cont in enumerate(contours, start=0):
        M = cv2.moments(cont)
        centers.append( [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])] )
    # returns centres of green block + contours to plot it
    return [centers, contours]

# returns the location (of centre) + orientation of the robot
def find_robots(frame, colorLower, colorUpper, robot_ID):
    circles                         = find_location(frame, colorLower, colorUpper);
    (green_centre, green_contours)  = find_orientation_block(frame);
    robots = [0,0,0]
    for _, i in enumerate(circles):
        if len(green_centre) > 0:
            for j, green in enumerate(green_centre):
                x_delta = i[0] - green[0];
                y_delta = i[1] - green[1];
                distance = math.hypot(x_delta, y_delta);
                angle = math.atan2(y_delta, x_delta) * 180/math.pi;
                # only mates the green blocks to close by circle
                if (distance < i[2]*1.4): 
                    robots = [i[0], i[1], angle];
                    # found robot
                    cv2.circle(frame, (i[0],i[1]),i[2],(255,0,0),2); # draw the outer circle
                    cv2.circle(frame, (i[0],i[1]),2,   (0,0,255),3); # draw the center of the circle
                    cv2.circle(frame,(green[0],green[1]),2,(0,255,255),3); # draw the center of the green
                    cv2.drawContours(frame, green_contours[j], -1, (0,255,0), 1) #draw green contours
    cv2.putText(frame, str(robot_ID) , (robots[0],robots[1]),
        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 1);

    # returns stats on robots [x_pos; y_pos; angle]
    return robots