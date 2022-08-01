from src.bll.CaptureScreen import CaptureScreen
from src.bll.Image import Image
from src.bll.Alert import Alert
# from src.bll.ORB import ORB
import pyautogui
import time
import cv2


class Main:
    # ss = CaptureScreen()
    # ss.run()
    # region_x, region_y, region_width, region_height = ss.get_region()
    # time.sleep(.3)

    # print(ss.get_region())

    if __name__ == "__main__":
        image_handler = Image()
        toast = Alert()
        region = {
            'x': 1100,
            'y': 0,
            'width': 256,
            'height': 256
        }

        myScreenshot = pyautogui.screenshot(
            region=(region['x'], region['y'], region['width'], region['height']))

        image_handler.define_image_from_ss(myScreenshot)

        frontal_face = image_handler.segment_face()

        if(frontal_face is False):
            toast.send('Hai Luhut', 'Mukakmu Offside')
        else:
            toast.send('Identifikasi selesai', 'Luhut Binsar Panjaitan Hadir')
