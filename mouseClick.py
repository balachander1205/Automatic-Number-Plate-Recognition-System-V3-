import numpy as np
import cv2

cap = cv2.VideoCapture('E:/MY-PROJECTS/pythonRest-ANPR - V2/static/videos/alpr-feed.mp4')
img_counter = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv2.imshow('frame',gray)
    k = cv2.waitKey(1)
    if k%256 == 32:
        # SPACE pressed
        img_name = "E:/MY-PROJECTS/pythonRest-ANPR - V2/static/videos/opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
cv2.namedWindow("test")

