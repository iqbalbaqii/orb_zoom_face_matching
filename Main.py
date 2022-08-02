from src.bll.Image import Image as ImageHandler
from src.bll.Alert import Alert
import pyautogui
import time
import random
from tkinter import *


class Main:

    def __init__(self):
        # STATIC VARIABLE
        self.WIDTH = 512
        self.HEIGHT = 512
        self.APP_WIDTH = 400
        self.APP_HEIGHT = 120

        # color
        self.primary = "#1F3BB3"
        self.secondary = "#F1F1F1"
        self.success = "#4aef69"
        self.danger = "#F95F53"
        self.warning = "#ffaf00"
        self.info = "#52CDFF"
        self.light = "#fbfbfb"
        self.dark = "#1F283E"

        # END STATIC VARIABLE

        # INSTANCE
        self.toast = Alert()
        self.image_handler = ImageHandler()

        # END INSTANCE
        self.x = 0
        self.y = 0
        self.width = 512
        self.height = 512
        self.log = ""

        self.master = None
        self.grey_dragging_frame = None
        self.capture_window = None


# WINDOWS

    def main_window(self):
        self.master = Tk()
        self.master.title("Zoom ORB Face Identification")
        self.master.geometry(
            "{}x{}+{}+{}".format(self.APP_WIDTH, self.APP_HEIGHT, 930, 550))
        # MENU BAR
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # EDIT MENU
        edit_menu = Menu(menu)
        menu.add_cascade(label="Edit", menu=edit_menu)

        edit_menu.add_command(label="Atur Tangkapan Layar",
                              command=self.capture_area_window)
        edit_menu.add_separator()
        edit_menu.add_command(label="Analisis Kehadiran")
        edit_menu.add_separator()
        edit_menu.add_command(label="Keluar", command=self.master.quit)

        # OPTION MENU

        option_menu = Menu(menu)
        menu.add_cascade(label="Option", menu=option_menu)

        option_menu.add_command(label="Analisis Kehadiran")
        option_menu.add_separator()
        option_menu.add_command(
            label="Informasi Area Tangkapan Layar", command=self.region_information)
        # END MENU BAR

        # FRAME

        frame_1 = Frame(self.master, bg=self.light,
                        width=self.APP_WIDTH, height=self.APP_HEIGHT * 1 / 3)
        frame_1.pack(side=TOP, fill=BOTH, expand=0)

        execute_identification_button = Button(
            frame_1, text="Presensi Kehadiran", command=self.identification_task, bg=self.primary, fg=self.light, border=0)
        execute_identification_button.pack(pady=10, expand=1)

        frame_2 = Frame(self.master, bg=self.dark,
                        width=self.APP_WIDTH, height=self.APP_HEIGHT * 2 / 3)
        frame_2.pack(side=BOTTOM, fill=BOTH, expand=1)
        title = Label(frame_2, text="--- activity ---",
                      bg=self.dark, fg=self.light, font="Arial 10 bold")
        title.pack(pady=1, padx=4, side=TOP, anchor=NW)

        frame_3 = Frame(frame_2, bg=self.dark)
        frame_3.pack(fill=BOTH, expand=0)

        scrollbar = Scrollbar(frame_3, orient='vertical', bg=self.dark)
        scrollbar.pack(side=RIGHT, fill='y')

        self.log = Text(frame_3, font=("Arial, 9"), yscrollcommand=scrollbar.set,
                        bg=self.dark, fg=self.light, highlightthickness=0, border=0, spacing1=3)
        self.log.tag_config('success', background=self.dark,
                            foreground=self.success)
        self.log.tag_config('danger', background=self.dark,
                            foreground=self.danger)
        self.log.tag_config('warning', background=self.dark,
                            foreground=self.warning)
        self.log.tag_config('light', background=self.dark,
                            foreground=self.light)
        # Attach the scrollbar with the text widget
        scrollbar.config(command=self.log.yview)

        self.log.pack(padx=3)

    def capture_area_window(self):
        self.grey_dragging_frame = Toplevel(self.master)

        self.grey_dragging_frame.wait_visibility(self.grey_dragging_frame)
        self.grey_dragging_frame.wm_attributes("-alpha", 0.5)
        self.grey_dragging_frame.attributes('-fullscreen', True)
        # Execute tkinter

        self.grey_dragging_frame.bind('<Button 1>', self.presssed)
        self.grey_dragging_frame.bind('<ButtonRelease-1>', self.released)

    def capture_area_message_window(self):
        self.capture_window = Toplevel(self.master, bg=self.light)
        self.capture_window.geometry("{}x{}+{}+{}".format(220, 100, 500, 200))

        self.capture_window.title("Pengaturan Area Tangkapan Layar")
        label = Label(self.capture_window, text="Save The Area ?",
                      bg=self.light, fg=self.dark, padx=100)
        label.pack(padx=10)

        saving_button = Button(
            self.capture_window, text="Simpan", command=self.saving_area_information, width=10, bg=self.primary, fg=self.light)
        saving_button.pack()

        close_button = Button(
            self.capture_window, text="Ulangi", command=self.capture_area_closing, width=10, bg=self.danger, fg=self.light)
        close_button.pack()

# END OF WINDOWS


# EVENT LISTENERS


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
        self.grey_dragging_frame.destroy()
        self.capture_area_message_window()

    def capture_area_closing(self):
        self.capture_window.destroy()
        self.capture_area_window()

    def greet(self):
        print("Greetings!")

    def saving_area_information(self):

        if(self.width < self.WIDTH or self.height < self.HEIGHT):
            self.log.insert(END, "Kesalahan area, ", 'danger')
            self.log.insert(
                END, "ukuran minimal area tangkapan layar 512 x 512\n", 'light')
            self.log.see(END)
        else:
            self.capture_window.destroy()

    def region_information(self):

        print("""
        point x = {}
        point y = {}
        width   = {}
        height  = {}
        """.format(self.x, self.y, self.width, self.height))

    def identification_task(self):
        if(self.x == -1):
            self.log.insert(END, "Kesalahan identifikasi, ", 'danger')
            self.log.insert(
                END, "area tangkapan layar belum didefinisi\n", 'light')
            self.log.see(END)
            return
        
        self.image_handler.capture_image(self.x, self.y, self.width, self.height)
        self.image_handler.save_image('test.png', self.image_handler.get_image)
        name = ['Muhammad Iqbal Baqi', 'Tiara Oktavian',
                'Luhut Binsar Panjaitan', 'Joko Widodo']

        ran = random.randint(0, 2)
        self.log.insert(END, "Identifikasi Selesai, ", 'success')
        self.log.insert(END, """"{}" hadir\n""".format(name[ran]), 'light')
        self.log.see(END)

        self.toast.send('Identifikasi Selesai', "{} hadir".format(name[ran]))
# END EVENT LISTENERS

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
