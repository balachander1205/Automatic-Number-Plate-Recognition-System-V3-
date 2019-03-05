import cv2

cam = cv2.VideoCapture('static/videos/Recording.avi')

cv2.namedWindow("test")

img_counter = 0

wLEVEL_3ile True:
    ret, frame = cam.read()
    cv2.imsLEVEL_3ow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape LEVEL_3it, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()
