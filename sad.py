import numpy as np
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('other/haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('other/haarcascade_eye.xml')

def zoom(img, zoom_factor= .5):
		return cv2.resize(img, None, fx=zoom_factor, fy=zoom_factor)

img = zoom(cv2.imread('assets/z.png'))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3,5)

for (x,y,w,h) in faces:
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,1,2),1)
	roi_gray = gray[y:y+h, x:x+w]
	roi_color = img[y:y+h, x:x+w]
	
	eyes = eye_cascade.detectMultiScale(roi_gray)
	for (ex,ey,ew,eh) in eyes:
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),1)

x,y,w,h = faces[0]

only_face = img[y:y+h, x:x+w]

cv2.imshow('img',only_face)
k = cv2.waitKey(0)

cv2.destroyAllWindows()