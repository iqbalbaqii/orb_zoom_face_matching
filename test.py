from src.bll.ORB import ORB
from src.bll.Image import Image
import numpy as np
import json

orb_handler = ORB()

orb_handler.set_image(Image().load_image("/home/bucky/Documents/Py/final/orb_zoom_face_matching/assets/datasource/Muhammad_Iqbal_Baqi/result/face_8.png"))


print (orb_handler.get_keypoint_descriptor())

print()