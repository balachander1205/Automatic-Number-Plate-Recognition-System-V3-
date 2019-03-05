url = 'rtsp://quicktime.tc.columbia.edu:554/users/lrf10/movies/sixties.mov'
# 'rtsp://184.72.239.149/vod/mp4:BigBuckBunny_175k.mov'

import cv2

cap = cv2.VideoCapture(url)
while True:
    _, frame = cap.read() 
    #Place options to overlay on the video here.
    #I'll go over that later.
    cv2.imshow('Camera', frame)
    k = cv2.waitKey(0) & 0xFF
    if k == 27: #esc key ends process
        cap.release()
        break
cv2.destroyAllWindows()