# importing necessary libraries
from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import sys
import numpy as np
from src.controller.IdentificationController import IdentificationController
from src.bll.Image import Image
from src.bll.ORB import ORB
import pickle
import cv2

orb_handler = ORB()
img_handle = Image()
# loading the iris dataset
img1 = img_handle.load_image(
    '/home/bucky/Documents/Py/final/orb_zoom_face_matching/assets/result/test.png')

face = img_handle.segment_face()
orb_handler.set_image(face)
kp1, des1 = orb_handler.get_keypoint_descriptor()

cont = IdentificationController()
keypoints, data, label, image = cont.load_data_image()

n = 128
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

for i, descriptor in enumerate(data):
    des2 = descriptor
    kp2 = keypoints[i]
    img2 = image[i]
    matches = bf.match(des1, des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)

    # Draw first 10 matches.
    
    img3 = cv2.drawMatches(face, kp1, img2, kp2, matches[:10], flags=2)
    img_handle.save_image('/home/bucky/Documents/Py/final/orb_zoom_face_matching/assets/kp/kp_{}.png'.format(i), img3)

# img_handle.show_image(face)
