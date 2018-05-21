from systemClass import *

system = system("/dev/cu.HC-05-DevB-1", "/dev/cu.HC-05-DevB-2", "/dev/cu.HC-05-DevB")

cam = cv2.VideoCapture(0)

###
system.play(cam)
###

cam.release()
cv2.destroyAllWindows()
