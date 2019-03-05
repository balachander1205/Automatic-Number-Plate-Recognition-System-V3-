import cv2
import datetime
import imutils
import time
import uuid
import logging

import DetectChars
import DetectPlates
import PossiblePlate
import DrawRedRectangleAroundPlate
# import OCR
import WriteLiPlateCharsOnImage
import ImageSkew

import urllib 
import numpy as np

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

class IPCamera(object):
    def __init__(self, camera):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        # self.video = cv2.VideoCapture('static/videos/video.avi')        
        self.camera = camera
        self.video = urllib.urlopen(self.camera)        
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()

    def get_frame_from_ip_cam(self):
        print('Entered in to IP cam')
        bytes=''
        ret, jpeg = ''  
        try:
            bytes+=self.video.read(1024)        
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            print('A :: '+str(a))
            # if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR) 
            cv2.imshow('image ', i)           
            ret, jpeg = cv2.imencode('.jpg', i)
        except Exception as e:
            print("[ Xception in IPCamera ] "+str(e))
        
        return jpeg.tobytes()  
    