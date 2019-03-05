import cv2

# Trained XML classifiers describes some features of some object we want to detect
cascPath = "haarcascade_frontalface_webcam.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

class detectFacesfromVideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture('static/Walking Next to People.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_face_detect_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        # convert to gray scale of each image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray,1.1,1)
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # rectangle over identified face
            sub_face = image[y:y+h, x:x+w]

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()