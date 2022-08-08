import numpy as np
import json
from src.bll.Image import Image as ImageHandler
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

        self.image_handler = ImageHandler()
        self.orb_handler = OrbHandler()
        self.DataImage = DatasetImage()
        self.DataLabel = DatasetLabel()
        self.data_handler = DataHandler()
        self.DB = General()

        self.data_set = None
        self.result = None
        self.k = 30

    def get_result(self):
        return self.result

    def identification_task(self, region):
        x, y, width, height = region
        self.image_handler.capture_image(
            x, y, width, height)
        frontal_face = self.image_handler.segment_face()
        if frontal_face is False:
            return frontal_face

        self.get_identification_result(frontal_face)

        # self.image_handler.save_image(self.APP_PATH.format(
        #     "assets/result/face.png"), frontal_face)

    def do_the_comparation(self, face):

        test_keypoint, test_descriptor = self.orb_handler.get_keypoint_descriptor2(
            face)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        comparation = []
        labels = []
        for row in self.data_set:
            descriptor = row['descriptor']
            try:
                matches = bf.match(test_descriptor, descriptor)
                matches = sorted(matches, key=lambda x: x.distance)
            except:
                continue
            comparation.append({
                'compare_with_face': row['label'],
                'len_face_descriptor': len(test_descriptor),
                'len_query_descriptor': len(descriptor),
                'len_match_descriptor': len(matches)
            })

        return sorted(comparation, key=operator.itemgetter('len_match_descriptor'), reverse=True)

    def load_data_image(self):
        self.data_set = []
        datas, _ = self.data_handler.define_orb_on_label_batch("group_0")
        for label, row in datas.items():
            for i, path in enumerate(row):
                image = self.image_handler.load_image(path)
                try:
                    self.orb_handler.set_image(image)
                    key, desc = self.orb_handler.get_keypoint_descriptor()
                    self.data_set.append({
                        'label': label,
                        'path': path,
                        'keypoint': key,
                        'descriptor': desc
                    })
                except:
                    continue
        print('data-load succesfully')

    def get_identification_result(self, face):
        temp_sorted_result = np.array(self.do_the_comparation(face))[:23]
        under_half = 0
        upper_half = 0

        deleted_element = []
        for i, row in enumerate(temp_sorted_result):
            matches_desc = row['len_match_descriptor']
            dataset_desc = row['len_query_descriptor']
            face_desc = row['len_face_descriptor']

            if matches_desc / face_desc > 0.2 and matches_desc / dataset_desc > 0.2:
                continue
            else:
                deleted_element.append(i)

        filtering_set = np.delete(temp_sorted_result, deleted_element)

        labels = np.unique(np.array(list(val for dic in filtering_set.copy(
        ) for key, val in dic.items() if key == 'compare_with_face'))).tolist()

        label_counting = {a: 0 for a in labels}

        for row in filtering_set:
            label_counting[row['compare_with_face']
                           ] = label_counting[row['compare_with_face']]+1

        if label_counting == {}:
            pass
        else:
            array_names = list(label_counting)
        array_value = list(label_counting.values())

        def find_positions(lst, name):
            return next((index for (index, d) in enumerate(lst) if d["compare_with_face"] == name), None)

        a, seen, result = array_value, set(), []
        final_result = label_counting;
        for idx, item in enumerate(a):
            if item not in seen:
                seen.add(item)          # First time seeing the element
            else:
                # Already seen, add the index to the result
                result.append(idx)

        if len(array_value) > 1 and len(array_value) == len(result)+1:
            minimum = self.k
            top = -1
            for index in result:
                x = find_positions(filtering_set, array_names[index])

                if (x < minimum):
                    minimum = x
                    top = index
            final_result = array_names[top]
        else:
            the_max = max(array_value)
            if result == []:
                final_result = array_names[array_value.index(the_max)]
            elif the_max <= array_value[result[0]]:
                minimum = self.k
                top = -1
                for index in result:
                    x = find_positions(filtering_set, array_names[index])

                    if (x < minimum):
                        minimum = x
                        top = index
                final_result = array_names[top]
            else:
                final_result = array_names[array_value.index(the_max)]
        self.result = final_result


# 1
