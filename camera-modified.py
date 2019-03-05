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
# from datetime import datetime

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

# Trained XML classifiers describes some features of some object we want to detect
car_cascade = cv2.CascadeClassifier('haarcascade/cars.xml')
cascPath = "haarcascade/haarcascade_frontalface_webcam.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

THRESHOLD = 3000
timeCheck = datetime.datetime.now().strftime('%Ss')

def diffImg(t0, t1, t2):
        d1 = cv2.absdiff(t2, t1)
        d2 = cv2.absdiff(t1, t0)
        diff = cv2.bitwise_and(d1, d2)
        # print("DIFF Image >>>>-----> \n",diff)
        return cv2.bitwise_and(d1, d2)

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

    def get_anpr_from_video(self):        
        # Read three images first:
        t_minus = cv2.cvtColor(self.video.read()[1], cv2.COLOR_RGB2GRAY)
        t = cv2.cvtColor(self.video.read()[1], cv2.COLOR_RGB2GRAY)
        t_plus = cv2.cvtColor(self.video.read()[1], cv2.COLOR_RGB2GRAY)

        ret,frame = self.video.read()
        totalDiff = cv2.countNonZero(diffImg(t_minus, t, t_plus))   # this is total difference number
        text = "threshold: " + str(totalDiff)               # make a text showing total diff.
        # numplateimgname = str(uuid.uuid4())
        
        # cv2.rectangle(frame1, (0, 40), (730, 200), (0, 0, 255), 1)
        # frame = frame1[40:200 ,0:730]
        
        # cv2.imwrite("static/temp/Cropped"+numplateimgname+".png", frame)
        blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()                     # attempt KNN training
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
            num_plate_img = DrawRedRectangleAroundPlate.crop_number_plate_from_img(frame, licPlate)

            # numberPlate = cv2.cvtColor( num_plate_img, cv2.COLOR_RGB2GRAY)
            cv2.imwrite("static/temp/videoanpr-image.png", num_plate_img)

            #  Overlay image on background
            overlay = cv2.imread("static/temp/videoanpr-image.png")
            rows,cols,channels = overlay.shape
            overlay=cv2.addWeighted(frame[1:1+rows, 0:0+cols],0.5,overlay,0.5,0)
            frame[1:1+rows, 0:0+cols ] = overlay
            if len(num_plate_img):
                print("Entered Image Diff")
                THRESHOLD = totalDiff
                if totalDiff == THRESHOLD:
                # and timeCheck != datetime.datetime.now().strftime('%Ss'):
                    # if num_plate_img:
                    print("THRESHOLD Checked")
                    dimg= self.video.read()[1]
                    # cv2.imwrite('static/motions/'+datetime.datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg', frame)                
                else:
                    THRESHOLD = totalDiff
            timeCheck = datetime.now().strftime('%Ss')
            # Swapping of Frames
            t_minus = t
            t = t_plus
            t_plus = cv2.cvtColor(self.video.read()[1], cv2.COLOR_RGB2GRAY)

            # if num_plate_img is not None:
            #     cv2.imshow("frame", num_plate_img)
            #     if cv2.waitKey(1) & 0xFF == ord('q'):
            #         out = cv2.imwrite('capture.jpg', frame)                    
            #     cv2.waitKey(0)                
                
            # liplateNum = WriteLiPlateCharsOnImage.writeLicensePlateCharsOnImage(frame, licPlate)
            # cv2.putText(frame, liplateNum,
            # (10, frame.shape[0] - 11), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 2)
            
            # numberPlate = ImageSkew.imageskew("static/temp/videoanpr-image.png")
            # do OCR on license plate
            # liplatenum = OCR.doOCR("static/temp/videoanpr-image.png")
            # print("ALPR Image Text "+str(liplatenum))
            cv2.putText(frame, text, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)   # display it on screen        
        except Exception as e:
        	print("[ Xception in camera.get_anpr_from_video() ]  "+str(e))
        # OCR.doOCR(licPlate.imgPlate)
        # WriteLiPlateCharsOnImage.writeLicensePlateCharsOnImage(frame, licPlate)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
            (10, frame.shape[0] - 10), 0, 1, (0,0,0), 2, cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    
        