import numpy as np
from src.bll.Image import Image
from src.controller.DataController import DataController as DataHandler
from src.bll.ORB import ORB as OrbHandler
from src.model.DataTest import DataTest
from src.model.Meeting import Meeting
from src.model.Transaction import Transaction
from src.bll.SIFT import SIFT as SF
import operator
import os
from datetime import datetime
import time
import statistics
import pickle
import json
from copy import deepcopy


class IdentificationController(OrbHandler):
    def __init__(self):
        super().__init__()
        # STATIC VARIABLE
        self.APP_PATH = "/home/bucky/Documents/Py/final/orb_zoom_face_matching/{}"
        self.TODAY = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.k = 7
        self.start_time = None
        # END STATIC VARIABLE

        # INSTANCE MODEL
        self.DataTest = DataTest()
        self.Transaction = Transaction()
        self.Meeting = Meeting()
        # END
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

    def get_meeting_id(self):
        return self.Meeting.get_latest()[0].id

    def get_result(self):
        label, loc = self.result
        if(loc / self.k < 0.65):
            print('tidak diketahui')
            return False

        return label

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
        kp, desc = self.get_keypoint_descriptor(test_image.get_face())
        test_image.set_descriptor(desc)
        test_image.set_keypoint(kp)
        # test_image.find_landmark()
        self.identify(test_image)

    def load_data_image(self):
        raw_label = self.data_handler.load_group_image()
        self.data_set = []
        for idx, row in raw_label.items():
            try:
                image = Image()
                image.load_image(row['path'])
                image.set_label(row['name'])
                image.set_id(row['id'])
                image.set_counter("counter{}{}".format(row['id'], idx))
                kp, desc = self.get_keypoint_descriptor(image.get_face())
                image.set_descriptor(desc)
                image.set_keypoint(kp)
                self.data_set.append(image)
            except:
                continue

        print("Data load sucessfully. Total data {}".format(len(self.data_set)))

    def identify(self, face):
        students = np.copy(self.data_set)
        result = []
        label = ''
        keypoint_match = {}
        for i, student in enumerate(students):
            start_time = time.time()
            matches, similarity = self.compare_2_face(
                face.get_descriptor(), student.get_descriptor())

            kp_match = []
            face_match = []
            for match in matches:
                face_match.append(face.get_keypoint()[match.queryIdx])
                kp_match.append(student.get_keypoint()[match.trainIdx])

            keypoint_match[student.get_counter()] = tuple(face_match)

            students[i].set_keypoint_match(tuple(kp_match))
            students[i].set_descriptor_match(len(matches))
            students[i].set_similarity(similarity)
            students[i].set_draw_match(
                face.get_face(), face.get_keypoint(), matches)
            students[i].set_execution_time(
                str(round(time.time() - start_time, 3)))


        self.kuadran_section(face, keypoint_match, students)

        result = sorted(students,
                        key=lambda x: (-x.get_similarity(), x.get_miss_match()))
        # Checking Kuadran Keypoint
        nb = result[0:self.k]

        # print([{'label': p.get_label(),'similarity': round(p.get_similarity(),2), 'miss': round(p.get_miss_match(),2)} for p in nb])

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
        end_time = time.time()
        the_label = filter(lambda x: x.get_label() == sort_orders[0][0], nb)
        average_similarity = 0
        for data in list(the_label):
            average_similarity = average_similarity + data.get_similarity()

        average_similarity = round(
            average_similarity / int(sort_orders[0][1]), 3)
        identification_accuracy = round(int(sort_orders[0][1]) / self.k, 3)

        face_path = 'flask/meeting_{}/capture_{}'.format(
            self.meeting_id, self.capture_count)

        try:
            os.makedirs('static/'+face_path)
        except Exception as e:
            pass

        try:
            os.makedirs('static/'+face_path+'/matches')
            os.makedirs('static/'+face_path+'/landmark')
        except Exception as e:
            pass
        face.mask_original_image()
        face.find_landmark()

        face.save_image('static/'+face_path+"/original.png",
                        face.get_original_image())
        face.save_image('static/'+face_path+"/gray.png", face.get_image_gray())

        face.save_image('static/'+face_path+"/keypoint.png",
                        face.get_draw_keypoint_image())
        face.save_image('static/'+face_path+"/landmark.png",
                        face.get_landmark_img())

        for i, data in enumerate(nb):
            filename1 = face_path+'/matches/{}_capture_{}__compare__face_{}.png'.format(
                i, self.capture_count, data.get_id())
            filename2 = face_path+'/landmark/{}_capture_{}__compare__face_{}.png'.format(
                i, self.capture_count, data.get_id())
            data.save_image('static/'+filename1, data.get_draw_match_image())
            data.draw_landmark_and_kp()
            data.save_image('static/'+filename2, data.get_landmarkkp_img())

            self.Transaction.store({
                'id_image_test': 'meeting_{}__capture_{}'.format(self.meeting_id, self.capture_count),
                'execution_time': data.get_execution_time(),
                'keypoint_match': str(data.get_descriptor_match()),
                'file_name': filename1,
                'file_name2': filename2,
                'similarity': str(data.get_similarity()),
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
            'identification_time': str(round(end_time - self.start_time, 3)),
            'identification_result': self.result[0]
        })
        self.capture_count = self.capture_count + 1

        # TESTING

    def analyze_task(self):
        image_tests = self.data_handler.load_data_test()

        nfeature = [512, 1024, 3072]
        hamming = [32, 50, 64]
        k_knn = [7, 15, 30]
        loc = [0.20, 0.35, 0.50, 0.65, 0.80]

        test_combination = []
        count = 0
        for f in nfeature:
            for hamm in hamming:
                for k in k_knn:
                    for j in loc:
                        count = count + 1
                        test_combination.append({
                            'no': count,
                            'kombinasi': "nfeature: {}, hamming_tolerance: {}, k_knn: {}, loc: {}".format(f, hamm, k, j),
                            'data': (f, hamm, k, j)
                        })
        ret = []
        for combination in test_combination:
            print("Kombinasi " + str(combination['no']))
            nfeature, hamming, k_k, loc_ = combination['data']
            self.orb.setMaxFeatures(nfeature)
            self.set_hamming_tolerance(hamming)
            combo = {
                'nfeature': nfeature,
                'hamming_tolerance': hamming,
                'k_knn': k_k,
                'loc': loc_
            }
            temp = []
            for j, current in enumerate(np.copy(image_tests)):
                if(j == int(len(image_tests) * .5) or j == int(len(image_tests) * .3) or j == int(len(image_tests) * .6) or j == len(image_tests) - 1):
                    print("processing image " + str(j))
                start_process = time.time()
                kp, desc = self.get_keypoint_descriptor(current.get_face())
                current.set_keypoint(kp)
                current.set_descriptor(desc)
                students = np.copy(self.data_set)
                orb_times = []
                for i, student in enumerate(students):
                    start_orb = time.time()
                    try:
                        matches, similarity = self.compare_2_face(
                            student.get_descriptor(), current.get_descriptor())
                    except:
                        print(current.get_label())
                        return
                    students[i].set_descriptor_match(len(matches))
                    students[i].set_similarity(similarity)
                    students[i].set_draw_match(
                        current.get_face(), current.get_keypoint(), matches)
                    temp_time = round(time.time() - start_orb, 3)
                    students[i].set_execution_time(
                        str(temp_time))

                    orb_times.append(temp_time)

                result = sorted(students,
                                key=lambda x: x.get_similarity(), reverse=True)

                nb = result[0:k_k]
                count = {}
                for data in nb:
                    try:
                        count[data.get_label()]
                    except:
                        count[data.get_label()] = 1
                        continue
                    count[data.get_label()] = count[data.get_label()]+1

                sort_orders = sorted(
                    count.items(), key=lambda x: x[1], reverse=True)
                the_label = filter(lambda x: x.get_label()
                                   == sort_orders[0][0], nb)
                average_similarity = 0
                for data in list(the_label):
                    average_similarity = average_similarity + data.get_similarity()

                average_similarity = round(
                    average_similarity / int(sort_orders[0][1]), 3)
                identification_accuracy = round(
                    int(sort_orders[0][1]) / k_k, 3)

                final_label, _ = sort_orders[0]
                if(float(identification_accuracy) < loc_):
                    final_label = "Tidak Diketahui"

                true_label = str(current.get_label()).split('_')[0]
                temp.append({
                    'base_path': "kombinasi_{}/capture_{}".format(str(combination['no']), j),
                    'valid_result': True if final_label == true_label else False,
                    'label': true_label,
                    'identification_result': final_label,
                    'keypoint_length': len(current.get_keypoint()),
                    'average_similarity': average_similarity,
                    'identification_accuracy': identification_accuracy,
                    'identification_time': round(time.time() - start_process, 3),
                    'average_orb_executiion': round(statistics.fmean(orb_times), 3),
                })

                # face_path = 'flask/testing/kombinasi_{}/capture_{}'.format(str(combination['no']),j)

                # try:
                #     os.makedirs('static/'+face_path)
                # except Exception as e:
                #     pass

                # try:
                #     os.makedirs('static/'+face_path+'/matches')
                # except Exception as e:
                #     pass

                # current.save_image('static/'+face_path+"/original.png",
                #                 current.get_original_image())
                # current.save_image('static/'+face_path+"/gray.png",
                #                 current.get_image_gray())
                # current.mask_original_image()
                # current.save_image('static/'+face_path+"/keypoint.png",
                #                 current.get_draw_keypoint_image())

                # for i, data in enumerate(nb):
                #     filename = face_path+'/matches/{}_capture_{}__compare__face_{}.png'.format(i, j, data.get_id())
                #     data.save_image('static/'+filename,
                #                     data.get_draw_match_image())

            ret.append({
                'kombinasi': combination['kombinasi'],
                'combo': combo,
                'data': temp
            })
            print("Kombinasi {} Finish".format(str(combination['no'])))

        with open('kombinasi.json', 'w', encoding='utf-8') as f:
            json.dump(ret, f, ensure_ascii=False, indent=4)

        return 0

        ret_name = "kombinasi.pkl"
        pickle.dump(ret, open(ret_name, 'wb'))
        return 0

    def compare_with_sift(self):
        sift = SF()
        image_tests = self.data_handler.load_data_test()
        temp = []
        for j, current in enumerate(np.copy(image_tests)):

            start_process = time.time()
            kp, desc = sift.get_keypoint_descriptor(current.get_face())
            current.set_keypoint(kp)
            current.set_descriptor(desc)
            students = np.copy(self.data_set)
            orb_times = []
            for i, student in enumerate(students):
                start_orb = time.time()
                matches, similarity = sift.compare_2_face(
                    student.get_descriptor(), current.get_descriptor())
                try:
                    pass
                except Exception as e:
                    print(e)
                    return
                students[i].set_descriptor_match(len(matches))
                students[i].set_similarity(similarity)
                temp_time = round(time.time() - start_orb, 3)
                students[i].set_execution_time(
                    str(temp_time))

                orb_times.append(temp_time)

            result = sorted(students,
                            key=lambda x: x.get_similarity(), reverse=True)
            nb = result[0:7]
            count = {}
            for data in nb:
                try:
                    count[data.get_label()]
                except:
                    count[data.get_label()] = 1
                    continue
                count[data.get_label()] = count[data.get_label()]+1

            sort_orders = sorted(
                count.items(), key=lambda x: x[1], reverse=True)
            the_label = filter(lambda x: x.get_label()
                               == sort_orders[0][0], nb)
            average_similarity = 0
            for data in list(the_label):
                average_similarity = average_similarity + data.get_similarity()

            average_similarity = round(
                average_similarity / int(sort_orders[0][1]), 3)
            identification_accuracy = round(
                int(sort_orders[0][1]) / 7, 3)
            final_label, _ = sort_orders[0]
            if(float(identification_accuracy) < 0.5):
                final_label = "Tidak Diketahui"

            true_label = str(current.get_label()).split('_')[0]

            temp.append({
                'valid_result': True if final_label == true_label else False,
                'label': true_label,
                'identification_result': final_label,
                'keypoint_length': len(current.get_keypoint()),
                'average_similarity': average_similarity,
                'identification_accuracy': identification_accuracy,
                'identification_time': round(time.time() - start_process, 3),
                'average_sift_executiion': round(statistics.fmean(orb_times), 3),
            })
        return temp

    def kuadran_section(self, face, keypoint_matches, stundents):
        (height, width, color) = face.get_face().shape

        res = []
        for i, student in enumerate(stundents):
            current_keypoint_match = keypoint_matches[student.get_counter()]
            test_pts = [p.pt for p in current_keypoint_match]
            train_pts = [p.pt for p in student.get_keypoint_match()]

            (train_height, train_width, _) = student.get_face().shape

            miss_match = 1
            for ix, pt in enumerate(test_pts):
                kuadran_face = self.check_kuadran(width, height, test_pts[ix])
                kuadran_train = self.check_kuadran(
                    train_width, train_height, train_pts[ix])
                if(kuadran_face != kuadran_train):
                    miss_match = miss_match+1

            try:
                stundents[i].set_miss_match(miss_match / student.get_descriptor_match())
            except:
                pass

    def check_kuadran(self, width, height, point):

        x, y = point

        if (x > width/2 and x <= width) and (y >= 0 and y < height/2):
            return 1
        elif (x >= 0 and x <= width/2) and (y >= 0 and y < height/2):
            return 2
        elif (x > 0 and x <= width/2) and (y >= height/2 and y < height):
            return 3
        else:
            return 4
