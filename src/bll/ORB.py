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

    def set_image(self, image):
        self.image = image

    def get_keypoint_descriptor(self):
        orb = cv2.ORB_create(scoreType=cv2.ORB_FAST_SCORE)

        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        test_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        keypoint, descriptor = orb.detectAndCompute(test_gray, None)
        return type(descriptor)
        keypoint = [{'angle': k.angle, 'response': k.response} for k in keypoint]
        descriptor = descriptor.tolist()
        return keypoint, descriptor

    def locatekeypoint():
        fast = cv2.FastFeatureDetector_create(threshold=25)
        # find and draw the keypoints
        kp = fast.detect(self.image,)

    def match_the_faces(face_main, face_query):
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        match = bf.match(queryDescriptors, trainDescriptors)


    
