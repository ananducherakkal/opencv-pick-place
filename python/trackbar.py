import cv2

def nothing (x):
    pass

class Trackbar():
    def __init__(self, trackbars):     
        self.trackbars = trackbars
        self.window_name = "Trackbar"

    def showTrackbar (self):
        cv2.namedWindow(self.window_name)
        for key, value in self.trackbars.items():
            cv2.createTrackbar(key,self.window_name,value[0],value[1],nothing)
            cv2.setTrackbarPos(key,self.window_name,value[2])
    
    def getTrackbarValue (self, name):
        trackbar = self.trackbars[name]
        value = cv2.getTrackbarPos(name, self.window_name)
        if trackbar[2] and value % 2 == 0:
            value += 1
        return value