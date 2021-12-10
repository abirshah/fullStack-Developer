import os.path

import cv2
import numpy as np
from pet_detection import petDetection
import math
import sys
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.cluster import MiniBatchKMeans

# the main method
def main():
    pd = petDetection()
    my_img = cv2.imread('test_images/dog.jpg')
    my_img2 = my_img.reshape((-1, 3))

    my_img2 = np.float32(my_img2)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    #CLusters
    k = 10
    attempts = 10
    ret, label, center = cv2.kmeans(my_img2, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((my_img.shape))
    cv2.imwrite('segmented2.jpg', res2)


if __name__ == "__main__":
    main()
