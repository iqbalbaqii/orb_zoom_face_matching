from src.bll.Image import Image
import pyautogui
import cv2
import numpy as np
image_handler = Image()
image = pyautogui.screenshot()
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

face_cascade = cv2.CascadeClassifier(
    'other/haarcascade_frontalface_default.xml')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05,
	minNeighbors=5, minSize=(30, 30),
	flags=cv2.CASCADE_SCALE_IMAGE)

for (x, y, w, h) in faces:
    # draw the face bounding box on the image
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


image_handler.save_image('/home/bucky/Documents/Py/final/orb_zoom_face_matching/assets/result/ss.png', image)
