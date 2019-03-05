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
from base64toImageFile import writeBase64ToImageFile
import blob
import listFilesAsJson

import json
import uuid
import qrcode
from camera import VideoCamera
import pytesseract
import argparse
import re
import OCR
from crossdomain import crossdomain
import savedata
from queueProducer import QueueProducer
from getsqldata import get_alpr_sql_table_data
from getvehiclehotlist import get_vehicle_hotlist_data
from update_alpr_data import update_data_to_sql_table
from properties import getProperties
import time
from readCsv import readCsvFileAsJson
from anpr import maintest

# from facedetect import detectFacesfromVideoCamera

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

app = Flask(__name__)

## Genarate QRcode for Number plate
now = datetime.now()
currdate = now.strftime("%Y-%m-%d")
directory = "static/NumberPlates/"+currdate+"/"
qrcodedir = directory+"/qrcodes/"
numplatesdir = directory+"numplates/"

queueProducerObj = QueueProducer()
vehicle_hotlist_data = get_vehicle_hotlist_data()
## Decode QR-code
def decodeQRCode():
    d = qrcode.Decoder()
    if d.decode('out.png'):
        print ('result: ' + d.result)
## End of decode QR-code/////////////////////////////////////////////////

def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0                             # this will be the center of the area the text will be written to
    ptCenterOfTextAreaY = 0

    ptLowerLeftTextOriginX = 0                          # this will be the bottom left of the area that the text will be written to
    ptLowerLeftTextOriginY = 0

    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX                      # choose a plain jane font
    fltFontScale = float(plateHeight) / 30.0                    # base font scale on height of plate area
    intFontThickness = int(round(fltFontScale * 1.5))           # base font thickness on font scale

    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)        # call getTextSize

            # unpack roatated rect into center point, width and height, and angle
    ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)              # make sure center is an integer
    intPlateCenterY = int(intPlateCenterY)

    ptCenterOfTextAreaX = int(intPlateCenterX)         # the horizontal location of the text area is the same as the plate

    if intPlateCenterY < (sceneHeight * 0.75):                                                  # if the license plate is in the upper 3/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))      # write the chars in below the plate
    else:                                                                                       # else if the license plate is in the lower 1/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))      # write the chars in above the plate
    # end if

    textSizeWidth, textSizeHeight = textSize                # unpack text size width and height

    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))           # calculate the lower left origin of the text area
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))          # based on the text area center, width, and height

            # write the text on the image
    cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)
# end function

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def genfacedetect(detectFacesfromVideoCamera):
    while True:
        frame = detectFacesfromVideoCamera.get_face_detect_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def genanprfromcam(anprfromcam):
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()
    while True:
        frame, response = anprfromcam.get_anpr_from_video(blnKNNTrainingSuccessful, vehicle_hotlist_data)
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def countvehicle(anprfromcam):
    while True:
        frame = anprfromcam.countvehicle()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# capture frame onclick button 
