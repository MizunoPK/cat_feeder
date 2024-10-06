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
TRAINING_PROPORTION = 0.7
STARTING_WHITE = 70
ENDING_WHITE = 200
INCREMENT = 5


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

whiteVals = {}

for whiteVal in range(STARTING_WHITE, ENDING_WHITE, INCREMENT):

    # Format from 1 Dir: [(bgr avg), (bgr med), (bgr max), (bgr min)]
    final_data = []

    print(f"WHITE={whiteVal} TRAINING...")

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


        bgr_avg = [ statistics.mean(blue), statistics.mean(green), statistics.mean(red) ]
        bgr_medians = [ statistics.median(blue), statistics.median(green), statistics.median(red) ]
        bgr_max = [ max(blue), max(green), max(red) ]
        bgr_min = [ min(blue), min(green), min(red) ]

        final_data.append([bgr_avg, bgr_medians, bgr_max, bgr_min])

    for i in range(len(final_data)):
        print(f'{directories[i]} - FINAL BGRY MEAN: {final_data[i][0]}')
        print(f'{directories[i]} - FINAL BGRY MEDIAN: {final_data[i][1]}')
        print(f'{directories[i]} - FINAL BGRY MAX: {final_data[i][2]}')
        print(f'{directories[i]} - FINAL BGRY MIN: {final_data[i][3]}')
    whiteVals[whiteVal] = [final_data]



    # TESTING
    print(f"WHITE={whiteVal} TESTING CLASSIFIER...")

    meanColorSet = [final_data[0][0], final_data[1][0]]
    medianColorSet = [final_data[0][1], final_data[1][1]]
    colorSetNames = ["Mean", "Median"]
    colorSets = [meanColorSet, medianColorSet]
    accuracies = []

    for colorSetIdx, colorSet in enumerate(colorSets):
        dirAccuracies = []
        for dirIdx, directory in enumerate(directories):
            correctDetections = 0
            imgsProcessed = 0
            for filename in testingSets[dirIdx]:
                avgColors = getColors(directory, filename, whiteVal)
                if avgColors is None:
                    continue

                catDetected = cameraController.getWhichCat(avgColors, colorSet)
                if catDetected == dirIdx:
                    correctDetections += 1
                imgsProcessed += 1
            
            accuracy = round((float(correctDetections) / float(imgsProcessed)) * 100, 2)
            dirAccuracies.append(accuracy)
            print(f"{colorSetNames[colorSetIdx]} - {directory} - Accuracy: {accuracy}%")
        accuracies.append(dirAccuracies)

    # save to the white vals dict
    whiteVals[whiteVal].append(accuracies)

# Find the white with the highest accuracies
bestWhite = 0
bestMeasure = 0
accuracyVal = 0
for whiteVal in whiteVals:
    accuracies = whiteVals[whiteVal][1]
    for measureIdx, measureAccuracies in enumerate(accuracies):
        newAccuracyVal = sum(measureAccuracies)
        if newAccuracyVal > accuracyVal:
            bestWhite = whiteVal
            bestMeasure = measureIdx
            accuracyVal = newAccuracyVal

# Print the info
print("BEST VALUES:")
print("White:", bestWhite)
for dirIdx, dir in enumerate(directories):
    bestVals = whiteVals[bestWhite][0][dirIdx][bestMeasure]
    accuracy = whiteVals[bestWhite][1][bestMeasure][dirIdx]
    print(f"{dir} - {bestVals} - Accuracy={accuracy}%")
