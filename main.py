from src import CaptureScreen
from src import Image
import pyautogui
import time

ss = CaptureScreen.Region()
ss.run();

region_x, region_y, region_width, region_height = ss.get_region()
time.sleep(.3)
myScreenshot = pyautogui.screenshot(region=(region_x, region_y, region_width, region_height))
myScreenshot.save(r'z.png')

