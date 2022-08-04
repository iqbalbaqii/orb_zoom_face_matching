from src.bll.Image import Image as ImageHandler
from src.bll.Data import Data as DataHandler
from src.bll.ORB import ORB as OrbHandler
from src.model.DatasetImage import DatasetImage
from src.model.DatasetLabel import DatasetLabel


class IdentificationController:
    def __init__(self):

        #STATIC VARIABLE
        self.APP_PATH = "/home/bucky/Documents/Py/final/orb_zoom_face_matching/{}"
        #END STATIC VARIABLE
        
        self.image_handler = ImageHandler()
        self.orb_handler = OrbHandler()
        self.DataImage = DatasetImage()
        self.DataLabel = DatasetLabel()

    def identification_task(self, region):
        x, y, width, height = region
        self.image_handler.capture_image(
            x, y, width, height)
        frontal_face = self.image_handler.segment_face()
        if frontal_face is False:
            return frontal_face

        self.orb_handler.set_image(frontal_face)
        

        self.do_the_comparation(self.orb_handler.get_keypoint_descriptor())

        # self.image_handler.save_image(self.APP_PATH.format(
        #     "assets/result/face.png"), frontal_face)


    def do_the_comparation(self, test_face):
        test_keypoint, test_descriptor = test_face

        #Load Image In That Class
        #Information about the class will be skiped

        labels = self.DataLabel.get("label, nama, ", "kelas = '{}'".format('group_0'))
        
        print(labels)
        