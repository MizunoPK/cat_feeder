import os
import cv2
import statistics
import random

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
TRAINING_PROPORTION = 0.2
STARTING_WHITE = 180
ENDING_WHITE = 200
WHITE_INCREMENT = 2

COLOR_RANGE = 5 # How far above and below the avg color to test


def getColors(dir, file, whiteVal):
    file_path = os.path.join(dir, file)
    if os.path.isfile(file_path):
        img = cv2.imread(file_path)
        img, objectInfo = cameraController.detectCat(img)
        
        if len(objectInfo) == 1:
            return cameraController.getAverageColor(img, objectInfo[0][0], whiteVal)
    return None


# Split up the images in each dir into a training and test set
trainingSets = []
testingSets = []
for dir in directories:
    dirList = os.listdir(dir)
    random.shuffle(dirList)
    splitIdx = int(TRAINING_PROPORTION * len(dirList))
    
    trainingList = dirList[:splitIdx]
    testingList = dirList[splitIdx:]

    trainingSets.append(trainingList)
    testingSets.append(testingList)

bestWhite = 0
bestBgr = None
bestAccuracies = [0,0]

# Loop through the White values, getting data for each
for whiteVal in range(STARTING_WHITE, ENDING_WHITE, WHITE_INCREMENT):

    # Format from 1 Dir: [(bgr avg), (bgr med), (bgr max), (bgr min)]
    median_data = []

    print(f"WHITE={whiteVal} TRAINING...")

    # Get Color data for each dir
    for dirIdx, directory in enumerate(directories):
        blue = []
        green = []
        red = []

        for filename in trainingSets[dirIdx]:
            avgColors = getColors(directory, filename, whiteVal)
            if avgColors is not None:
                blue.append(avgColors[0])
                green.append(avgColors[1])
                red.append(avgColors[2])

                # print(f'{directory} - {filename} - {avgColors}')

        bgr_medians = [ statistics.median(blue), statistics.median(green), statistics.median(red) ]

        median_data.append(bgr_medians)

    for i in range(len(median_data)):
        print(f'{directories[i]} - BGRY MEDIAN: {median_data[i]}')

    # TESTING
    print(f"WHITE={whiteVal} TESTING CLASSIFIER...")
    colorStorage = {}
    def getFromStorage(dir, file):
        if dir in colorStorage and file in colorStorage[dir]:
            return colorStorage[dir][file]
        return None
    def addToStorage(dir, file, color):
        if dir in colorStorage:
            colorStorage[dir][file] = color
        else:
            colorStorage[dir] = {file : color}

    # Loop through the range of colors to see what combination works best
    for i in range(-1*COLOR_RANGE, COLOR_RANGE+1):
        for j in range(-1*COLOR_RANGE, COLOR_RANGE+1):
            test_data = [[x + i for x in median_data[0]], [y + j for y in median_data[1]]]
            dirAccuracies = []
            # Check each dir
            for dirIdx, directory in enumerate(directories):
                correctDetections = 0
                imgsProcessed = 0
                # Check each file
                for filename in testingSets[dirIdx]:
                    # The the color of the img
                    avgColors = getFromStorage(dirIdx, filename)
                    if avgColors is None:
                        avgColors = getColors(directory, filename, whiteVal)
                        addToStorage(dirIdx, filename, avgColors)
                    if avgColors is None:
                        continue

                    # See which cat it thinks it is
                    catDetected = cameraController.getWhichCat(avgColors, test_data)
                    if catDetected == dirIdx:
                        correctDetections += 1
                    imgsProcessed += 1
                
                accuracy = round((float(correctDetections) / float(imgsProcessed)) * 100, 2)
                dirAccuracies.append(accuracy)

            print(f"White={whiteVal} - Accuracies={dirAccuracies} - BGRs={test_data}")
            # Determine if this set of colors has the better accuracies
            if sum(dirAccuracies) > sum(bestAccuracies):
                bestWhite = whiteVal
                bestBgr = test_data
                bestAccuracies = dirAccuracies


# Print the info
print("BEST VALUES:")
print("White:", bestWhite)
for dirIdx, dir in enumerate(directories):
    print(f"{dir} - {bestBgr[dirIdx]} - Accuracy={bestAccuracies[dirIdx]}%")
