import cv2
import vision
from ballClass import ball 

cam = cv2.VideoCapture(0)
while(1):
    got_frame, frame = cam.read()

    vision.find_balls(frame)

    cv2.imshow("frame",frame)
    k = cv2.waitKey(10)
    if k == 27:
        break 