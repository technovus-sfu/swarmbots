import math

class ball:


    def __init__(self, xpos=0, ypos=0, radius=0):
        self.pos = [xpos, ypos, radius]
        self.history = []
        self.live = True
    
