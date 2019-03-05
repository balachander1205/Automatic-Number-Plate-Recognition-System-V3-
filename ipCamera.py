# import cv2

# video = cv2.VideoCapture('http://wmccpinetop.axiscam.net//mjpg/video.mjpg')

import cv2
import urllib 
import numpy as np

stream=urllib.urlopen('http://wmccpinetop.axiscam.net//mjpg/video.mjpg')
#'http://iris.not.iac.es/axis-cgi/mjpg/video.cgi')
# 'http://88.53.197.250/axis-cgi/mjpg/video.cgi')
# 'http://wmccpinetop.axiscam.net//mjpg/video.mjpg'
bytes=''
while True:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
        cv2.imshow('i',i)
        if cv2.waitKey(1) ==27:
            exit(0)