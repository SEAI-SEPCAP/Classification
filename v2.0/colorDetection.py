## function for returning colors found in a image
## written specifically for SEAI-SEPCAP project
##
## inputs: (image) image to detect color         
##
## outputs: (colors_detected) capsule colors detected


#imports
from boundingBox import boundBox
from aux_functions import area
import cv2 as cv
import numpy as np

def colorDetector(image, min_area, proportion):

    colors_detected = []
    p = proportion

    #boundaries for each color - NEED ADJUSTING
    boundaries = [
    ([80,80,220],[110,110,255], 'red'), 
    ([90,120,50],[120,160,110], 'dark green'),
    ([185,200,160],[210,220,180], 'light green'),
    ([235,235,235],[255,255,255], 'white'),
    ([100,210,230],[130,230,255], 'nude'),
    ([50,200,220],[80,240,255], 'yellow'),
    ([100,170,220],[130,210,255], 'orange')
    ]

    #black mask for detection of capsule and cropping
    mask = cv.inRange(image, np.array([0,0,0]) , np.array([85,85,85]))
    mask = (255 - mask)

    rect = boundBox(image, mask, min_area = min_area)

    if len(rect) == 1:
        #crop image
        crop = image[rect[0][1]+int((1-p) * rect[0][1]):rect[0][1] + int(p * rect[0][3]), \
             rect[0][0]+int((1-p) * rect[0][2]):rect[0][0] + int(p * rect[0][2])]
        
        cv.imshow("Cropped image", cv.resize(crop, None, fx = 3, fy = 3, interpolation= cv.INTER_CUBIC))

        #detect colors in cropped image
        for (lower,upper, color) in boundaries:
            lower = np.array(lower, dtype = 'uint8')
            upper = np.array(upper, dtype= 'uint8')
            
            if cv.inRange(crop, lower, upper).any():
                colors_detected.append(color)
    
    else:
        colors_detected = []

    return colors_detected