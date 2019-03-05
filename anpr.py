import os
import logging
from flask import Flask,render_template, request,json,Response
from PIL import Image
from datetime import datetime
import cv2
import numpy as np
import os
import base64
# from StringIO import StringIO
from io import BytesIO

import DetectChars
import DetectPlates
import PossiblePlate
import DrawRedRectangleAroundPlate
import ImageSkew
import base64toImage
import blob
import listFilesAsJson

import json
import uuid
import qrcode
import pytesseract
import argparse
import re
import OCR
from crossdomain import crossdomain
import savedata
from queueProducer import QueueProducer
from getsqldata import get_alpr_sql_table_data
from update_alpr_data import update_data_to_sql_table
from properties import getProperties
import time
from readCsv import readCsvFileAsJson

imagefilesDir = "static/tests/"
# tesseract configurations
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C:/Program Files (x86)/Tesseract-OCR/tessdata"'


SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

## Genarate QRcode for Number plate
now = datetime.now()
currdate = now.strftime("%Y-%m-%d")
directory = "static/NumberPlates/"+currdate+"/"
qrcodedir = directory+"/qrcodes/"
numplatesdir = directory+"numplates/"
queueProducerObj = QueueProducer()

def generateQRCode(qrcodefilename, data, numplateimgpath, imagefilepath, alpr_id):
    now_1 = datetime.now()    
    cur_datetime = now_1.strftime("%Y-%m-%d %H:%M")
    global startdatetime
    startdatetime = cur_datetime
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data("<data>")
    qr.add_data("<id>"+alpr_id+"</id>")
    qr.add_data("<veh_img>"+imagefilepath+"</veh_img>")
    qr.add_data("<img>"+numplateimgpath+"</img>")
    qr.add_data("<date>"+currdate+"</date>")
    qr.add_data("<time>"+cur_datetime+"</time>")    
    qr.add_data("<qrcode>"+qrcodefilename+"</qrcode>")
    qr.add_data("</data>")
    qr.make(fit=True)

    img = qr.make_image()
    file_extension = "png"
    file_name = qrcodefilename+"."+file_extension  # created file with extention
    img.save(file_name,file_extension.upper()) #write qrcode encoded data to the image file.
## End of QRCode generation

def maintest(imagefilepath):
    start_time = time.time()

    json_data = {}
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()         # attempt KNN training

    if blnKNNTrainingSuccessful == False:                                   # if KNN training was not successful
        print("\nerror: KNN traning was not successful\n")                  # show error message
        return                                                              # and exit program
    # end if
    imgOriginalScene  = cv2.imread(imagefilepath)               # open image
    if imgOriginalScene is None:                                # if image was not read successfully
        print("\nerror: image not read from file \n\n")         # print error message to std out
        os.system("pause")                                      # pause so user can see error message
        return                                                  # and exit program
    # end if

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)           # detect plates
    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates

    if len(listOfPossiblePlates) == 0:                          # if no plates were found
        print("\nno license plates were detected\n")            # inform user no plates were found
    else:                                                       # else
        # if we get in here list of possible plates has at leat one plate
        # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

                # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = listOfPossiblePlates[0]        

        num_plate_img, centroid = DrawRedRectangleAroundPlate.crop_number_plate_from_img(imgOriginalScene, licPlate)        

        # numberPlate = cv2.cvtColor( licPlate.imgPlate, cv2.COLOR_RGB2GRAY )
        numberPlate = cv2.cvtColor(num_plate_img, cv2.COLOR_RGB2GRAY )
        cv2.imwrite("imageplate.png",numberPlate)
        numplateimgname = str(uuid.uuid4())
        
        # creation of directory wit current date
        if not os.path.exists(directory):
            os.makedirs(directory)
        # creation of directory for qrcodes under current date
        if not os.path.exists(qrcodedir):
            os.makedirs(qrcodedir)
        # creation of directory for qrcodes under current date
        if not os.path.exists(numplatesdir):
            os.makedirs(numplatesdir)
        
        cv2.imwrite(numplatesdir+numplateimgname+".png", numberPlate)
        
        # Number plate skewing
        ImageSkew.imageskew(numplatesdir+numplateimgname+".png")
        # do OCR on license plate
        liplatenum = ""
        try:
            liplatenum = OCR.doOCR(numplatesdir+numplateimgname+".png")            
        except Exception as e:
            print("[ Xception @ OCR.doOCR ] "+str(e))            
        
        # reliplatenum = re.sub(r'[?|$|.|!*]',r'',str(licPlate))
        # reliplatenum = liplatenum.replace('*','')                # replace special characters from string
        # reliplatenum = liplatenum.strip('|,[]#@$!%^&*()')
        # print(reliplatenum)

        if len(licPlate.strChars) == 0:                     # if no chars were found in the plate
            print("\nno characters were detected\n\n")      # show message
            return                                          # and exit program
        # end if
        # DrawRedRectangleAroundPlate.drawRedRectangleAroundPlate(imgOriginalScene, licPlate)             # draw red rectangle around plate

        print ("\n[INFO] license plate read from image = " + licPlate.strChars + "\n")       # write license plate text to std out
        print ("----------------------------------------")

        cv2.imwrite("static/originalImage/imgOriginalScene.png", imgOriginalScene)           # write image out to file
        vehicleNumber = licPlate.strChars

        # generate QR code
        qrcodefilename = qrcodedir+numplateimgname+"_qrcode"
        numplateimgpath = numplatesdir+numplateimgname+".png"
        generateQRCode(qrcodefilename, vehicleNumber, numplateimgpath, imagefilepath, numplateimgname)
        processing_time = (time.time() - start_time)        

        data = {}
        data['number'] = liplatenum        
        data['numplatedetectimg'] = "static/originalImage/imgOriginalScene.png"
        data['numberplate'] = numplatesdir+numplateimgname+".png"
        data['qrcode'] = qrcodedir+numplateimgname+"_qrcode"+".png"
        data['vehicle_img'] = imagefilepath 
        data['startdatetime'] = startdatetime
        data['enddatetime'] = startdatetime
        data['alpr_id'] = numplateimgname
        data['processtime'] = processing_time
        data['vehicle_number'] = vehicleNumber
        json_data = json.dumps(data)

    # end if else
    cv2.waitKey(0)                  # hold windows open until user presses a key
    return json_data
# end main