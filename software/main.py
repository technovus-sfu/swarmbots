from systemClass import *

system = system("COM6", "COM7", "COM9")

cam = cv2.VideoCapture(2)

###
system.play(cam)
###

cam.release()
cv2.destroyAllWindows()
