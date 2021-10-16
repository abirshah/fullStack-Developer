import cv2
import numpy as np
import matplotlib.pyplot as plt

#network to custom weight file and cfg file
net = cv2.dnn.readNetFromDarknet("custom_files/yolov3_custom.cfg",r"custom_files\yolov3_custom_2000.weights")
#reading the classes.names file 
classes = []
with open('custom_files/classes.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]
print(classes)

#Opening the webcam
cap = cv2.VideoCapture(0)

while 1:
    _, img = cap.read()
    #Resizing the image
    img = cv2.resize(img,(1280,720))
    #getting the height and weight
    hight,width,_ = img.shape
    blob = cv2.dnn.blobFromImage(img, 1/255,(416,416),(0,0,0),swapRB = True,crop= False)

    net.setInput(blob)

    output_layers_name = net.getUnconnectedOutLayersNames()

    layerOutputs = net.forward(output_layers_name)

    #Getting the bonding boxes, confidence for each box, and class ids
    boxes =[]
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            score = detection[5:]
            #retrieve the class id
            class_id = np.argmax(score)
            #retrieve the confidence
            confidence = score[class_id]
            #check whether the confidence is above 70 percent
            if confidence > 0.7:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * hight)
                w = int(detection[2] * width)
                h = int(detection[3]* hight)
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                #append the coordinates of the bounding box
                boxes.append([x,y,w,h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)
    #indexes will be empty if there is no objext detected in the image
    indexes = cv2.dnn.NMSBoxes(boxes,confidences,.5,.4)

    boxes =[]
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            score = detection[5:]
            class_id = np.argmax(score)
            confidence = score[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * hight)
                w = int(detection[2] * width)
                h = int(detection[3]* hight)

                x = int(center_x - w/2)
                y = int(center_y - h/2)



                boxes.append([x,y,w,h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes,confidences,.8,.4)
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
            cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
            cv2.putText(img,label + " " + confidence, (x,y+400),font,2,color,2)


    #Displaying the image
    cv2.imshow('img',img)
    #Do not close the camera until q is pressed
    if cv2.waitKey(1) == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()