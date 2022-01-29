import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import scipy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image

checkpoint_path = 'TensorWeight/cp.ckpt'
model = tf.keras.models.Sequential([ tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape = (416,416,3)),
                                     tf.keras.layers.MaxPool2D(2, 2),
                                     #
                                     tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
                                     tf.keras.layers.MaxPool2D(2, 2),
                                     #
                                     tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                                     tf.keras.layers.MaxPool2D(2, 2),
                                     #
                                     tf.keras.layers.Flatten(),
                                     ##
                                     tf.keras.layers.Dense(512, activation='relu'),
                                     ##
                                     tf.keras.layers.Dense(1, activation='sigmoid')
                                     ])

model.load_weights(checkpoint_path)
dir_path = 'pet_images/test'
for i in os.listdir(dir_path):
    img = image.load_img(dir_path + '//' + i, target_size=(416,416))
    plt.imshow(img)
    plt.show()

    X = image.img_to_array(img)
    X = np.expand_dims(X, axis=0)
    images = np.vstack([X])

    print(model.predict(images))