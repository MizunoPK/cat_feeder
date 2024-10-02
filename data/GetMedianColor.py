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

# (y=gray)
# Format from 1 Dir: [(bgry avg), (bgry med), (bgry max), (bgry min)]
final_data = []

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
                    avgColors = cameraController.getAverageColor(img, cat[0])
                    blue.append(avgColors[0])
                    green.append(avgColors[1])
                    red.append(avgColors[2])
                    gray.append(avgColors[3])

                print(f'{file_path} - {avgColors}')

                cv2.imshow("img", img)
                cv2.waitKey(0)


    bgry_avg = ( statistics.mean(blue), statistics.mean(green), statistics.mean(red), statistics.mean(gray) )
    bgry_medians = ( statistics.median(blue), statistics.median(green), statistics.median(red), statistics.median(gray) )
    bgry_max = ( max(blue), max(green), max(red), max(gray) )
    bgry_min = ( min(blue), min(green), min(red), min(gray) )

    final_data.append([bgry_avg, bgry_medians, bgry_max, bgry_min])

for i in range(len(final_data)):
    print("")
    print(f'{directories[i]} - FINAL BGRY MEAN: {final_data[i][0]}')
    print(f'{directories[i]} - FINAL BGRY MEDIAN: {final_data[i][1]}')
    print(f'{directories[i]} - FINAL BGRY MAX: {final_data[i][2]}')
    print(f'{directories[i]} - FINAL BGRY MIN: {final_data[i][3]}')