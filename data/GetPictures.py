import os
import cv2
import datetime
import time

import sys
module_dir = os.path.abspath('.')
print(module_dir)
sys.path.insert(0, module_dir)
from CameraController import CameraController


img_folder = "C:/code/cat_feeder/data/CatPics/unsorted"
cameraController = CameraController()

while True:
    # Get an image and see if a cat is there
    img = cameraController.getImageFromCamera()
    if img is None:
        continue
    _, objectInfo = cameraController.detectCat(img)
    cv2.imshow("output", img)
    cv2.waitKey(1)

    # Save the image if a cat was there
    print(objectInfo)
    if len(objectInfo) == 1:
        current_time = datetime.datetime.now()
        file_safe_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        cv2.imwrite(f'{img_folder}/{file_safe_time}.jpg', img)

        # Wait a bit before continuing
        time.sleep(3)