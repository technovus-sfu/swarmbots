from systemClass import *

system = system(["COM5"])

cam = cv2.VideoCapture(3)

###
system.play(cam)
###

cam.release()
cv2.destroyAllWindows()
