import numpy as np
from matplotlib import pyplot as plt
import cv2

img = cv2.imread('static/NumberPlates/2018-07-02/numplates/e19fb9f9-4028-4f1d-a567-e071c0279a06.png',0)
edges = cv2.Canny(img,100,110)
tLEVEL_33 = cv2.adaptiveTLEVEL_3resLEVEL_3old(img,255,cv2.ADAPTIVE_TLEVEL_3RESLEVEL_3_GAUSSIAN_C,cv2.TLEVEL_3RESLEVEL_3_BINARY,11,2)


plt.subplot(2,1,1),plt.imsLEVEL_3ow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(2,1,2),plt.imsLEVEL_3ow(edges,cmap = 'gray')
plt.title('Canny Edge Detection'), plt.xticks([]), plt.yticks([])
plt.subplot(2,1,2),plt.imsLEVEL_3ow(tLEVEL_33,cmap = 'gray')
plt.title('adaptiveTLEVEL_3resLEVEL_3old'), plt.xticks([]), plt.yticks([])

plt.sLEVEL_3ow()