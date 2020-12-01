import numpy as np
import cv2 as cv




def area(w, h):
    return w * h


def color_in_frame(image):

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

    if cv.inRange(image, lower, upper).any():
        mask = cv.inRange(image, lower, upper)
        print("Color detected: " + color)
        output = cv.bitwise_and(image, image, mask=mask)
    else:
        print("Color not detected")

    if 'output' in vars():
        cv.imshow("image",np.hstack([image,output]))
        


def thresh_callback(image, gray_image, val):
    
    
    
    threshold = val

    canny_output = cv.Canny(gray_image, threshold, threshold * 2)

    cv.imshow("Canny", canny_output)
    
    contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contours_poly = [None] * len(contours)
    boundRect = [None] * len(contours)
    
    


    ## boundingRect returns x, y, w, h -> w is width and h is height
    ## Rect area equals w*h 
    ## if len boundRect = 1 and area is bigger than a certain limit, check colors in frame ( or middle of rect) and return
    ## if len boundRect = 2 and both area is bigger than a certain limit, check colors in frame (or middle of rect) and return
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c,3,True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
    
    

    final_img = image

    for i in range(len(contours)):
        color = (0,255,255)
        color_rect = (0, 255, 0)
        #cv.drawContours(drawing, contours_poly, i, color)

        #cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
        #    (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color_rect, 2)

        cv.rectangle(final_img, (int(boundRect[i][0]), int(boundRect[i][1])), \
            (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color_rect, 2)
    

    
    #cv.putText(final_img,'White', (60,120),cv.FONT_HERSHEY_PLAIN,0.8, (255,255,255), 1)
    #cv.putText(final_img,'Red', (120,120),cv.FONT_HERSHEY_PLAIN,0.8, (0,0,255), 1)
    #cv.imshow('Contours', drawing)
    cv.imshow('Square image', final_img)


##MAIN

cap = cv.VideoCapture("video.mp4")

while(cap.isOpened()):

    ret, frame = cap.read()
    

    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.blur(gray, (3,3))


    cv.imshow('frame', frame)
    
    thresh = 100

    thresh_callback(frame, gray, thresh)
    color_in_frame(frame)



    if cv.waitKey(0) == ord('q'):
        break




cap.release()
cv.destroyAllWindows()

