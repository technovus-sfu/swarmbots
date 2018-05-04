import cv2
import vision

cam = cv2.VideoCapture(0)

while(1):
    got_frame, frame = cam.read()
    circles = vision.find_location(frame)
    
    print(circles)
    if circles is not None:
        for c in circles[0,:]:
            cv2.circle(frame,(c[0],c[1]), c[2] ,(0,0,255),3)
            cv2.circle(frame,(c[0],c[1]), 1 ,(0,0,255),3)

    cv2.imshow("frame",frame)
    k = cv2.waitKey(0)
    if k == 27:
        break