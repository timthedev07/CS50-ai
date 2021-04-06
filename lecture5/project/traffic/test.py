import sys
import os
import cv2
import numpy as np

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4

def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")
    load_data("gtsrb/")
    print("loading")

def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []
    category_dirs = [os.path.join(data_dir, str(i)) for i in range(NUM_CATEGORIES - 1)]
    for category in sorted(category_dirs):
        for ppmFile in os.listdir(category):
            image = cv2.imread(os.path.join(category, ppmFile))
            image.resize(IMG_WIDTH, IMG_HEIGHT, 3)
            images.append(image)
            if len(category) == 7:
                labels.append(int(category[-1:]))
            else:
                labels.append(int(category[-2:]))
    return tuple([images, labels])
if __name__ == "__main__":
    main()