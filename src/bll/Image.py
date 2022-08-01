import cv2
import numpy as np

class Image:

    # Semua handle image ada di Class ini termasuk segment, show, dan clean image ALL ABOUT CV2

    def __init__(self):
        self.image = None

    def set_image(self, image):
        self.image = image

    def get_image(self):
        return self.image

    def define_image_from_ss(self, image):
        self.image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    def segment_face(self):
        face_cascade = cv2.CascadeClassifier(
            'other/haarcascade_frontalface_default.xml')

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) < 1:
            return False

        x, y, w, h = faces[0] #len(faces)-1
        original_segmented = self.image[y:y+h, x:x+w]

        return original_segmented

    def show_image(self, image):
        cv2.imshow('preview', image)
        cv2.waitKey(0)

    def save_image(self, path, image):
        cv2.imwrite(path, image)

    def load_image(self, path):
        return cv2.imread(path)



