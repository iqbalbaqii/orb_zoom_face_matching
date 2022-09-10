from src.model.DataTest import DataTest
from src.model.Transaction import Transaction
from src.controller.IdentificationController import IdentificationController
import os
import json


class ViewController:
    def __init__(self):
        self.DataTest = DataTest()
        self.Transaction = Transaction()
        self.IdentificationController = IdentificationController()

    def front_analyze(self):
        meeting_id = self.IdentificationController.get_meeting_id()
        print(meeting_id)
        raw = self.DataTest.get(by="meeting_id = {}".format(meeting_id))
        identification_image = self.Transaction.get(
            select_clause="*", by="id_image_test LIKE '%meeting_{}%'".format(meeting_id))
        front = []
        data = []
        for row in raw:
            front.append({
                'original_image': row['base_path']+'/original.png',
                'keypoint_image': row['base_path']+'/keypoint.png',
                'gray_image': row['base_path']+'/gray.png',
            })

            comparation = list(filter(
                lambda x: x['id_image_test'] == row['unique_name'], identification_image))

            orb_time = list(
                map(lambda x: float(x['execution_time']), comparation))

            orb_time = round(sum(orb_time) / len(orb_time), 5)

            label = row['identification_result']
            prediction = str(label).replace(' ', '_')
            prediction_base_path = "/home/bucky/Documents/Py/final/orb_zoom_face_matching/static/datasource/{}/result".format(
                prediction)
            image_label = list(map(
                lambda x: 'datasource/{}/result/{}'.format(prediction, x), os.listdir(prediction_base_path)))

            accuracy = float(row['identification_accuracy'])
            accuracy = "{0:.1f}".format(accuracy * 100)

            similarity = "{0:.1f}".format(
                float(row['average_similarity']) * 100)
            data.append({
                'label': label,
                'identification_time': row['identification_time'],
                'orb_time': orb_time,
                'identification_accuracy': accuracy,
                'keypoint_found': row['keypoint_length'],
                'average_similarity': similarity,
                'similar_image_of_label': image_label,
                'comparation_image': comparation
            })
        return front, data