def captureframeonclick(anprfromcam):
    print('Entered captureframeonclick --------------------')
    while True:
        frame = anprfromcam.get_frame_onclick()                
        print('Captured Image >>>>--------->>>>')
        img = cv2.imdecode(np.fromstring(frame, dtype=np.uint8), 1)
        numplateimgname = str(uuid.uuid4())
        img_name = "static/temp/opencv_frame_"+numplateimgname+".png"              
        cv2.imwrite(img_name, img)
        response = maintest(img_name)
        print(response) 
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/livefeedfromCam')
@crossdomain(origin='*')
def livefeedfromCam():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detectfacesfromcam')    
@crossdomain(origin='*')
def detectfacesfromcam():
    return Response(genfacedetect(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/anprfromcam', methods=['POST', 'GET'])    
@crossdomain(origin='*')
def anprfromcam():
    camera = request.args.get('camera', '')
    return Response(genanprfromcam(VideoCamera(camera)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/countvehicle', methods=['POST', 'GET'])    
@crossdomain(origin='*')
def countvehicle():
    camera = request.args.get('camera', '')
    return Response(countvehicle(VideoCamera(camera)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
@crossdomain(origin='*')
def hello():
    return 'Welcome to Automatic License Plate Recognition!'

@app.route('/anpr')
@crossdomain(origin='*')
def anpr():
    cameras = readCsvFileAsJson()
    return render_template('index.html', fileslist=json.dumps([listFilesAsJson.list_all_files(imagefilesDir)]), cameras=cameras)

@app.route('/imageanpr')
@crossdomain(origin='*')
def imageanpr():
    return render_template('imagealpr.html', fileslist2=json.dumps([listFilesAsJson.list_all_files(imagefilesDir)]))

@app.route('/analytics')
@crossdomain(origin='*')
def analytics():
    return render_template('analytics.html', fileslist2=json.dumps([listFilesAsJson.list_all_files(imagefilesDir)]))

# onclick capture frame
@app.route('/capture')
@crossdomain(origin='*', methods=['GET'])
def capture():
    try:
        camera = request.args.get('camera', '')                        
        # SPACE pressed        
        return Response(captureframeonclick(VideoCamera(camera)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')                
        # response = maintest(img_name)                
    except Exception as e:
        print('[ Xception @ capture service ] :: '+str(e))

@app.route('/properties')
@crossdomain(origin='*')
def properties():    
    response = getProperties()
    print(response)
    # , properties=json.dumps([properties.getProperties()])
    return render_template('properties.html', properties=response)

@app.route('/base64toimage', methods=['POST'])
@crossdomain(origin='*')
def base64toimage():
    try:
        base64_str = request.args.get('base64str')
        writeBase64ToImageFile(str(base64_str))
        # print(base64_str)
    except Exception as e:
        print('{ Xception @ base64toimage } ',str(e))
    return 'Written to base64 to image'

@app.route('/anprprocess', methods=['POST'])
@crossdomain(origin='*')
def anprprocess():
    # user =  request.form['username'];
    # password = request.form['password'];
    anprimage = request.args.get('image', '')
    print(anprimage)
    if "data:image" in str(anprimage):
        print("IT is a base 64 string >>>>------->")
        print("ANPR CROPPED IMG :: "+anprimage)
        # cvimg = base64toImage.base64toImage(anprimage)
        cvimg = blob.readb64(anprimage)

        cv2.imwrite("static/temp/croppedimage.jpg",cvimg)
        cv2.waitKey(0)
        response = maintest("static/temp/croppedimage.jpg")
    else:
        response = maintest(anprimage)
    numplatecount = 0
    numplateqrcount = 0
    numplateimageslist = []

    now_2 = datetime.now()
    curr_date = now_2.strftime("%Y-%m-%d")
    
    for file in os.listdir(numplatesdir):        
        numplatecount += 1
        numplateqrcount += 1
        filepath = os.path.join(numplatesdir, file)
        imgsrc = "<img src='"+filepath+"' style='height:37px;width: 189px; padding-top: 3px; padding-left:5px'>"
        numplateimageslist.append({'Number Plate':imgsrc, 'Date Entered':curr_date, 'Camera' : 'Cam-1','Date Exit':curr_date})
    # Saving ALPR data ro sql table
    try:
        # savedata.save_data_to_sql_table(response)
        queueProducerObj.send_message_to_queue(response)
    except Exception as e:
        print(str(e))
    return json.dumps({'status':'OK','imagesrc':anprimage, 'data':response, 'date':curr_date, 'vehcount':numplatecount, 'qrcount':numplateqrcount, 'tabledata':numplateimageslist});

@app.route('/gettabledata', methods=['POST'])
@crossdomain(origin='*')
def getTableData():
    date = request.args.get('date', '')
    directory = "static/NumberPlates/"+date+"/"
    numplatesdir = directory+"/numplates/"
    numplateimageslist = []
    for file in os.listdir(numplatesdir):        
        filepath = os.path.join(numplatesdir, file)
        imgsrc = "<img src='"+filepath+"' style='height:37px;width: 189px; padding-top: 3px; padding-left:5px'>"
        numplateimageslist.append({'Number Plate':imgsrc, 'Date Entered':date, 'Camera' : 'Cam-1', 'Date Entered':currdate})
    return json.dumps({'tabledata':numplateimageslist});

# definition to get ALPR SQL table data
@app.route('/getalprsqltabledata', methods=['POST'])
@crossdomain(origin='')
def getALPRSQLTableData():
    alpr_sql_data = ''
    try:
        date = request.args.get('date','')
        from_date = request.args.get('fromdate','')
        to_date = request.args.get('todate','')        
        alpr_sql_data = get_alpr_sql_table_data(date, from_date, to_date)                
    except Exception as e:
        print(str(e))
    return alpr_sql_data

@app.route('/updatealprdata', methods=['POST'])
@crossdomain(origin='')
def updateALPRSQLTableData():
    try:
        alprid = request.args.get('alprid','')
        startdatetime = request.args.get('startdatetime','')
        enddatetime = request.args.get('enddatetime','')
        print(alprid)
        update_data_to_sql_table(alprid, startdatetime, enddatetime)
    except Exception as e:
        print(str(e))

    
if __name__=="__main__":
    # logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.basicConfig(format='%(levelname)s:%(message)s', filename='static/logs/anpr_'+currdate+'.log', level=logging.INFO)
    # logging.info('Started')
    app.run(host='127.0.0.1',debug=True, threaded=True)
