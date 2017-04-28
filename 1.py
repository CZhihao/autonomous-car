# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
 
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
        #white line detection
	image0=image.copy()
	traite=image0[400:480, 0:600]
        gray0=cv2.cvtColor(traite,cv2.COLOR_BGR2GRAY)
        blur=cv2.GaussianBlur(gray0,(5,5),0)
        
        
        ret,thresh=cv2.threshold(blur,170,255,cv2.THRESH_BINARY)

        cont,contours,hierarchy=cv2.findContours(thresh,1,cv2.CHAIN_APPROX_NONE)

        if len(contours)>0:
            c=max(contours,key=cv2.contourArea)
            M=cv2.moments(c)
            if M['m00']>0:
                cx=int(M['m10']/M['m00'])
                cy=int(M['m01']/M['m00'])
            else:
                cx=300
                cy=0
            cv2.line(image0,(cx,0),(cx,480),(255,0,0),1)
            cv2.line(image0,(0,cy+400),(600,cy+400),(255,0,0),1)

            cv2.drawContours(traite,contours,-1,(0,255,0),3)
        #end white line detecter

        #red traffic sign detection
        image_red=image[0:400,0:600]

        hsv=cv2.cvtColor(image_red,cv2.COLOR_BGR2HSV)
        lower_red1=np.array([0,50,50])
        upper_red1=np.array([10,255,255])
        lower_red2=np.array([170,50,50])
        upper_red2=np.array([180,255,255])
        mask1=cv2.inRange(hsv,lower_red1,upper_red1)
        mask2=cv2.inRange(hsv,lower_red2,upper_red2)
        mask=cv2.bitwise_or(mask1,mask2)
        res=cv2.bitwise_and(image_red,image_red,mask=mask)

        
        gray1=cv2.cvtColor(image_red,cv2.COLOR_BGR2GRAY)
        ret,thresh1=cv2.threshold(gray1,127,255,0)
        cont1,contour1,hierarchy=cv2.findContours(mask,1,cv2.CHAIN_APPROX_SIMPLE)
        if len(contour1)>0:
        
                cmax1=max(contour1,key=cv2.contourArea)
                (x,y),radius=cv2.minEnclosingCircle(cmax1)
                center=(int(x),int(y))
                radius=int(radius)
                cv2.circle(image0,center,radius,(0,255,0),3)
        else:
                
                radius=0    
        
	# show the frame
	cv2.imshow("Frame", image0)
	cv2.imshow("Frame0", image)
	
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)



 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
