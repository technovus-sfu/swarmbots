import math

class ball:

    def __init__(self, xpos=0, ypos=0, radius=0):
        self.pos = [xpos, ypos]
        self.rad = radius
        self.history = []
        self.live = True
    

    # given a number of detected possible positions, guess which belongs to this instance.
    # returns index in position array
    # def positionisvalid(self, position):
