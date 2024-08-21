import cv2
import numpy as np

DETECTION_THRESHOLD = 0.6  #threshold to detect an object
COLOR_THRESHOLD = 40  # threshold to say this is nori vs bento - scale of 0-255 where 0 is closer to black
SHOW_VIDEO = True # Whether or not to show the images as they are read

classNames = []
classFile = "./Object_Detection_Files/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "./Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "./Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (SHOW_VIDEO):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    return img,objectInfo


def getWhichCat(img, catBox):
    # Get the box info of what we want to scan
    width = int(catBox[2] / 2)
    height = int(catBox[3] / 2)
    x = int(catBox[0] + (width / 2))
    y = int(catBox[1] + (width / 2))

    # Get the average color
    roi = img[y:y + height, x:x + width]
    average_color = cv2.mean(roi) 
    average_color_bgr = average_color[:3]
    average_color_image = np.array([[average_color_bgr]], dtype=np.uint8)
    gray_image = cv2.cvtColor(average_color_image, cv2.COLOR_BGR2GRAY)
    gray_value_cv = gray_image[0, 0]

    # Draw the box on the image
    if ( SHOW_VIDEO ):
        top_left = (x, y)
        bottom_right = (x + width, y + height)
        cv2.rectangle(img, top_left, bottom_right, color=(0,0,255), thickness=2)

    print(gray_value_cv)
    if gray_value_cv <= COLOR_THRESHOLD:
        return "bento"
    else: 
        return "nori"



if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)


    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img, DETECTION_THRESHOLD, 0.2, objects=['cat'])
        
        for cat in objectInfo:
            print(getWhichCat(img, cat[0]))

        if SHOW_VIDEO:
            cv2.imshow("Output",img)
        cv2.waitKey(1)
