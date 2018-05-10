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


def find_balls(frame, balls):
    circles = find_circles(frame,50,150)

    Lower = (164, 200, 120)
    Upper = (15, 255, 255)

    red_centers, red_contours = find_color_blocks(frame, Lower, Upper)
    cv2.drawContours(frame, red_contours, -1, (0,255,0), 1)
    
    print(circles)

    # find positions where balls are
    positions = []
    if circles is not None:
        for circle in circles[0,:]:
            cv2.circle(frame,(circle[0],circle[1]), circle[2] ,(0,0,255),3)
            cv2.circle(frame,(circle[0],circle[1]), 1 ,(0,0,255),3)
            if len(red_centers) > 0:
                for center in red_centers:
                    dist = math.hypot(circle[0] - center[0], circle[1] - center[1])
                    if dist < circle[2]: 
                        positions.append(circle)

    # each position finds closest ball, prioritizing live balls, 
    selected_balls = []
    selected_balls_live = []
    if len(positions) > 0:
        for position in positions:
            best_dist = None
            if len(balls) > 0:
                for ball in balls:
                    dist = math.hypot(position[0] - ball.pos[0], position[1] - ball.pos[1])
                    if (dist < best_dist or best_dist == None) and ball.positionisvalid(position):
                        closest = ball
                        best_dist = dist
                        if ball.live:
                            closest_live = ball
            
            selected_balls.append(closest)   
            selected_balls_live.append(closest_live)
    

        

    print(positions)
    for p in positions:
        cv2.circle(frame, (p[0],p[1]), 3, (255,0,0),3)


# find positions where balls are
# each position finds closest ball and closest live ball
# ask balls if that position is within predicted area
    # proximity
    # projected velocity
# tag each ball with position
# if ball has no position, ice it
    # if iced ball claims position, revive it
# if unclaimed position, make new ball and delete iced balls

