import cv2
import numpy as np
from src.model.DatasetImage import DatasetImage
from src.model.DatasetLabel import DatasetLabel
import json
import time


class SIFT:
    # Kelas untuk mengakomodasi kebutuhan utama ORB

    def __init__(self):
        self.image = None
        self.sift = cv2.xfeatures2d.SIFT_create(nfeatures=1024) 
        

    def set_hamming_tolerance(self, data):
        self.hamming_tolerance = data

    def set_image(self, image):
        self.image = image

    def get_hamming_tolerance(self):
        return self.hamming_tolerance

    def get_keypoint_descriptor(self, raw):
        image = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)
        test_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return self.sift.detectAndCompute(test_gray, None)

    def compare_2_face(self, main_desc, train_desc):

        bf = cv2.BFMatcher()        
        matches = bf.knnMatch(main_desc, train_desc,k=2)
        # Apply ratio test
        good = []
        t = []
        for m,n in matches:
            t.append(1)
            if m.distance < 0.75*n.distance:
                good.append([m])

        similarity = len(good)/len(t)
        return matches, similarity