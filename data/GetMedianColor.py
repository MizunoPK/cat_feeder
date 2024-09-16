import os
import cv2
import statistics

import sys
module_dir = os.path.abspath('.')
print(module_dir)
sys.path.insert(0, module_dir)
from CameraController import CameraController

print("Loading...")

cameraController = CameraController()

# Tool: Get Median Color
# Description: Given a folder of pictures of a cat, get the median BGR of the cat
#              Copy this value over to the Config file's CAT_EXPECTED_COLORS 
#               variable to use when determining which cat is which
directories = ['./data/CatPics/nori', './data/CatPics/bento']
final_bgr_medians = []
final_gray_medians = []

for directory in directories:
    blue = []
    green = []
    red = []
    gray = []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            img = cv2.imread(file_path)
            img, objectInfo = cameraController.detectCat(img)
            
            if len(objectInfo) > 0:
                for cat in objectInfo:
                    (avg_bgr, avg_gray) = cameraController.getAverageColor(img, cat[0])
                    blue.append(avg_bgr[0])
                    green.append(avg_bgr[1])
                    red.append(avg_bgr[2])
                    gray.append(avg_gray)

                print(f'{file_path} - {avg_bgr} - {avg_gray}')


    bgr_medians = ( statistics.median(blue), statistics.median(green), statistics.median(red)  )
    gray_median = statistics.median(gray)

    final_bgr_medians.append(bgr_medians)
    final_gray_medians.append(gray_median)

for i in range(len(final_bgr_medians)):
    print("")
    print(f'{directories[i]} - FINAL BGR MEDIAN: {final_bgr_medians[i]}')
    print(f'{directories[i]} - FINAL GRAY MEDIAN: {final_gray_medians[i]}')