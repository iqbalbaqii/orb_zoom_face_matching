from src.model.DatasetLabel import DatasetLabel
from src.bll.Image import Image
import os


class DataController:

    def __init__(self):
        self.data_label = DatasetLabel()
        self.parrent_dir = '/home/bucky/Documents/Py/final/orb_zoom_face_matching/static'

    # the output is showing image face only to result folder

    def get_parrent_dir(self):
        return self.parrent_dir

    def clean_raw(self, label):
        user = label
        _dir = self.parrent_dir+'/datasource/'

        try:
            os.mkdir(_dir+user+'/result')
        except:
            pass

        for i, filename in enumerate(os.listdir(_dir+user+'/raw')):
            try:
                raw_image = Image()
                raw_image.load_image(_dir+user+'/raw/'+filename)
                raw_image.segment_face()
                raw_image.save_image(
                    _dir+user+'/result/face_' + str(i)+'.png', raw_image.get_face())
            except Exception as e:
                # directory
                continue

    def load_group_image(self, kelas="group_0"):

        students = self.data_label.get(
            'id, nama', "kelas =    '{}' ORDER BY nama asc".format(kelas))
        ret = {}
        not_found = []
        for i, student in enumerate(students):
            name = student.nama
            label = str(name).replace(' ', '_')
            try:
                directory = self.parrent_dir+'/datasource/'+label+'/result/'
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

    def load_data_test(self):
        _dir = self.parrent_dir+'/datatest/'
        image_tests = []
        for i, filename in enumerate(os.listdir(_dir)):
            try:
                image = Image()
                image.set_label(filename)
                image.load_image(_dir+filename)
                image.segment_face()
                image.extract_kp_desc()
                image_tests.append(image)
            except Exception as e:
                print(e)
                continue
        return image_tests