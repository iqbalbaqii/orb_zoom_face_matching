from src.model.DatasetLabel import DatasetLabel
from src.controller.IdentificationController import IdentificationController
from src.bll.Image import Image
from src.bll.ORB import ORB as ORBS
import pyautogui
import cv2
import numpy as np


def identification_2():
    orb_handler = ORBS()
    identification = IdentificationController()

    DataHandler = DatasetLabel()
    students = DataHandler.get('*', "kelas = '{}'".format('group_0'))

    image_handler = Image()
    # image = pyautogui.screenshot()
    # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    image = image_handler.load_image(
        '/home/bucky/Documents/Py/final/orb_zoom_face_matching/assets/datasource/Zhicma_Nabillah/raw/Screenshot from 2022-07-18 09-27-41.png')

    face_cascade = cv2.CascadeClassifier(
        'other/haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gallery_view_faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    result = []
    for face in gallery_view_faces:
        x, y, w, h = face
        segment_face = image[y:y+h, x:x+w]
        result = identification.identify(segment_face)

    
    return result


identification_2()
