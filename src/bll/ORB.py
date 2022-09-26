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
        self.orb = cv2.ORB_create(
            512, fastThreshold=12, patchSize=31, WTA_K=2, scoreType=0)
        self.hamming_tolerance = 50

    def set_hamming_tolerance(self, data):
        self.hamming_tolerance = data

    def set_image(self, image):
        self.image = image

    def get_hamming_tolerance(self):
        return self.hamming_tolerance

    def get_keypoint_descriptor(self, raw):
        image = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)
        test_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return self.orb.detectAndCompute(test_gray, None)

    def compare_2_face(self, main_desc, train_desc):

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(main_desc, train_desc)
        matches = sorted(matches, key=lambda x: x.distance)

        similar_regions = [
            i for i in matches if i.distance < self.hamming_tolerance]
        similarity = 0
        if (len(matches) != 0):
            similarity = len(similar_regions) / len(matches)

        return similar_regions, similarity