import numpy as np
import json
from src.bll.Image import Image
from src.bll.Data import Data as DataHandler
from src.bll.ORB import ORB as OrbHandler
from src.model.DatasetImage import DatasetImage
from src.model.DatasetLabel import DatasetLabel
from src.model.General import General
import cv2
import operator


class IdentificationController:
    def __init__(self):
        # STATIC VARIABLE
        self.APP_PATH = "/home/bucky/Documents/Py/final/orb_zoom_face_matching/{}"
        # END STATIC VARIABLE

        self.orb_handler = OrbHandler()
        self.DataImage = DatasetImage()
        self.DataLabel = DatasetLabel()
        self.data_handler = DataHandler()
        self.DB = General()

        self.data_set = None
        self.result = None
        self.k = 30
        self.file_count = 0

    def get_result(self):
        return self.result

    def identification_task(self, region):
        x, y, width, height = region

        test_image = Image()
        test_image.capture_image(x, y, width, height)
        found = test_image.segment_face()
        test_image.extract_kp_desc()
        if found is False:
            return frontal_face

        self.identify(test_image)

    def load_data_image(self):
        raw_label = self.data_handler.define_orb_on_label()
        self.data_set = []
        for idx, row in raw_label.items():
            try:
                image = Image()
                image.load_image(row['path'])
                image.set_label(row['name'])
                image.set_id(row['id'])
                image.extract_kp_desc()
                self.data_set.append(image)
            except:
                continue
        
        print("Data load sucessfully. Total data {}".format(len(self.data_set)))

    def identify(self, face):
        students = np.copy(self.data_set)
        result = []
        
        label = ''
        for i,student in enumerate(students):
            matches, similarity = self.orb_handler.compare_2_face(student.get_descriptor(), face.get_descriptor())
            students[i].set_descriptor_match(len(matches))
            students[i].set_similarity(similarity)
        
        students = students.tolist()
        nl = sorted(students, key=lambda x: x.get_similarity(), reverse=True)
        result = map(lambda x: {'face': x.get_label(), 'loc': x.get_similarity()}, nl)
        result = list(result)

        get_20 = result[0:20]
        count = {}
        for data in get_20:
            try:
                count[data['face']]
            except:
                count[data['face']] = 1
                continue
            count[data['face']] = count[data['face']]+1

        
        sort_orders = sorted(count.items(), key=lambda x: x[1], reverse=True)
        self.result = sort_orders[0]