import numpy as cv 
import cv2 as cv




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
        
    
    print(boundRect)

    

    
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

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.blur(gray, (3,3))


    cv.imshow('frame', frame)
    
    thresh = 100

    thresh_callback(frame, gray, thresh)



    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()