import cv2
import numpy as np
from Config import Config
from Logger import Logger
from LogType import LogType
from pathlib import Path
import os
import datetime
from dotenv import load_dotenv, dotenv_values
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Class: CameraController
# Description:
#       Controls the camera and sends signals when a cat has been detected
# Logs:
#   1: Cat Identified
#   2: Cat Detected
#   3: All tracking logs
#   5: All function invocations
class CameraController:

    # Function: init
    # Description: Get the object ready to do some object detection
    def __init__(self):
        Logger.log(LogType.CAMERA, 5, "(func: __init__) function invoked")
        # -- Set up Camera
        self.__cap = cv2.VideoCapture(0)

        # -- Set up Detector
        self.__classNames = []
        classFile = "./Object_Detection_Files/coco.names"
        with open(classFile,"rt") as f:
            self.__classNames = f.read().rstrip("\n").split("\n")

        configPath = "./Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        weightsPath = "./Object_Detection_Files/frozen_inference_graph.pb"

        self.__net = cv2.dnn_DetectionModel(weightsPath, configPath)
        self.__net.setInputSize(320,320)
        self.__net.setInputScale(1.0/ 127.5)
        self.__net.setInputMean((127.5, 127.5, 127.5))
        self.__net.setInputSwapRB(True)

        # -- Set up tracking info
        # Each idx in the array is a cat represented by [framesSeen, framesNotSeen]
        self.__trackingInfo = []
        for _ in Config.CATS:
            self.__trackingInfo.append([0,0])

        # Initialize env variables
        load_dotenv()


    # Function: checkCamera:
    # Descrption: Gets an image from the camera and checks it for a cat
    def checkCamera(self, img=None):
        Logger.log(LogType.CAMERA, 5, "(func: checkCamera) function invoked")
        if img is None:
            # Get an image from the camera
            img = self.getImageFromCamera()
            if img is None:
                return []
        Logger.log(LogType.CAMERA, 3, "(func: checkCamera) New frame being processed...")

        # Detect cats
        img, objectInfo = self.detectCat(img)

        # Analyze any potential cats
        detectedCats = []
        for catInfo in objectInfo:
            catColors = self.getAverageColor(img, catInfo[0])
            catIndex = self.__getWhichCat(catColors)
            if catIndex in detectedCats:
                continue
            else:
                detectedCats.append(catIndex)

            Logger.log(LogType.CAMERA, 2, f"(func: checkCamera) Cat Detected: {Config.CATS[catIndex]} --- Color: {catColors}")
        
        # Update tracking info
        savedImgName = None
        for idx in range(len(Config.CATS)):
            catSeen = idx in detectedCats
            self.__updateTrackingNumbers(idx, catSeen)
            if catSeen and Config.SAVE_IMAGES:
                savedImgName = self.__saveImage(img, idx)
        if len(objectInfo) == 0:
            Logger.log(LogType.CAMERA, 3, f"(func: checkCamera) No Cat Detected")

        # Display the video
        if Config.SHOW_VIDEO:
            cv2.imshow("Output",img)
            waitTime = 0 if Config.STEP_THROUGH_VIDEO else 1
            cv2.waitKey(waitTime)

        # Return which cats have been identified
        catsIdentified = []
        for i in range(len(Config.CATS)):
            if self.__trackingInfo[i][0] >= Config.FRAMES_FOR_CONFIRMATION:
                catsIdentified.append(i)

                # Email image
                if Config.EMAIL_IMAGES:
                    if savedImgName is None:
                        savedImgName = self.__saveImage(img, i)
                    self.__emailImage(savedImgName, i)
        return catsIdentified


    # Function: getImageFromCamera
    # Description:
    #       Fetch the current frame from the camera
    def getImageFromCamera(self):
        Logger.log(LogType.CAMERA, 5, "(Func: getImageFromCamera) function invoked")
        success, img = self.__cap.read()
        if not success:
            Logger.log(LogType.CAMERA, 4, "(func: checkCamera) Error fetching image from camera....")
            return None
        img = cv2.resize(img, (0,0), fx=Config.IMAGE_SCALE, fy=Config.IMAGE_SCALE)
        return img


    # Function: saveImage
    # Description: Save the image we just used to identify the cat, returns the img name
    def __saveImage(self, img, catNum):
        Logger.log(LogType.CAMERA, 5, "(Func: __saveImage) function invoked")

        # Get the directory
        imgDir = Config.SAVED_IMG_DIRS[catNum]

        # Create the dirs if need be
        Path(imgDir).mkdir(parents=True, exist_ok=True)

        # Delete the oldest image if we've reached the cap
        imgs = os.listdir(imgDir)
        if not (not Config.SAVE_IMAGES and Config.EMAIL_IMAGES):
            if len(imgs) >= Config.MAX_IMGS:
                imgs_full_path = [os.path.join(imgDir, f) for f in imgs if os.path.isfile(os.path.join(imgDir, f))]
                oldest_file = min(imgs_full_path, key=os.path.getctime)
                os.remove(oldest_file)

        # Save
        current_time = datetime.datetime.now()
        file_safe_time = current_time.strftime(f"{Config.CATS[catNum]}-%Y-%m-%d_%H-%M-%S.jpg")
        file_path = os.path.join(imgDir, file_safe_time)
        Logger.log(LogType.CAMERA, 1, "(Func: __saveImage) saving image to {file_path}")
        cv2.imwrite(file_path, img)
        return file_safe_time


    # Function: __emailImage
    # Description: Email the image to the specified email
    def __emailImage(self, imgName, catNum):
        Logger.log(LogType.CAMERA, 5, "(Func: __emailImage) function invoked")
        smtp_port = 587                 # Standard secure SMTP port
        smtp_server = "smtp.gmail.com"  # Google SMTP Server
        pswd = os.getenv("GOOGLE_PASS")
        subject = f"Cat Feeder - {imgName}"
        body = ""

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = Config.EMAIL
        msg['To'] = Config.EMAIL
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        # Define the file to attach
        filename = os.path.join(Config.SAVED_IMG_DIRS[catNum], imgName)

        # Open the file in python as a binary
        attachment= open(filename, 'rb')  # r for read and b for binary

        # Encode as base 64
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(attachment_package)

        # Cast as string
        text = msg.as_string()

        # Connect with the server
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(Config.EMAIL, pswd)

        # Send emails to "person" as list is iterated
        TIE_server.sendmail(Config.EMAIL, Config.EMAIL, text)

        Logger.log(LogType.CAMERA, 1, f"(Func: __emailImage) Email sent to {Config.EMAIL} with image {imgName}")

        # Close the port
        TIE_server.quit()

        # If we aren't saving images, then delete the image we just sent
        if not Config.SAVE_IMAGES:
            os.remove(filename)
            Logger.log(LogType.CAMERA, 1, f"(Func: __emailImage) {imgName} Deleted")


    # Function: detectCat
    # Description:
    #       Given an image, see if a cat is present
    #       If there is a cat, then return the bounds of where the cat is
    def detectCat(self, img, 
                  thres=Config.CAMERA_DETECTION_THRESHOLD,
                  nms=0.2,
                  objects=['cat']
                  ):
        Logger.log(LogType.CAMERA, 5, "(Func: detectCat) function invoked")
        # Use the detector to find objects in the image
        classIds, confs, bbox = self.__net.detect(img,confThreshold=thres,nmsThreshold=nms)
        
        # If no objects were provided to search for, then search for all the possible classifications
        if len(objects) == 0: objects = self.__classNames
        
        # If objects were found, then gather info on the objects
        objectInfo =[]
        if len(classIds) != 0:
            for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                className = self.__classNames[classId - 1]
                if className in objects:
                    # Store the info on the object detected
                    objectInfo.append([box,className])

                    # Draw a box over what was spotted
                    if (Config.SHOW_VIDEO and Config.DRAW_ON_IMAGE):
                        cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                        cv2.putText(img,self.__classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                        cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

        return img, objectInfo
    

    # Function: getAverageColor
    # Description: given an image an a box where a cat was detected, 
    #               determine the average color of the area
    #           Returns a tuple for the average bgr value and greyscale value
    def getAverageColor(self, img, catBox):
        Logger.log(LogType.CAMERA, 5, "(Func: getAverageColor) function invoked")
        # Get the box info of what we want to scan
        width = int(catBox[2] / 2)
        height = int(catBox[3] / 2)
        x = int(catBox[0] + (width / 4))
        y = int(catBox[1] + (height / 4))

        # Crop the image to just what is seen as the cat
        cropped_img = img[y:y + height, x:x + width]

        # Get the grayscale values of each pixel
        gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

        # Go through each pixel, and only consider the ones that are above the gray threshold
        height, width, _ = cropped_img.shape
        compiled_colors = [[0,0], [0,0], [0,0], [0,0]] # [sum, num] for bgr+gray
        for y in range(height):
            for x in range(width):
                gray = gray_img[y, x]
                if gray > Config.GRAY_UPPER_THRESHOLD:
                    continue

                blue, green, red = cropped_img[y, x]
                new_vals = [blue, green, red, gray]
                for idx, val in enumerate(new_vals):
                    compiled_colors[idx][0] += float(val)
                    compiled_colors[idx][1] += 1
                

        # Compute the final avg values
        avg_colors = [0,0,0,0]
        for idx, val in enumerate(compiled_colors):
            if compiled_colors[idx][1] > 0:
                avg_colors[idx] = compiled_colors[idx][0] / compiled_colors[idx][1]

        # We can now draw over the image with a box over the cat area if needed
        if ( Config.SHOW_VIDEO and Config.DRAW_ON_IMAGE ):
            top_left = (x, y)
            bottom_right = (x + width, y + height)
            cv2.rectangle(img, top_left, bottom_right, color=(0,0,255), thickness=2)

        return avg_colors
    
    
    # Function: getWhichCat
    # Description: Determine which cat we're looking at based on the detected colors
    def __getWhichCat(self, detectedColors):
        Logger.log(LogType.CAMERA, 5, "(Func: __getWhichCat) function invoked")
        # Get values for how different the detected color is from the expected colors
        colorDiffs = []
        for i in range(len(Config.CAT_EXPECTED_COLORS)):
            expectedColors = Config.CAT_EXPECTED_COLORS[i]
            colorDiff = 0
            for j in range(len(expectedColors)):
                colorDiff += abs(expectedColors[j] - detectedColors[j])
            colorDiffs.append(colorDiff)

        # Determine which was the closest match
        bgrClosestMatchIndex = colorDiffs.index(min(colorDiffs))

        return bgrClosestMatchIndex
    
    
    # Function: updateTrackingNumbers
    # Description: based on what was just detected, update the tracking numbers
    def __updateTrackingNumbers(self, catIdx, catSeen):
        Logger.log(LogType.CAMERA, 5, f"(Func: __updateTrackingNumbers) function invoked - catIdx={catIdx}, catSeen={catSeen}")
        if catSeen:
            self.__trackingInfo[catIdx][0] += 1
        else:
            self.__trackingInfo[catIdx][1] += 1
        
        # If a cat has been detected, then reset the NoCat event
        # If a cat has been identified, then reset the NoCat event
        if catSeen and (self.__trackingInfo[catIdx][0] == 1 or self.__trackingInfo[catIdx][0] == Config.FRAMES_FOR_CONFIRMATION):
            self.__trackingInfo[catIdx][1] = 0

        # If the NoCat event goes through, then reset the Cat events
        elif self.__trackingInfo[catIdx][1] == Config.FRAMES_FOR_CANCEL:
            self.resetCatTracking(catIdx)
            Logger.log(LogType.CAMERA, 1, f'(Func: __updateTrackingNumbers) Cat {catIdx} not been detected in {Config.FRAMES_FOR_CONFIRMATION} frames -- resetting...')


        if self.__trackingInfo[catIdx][0] == Config.FRAMES_FOR_CONFIRMATION:
            Logger.log(LogType.CAMERA, 1, f'(Func: __updateTrackingNumbers) {Config.CATS[catIdx]} IDENTIFIED')
                

        Logger.log(LogType.CAMERA, 3, f'(Func: __updateTrackingNumbers) Tracking State: {self.__trackingInfo}')


    # Function: resetCatTracking
    # Description: resets the tracking info for the given cat
    def resetCatTracking(self, catIdx):
        Logger.log(LogType.CAMERA, 5, f"(Func: resetCatTracking) function invoked - catIdx={catIdx}")
        
        self.__trackingInfo[catIdx][0] = 0
        self.__trackingInfo[catIdx][1] = 0


# FOR TESTING THIS CLASS SPECIFICALLY
if __name__ == "__main__":
    cc = CameraController()
    while True:
        catsIdentified = cc.checkCamera()
        Logger.log(LogType.CONTROL, 1, f"Cats indentified: {catsIdentified}")
