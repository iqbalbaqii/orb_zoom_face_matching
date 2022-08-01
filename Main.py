from src.bll.CaptureScreen import CaptureScreen
from src.bll.Image import Image
from src.bll.Alert import Alert
import pyautogui
import time
from tkinter import Tk, Label, Button, Toplevel


class Main:

    def __init__(self):
        self.region = None
        self.master = Tk()
        self.master.title("A simple GUI")

    def main_window(self):
        label = Label(self.master, text="This is our first GUI!")
        label.pack()

        open_capture_area_window = Button(
            self.master, text="Open Window", command=self.capture_area_window)
        open_capture_area_window.pack(pady=10)
        
        close_button = Button(
            self.master, text="Close", command=self.master.quit)
        close_button.pack()

    def capture_area_window(self):

        def on_closing():
            print('this show after capture windows dissapeare')
        
        window = Toplevel(self.master)

        # sets the title of the
        # Toplevel widget
        window.title("Area Tangkapan Wajah")

        # sets the geometry of toplevel
        window.geometry("200x200")

        # A Label widget to show in toplevel
        Label(window,
              text="This is a new window").pack()

        btn = Button(window, text="button save", command=self.saving)
        btn.pack()

        window.protocol("WM_DELETE_WINDOW", on_closing)

        


    

    def saving(self):
        print("Saving Region")

    def greet(self):
        print("Greetings!")

    def run(self):
        self.master.mainloop()


app = Main()
app.main_window()
app.run()

# image_handler = Image()
# toast = Alert()
# region = {
#     'x': 1100,
#     'y': 0,
#     'width': 256,
#     'height': 256
# }

# myScreenshot = pyautogui.screenshot(
#     region=(region['x'], region['y'], region['width'], region['height']))

# image_handler.define_image_from_ss(myScreenshot)

# frontal_face = image_handler.segment_face()

# if(frontal_face is False):
#     toast.send('Hai Luhut', 'Mukakmu Offside')
# else:
#     toast.send('Identifikasi selesai', 'Luhut Binsar Panjaitan Hadir')
