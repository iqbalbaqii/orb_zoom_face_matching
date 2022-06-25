from src import CaptureScreen
from src import Image
from src import Face
import pyautogui
import time

ss = CaptureScreen.Region()
ss.run()
region_x, region_y, region_width, region_height = ss.get_region()
time.sleep(.3)
myScreenshot = pyautogui.screenshot(region=(region_x, region_y, region_width, region_height))

screenshot = Image.define_image_from_ss(myScreenshot)
face_region = Face.segment_face(screenshot)
Image.show_image(face_region)






