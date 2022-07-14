import cv2
import numpy as np
from src.model import DatasetImage
from src.model import DatasetLabel
from hashlib import sha256
import json
import time


class ORB:

    def __init__(self):
        self.image = None

    def setImage(self, image):
        self.image = image

    def run(self):
        orb = cv2.ORB_create(scoreType=cv2.ORB_FAST_SCORE)

        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        test_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        keypoint, descriptor = orb.detectAndCompute(test_gray, None)

        img2_kp = cv2.drawKeypoints(self.image, keypoint, None, color=(120, 255, 0),
                                    flags=cv2.DrawMatchesFlags_DEFAULT)
        return img2_kp

        # keypoints_without_size = np.copy(self.image)
        # keypoints_with_size = np.copy(self.image)
        return keypoint, descriptor

    def definedataset(self):
        label = 'Muhammad_Iqbal_Baqi'
        files = label.lower()

        for i in range(1, 11):
            img = cv2.imread(
                '/home/bucky/Documents/Py/final/orb_zoom_face_matching/assets/datasource/'+label+'/result/'+files+'_'+str(i)+'.png')
            self.setImage(img)
            keypoint, descriptor = self.run()
            keypoint = [{'angle': k.angle, 'response': k.response}
                        for k in keypoint]
            descriptor = descriptor.tolist()

            DatasetImage.store({
                'label': '453b02',
                'image': '/home/bucky/Documents/Py/final/orb_zoom_face_matching/assets/datasource/'+label+'/result/'+files+'_'+str(i)+'.png',
                'keypoint': json.dumps(keypoint),
                'deskriptor': json.dumps(descriptor),
                'meet_id': '0',
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': time.strftime('%Y-%m-%d %H:%M:%S')
            })

    def locatekeypoint():
        fast = cv2.FastFeatureDetector_create(threshold=25)
        # find and draw the keypoints
        kp = fast.detect(self.image,)
