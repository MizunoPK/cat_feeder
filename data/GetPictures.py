import os
import cv2
import datetime
import time

import sys
module_dir = os.path.abspath('.')
print(module_dir)
sys.path.insert(0, module_dir)
from CameraController import CameraController

from pathlib import Path


NUM_CATS = 0 # number of cats to be in frame for a pic to be taken
WAIT_TIME = 3 # seconds to wait between shots
PICS_TO_TAKE = 5
picsTaken = 0


img_folder = "./data/CatPics/unsorted"
Path(img_folder).mkdir(parents=True, exist_ok=True)

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
    if len(objectInfo) == NUM_CATS:
        current_time = datetime.datetime.now()
        file_safe_time = current_time.strftime("%Y-%m-%d_%H-%M-%S.jpg")
        file_path = os.path.join(img_folder, file_safe_time)
        print("Writing to", file_path)
        cv2.imwrite(file_path, img)
        picsTaken+=1
        if picsTaken >= PICS_TO_TAKE:
            break

        # Wait a bit before continuing
        time.sleep(WAIT_TIME)