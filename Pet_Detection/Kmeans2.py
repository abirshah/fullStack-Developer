import os
import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans

def main():
    images = [] # x_train
    labels = [] # y_train
    y_test = np.array([1])
    for i in os.listdir('user_pet_images/train'):
        image = cv2.imread('user_pet_images/train' + i)
        #image = cv2.resize(image, (800, 600))
        labels.append(1)
        images.append(image)

    images1 = np.array(images)
    labels = np.array(labels)
    print(images1.shape)


    #images = np.float32(images)
    images1 = images1.astype('float32')
    images1 = images1 / 255.0

    Images = images1.reshape(len(images1), -1)
    print(Images.shape)

    total_clusters = len(np.unique(y_test))
    # Initialize the K-Means model
    kmeans = MiniBatchKMeans(n_clusters=total_clusters)
    # Fitting the model to training set
    kmeans.fit(Images)
    kmeans.labels_
    reference_labels = retrieve_info(kmeans.labels_, labels)
    print(reference_labels)

def retrieve_info(cluster_labels,y_train):
    # Initializing
    reference_labels = {}
    # For loop to run through each label of cluster label
    for i in range(len(np.unique(cluster_labels))):
        index = np.where(cluster_labels == i,1,0)
        num = np.bincount(y_train[index==1]).argmax()
        reference_labels[i] = num
    return reference_labels

if __name__ == "__main__":
    main()