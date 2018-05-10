import cv2
import vision

cam = cv2.VideoCapture(1)
while(1):
    got_frame, frame = cam.read()
    # frame = cv2.imread('colorbar.png',1)
    minR = 50
    maxR = 125
    circles = vision.find_circles(frame,minR,0)

    #hue in find_color_blocks is cyclical; if lower bigger than upper, the range wraps around
    redLower = (164, 150, 150)
    redUpper = (15, 255, 255)

    gotContours, red_contours = vision.find_color_blocks(frame, redLower, redUpper)
    cv2.drawContours(frame, red_contours, -1, (0,255,255), 2)

    print(circles)
    if circles is not None:
        for c in circles[0,:]:
            cv2.circle(frame,(c[0],c[1]), c[2] ,(255,0,0),3)
            cv2.circle(frame,(c[0],c[1]), 1 ,(255,0,0),3)

    cv2.imshow("frame",frame)
    k = cv2.waitKey(0)
    if k == 27:
        break 