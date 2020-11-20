import cv2
import numpy as np
import argparse

image = cv2.imread("cap_light.jpg")

## just to resize image that's too big
image = cv2.resize(image,None,fx=0.5,fy=0.5, interpolation = cv2.INTER_CUBIC)

# defining color boundaries - list of tuples with RGB values of upper and lower limits of the color
# we must define all the colors present
# red  white dark_green  light_green  yellow  orange
boundaries = [
    ([17,15,100],[50,56,200], 'red') 
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



