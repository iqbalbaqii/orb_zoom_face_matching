from src.model.DatasetImage import DatasetImage
from src.model.DatasetLabel import DatasetLabel
from src.bll.Image import Image
from src.bll.ORB import ORB
import os
import json
import time
import numpy as np


class Data:

    def __init__(self):
        self.data_image = DatasetImage()
        self.data_label = DatasetLabel()
        self.image_handler = Image()
        self.orb_handler = ORB()
        self.parrent_dir = '/home/bucky/Documents/Py/final/orb_zoom_face_matching/static/datasource/'

    # the output is showing image face only to result folder

    def get_parrent_dir(self):
        return self.parrent_dir

    def clean_raw(self, label):
        user = label

        try:
            os.mkdir(self.parrent_dir+user+'/result')
        except:
            pass

        for i, filename in enumerate(os.listdir(self.parrent_dir+user+'/raw')):
            img = self.image_handler.load_image(
                self.parrent_dir+user+'/raw/'+filename)

            self.image_handler.set_image(img)
            segmented = self.image_handler.segment_face()
            self.image_handler.save_image(
                self.parrent_dir+user+'/result/face_' + str(i)+'.png', segmented)

    # the result is put ORB info to image (resul forlder) dan the label

    def define_orb_on_label(self, kelas="group_0"):

        students = self.data_label.get(
            'id, nama', "kelas =    '{}' ORDER BY nama asc".format(kelas))
        ret = {}
        not_found = []
        for i, student in enumerate(students):
            name = student.nama
            label = str(name).replace(' ', '_')
            try:
                directory = self.parrent_dir+label+'/result/'
                temp = os.listdir(directory)
            except:
                not_found.append(name)
                continue

            for j, filename in enumerate(temp):
                path = os.path.join(directory, filename)
                
                ret[len(ret)] = {
                    'id': student.id,
                    'name': name,
                    'path': path
                }

            
        return ret
        # for i in range(0, 10):
        #     img = self.image_handler.load_image(
        #         self.parrent_dir+label+'/result/face_'+str(i)+'.png')
        #     self.orb_handler.set_image(img)
        #     keypoint, descriptor = self.orb_handler.get_keypoint_descriptor()
        #     keypoint = [{'angle': k.angle, 'response': k.response}
        #                 for k in keypoint]
        #     descriptor = descriptor.tolist()
