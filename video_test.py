import numpy as np
import cv2 as cv


flag = 0




def click(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
         print(frame[y,x])
         print(y)




def nothing(x):
    pass


def area(w, h):
    return w * h


def color_in_frame(image):

    
    colors_detected = []
    area_list = []

    boundaries = [
    ([80,80,220],[110,110,255], 'red'), 
    ([90,120,80],[120,140,110], 'dark green'),
    ([185,200,160],[210,220,180], 'light green'),
    ([200,200,200],[255,255,255], 'white'),
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
            #print("Color detected: " + color)
            
            rect = thresh_callback(image, mask, 150)
            for i, values in enumerate(rect):
                if area(values[2],values[3]) > 2000:
                    colors_detected.append(color)
                    area_list.append(area(values[2],values[3]))
            

    print("Area sum: ",sum(area_list))

    if sum(area_list) > 5000:
        #print("Colors Detected: ", colors_detected)
        
        #print(sum(area_list))  
        return colors_detected

              ##output = cv.bitwise_and(image, image, mask=mask)
        ##else:
          ##  print("Color not detected" + color)

        #if 'output' in vars():
        #    cv.imshow("image",np.hstack([image,output]))         
        


def thresh_callback(image, gray_image, val):
    
    
    
    threshold = val

    #canny_output = cv.Canny(gray_image, threshold, threshold * 2)

    cv.imshow("Canny", gray_image)
    
    contours, _ = cv.findContours(gray_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contours_poly = [None] * len(contours)
    boundRect = [None] * len(contours)
    finalRect = []
    
    


    ## boundingRect returns x, y, w, h -> w is width and h is height
    ## Rect area equals w*h 
    ## if len boundRect = 1 and area is bigger than a certain limit, check colors in frame ( or middle of rect) and return
    ## if len boundRect = 2 and both area is bigger than a certain limit, check colors in frame (or middle of rect) and return
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c,3,True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
    
    for i, values in enumerate(boundRect):
       # print(area(boundRect[i][2], boundRect[i][3]))
        if area(boundRect[i][2], boundRect[i][3]) > 2000:
            finalRect.append(boundRect[i])
            
    #print(finalRect)

    final_img = image

    for i in range(0,len(finalRect)):
        color = (0,255,255)
        color_rect = (0, 255, 0)
        #cv.drawContours(drawing, contours_poly, i, color)

        #cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
        #    (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color_rect, 2)
        if 140 < (finalRect[i][1]+finalRect[i][3]/2) < 240:
            cv.rectangle(final_img, (int(finalRect[i][0]), int(finalRect[i][1])), \
                (int(finalRect[i][0]+finalRect[i][2]), int(finalRect[i][1]+finalRect[i][3])), color_rect, 2)
    

    
    #cv.putText(final_img,'White', (60,120),cv.FONT_HERSHEY_PLAIN,0.8, (255,255,255), 1)
    #cv.putText(final_img,'Red', (120,120),cv.FONT_HERSHEY_PLAIN,0.8, (0,0,255), 1)
    #cv.imshow('Contours', drawing)
    return finalRect
    cv.imshow('Square image', final_img)





##MAIN

cap = cv.VideoCapture("videos\\video_4s.mp4")


cv.namedWindow("Trackbars",)
cv.createTrackbar("lb","Trackbars",0,255,nothing)
cv.createTrackbar("lg","Trackbars",0,255,nothing)
cv.createTrackbar("lr","Trackbars",0,255,nothing)
cv.createTrackbar("ub","Trackbars",255,255,nothing)
cv.createTrackbar("ug","Trackbars",255,255,nothing)
cv.createTrackbar("ur","Trackbars",255,255,nothing)

while(cap.isOpened()):

    e1 = cv.getTickCount()

    ret, frame = cap.read()
    

    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.blur(gray, (3,3))

    #frame = cv.blur(frame, (3,3))
    #frame = cv.bilateralFilter(frame, 45, 75, 75)
    frame = cv.medianBlur(frame,9)

   

    #height, width = frame.shape[:2]
    #frame = cv.resize(frame,(width/5, height/5), interpolation = cv.INTER_CUBIC)
    #hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

    #cv.imshow("hsv", hsv)

    lb = cv.getTrackbarPos("lb","Trackbars")
    lg = cv.getTrackbarPos("lg","Trackbars")
    lr = cv.getTrackbarPos("lr","Trackbars")
    ub = cv.getTrackbarPos("ub","Trackbars")
    ug = cv.getTrackbarPos("ug","Trackbars")
    ur = cv.getTrackbarPos("ur","Trackbars")

    l_blue = np.array([lb,lg,lr])
    u_blue = np.array([ub,ug,ur])
    mask = cv.inRange(frame, l_blue, u_blue)
    result = cv.bitwise_and(frame,frame,mask=mask)
    #cv.imshow('frame', frame)
    
    thresh = 100

    #thresh_callback(frame, cv.cvtColor(result, cv.COLOR_BGR2GRAY), thresh)
    colors = color_in_frame(frame)

    print("Flag before: ",flag)
    #print(colors)
    if colors != None and flag == 0:
        flag = 1
        print("Colors: ", colors)
    elif colors == None and flag == 1:
        flag = 0

    print("Flag after: ", flag)
    

    cv.imshow("frame", frame)
   
    cv.setMouseCallback("frame", click)
    #cv.imshow("mask", mask)
    #cv.imshow("result",result)
    


    if cv.waitKey(0) == ord('q'):            
        break

    e2 = cv.getTickCount()
    time = (e2 - e1) / cv.getTickFrequency()
    #print(time)




cap.release()
cv.destroyAllWindows()

