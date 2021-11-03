import unittest
import sys

class OpenCvTest(unittest.TestCase):

    def test_import(self):
        import cv2
        import matplotlib.pyplot
        import numpy

    def test_image_capture(self):
        import cv2
        import matplotlib.pyplot as plt
        my_img = cv2.imread('test_images/Dataset.jpg')
        self.assertTrue(plt.imshow(my_img))

    def test_image_shape(self):
        import cv2
        my_img = cv2.imread('test_images/Dataset.jpg')
        my_img = cv2.resize(my_img, (800, 600))
        self.assertTrue(my_img.shape)

    def test_blob_shape(self):
        import cv2
        my_img = cv2.imread('test_images/Dataset.jpg')
        my_img = cv2.resize(my_img, (800, 600))
        blob = cv2.dnn.blobFromImage(my_img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
        self.assertTrue(blob.shape)

    def test_network(self):
        import cv2
        net = cv2.dnn.readNetFromDarknet('cfg_files/yolov4.cfg', 'weight_files/yolov4.weights')
        self.assertTrue(net)

    def test_foward_pass(self):
        import cv2
        net = cv2.dnn.readNetFromDarknet('cfg_files/yolov4.cfg', 'weight_files/yolov4.weights')
        self.assertTrue(net.getUnconnectedOutLayersNames())

    def test_text_font(self):
        import cv2
        self.assertTrue(cv2.FONT_HERSHEY_PLAIN)





