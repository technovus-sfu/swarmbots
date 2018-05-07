import cv2
import vision

cam = cv2.VideoCapture(0)

while(1):
    got_frame, frame = cam.read()

    minR = 50
    maxR = 125
    circles = vision.find_circles(frame,minR,0)
    
    redLower = (0, 150, 50)
    redUpper = (255, 255, 130)

    gotContours, red_contours = vision.find_color_blocks(frame, redLower, redUpper)
    cv2.drawContours(frame, red_contours, -1, (0,255,0), 1)

    print(circles)
    if circles is not None:
        for c in circles[0,:]:
            cv2.circle(frame,(c[0],c[1]), c[2] ,(0,0,255),3)
            cv2.circle(frame,(c[0],c[1]), 1 ,(0,0,255),3)

    cv2.imshow("frame",frame)
    k = cv2.waitKey(0)
    if k == 27:
        break 