import cv2

import time


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    #cap.set(3,640)
    #cap.set(4,480)
    #cap.set(10,70)
    
    
    while True:
        success, img = cap.read()
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
        
        cv2.imshow("Output",img)
        cv2.waitKey(1)
    
