import cv2
import vision
from ballClass import ball 

cam = cv2.VideoCapture(0)

balls = []
while(1):
    got_frame, frame = cam.read()

    
    vision.find_balls(frame, balls)

    for b in balls:
        cv2.circle(frame, (b.pos[0],b.pos[1]), 3, (255,0,0),3)
    
    cv2.imshow("frame",frame)
    k = cv2.waitKey(0)
    if k == 27:
        break 