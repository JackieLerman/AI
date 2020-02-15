'''

'''

from math import *
import cv2
import numpy as np
import imageUtils as iu


from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(1)
camera.capture('image.jpg')
camera.stop_preview()
