import cv2


MODE_VIEW = 0
MODE_PICKCOLOR = 1


class activeFrame:
    
    title = "Title"
    text = "[- - -]"
    frame = None
    color = (0,255,255)
    mode = MODE_VIEW
    retval = None

    def __init__(self,cam,mode=MODE_VIEW):
        self.cam = cam
        self.mode = mode
        cv2.namedWindow('frame')
        cv2.setMouseCallback('frame',self.mouse_event)

    def analizeframe(self,title="Title"):   
        self.title = title
        while 1:
            ret, self.frame = self.cam.read()
            cv2.putText(self.frame,self.title,(5,25),cv2.FONT_HERSHEY_PLAIN ,2,self.color,2,cv2.LINE_8,False)
            cv2.putText(self.frame,self.text,(5,53),cv2.FONT_HERSHEY_PLAIN ,2,self.color,2,cv2.LINE_8,False)
            cv2.imshow('frame',self.frame)
            if cv2.waitKey(20) & 0xFF == 27:
                return None
            if self.retval is not None: 
                temp = self.retval
                self.retval = None
                return temp

    def mouse_event(self, event,x,y,flags,param):
        if event == cv2.EVENT_MOUSEMOVE:
            self.text = str(self.frame[y][x])
            self.color = (int(self.frame[y][x][0]),int(self.frame[y][x][1]),int(self.frame[y][x][2]))
        if event == cv2.EVENT_LBUTTONDOWN and self.mode == MODE_PICKCOLOR:
            self.retval = self.frame[y][x]
        

# fuck = activeFrame(cv2.VideoCapture(2))     
