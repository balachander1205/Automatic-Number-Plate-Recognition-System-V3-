
import cv2
import numpy as np
import os
import uuid
from centroidtracker import CentroidTracker
import math

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False
ct = CentroidTracker()

X_1 = 0
Y_1 = 0
dist = 0
text = 0
i = 0

def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)            # get 4 vertices of rotated rect    
    
    lists_of_lists = [p2fRectPoints[1], [-25,-25]]
    updated_cords = [sum(x) for x in zip(*lists_of_lists)]
    p2fRectPoints[1] = updated_cords

    lists_of_lists = [p2fRectPoints[3], [25,25]]
    updated_cords = [sum(x) for x in zip(*lists_of_lists)]
    p2fRectPoints[3] = updated_cords

    cv2.rectangle(imgOriginalScene,tuple(p2fRectPoints[1]),tuple(p2fRectPoints[3]),SCALAR_GREEN,2)    			

    x1 = int(p2fRectPoints[1][0])
    x2 = int(p2fRectPoints[1][1])

    y1 = int(p2fRectPoints[3][0])
    y2 = int(p2fRectPoints[3][1])

    # cv2.rectangle(imgOriginalScene, (x1, y2 + 25), (y1, y2), SCALAR_GREEN, cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    # cv2.putText(imgOriginalScene, "Number Plate", (x1 + 6, y2 + 12), font, 0.5, (255, 255, 255), 1)

def crop_number_plate_from_img(imgOriginalScene, licPlate):
    global X_1
    global Y_1
    global dist
    global text
    global i
    diff_range = range(-500, -750)

    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)
    
    lists_of_lists = [p2fRectPoints[1], [-30,-30]]
    updated_cords = [sum(x) for x in zip(*lists_of_lists)]
    p2fRectPoints[1] = updated_cords

    lists_of_lists = [p2fRectPoints[3], [35,35]]
    updated_cords = [sum(x) for x in zip(*lists_of_lists)]
    p2fRectPoints[3] = updated_cords

    x1 = int(p2fRectPoints[1][0])
    x2 = int(p2fRectPoints[1][1])

    y1 = int(p2fRectPoints[3][0])
    y2 = int(p2fRectPoints[3][1])    

    rect_img = cv2.rectangle(imgOriginalScene,tuple(p2fRectPoints[1]),tuple(p2fRectPoints[3]),SCALAR_GREEN,2)
    # Finding center of rectangle.    
    M = cv2.moments(p2fRectPoints)    
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    centroid = [cX, cY]    

    # np_dist = calculateDistance(X_1, Y_1, cX, cY)
    
    # print('[ Previous Centroid ]  ['+str(X_1)+','+str(Y_1)+']')
    # print('[ New Centroid ]  ['+str(cX)+','+str(cY)+']')
    # diff_dist = int(dist)-int(np_dist)
    # if int(diff_dist)<10:        
    # if int(diff_dist) in range(-750, -600):
        # i = int(i)+int(1)
        # text = str(i)
        # print('[ Value not liew between  -600 <= '+str(diff_dist)+' <= -750]==========================')        
        # print('--- [ Diff Distance ] '+str(diff_dist))        
    # else:        
        # text = str(i)        
        # print('--- [ Diff Distance ] '+str(diff_dist))
        
    # X_1 = cX
    # Y_1 = cY
    # dist = np_dist
    
    # box = np.array([x1, (y2 + 25), y1, y2])        
    # rects = []
    # rects.append(box.astype("int"))
    # update our centroid tracker using the computed set of bounding
    # box rectangles
    # objects = ct.update(rects)

    # loop over the tracked objects
    # for (objectID, centroid) in objects.items():        
        # draw both the ID of the object and the centroid of the
        # object on the output frame
        # text = "ID {}".format(objectID)
        # cv2.putText(imgOriginalScene, text, (cX, cY),
            # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # cv2.circle(imgOriginalScene, (cX, cY), 4, (0, 255, 0), -1)

    # cv2.rectangle(imgOriginalScene, (x1, y2 + 25), (y1, y2), SCALAR_GREEN, cv2.FILLED)    
    # Drawing center of rectangle..
    # cv2.putText(imgOriginalScene, "centroid : ["+str(cX)+","+str(cY)+"]", (cX, cY),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # cv2.circle(imgOriginalScene, (cX, cY), 7, (0,255,0), -1)
    # font = cv2.FONT_HERSHEY_DUPLEX
    # cv2.putText(imgOriginalScene, text, (x1 + 6, y2 + 12), font, 0.5, (255, 255, 255), 1)
    # rectangle crop of number plate
    num_plate = rect_img[x2:y2, x1:y1]
    return num_plate, centroid
  
def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist

# print calculateDistance(x1, y1, x2, y2)  


