from src.bll import CaptureScreen
from src.bll import Image
from src.bll import Face
from src.bll import ORB
import pyautogui
import time
import cv2

# ss = CaptureScreen.Region()
# ss.run()
# region_x, region_y, region_width, region_height = ss.get_region()
# time.sleep(.3)
# myScreenshot = pyautogui.screenshot(
#     region=(region_x, region_y, region_width, region_height))

# screenshot = Image.define_image_from_ss(myScreenshot)
# face_region = Face.segment_face(screenshot)

# face_region = cv2.imread(
#     '/home/bucky/Documents/Py/final/orb_zoom_face_matching/assets/datasource/Gege_Ardiyansyah/result/label_1.png')

orb = ORB.ORB()

img = None
for i in range(1,3):
	face_region = cv2.imread(
	    '/home/bucky/Documents/Py/final/orb_zoom_face_matching/assets/datasource/Toni_Ismail/result/toni_ismail_'+str(i)+'.png')
	orb.setImage(face_region)
	img = orb.run()

Image.show_image(img)




