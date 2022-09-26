import cv2
import numpy as np
import pyautogui
from src.bll.ORB import ORB


class Image:

    def __init__(self):
        self.id = None
        self.label = None

        # Image
        self.original = None
        self.face = None
        self.draw_keypoint = None
        self.draw_match = None
        self.gray = None
        # =====
        self.face_cordinat = None

        # =====
        self.keypoint = None
        self.descriptor = None
        self.descriptor_match = None
        self.similarity = -1

        # TIME
        self.execution_time = 0

        self.orb_handle = ORB()

    def set_execution_time(self, time):
        self.execution_time = time

    def set_id(self, id):
        self.id = id

    def set_label(self, label):
        self.label = label

    def load_image(self, path, resize=False):
        image = cv2.imread(path)

        if(resize):
            self.original = cv2.resize(image, (960, 540))
        else:
            self.original = np.copy(image)

        # we asume this function will use by clean face image data
        self.face = np.copy(image)

    def set_descriptor_match(self, array):
        self.descriptor_match = array

    def set_similarity(self, data):
        self.similarity = data

    def set_draw_match(self, test_image, test_keypoints, matches):
        self.draw_match = cv2.drawMatches(self.face, self.keypoint,
                                          test_image, test_keypoints, matches[:32], test_image, flags=2)

    def set_descriptor(self, desc):
        self.descriptor = desc

    def set_keypoint(self, kp):
        self.keypoint = kp

    # GETTER
    def get_execution_time(self):
        return self.execution_time

    def get_id(self):
        return self.id

    def get_label(self):
        return self.label

    def get_original_image(self):
        return self.original

    def get_image_gray(self):
        return self.gray

    def get_draw_keypoint_image(self):
        return self.draw_keypoint

    def get_draw_match_image(self):
        return self.draw_match

    def get_face(self):
        return self.face

    def get_similarity(self):
        return self.similarity

    def get_descriptor_match(self):
        return self.descriptor_match

    def get_keypoint(self):
        return self.keypoint

    def get_descriptor(self):
        return self.descriptor
    # END GETTER

    def capture_image(self, x=0, y=0, width=0, height=0, fullscreen=False):
        if not fullscreen:
            image = pyautogui.screenshot(region=(x, y, width, height))
        else:
            image = pyautogui.screenshot()

        self.original = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    def segment_face(self):
        face_cascade = cv2.CascadeClassifier(
            'other/haarcascade_frontalface_default.xml')

        gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(np.copy(gray), (5, 5), cv2.BORDER_DEFAULT)
        self.gray = gray
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) < 1:
            return False

        x, y, w, h = faces[0]
        self.face_cordinat = faces[0]
        original_segmented = self.original[y:y+h, x:x+w]
        self.face = original_segmented
        return True

    

    def mask_original_image(self):
        face_keypoint = cv2.drawKeypoints(
            self.face, self.keypoint, np.copy(self.face), color=(77, 255, 121))

        copy_ori = self.original.copy()
        start_x, start_y, w, h = self.face_cordinat

        for i in range(w):
            for j in range(h):
                x = i + start_x
                y = j + start_y
                copy_ori[y, x] = face_keypoint[j, i]
        self.draw_keypoint = copy_ori
    # MISC

    def show_original_image(self):
        cv2.imshow('preview', self.original)
        cv2.waitKey(0)

    def show_face(self):
        cv2.imshow('preview', self.face)
        cv2.waitKey(0)

    def show_draw_keypoint(self):
        cv2.imshow('preview', self.draw_keypoint)
        cv2.waitKey(0)

    def save_image(self, path, image):
        cv2.imwrite(path, image)
