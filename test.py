import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt
import time

start_time = time.time()

FIXED_SIZE = 256

def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # Grab the image size and initialize dimensions
    dim = None
    (h, w) = image.shape[:2]

    # Return original image if no need to resize
    if width is None and height is None:
        return image

    # We are resizing height if width is none
    if width is None:
        # Calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # We are resizing width if height is none
    else:
        # Calculate the ratio of the width and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # Return the resized image
    return cv2.resize(image, dim, interpolation=inter)

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


image = cv2.imread('assets/naya.jpg')

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
# result = image

show_image(result, 0)
sys.exit("--- %s seconds ---" % (time.time() - start_time))
