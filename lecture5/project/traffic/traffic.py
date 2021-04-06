import cv2
import numpy as np
import os
import sys
import tensorflow as tf
import math

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])
    print('\033[92m' +"Finish loading data"+'\033[0m')
    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)
    
    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


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
    # create lists for images and labels respectively
    images = []
    labels = []

    # get the list of strings of directories numbered 0 to 42
    category_dirs = [os.path.join(data_dir, str(i)) for i in range(NUM_CATEGORIES)]

    categoryNum = 0

    # iterate over the numbered directories
    for category in sorted(category_dirs):

        # iterate over the ppm files
        for ppmFile in os.listdir(category):

            # read ppm file
            image = cv2.imread(os.path.join(category, ppmFile))

            # resize it to the desired size.
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))

            # append the resized image formatted in a ndarray to the images list
            images.append(image)

            # append corresponding digits to the labels list
            labels.append(categoryNum)
            
        categoryNum += 1

    # return
    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    
    # initialize model
    model = tf.keras.models.Sequential([

        # convolutional layer with 32 filters using a 4 * 4 kernel
        tf.keras.layers.Conv2D(
            32, (4, 4), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # max pooling layer of 3 * 3
        tf.keras.layers.MaxPooling2D(pool_size=(3, 3)),

        # another convolutional layer with 32 filters using a 3 * 3 kernel
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # flattening
        tf.keras.layers.Flatten(),

        # Hidden layer with drop out 0.5
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.4),

        # Another hidden layer without drop out
        tf.keras.layers.Dense(128, activation="relu"),

        # output layer corresponding to all 42 categories
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    # compile model
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    main()
