import os
import cv2
import statistics
from CameraController import CameraController

cameraController = CameraController()

# Tool: Get Median Color
# Description: Given a folder of pictures of a cat, get the median BGR of the cat
#              Copy this value over to the Config file's CAT_EXPECTED_COLORS 
#               variable to use when determining which cat is which
directory = './CatPics/bento'

blue = []
green = []
red = []

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        img = cv2.imread(file_path)
        _, objectInfo = cameraController.detectCat(img)
        if len(objectInfo) > 0:
            for cat in objectInfo:
                avg_color = cameraController.getAverageColor(img, cat[0])
                blue.append(avg_color[0])
                green.append(avg_color[1])
                red.append(avg_color[2])

            print(f'{file_path} - {avg_color}')


finalMedians = ( statistics.median(blue), statistics.median(green), statistics.median(red)  )

print(f'FINAL MEDIAN: {finalMedians}')