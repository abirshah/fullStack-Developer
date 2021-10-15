#!/usr/bin/env python
# coding: utf-8

import cv2
import matplotlib.pyplot as plt
import numpy as np

#network to coco weight file and cfg file
net = cv2.dnn.readNetFromDarknet('yolov4.cfg','yolov4.weights')
#reading the classes.names file
classes = []
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]
print(classes)

#Reading the image you are testing
my_img = cv2.imread('../Dataset.jpg')
#Resizing the image
my_img = cv2.resize(my_img,(800,600))

plt.imshow(my_img)
#getting the height and width
ht, wt , _ = my_img.shape 
blob = cv2.dnn.blobFromImage(my_img, 1/255,(416,416),(0,0,0),swapRB = True,crop= False)
blob.shape
net.setInput(blob)
last_layer = net.getUnconnectedOutLayersNames()
layer_out = net.forward(last_layer)

#Getting the bonding boxes, confidence for each box, and class ids
boxes =[]
confidences = []
class_ids = []

for output in layer_out:
    for detection in output:
        score = detection[5:]
        #retrieve the class id
        class_id = np.argmax(score)
        #retrieve the confidence
        confidence = score[class_id]
        #check whether the confidence is above 60 percent
        if confidence > 0.6:
            center_x = int(detection[0] * wt)
            center_y = int(detection[1] * ht)
            w = int(detection[2] * wt)
            h = int(detection[3]* ht)
            x = int(center_x - w/2)
            y = int(center_y - h/2)
            #append the coordinates of the bounding box
            boxes.append([x,y,w,h])
            confidences.append((float(confidence)))
            class_ids.append(class_id)

#indexes will be empty if there is no objext detected in the image
indexes = cv2.dnn.NMSBoxes(boxes,confidences,.5,.4)

font = cv2.FONT_HERSHEY_PLAIN
#generate different colors foreach bounding box
colors = np.random.uniform(0,255,size =(len(boxes),3))
if  len(indexes)>0:
    for i in indexes.flatten():
        x,y,w,h = boxes[i]
        #Retrieving the class name
        label = str(classes[class_ids[i]])
        confidence = str(round(confidences[i],2))
        color = colors[i]
        #using OpenCV to write on the image.
        cv2.rectangle(my_img,(x,y),(x+w,y+h),color,2)
        cv2.putText(my_img,label + " " + confidence, (x,y+20),font,2,(0,0,0),2)
else:
    print("No object detected")

#Displaying the image
cv2.imshow('img',my_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

