import numpy as np
import cv2
import math
from ballClass import ball

# finds coordinates of all circles
# formerly named find_position
def find_circles(frame, minR=0, maxR=0):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # cv2.HoughCircles(image, method, dp, minDist)
    minDist = max((2*.9)*minR,1)
    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT, 2, minDist,
        param1=150, param2=100, minRadius=minR, maxRadius=maxR) #150/100

    if circles is not None:
        circles = np.uint16(np.around(circles))
        # returns circles = [x_Centre y_centre radius]
        return circles

# find contours of color specified
def rangeContours(hsv, colorLower, colorUpper):
    if colorLower[0] > colorUpper[0]:
        mask = cv2.inRange(hsv,(0,colorLower[1],colorLower[2]),colorUpper)
        mask2 = cv2.inRange(hsv,colorLower,(179,colorUpper[1],colorUpper[2]))
        mask = mask | mask2
    else:
        mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # returns contours of the color speicified
    return cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# finds coordinates of the green orientation block
def find_color_blocks(frame, lower, upper):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    cont_frame, contours, hierarchy = rangeContours(hsv, lower, upper)
    centers = []

    for i, cont in enumerate(contours, start=0):
        M = cv2.moments(cont)
        centers.append( [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])] )
    # returns centres of green block + contours to plot it
    return [centers, contours]

# returns the location (of centre) + orientation of the robot
def find_robots(frame):
    minR = 50; 
    maxR = 125;
    
    circles = cv2.find_circles(frame, minR, maxR)
    
    greenLower = (90, 150, 50)
    greenUpper = (186, 255, 130)
    
    #find orientation block
    (green_centre, green_contours)  = find_color_blocks(frame, greenLower, greenUpper);
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


def find_balls(frame):
    circles = find_circles(frame,50,0)

    red_centers, red_contours = find_color_blocks(frame, ball.Lower, ball.Upper)
    cv2.drawContours(frame, red_contours, -1, (0,255,0), 1)

    print("color centres: ", red_contours)
    print("circles: ",circles)
    
    # find positions where balls are
    positions = []
    if circles is not None:
        for i in circles[0,:]:
            cv2.circle(frame,(i[0],i[1]), i[2] ,(0,0,255),3)
            cv2.circle(frame,(i[0],i[1]), 1 ,(0,0,255),3)
            if red_centers is not None:
                for j in red_centers:
                    x_delta = i[0] - j[0]
                    y_delta = i[1] - j[1]
                    distance = math.hypot(x_delta, y_delta);
                    if (distance < i[2]*1.5): 
                        positions.append([i[0], i[1]])

# find positions where balls are
# ask balls if a position is within predicted area
    # proximity
    # projected velocity
# tag each ball with position
    # if multiple claim same position, closest wins, iced loses 
# if ball has no position, ice it
    # if iced ball claims position, de-ice it
# if unclaimed position, make new ball and delete iced balls

