# import the necessary packages
# from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
import RPi.GPIO as gp
import os

def CameraTest():
    gp.setwarnings(False)
    gp.setmode(gp.BOARD)

    gp.setup(7, gp.OUT)   # Selection Pin
    gp.setup(11, gp.OUT)  # Enable 1
    gp.setup(12, gp.OUT)  # Enable 2

    gp.output(11, True)   # Set to disable cameras
    gp.output(12, True)   # Set to disable cameras


    # Camera A and C are using 
    # Selection Pin | Enable 1 | Enable 2 |
    # For Selecting Cam A 
    #   0           |   0      |    1     |
    # For Selecting Cam C
    #   0           |   1      |    0     |


    # Selecting Cam A
    gp.output(7,  False)
    gp.output(11, False)
    gp.output(12, True)
    camera = PiCamera()
    camera.start_preview()
    time.sleep(20)


    # Selecting Cam C
    gp.output(7,  False)
    gp.output(11, True)
    gp.output(12, False)
    time.sleep(20)
    camera.stop_preview()
    return
