import numpy as np
import cv2 as cv
import random as rng

## para calcular a cor talvez ver a cor no centro dos contornos
## ver codigo para calcular o centro, ver as coordenadas e calcular na imagem real



def thresh_callback(val):
    threshold = val

    canny_output = cv.Canny(src_gray, threshold, threshold * 2)
    
    contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contours_poly = [None] * len(contours)
    boundRect = [None] * len(contours)
    centers = [None]*len(contours)


    ## boundingRect returns x, y, w, h -> w is width and h is height
    ## Rect area equals w*h 
    ## if len boundRect = 1 and area is bigger than a certain limit, check colors in frame ( or middle of rect) and return
    ## if len boundRect = 2 and both area is bigger than a certain limit, check colors in frame (or middle of rect) and return
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c,3,True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
        
    
    print(boundRect)

    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype = np.uint8)
    final_img = img
    for i in range(len(contours)):
        color = (0,255,255)
        color_rect = (0, 255, 0)
        cv.drawContours(drawing, contours_poly, i, color)
        
        cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
            (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color_rect, 2)

        cv.rectangle(final_img, (int(boundRect[i][0]), int(boundRect[i][1])), \
            (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color_rect, 2)
    
    cv.putText(final_img,'White', (60,120),cv.FONT_HERSHEY_PLAIN,0.8, (255,255,255), 1)
    cv.putText(final_img,'Red', (120,120),cv.FONT_HERSHEY_PLAIN,0.8, (0,0,255), 1)
    cv.imshow('Contours', drawing)
    

    
    cv.imshow('Square image', final_img)




img = cv.imread('red_white.jpg', cv.IMREAD_REDUCED_COLOR_2)
img = cv.resize(img,None, fx = 1.5, fy = 1.5, interpolation= cv.INTER_CUBIC)

src_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
src_gray = cv.blur(src_gray, (3,3))
_, thres_img = cv.threshold(img,150,255,cv.THRESH_BINARY)
adapt_thres_img = cv.adaptiveThreshold(src_gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 9, 4)



source_window = 'Source'
cv.namedWindow(source_window)
cv.imshow('Thresh', thres_img)
cv.imshow('Adaptive thresh', adapt_thres_img)
cv.imshow(source_window, img)
max_thresh = 255
thresh = 150 # initial threshold
cv.createTrackbar('Canny thresh:', source_window, thresh, max_thresh, thresh_callback)
thresh_callback(thresh)

print("Image shape: ", img.shape)


cv.waitKey(0)
cv.destroyAllWindows()


