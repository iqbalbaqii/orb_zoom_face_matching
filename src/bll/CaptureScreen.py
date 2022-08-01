import pyautogui
from tkinter import *
import time


class CaptureScreen:

    # Area tangkapan layar disini, return image tangkapan ? atau region aja

    def __init__(self):
        self.x = -1
        self.y = -1
        self.width = 0
        self.heiight = 0

    def presssed(self, event):
        self.x, self.y = event.x, event.y

    def released(self, event):

        self.width, self.height = abs(event.x - self.x), abs(event.y - self.y)

        if(event.x < self.x):
            self.x = event.x
        if(event.y < self.y):
            self.y = event.y
        if(self.x < 0):
            self.x = 0

        if(self.y < 0):
            self.y = 0

        self.window.destroy()

    def run(self):

        self.window = Tk()

        self.window.wait_visibility(self.window)
        self.window.wm_attributes("-alpha", 0.5)
        self.window.attributes('-fullscreen', True)
        # Execute tkinter

        self.window.bind('<Button 1>', self.presssed)
        self.window.bind('<ButtonRelease-1>', self.released)

        self.window.mainloop()

    def get_region(self):
        return self.x, self.y, self.width, self.height


# region = Region()
# region.run()
# region_x, region_y, region_width, region_height = region.get_region()
# print(region_x, region_y, region_width, region_height)
# time.sleep(.3)
# myScreenshot = pyautogui.screenshot(region=(region_x, region_y, region_width, region_height))
# myScreenshot.save(r'z.png')
