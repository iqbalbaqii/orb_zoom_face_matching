from src.controller.IdentificationController import IdentificationController
from src.bll.Image import Image
from src.bll.ORB import ORB
import pickle
import numpy as np
orb_handler = ORB()
img_handle = Image()

face = img_handle.load_image('/home/bucky/Documents/Py/final/orb_zoom_face_matching/assets/result/test.png')

orb_handler.set_image(face)
keypoint, desc = orb_handler.get_keypoint_descriptor()

minus_length = 128 - len(desc)

new_array = np.full([minus_length, 32], -99)
desc = np.concatenate((desc, new_array), axis=0)
X_test = np.concatenate(desc)

loaded_model = pickle.load(open('/home/bucky/Documents/Py/final/orb_zoom_face_matching/finalized_model.sav', 'rb'))

predict = loaded_model.predict([X_test])
print((predict))