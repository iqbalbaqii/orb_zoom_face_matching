
# Import module
from tkinter import *
 
# Create object
root = Tk()
 
# Adjust sizeimport tkinter as tk
root = tk.Tk()

def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))

root.bind('<Motion>', motion)
root.mainloop() 
root.geometry()
 
# Create transparent window
# root.overrideredirect(True)
root.wait_visibility(root)
root.wm_attributes("-alpha", 0.7)
root.attributes('-fullscreen',True)
# Execute tkinter
root.mainloop()