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
import os

orb_handler = ORB()
img_handle = Image()
# loading the iris dataset
img1 = img_handle.load_image(
    '/home/bucky/Documents/Py/final/orb_zoom_face_matching/assets/result/kk.jpg')
img_handle.set_image(img1)
face = img_handle.segment_face()
orb_handler.set_image(face)
test_keypoints, test_desc = orb_handler.get_keypoint_descriptor()

face_path = '/home/bucky/Documents/Py/final/orb_zoom_face_matching/assets/flask'+'/face_1'
try:
    os.mkdir(face_path)
    os.mkdir(face_path+'/matches')
except:
    pass

img_handle.save_image(face_path+'/original_face.png', img1)

face_img_kp = cv2.drawKeypoints(face, test_keypoints, np.copy(face), color = (0, 255, 0))

img_handle.save_image(face_path+'/face_kp.png', face_img_kp)

test_gray = orb_handler.get_img_gray()

cont = IdentificationController()
keypoints, data, label, image = cont.load_data_image()

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

for i, descriptor in enumerate(data):
    train_desc = descriptor
    train_keypoints = keypoints[i]
    training_image = image[i]

    
    keypoints_without_size = np.copy(training_image)
    keypoints_with_size = np.copy(training_image)

    train_img_kp = cv2.drawKeypoints(training_image, train_keypoints, keypoints_without_size, color = (0, 255, 0))

    matches = bf.match(train_desc,test_desc)
    matches = sorted(matches, key=lambda x: x.distance)
    
    try:
        result = cv2.drawMatches(training_image, train_keypoints,
                                 face, test_keypoints, matches[:300], face, flags=2)
        img_handle.save_image(
            face_path+'/matches/'+'/kp_{}.png'.format(i), result)
    except Exception as e:
        print(e)
    

# img_handle.show_image(face)
