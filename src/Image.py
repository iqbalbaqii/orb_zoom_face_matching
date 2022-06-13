import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class Image:

    def __init__(self):
        self.image = None

    def set_image(self, image):
        self.image = mpimg.imread(image)

    def show_image(self):
        imgplot = plt.imshow(self.image)
        plt.show()
        
