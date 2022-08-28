import cv2
import numpy as np
from src.model.DatasetImage import DatasetImage
from src.model.DatasetLabel import DatasetLabel
import json
import time


class ORB:
    # Kelas untuk mengakomodasi kebutuhan utama ORB

    def __init__(self):
        self.image = None
        self.orb = cv2.ORB_create(nfeatures=512, fastThreshold = 12, patchSize = 31)
        
    def set_image(self, image):
        self.image = image

    def get_keypoint_descriptor(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        test_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        return self.orb.detectAndCompute(test_gray, None)


    def compare_2_face(self, main_desc, train_desc):

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(main_desc, train_desc)
        matches = sorted(matches, key=lambda x: x.distance)
        return matches

    def get_keypoint_descriptor2(self, img):
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        test_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        return self.orb.detectAndCompute(test_gray, None)