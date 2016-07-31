# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import RPi.GPIO as gp
import os

# camera 0(A) and 1(C) are using
# selection Pin | Enable 1 | Enable 2 |
# for Selecting Cam 0
#       0       |    0     |    1     |
# for Selecting Cam 1
#       0       |    1     |    0     |

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
    lowerGreen = np.array([70,  50,  50 ])
    upperGreen = np.array([170, 255, 255])
    
    obj = cv2.inRange(hsvimg, lowerGreen, upperGreen)
    return obj


# function for getting centroid of the object
def getcent(img):

# function for calculating position by two centroid
def getposition(centeoid0, centroid1):

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
    cent0 = getcent(obj0)
    cent1 = getcent(obj1)
    objDistance, objHorizonalOffset = getposition(cent0, cent1)

    # generate command message for arduino

