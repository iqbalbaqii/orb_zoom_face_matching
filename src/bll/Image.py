import cv2
import numpy as np
import pyautogui
from src.bll.ORB import ORB
import dlib


class Image:

    def __init__(self):
        
        self.id = None
        self.label = None
        self.counter = None

        # Image
        self.original = None
        self.face = None
        self.draw_keypoint = None
        self.draw_match = None
        self.gray = None
        self.landmark = None
        self.landmark_kp = None
        # =====
        self.face_cordinat = None

        # =====
        self.keypoint = None
        self.descriptor = None
        self.descriptor_match = None
        self.keypoint_match = None
        self.similarity = -1
        self.miss_match = 1

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
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.gray = gray
        self.face = np.copy(image)
        height, width, _ = image.shape
        self.face_cordinat = 0,0, width, height

    def set_descriptor_match(self, array):
        self.descriptor_match = array

    def set_keypoint_match(self, array):
        self.keypoint_match = array

    def set_similarity(self, data):
        self.similarity = data

    def set_draw_match(self, test_image, test_keypoints, matches):
        self.draw_match = cv2.drawMatches(test_image, test_keypoints, self.face, self.keypoint, matches, test_image, flags=2)

    def set_descriptor(self, desc):
        self.descriptor = desc

    def set_keypoint(self, kp):
        self.keypoint = kp

    def set_miss_match(self, number):
        self.miss_match = number
    
    def set_counter(self, counter):
        self.counter = counter
        
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

    def get_landmark_img(self):
        return self.landmark

    def get_landmarkkp_img(self):
        return self.landmark_kp

    def get_similarity(self):
        return self.similarity

    def get_descriptor_match(self):
        return self.descriptor_match

    def get_keypoint_match(self):
        return self.keypoint_match

    def get_keypoint(self):
        return self.keypoint

    def get_descriptor(self):
        return self.descriptor

    def get_miss_match(self):
        return self.miss_match

    def get_counter(self):
        return self.counter
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

        face_keypoint_match = cv2.drawKeypoints(
            self.face, self.keypoint_match, np.copy(self.face), color=(77, 255, 121))
            
        copy_ori1 = self.original.copy()
        copy_ori2 = self.original.copy()
        start_x, start_y, w, h = self.face_cordinat

        for i in range(w):
            for j in range(h):
                x = i + start_x
                y = j + start_y
                copy_ori1[y, x] = face_keypoint[j, i]
                copy_ori2[y, x] = face_keypoint_match[j, i]
        self.draw_keypoint = copy_ori1
        self.landmark_kp = copy_ori2

    def find_landmark(self):
        gray = self.gray.copy()
        face_landmark_lib = dlib.shape_predictor(
            "/home/bucky/Documents/Py/final/orb_zoom_face_matching/other/shape_predictor_68_face_landmarks.dat")
        hog_face_detector = dlib.get_frontal_face_detector()

        faces = hog_face_detector(gray)
        frame = self.original.copy()
        landmark_kp = self.landmark_kp.copy()
        face = faces[0]
        face_landmark = face_landmark_lib(gray, face)
        for n in range(0, 68):
            x = face_landmark.part(n).x
            y = face_landmark.part(n).y
            cv2.circle(frame, (x, y), 1, (0, 255, 255), 2)
            cv2.circle(landmark_kp, (x, y), 1, (0, 255, 255), 2)

        self.landmark = frame
        self.landmark_kp = landmark_kp

    def draw_landmark_and_kp(self):
        self.mask_original_image()
        self.find_landmark()
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

    def show_gray_image(self):
        cv2.imshow('preview', self.gray)
        cv2.waitKey(2000)
