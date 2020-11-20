import cv2
import numpy as np
import argparse

image = cv2.imread("Images\\no_flash.jpeg")

## just to resize image that's too big
image = cv2.resize(image,None,fx=0.2,fy=0.2, interpolation = cv2.INTER_CUBIC)

# defining color boundaries - list of tuples with RGB values of upper and lower limits of the color
# we must define all the colors present
# red  white dark_green  light_green  yellow  orange
boundaries = [
    ([40,20,200],[55,35,240], 'red'), 
    ([80,100,0],[100,120,35], 'dark green'),
    ([185,200,160],[210,220,180], 'light green'),
    ([200,220,220],[255,255,255], 'white'),
    ([70,180,200],[90,195,225], 'nude'),
    ([0,200,220],[5,225,245], 'yellow'),
    ([70,150,220],[85,170,245], 'orange')
    
]

for (lower,upper, color) in boundaries:
    lower = np.array(lower, dtype = 'uint8')
    upper = np.array(upper, dtype= 'uint8')
    color = color

    if cv2.inRange(image, lower, upper).any():
        mask = cv2.inRange(image, lower, upper)
        print("Color detected: " + color)
        output = cv2.bitwise_and(image, image, mask=mask)
    else:
        print("Color not detected")

    if 'output' in vars():
        cv2.imshow("image",np.hstack([image,output]))
        cv2.waitKey(0)



