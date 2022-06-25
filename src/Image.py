import cv2
import numpy as np

  

def define_image_from_ss(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    

def show_image(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
        
