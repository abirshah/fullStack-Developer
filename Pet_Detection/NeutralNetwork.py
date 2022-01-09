import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import scipy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import RMSprop


train = ImageDataGenerator(rescale=1/255)
validation = ImageDataGenerator(rescale=1/255)


train_dataset = train.flow_from_directory('pet_images/train/', target_size=(416, 416), batch_size=3,
                                          class_mode='binary')
validation_dataset = train.flow_from_directory('pet_images/validation/', target_size=(416, 416), batch_size=3,
                                          class_mode='binary')

#train_dataset.class_indices
#train_dataset.classes

checkpoint_path = 'TensorWeight/cp.ckpt'
checkpoint_dir = os.path.dirname(checkpoint_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                 save_weight_only=True,
                                                 verbose=1)
#
#
#
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

model.compile(loss='binary_crossentropy', optimizer=RMSprop(lr=0.001), metrics=['accuracy'])
model_fit = model.fit(train_dataset, steps_per_epoch=3, epochs=30, validation_data=validation_dataset, callbacks=[cp_callback])


dir_path = 'pet_images/test'
for i in os.listdir(dir_path):
    img = image.load_img(dir_path + '//' + i, target_size=(416,416))
    plt.imshow(img)
    plt.show()

    X = image.img_to_array(img)
    X = np.expand_dims(X, axis=0)
    images = np.vstack([X])

    print(model.predict(images))