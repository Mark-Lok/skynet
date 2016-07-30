# import the necessary packages
# from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import RPi.GPIO as gp
import os

# Camera 0(A) and 1(C) are using 
# Selection Pin | Enable 1 | Enable 2 |
# For Selecting Cam 0
#       0       |    0     |    1     |
# For Selecting Cam 1
#       0       |    1     |    0     |

# initialize the camera
gp.setwarnings(False)
gp.setmode(gp.BOARD)
gp.setup(7,  gp.OUT)  # Selection Pin
gp.setup(11, gp.OUT)  # Enable 1
gp.setup(12, gp.OUT)  # Enable 2
gp.output(11, True)   # Set to disable cameras
gp.output(12, True)   # Set to disable cameras

# Function for switching camera
def gocam( mycam ):
    if mycam == '0':
        # Selecting Cam 0
        gp.output(7,  False)
        gp.output(11, False)
        gp.output(12, True)
    elif mycam == '1':
        # Selecting Cam 1
        gp.output(7,  False)
	gp.output(11, True)
        gp.output(12, False)
    elif mycam == 'off':
        # To disable all cameras
        gp.output(11, True)   
	gp.output(12, True)   
    else:
        gp.output(11, True)   	
	gp.output(12, True)   

# Function for isolating green object in the image
def getobj(img):

# Function for getting centroid of the object
def getcent(img):

# Function for calculating position by two centroid
def getposition(centeoid0, centroid1):



# initialize the cameras and grab reference to the raw camera capture
camera = PiCamera()      # create an instance of the PiCamera class
gocam(0)
rawCapture0 = PiRGBArray(camera)
gocam(1)
rawCapture1 = PiRGBArray(camera)
# allow the cameras to warmup
time.sleep(0.1)

# main loop
loopFlag = 1
while loopFlag == 1 :
    # grab an image from camera 0
    gocam(0)
    camera.capture(rawCapture0, format="bgr")
    image0 = rawCapture0.array
    # grab an image from camera 1
    gocam(1)
    camera.capture(rawCapture1, format="bgr")
    image1 = rawCapture1.array

