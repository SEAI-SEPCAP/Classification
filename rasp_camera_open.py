# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2


boundaries = [
    ([17,15,100],[50,56,200], 'red') 
]

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	# show the frame
	cv2.imshow("Frame", image)

    
	for (lower, upper, color) in boundaries:
		lower = np.array(lower, dtype = 'uint8')
		upper = np.array(upper, dtype = 'uint8')
		color = color

		if cv2.inRange(image, lower, upper).any():
			mask = cv2.inRange(image,lower, upper)
			print("Color Detected: " +  color)
			output = cv2.bitwise_and(image, image, mask = mask)

		else:
			print("COlor not detected")
		
		if 'output' in vars():
			cv2.imshow("image", np.hstack([image,output]))
			cv2.waitKey(0)

	key = cv2.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break