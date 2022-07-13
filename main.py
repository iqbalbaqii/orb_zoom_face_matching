from src.bll import CaptureScreen
from src.bll import Image
from src.bll import Face
import pyautogui
import time

ss = CaptureScreen.Region()
ss.run()
region_x, region_y, region_width, region_height = ss.get_region()
time.sleep(.3)
myScreenshot = pyautogui.screenshot(region=(region_x, region_y, region_width, region_height))

screenshot = Image.define_image_from_ss(myScreenshot)
face_region = Face.segment_face(screenshot)









