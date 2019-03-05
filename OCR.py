import pytesseract
# from pytesseract import image_to_string
import cv2
import argparse
import re
import OCR
import os
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
    help="type of preprocessing to be done")
args = vars(ap.parse_args())


pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
tessdata_dir_config = '--tessdata-dir "/usr/bin/tesseract"'

def doOCR(liplateimage):
    print("LP image Path >>--->> "+liplateimage)
    # load the example image and convert it to grayscale
    image = cv2.imread(liplateimage)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # cv2.imshow("Image", gray)
    # image
    if args["preprocess"] == "thresh":
        gray = cv2.threshold(gray, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # make a check to see if median blurring should be done to remove
    # noise
    elif args["preprocess"] == "blur":
        gray = cv2.medianBlur(gray, 3)
    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    # filename = "static/temp/"+"{}.png".format(os.getpid())
    filename = "/static/temp/"+"{}.png".format(os.getpid())
    # filename = "D:/MY-PROJECTS/pythonRest/tesseract-python/8584.png"
    cv2.imwrite(filename, gray)
    print("OCR img file @ tesseract  ::: "+filename)
    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    # text = pytesseract.image_to_string(Image.open(filename), lang='eng', config=tessdata_dir_config)
    text = pytesseract.image_to_string(Image.open(filename), lang='eng')
    os.remove(filename)
    print("OCR TEXT from IMAGE >>>>  "+text)
    cv2.waitKey(0)
    return text

# doOCR("/home/alpr/Downloads/pythonRest-ANPR/static/temp/12586.png")
