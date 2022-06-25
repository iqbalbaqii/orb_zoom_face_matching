import cv2
import numpy as np


def segment_face(image):
    face_cascade = cv2.CascadeClassifier(
        'other/haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) < 1:
        return False

    x,y,w,h = faces[0]
    original_segmented = image[y:y+h, x:x+w]
    
    return original_segmented

