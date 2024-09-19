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

WAIT_TIME = 1 # seconds to wait between shots
UNSORTED_PICS_TO_TAKE = 0
SORTED_PICS_TO_TAKE = 200

unsorted_folder = "./data/CatPics/unsorted"
both_folder = "./data/CatPics/both"
none_folder = "./data/CatPics/none"
Path(unsorted_folder).mkdir(parents=True, exist_ok=True)
Path(both_folder).mkdir(parents=True, exist_ok=True)
Path(none_folder).mkdir(parents=True, exist_ok=True)

cameraController = CameraController()

def writeImg(dir, img):
    current_time = datetime.datetime.now()
    file_safe_time = current_time.strftime("%Y-%m-%d_%H-%M-%S.jpg")
    file_path = os.path.join(dir, file_safe_time)
    print("Writing to", file_path)
    cv2.imwrite(file_path, img)

def doneWithPics(dir):
    maxPics = UNSORTED_PICS_TO_TAKE if dir == unsorted_folder else SORTED_PICS_TO_TAKE
    return len(os.listdir(dir)) >= maxPics



while True:
    if doneWithPics(unsorted_folder) and doneWithPics(both_folder) and doneWithPics(none_folder):
        break

    # Get an image and see if a cat is there
    img = cameraController.getImageFromCamera()
    if img is None:
        continue
    _, objectInfo = cameraController.detectCat(img)

    # If no cat was there or 2 cats, resize and save
    if len(objectInfo) == 0 and not doneWithPics(none_folder):
        writeImg(none_folder, img)

    elif len(objectInfo) == 2 and not doneWithPics(both_folder):
        writeImg(both_folder, img)
    
    # if there was 1 cat there, throw into unsorted
    elif len(objectInfo) == 1 and not doneWithPics(unsorted_folder):
        writeImg(unsorted_folder, img)
    
    time.sleep(WAIT_TIME)