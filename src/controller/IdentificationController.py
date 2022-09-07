import numpy as np
import json
from src.bll.Image import Image
from src.bll.Data import Data as DataHandler
from src.bll.ORB import ORB as OrbHandler
from src.model.DatasetImage import DatasetImage
from src.model.DatasetLabel import DatasetLabel
from src.model.DataTest import DataTest
from src.model.Meeting import Meeting
from src.model.Transaction import Transaction
from src.model.General import General
import cv2
import operator
import os
from datetime import datetime
import time


class IdentificationController:
    def __init__(self):
        # STATIC VARIABLE
        self.APP_PATH = "/home/bucky/Documents/Py/final/orb_zoom_face_matching/{}"
        self.TODAY = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.k = 20
        self.start_time = None
        # END STATIC VARIABLE

        # INSTANCE MODEL
        self.DataLabel = DatasetLabel()
        self.DB = General()
        self.DataTest = DataTest()
        self.Transaction = Transaction()
        self.Meeting = Meeting()
        # END

        self.orb_handler = OrbHandler()
        self.DataImage = DatasetImage()
        self.data_handler = DataHandler()

        self.data_set = None
        self.result = None

        self.capture_count = 0
        self.meeting_id = 0

    def make_meeting(self):
        self.Meeting.store({
            'meeting_name': 'demo-project',
            'kelas': 'group_0',
            'created_at': self.TODAY,
            'updated_at': self.TODAY
        })

        self.meeting_id = self.Meeting.get_latest()[0].id

    def get_result(self):
        return self.result

    def get_capture_count(self):
        return self.capture_count

    def identification_task(self, region):
        self.start_time = time.time()
        x, y, width, height = region

        test_image = Image()
        test_image.capture_image(x, y, width, height)
        found = test_image.segment_face()
        if found is False:
            return found

        test_image.extract_kp_desc()
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
        for i, student in enumerate(students):
            matches, similarity = self.orb_handler.compare_2_face(
                student.get_descriptor(), face.get_descriptor())
            students[i].set_descriptor_match(len(matches))
            students[i].set_similarity(similarity)
            students[i].set_draw_match(
                face.get_face(), face.get_keypoint(), matches)

        result = sorted(students,
                        key=lambda x: x.get_similarity(), reverse=True)

        nb = result[0:self.k]
        count = {}
        for data in nb:
            try:
                count[data.get_label()]
            except:
                count[data.get_label()] = 1
                continue
            count[data.get_label()] = count[data.get_label()]+1

        sort_orders = sorted(count.items(), key=lambda x: x[1], reverse=True)
        self.result = sort_orders[0]

        the_label = filter(lambda x: x.get_label() == sort_orders[0][0], nb)
        average_similarity = 0
        for data in list(the_label):
            average_similarity = average_similarity + data.get_similarity()

        average_similarity = round(
            average_similarity / int(sort_orders[0][1]), 3)
        identification_accuracy = round(int(sort_orders[0][1]) / self.k, 3)

        face_path = 'static/flask'+'/meeting_{}/capture_{}'.format(self.meeting_id, self.capture_count)

        try:
            os.makedirs(face_path)
        except Exception as e:
            pass

        try:
            os.makedirs(face_path+'/matches')
        except Exception as e:
            pass

        face.save_image(face_path+"/original.png", face.get_original_image())
        face.mask_original_image()
        face.save_image(face_path+"/keypoint.png",
                        face.get_draw_keypoint_image())

        for i, data in enumerate(nb):
            filename = face_path+'/matches/{}_capture_{}__compare__face_{}.png'.format(
                i, self.capture_count, data.get_id())
            data.save_image(filename, data.get_draw_match_image())

            self.Transaction.store({
                'id_image_test': 'meeting_{}__capture_{}'.format(self.meeting_id, self.capture_count),
                'execution_time': str(round(time.time() - self.start_time, 3)),
                'keypoint_match': str(data.get_descriptor_match()),
                'file_name': filename,
                'comparation_label': data.get_label()
            })

        self.DataTest.store({
            'meeting_id': self.meeting_id,
            'unique_name': 'meeting_{}__capture_{}'.format(self.meeting_id, self.capture_count),
            'base_path': face_path,
            'keypoint_length': str(len(face.get_keypoint())),
            'created_at': self.TODAY,
            'updated_at': self.TODAY,
            'average_similarity': str(average_similarity),
            'identification_accuracy': str(identification_accuracy),
            'identification_time': str(round(time.time() - self.start_time, 3)),
            'identification_result': self.result[0]
        })
        self.capture_count = self.capture_count + 1
