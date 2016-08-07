# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import RPi.GPIO as gp
import os
import serial

# camera 0(A) and 1(C) are using
# selection Pin | Enable 1 | Enable 2 |
# for Selecting Cam 0
#       0       |    0     |    1     |
# for Selecting Cam 1
#       0       |    1     |    0     |

# initialize serial
port = serial.Serial("/dev/serial0", baudrate=9600, timeout=3.0)

# initialize the camera
gp.setwarnings(False)
gp.setmode(gp.BOARD)
gp.setup(7,  gp.OUT)  # selection Pin
gp.setup(11, gp.OUT)  # enable 1
gp.setup(12, gp.OUT)  # enable 2
gp.output(11, True)   # set to disable cameras
gp.output(12, True)   # set to disable cameras

# function for switching camera
def gocam( mycam ):
    if mycam == '0':
    # selecting Cam 0
        gp.output(7,  False)
        gp.output(11, False)
        gp.output(12, True)
    elif mycam == '1':
    # selecting Cam 1
        gp.output(7,  False)
	gp.output(11, True)
        gp.output(12, False)
    elif mycam == 'off':
    # to disable all cameras
        gp.output(11, True)   
	gp.output(12, True)   
    else:
        gp.output(11, True)   	
	gp.output(12, True)   


# function for isolating green object in the image
def getobj(img):
    # convert BGR to HSV
    hsvimg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define range of green color in HSV
    lowerGreen = np.array([30,  50,  50 ])
    upperGreen = np.array([100, 255, 255])
    obj = cv2.inRange(hsvimg, lowerGreen, upperGreen)
    return obj


# function for getting centroid of the object
def getcent(img):
    # find contours in the thresholded image
    cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    retX = -1
    retY = -1
    biggest = 0
    # loop over the contours
    for c in cnts:
        if cv2.contourArea(c) > 80: # 80 is a threshold value to filter out noises
            # compute the center of the contour
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # draw the contour and center of the shape on the image
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
            # cv2.putText(image, "center", (cX - 20, cY - 20),
            # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            print(cX, cY)
            if cv2.contourArea(c) >= biggest:
                biggest = cv2.contourArea(c)
                retX = cX
                retY = cY
            # show the image
            cv2.imshow("Image", image)
            cv2.waitKey(0)
    return retX, retY


# function for calculating position by two centroid
def generate(centeoid0, centroid1):
    


# initialize the cameras and grab reference to the raw camera capture
camera = PiCamera()      # create an instance of the PiCamera class
gocam(0)
rawCapture0 = PiRGBArray(camera)
gocam(1)
rawCapture1 = PiRGBArray(camera)

# allow the cameras to warmup
time.sleep(0.1)


# ------  main loop start here  ------

loopFlag = 1
while loopFlag == 1 :
    # load the image from camera 0
    gocam(0)
    camera.capture(rawCapture0, format="bgr")
    image0 = rawCapture0.array

    # load the image from camera 1
    gocam(1)
    camera.capture(rawCapture1, format="bgr")
    image1 = rawCapture1.array

    # image proccessing and analyse the object special location
    obj0 = getobj(image0)
    obj1 = getobj(image1)
    cent0X, cent0Y = getcent(obj0)
    cent1X, cent1Y = getcent(obj1)
    objDistance, objHorizonalOffset = getposition(cent0, cent1)

    # generate command message for arduino
    
