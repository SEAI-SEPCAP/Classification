import cv2 as cv

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self,c):
        shape = "unidentified"
        peri = cv.arcLength(c,True)
        approx = cv.approxPolyDP(c,0.04*peri,True)
        
        if len(approx)==3:
            shape = "triangle"

        elif len(approx)==4:
            (x,y,w,h) = cv.boundingRect(approx)
            ar = w / float(h)

            shape = "square" if ar >=0.95 and ar <=1.05 else "rectangle"

        elif len(approx)==5:
            shape = "pentagon"
        
        elif len(approx)==10:
            shape = "star"

        else:
            shape = "circle"

        return shape

