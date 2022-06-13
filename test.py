import cv2
import numpy as np
from matplotlib import pyplot as plt


# == Processing =======================================================================

# -- Read image -----------------------------------------------------------------------


def show_image(img, time):
    time = time * 1000
    height, width = img.shape[:2]
    max_height = 600
    max_width = 600

    # only shrink if img is bigger than required
    if max_height < height or max_width < width:
        # get scaling factor
        scaling_factor = max_height / float(height)
        if max_width/float(width) < scaling_factor:
            scaling_factor = max_width / float(width)
        # resize image
        img = cv2.resize(img, None, fx=scaling_factor,
                         fy=scaling_factor, interpolation=cv2.INTER_AREA)
    cv2.imshow("Shrinked image", img)
    key = cv2.waitKey(time)


image = cv2.imread('assets/we.png')

min_YCrCb = np.array([0, 133, 77], np.uint8)
max_YCrCb = np.array([235, 173, 127], np.uint8)

# Get pointer to video frames from primary device

imageYCrCb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
mask = cv2.inRange(imageYCrCb, min_YCrCb, max_YCrCb)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)
smooth_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
opening = cv2.morphologyEx(opening, cv2.MORPH_OPEN,
                           smooth_kernel, iterations=3)


result = cv2.bitwise_and(image, image, mask=opening)
height, width, _ = result.shape

x_max, y_max, x_min, y_min = -1, -1, 9999, 9999

for j in range(0, height):
    for i in range(0, width):
        blue, green, red = result[j, i]
        px = blue + green + red
        if px != 0:
            if(i < x_min):
                x_min = i
            
            if( i >= x_max):
                x_max = i

            if(j < y_min):
                y_min = j
            
            if(j >= y_max):
                y_max = j

for j in range(0, height):
    for i in range(0, width):
        if(i > x_min and i < x_max):
            print('')




show_image(result[y_min:y_max, x_min:x_max], 6)
