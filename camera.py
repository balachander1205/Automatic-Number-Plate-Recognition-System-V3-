import cv2
import datetime
import imutils
import time
import uuid
import logging
import numpy as np
# import pandas as pd

import DetectChars
import DetectPlates
import PossiblePlate
import DrawRedRectangleAroundPlate
# import OCR
import WriteLiPlateCharsOnImage
import ImageSkew
# import app
from PIL import Image
from math import sqrt
from anpr import maintest

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

# Trained XML classifiers describes some features of some object we want to detect
car_cascade = cv2.CascadeClassifier('haarcascade/cars.xml')
cascPath = "haarcascade/haarcascade_frontalface_webcam.xml"
video_alpr_image = "static/NumberPlates/temp/"

class VideoCamera(object):
    def __init__(self, camera):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        # self.video = cv2.VideoCapture('static/videos/video.avi')        
        self.camera = camera
        self.video = cv2.VideoCapture(self.camera)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        # convert to gray scale of each image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)        

        # Detects cars of different sizes in the input image
        cars = car_cascade.detectMultiScale(gray, 1.1, 1)
        
        # To draw a rectangle on each vehicles
        for (x,y,w,h) in cars:
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,255),2)
            # Display image in a window

        cv2.putText(image, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    # onclick capture frame
    def get_frame_onclick(self):
        ret,frame = self.video.read()                
        ret1, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def countvehicle(self):
        ret, frame = self.video.read()
        ret1, jpeg = cv2.imencode('.jpeg', frame)
        # frames_count, fps, width, height = cap.get(cv2.CAP_PROP_FRAME_COUNT), cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT) 
        # width = int(width)
        # height = int(height)
        # print(frames_count, fps, width, height)


        return jpeg.tobytes()
    
    def distance(self,a,b):
        return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def is_between(self,a,c,b):
        return self.distance(a,c) + self.distance(c,b) == self.distance(a,b)

    def collinear(self, a, b, c):
        "Return true iff a, b, and c all lie on the same line."
        return (b[0] - a[0]) * (c[1] - a[1]) == (c[0] - a[0]) * (b[1] - a[1])

    def within(self, p, q, r):
        "Return true iff q is between p and r (inclusive)."
        return p <= q <= r or r <= q <= p

    def is_on(self, a, b, c):
        "Return true iff point c intersects the line segment from a to b."
        # (or the degenerate case that all 3 points are coincident)
        return (self.collinear(a, b, c)
                and (within(a[0], c[0], b[0]) if a[0] != b[0] else 
                     within(a[1], c[1], b[1])))
        
    def get_anpr_from_video(self,blnKNNTrainingSuccessful, vehicle_hotlist_data):
        video_alpr_response = 0
        ret,frame = self.video.read()
        # vertical line
        
        # cv2.line(frame, (200, 0), (200, 500), (0, 0, 255), 2)        
        # cv2.line(frame, (500, 0), (500, 500), (0, 0, 255), 2)

        # horizantal line
        # hor_line = cv2.line(frame, (0, 150), (1500, 150), (0, 0, 255), 2)        
        
        # points = self.get_line(0,150,1500,150)

        # print("Intersection Line >>>---->>  "+str(points))
        # cv2.line(frame, (600, 0), (600, 300), (255, 255, 255), 2)            

        # numplateimgname = str(uuid.uuid4())
        
        # cv2.rectangle(frame1, (0, 40), (730, 200), (0, 0, 255), 1)
        # frame = frame1[40:200 ,0:730]
        
        # cv2.imwrite("static/temp/Cropped"+numplateimgname+".png", frame)
        # blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()                     # attempt KNN training
        listOfPossiblePlates = DetectPlates.detectPlatesInScene(frame)                      # detect plates
        listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates

        # if we get in here list of possible plates has at leat one plate
        # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)
        # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = 0
        try:
            licPlate = listOfPossiblePlates[0]
            numberPlate = cv2.cvtColor( licPlate.imgPlate, cv2.COLOR_RGB2GRAY)
            # cv2.imwrite("static/temp/videoanpr-image.png", numberPlate)
            # DrawRedRectangleAroundPlate.drawRedRectangleAroundPlate(frame, licPlate)             # draw red rectangle around plate
            num_plate_img, centroid = DrawRedRectangleAroundPlate.crop_number_plate_from_img(frame, licPlate)
            liplateNum = WriteLiPlateCharsOnImage.writeLicensePlateCharsOnImage(frame, licPlate)
            print("writeLicensePlateCharsOnImage ========================================="+str(liplateNum))
            hotlisted_vehicle = list(filter(lambda vehicle_hotlisted: (vehicle_hotlisted == liplateNum) , vehicle_hotlist_data))
            print("hotlisted_vehicle Data ***************************************************** [ ---"+str(hotlisted_vehicle)+"--- ]")
            Intersection_point = self.is_between([0,150],centroid,[1500,150])
            Intersection_point_within = self.within([0,150],centroid,[1500,150])
            Intersection_point_collinear = self.collinear([0,150],centroid,[1500,150])
            Intersection_point_is_on = self.is_on([0,150],centroid,[1500,150])
            # colinearity for horizantal line
            ab = sqrt((0-1500)**2 + (150-150)**2)
            ac = sqrt((0-centroid[0])**2 + (150-centroid[1])**2)
            bc = sqrt((1500-centroid[0])**2 + (150-centroid[1])**2)
            # colinearity for vertical line
            ab_ = sqrt((0-500)**2 + (500-500)**2)
            ac_ = sqrt((0-centroid[0])**2 + (500-centroid[1])**2)
            bc_ = sqrt((500-centroid[0])**2 + (500-centroid[1])**2)

            # is_on = self.is_on([0,150],centroid,[1500,150])
            # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!^^^^^^^^^^^^^^^^^^^^^^^^^^ '+str(Intersection_point_collinear))

            if int(ac+bc)== int(ab):
                print("#################### points are colinear in horizantal line @@@@@@@@@@@@@@@@@@@@@@----------")
                cv2.imwrite("static/temp/videoanpr-image.png", num_plate_img)
                numplateimgname = str(uuid.uuid4())
                # cv2.imwrite(video_alpr_image+"_"+numplateimgname+".png", num_plate_img)
                # video_alpr_response = maintest(video_alpr_image+"_"+numplateimgname+".png")

            if int(ac_+bc_)== int(ab_):
                print("#################### points are colinear in vertical line @@@@@@@@@@@@@@@@@@@@@@----------")
                cv2.imwrite("static/temp/videoanpr-image.png", num_plate_img)
                numplateimgname = str(uuid.uuid4())
                # cv2.imwrite(video_alpr_image+"_"+numplateimgname+".png", num_plate_img)
                # video_alpr_response = maintest(video_alpr_image+"_"+numplateimgname+".png")
            
            # print("Intersection_point ===================== "+str(Intersection_point))
            # print("Intersection_point_within ===================== "+str(Intersection_point_within))
            # print("Intersection_point_collinear ===================== "+str(Intersection_point_collinear))
            # print("Intersection_point_is_on ===================== "+str(Intersection_point_is_on))

            #  Overlay detected number plate image on original frame
            # overlay = cv2.imread("static/temp/videoanpr-image.png")
            # rows,cols,channels = overlay.shape
            # overlay=cv2.addWeighted(frame[250:250+rows, 0:0+cols],0.5,overlay,0.5,0)
            # frame[250:250+rows, 0:0+cols ] = overlay            
                        
        except Exception as e:
        	print("[ Xception in camera.get_anpr_from_video() ]  "+str(e))
        # OCR.doOCR(licPlate.imgPlate)
        # WriteLiPlateCharsOnImage.writeLicensePlateCharsOnImage(frame, licPlate.imgPlate)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
            (10, frame.shape[0] - 10), 0, 1, (0, 0, 255), 2, cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), video_alpr_response

    
        