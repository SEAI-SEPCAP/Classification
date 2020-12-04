## main algorithm of classification part of project SEAI-SEPCAP

#imports
from aux_functions import area, nothing
from boundingBox import boundBox
from colorDetection import colorDetector
import cv2 as cv
import numpy as np


#assistant function for detecting RGB variables
def click(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
         print(frame[y,x])
         print(y)


#starting variables
flag = 0
old_flag = 1
capsule_count = 0

#adjustable variables
speed = 1           #change value of speed if required
min_area = 7500     #change minimal area for each video and distance
blur = 9            #change value for minimum area
crop_p = 0.8        #proportion of crop



#video capture and analysis
video = "videos\\video_4s.mp4"
cap = cv.VideoCapture(video) #change video variable for different video / use 0 for webcam


#comment if no trackbar is used
cv.namedWindow("Trackbars",)
cv.createTrackbar("l_bue","Trackbars",0,255,nothing) 
cv.createTrackbar("l_green","Trackbars",0,255,nothing)
cv.createTrackbar("l_red","Trackbars",0,255,nothing)
cv.createTrackbar("u_blue","Trackbars",255,255,nothing)
cv.createTrackbar("u_green","Trackbars",255,255,nothing)
cv.createTrackbar("u_red","Trackbars",255,255,nothing)



#while loop for video capturing
while(cap.isOpened()):

    #comment if no time measurement is needed
    #e1 = cv.getTickCount()

    ret, frame = cap.read()

    if not ret:
        break
    
    #blur frame 
    frame = cv.medianBlur(frame, blur)


    #comment if no trackbar is used
    lb = cv.getTrackbarPos("l_blue","Trackbars")
    lg = cv.getTrackbarPos("l_green","Trackbars")
    lr = cv.getTrackbarPos("l_red","Trackbars")
    ub = cv.getTrackbarPos("u_blue","Trackbars")
    ug = cv.getTrackbarPos("u_green","Trackbars")
    ur = cv.getTrackbarPos("u_red","Trackbars")
    low_bound = np.array([lb,lg,lr])
    up_bound = np.array([ub,ug,ur])
    mask = cv.inRange(frame, low_bound, up_bound)
    result = cv.bitwise_and(frame, frame, mask = mask)

    

    #detect colors
    colors = colorDetector(frame, min_area= min_area, proportion= crop_p)

    #rising and falling edge
    if (colors != [] and flag == 0) and old_flag == 1:
        old_flag = flag
        flag = 1
        print("Capsule detected: ", colors)
        capsule_count = capsule_count + 1

    elif (colors == [] and flag == 1) and old_flag == 0:
        old_flag = flag
        flag = 0
        print("Capsule not in frame")

    
    cv.imshow("frame", frame)
    cv.setMouseCallback("frame", click)

    if cv.waitKey(speed) == ord("q"):
        break

    #comment if no time is measured
    #e2 = cv.getTickCount()
    #time = (e2 - e1) / cv.getTickFrequency()
    #print(time)

print("Total Capsules Detected: ", capsule_count)

cap.release()
cv.destroyAllWindows()