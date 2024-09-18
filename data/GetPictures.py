import os
import cv2
import datetime
import time
from skimage import io, transform
import numpy as np
import pickle

import sys
module_dir = os.path.abspath('.')
print(module_dir)
sys.path.insert(0, module_dir)
from CameraController import CameraController

from pathlib import Path

WAIT_TIME = 1 # seconds to wait between shots
PICS_TO_TAKE = 200

with open('./data/model.p', 'rb') as file:
    loaded_model = pickle.load(file)

nori_folder = "./data/CatPics/nori"
nori_pics_taken = 0
bento_folder = "./data/CatPics/bento"
bento_pics_taken = 0
both_folder = "./data/CatPics/both"
both_pics_taken = 0
none_folder = "./data/CatPics/none"
none_pics_taken = 0
Path(nori_folder).mkdir(parents=True, exist_ok=True)
Path(bento_folder).mkdir(parents=True, exist_ok=True)
Path(both_folder).mkdir(parents=True, exist_ok=True)
Path(none_folder).mkdir(parents=True, exist_ok=True)

cameraController = CameraController()

def writeImg(dir, img):
    current_time = datetime.datetime.now()
    file_safe_time = current_time.strftime("%Y-%m-%d_%H-%M-%S.jpg")
    file_path = os.path.join(dir, file_safe_time)
    print("Writing to", file_path)
    cv2.imwrite(file_path, img)

while True:
    if nori_pics_taken >= PICS_TO_TAKE and bento_pics_taken >= PICS_TO_TAKE and both_pics_taken >= PICS_TO_TAKE and none_pics_taken >= PICS_TO_TAKE:
        break

    # Get an image and see if a cat is there
    img = cameraController.getImageFromCamera()
    if img is None:
        continue
    _, objectInfo = cameraController.detectCat(img)

    # If no cat was there or 2 cats, resize and save
    if (len(objectInfo) == 0 and none_pics_taken < PICS_TO_TAKE):
        img = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
        writeImg(none_folder, img)
        none_pics_taken+=1
    elif (len(objectInfo) == 2 and both_pics_taken < PICS_TO_TAKE):
        img = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
        writeImg(both_folder, img)
        both_pics_taken+=1
    
    # if there was 1 cat there, id the cat then save
    elif len(objectInfo) == 1:
        old_resizing = cv2.resize(img, (0,0), fx=0.7, fy=0.7)
        image_resized =  transform.rescale(old_resizing, (.25/.7))
        image_flattened = image_resized.flatten()
        image_for_model = np.array([image_flattened])
        prediction = loaded_model.predict(image_for_model)
        if prediction[0] == 0 and nori_pics_taken < PICS_TO_TAKE:
            img = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
            writeImg(nori_folder, img)
            nori_pics_taken+=1
        if prediction[0] == 1 and bento_pics_taken < PICS_TO_TAKE:
            img = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
            writeImg(bento_folder, img)
            bento_pics_taken+=1
    
    time.sleep(WAIT_TIME)