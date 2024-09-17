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
        # Map used for tracking how many frames a result has been seen
        # -1 means that no cats are present
        # index values for each cat are added to track how many frames has seen each cat
        self.__trackingInfo = {
            -1: 0
        }
        for i in range(len(Config.CATS)):
            self.__trackingInfo[i] = 0

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
            (catColor, catGrayscale) = self.getAverageColor(img, catInfo[0])
            catIndex = self.__getWhichCat(catColor, catGrayscale)
            if catIndex in detectedCats:
                continue
            else:
                detectedCats.append(catIndex)

            Logger.log(LogType.CAMERA, 2, f"(func: checkCamera) Cat Detected: {Config.CATS[catIndex]} --- Color: {catColor}")

            self.__updateTrackingNumbers(catIndex)
        
        # Note if we did not find any cats
        if len(objectInfo) == 0:
            self.__updateTrackingNumbers(-1)
            Logger.log(LogType.CAMERA, 3, f"(func: checkCamera) No Cat Detected")

        # Display the video
        if Config.SHOW_VIDEO:
            cv2.imshow("Output",img)
            waitTime = 0 if Config.STEP_THROUGH_VIDEO else 1
            cv2.waitKey(waitTime)

        # Return which cats have been identified
        catsIdentified = []
        for i in range(len(Config.CATS)):
            if self.__trackingInfo[i] >= Config.FRAMES_FOR_CONFIRMATION:
                catsIdentified.append(i)

                # Save & Email image
                if Config.SAVE_IMAGES or Config.EMAIL_IMAGES:
                    imgName = self.__saveImage(img, i)
                    if Config.EMAIL_IMAGES:
                        self.__emailImage(imgName, i)
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
    # Description: Save the image we just used to identify the cat
    def __saveImage(self, img, catNum):
        Logger.log(LogType.CAMERA, 5, "(Func: __saveImage) function invoked")

        # Get the directory
        imgDir = Config.SAVED_IMG_DIRS[catNum]

        # Create the dirs if need be
        Path(imgDir).mkdir(parents=True, exist_ok=True)

        # Save
        current_time = datetime.datetime.now()
        file_safe_time = current_time.strftime(f"{Config.CATS[catNum]}-%Y-%m-%d_%H-%M-%S.jpg")
        file_path = os.path.join(imgDir, file_safe_time)
        Logger.log(LogType.CAMERA, 1, "(Func: __saveImage) saving image to {file_path}")
        cv2.imwrite(file_path, img)
        return file_safe_time


    # Function: emailImage
    # Description: Email the image to the specified email
    def emailImage(self, imgName, catNum):
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
        x = int(catBox[0] + (width / 2))
        y = int(catBox[1] + (width / 2))

        # Get the average bgr color
        roi = img[y:y + height, x:x + width]
        average_color_bgr = cv2.mean(roi) 
        average_color_bgr = average_color_bgr[:3]
        gray_img = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        average_gray = np.mean(gray_img)
        
        if ( Config.SHOW_VIDEO and Config.DRAW_ON_IMAGE ):
            top_left = (x, y)
            bottom_right = (x + width, y + height)
            cv2.rectangle(img, top_left, bottom_right, color=(0,0,255), thickness=2)

        return (average_color_bgr, average_gray)
    
    
    # Function: getWhichCat
    # Description: Determine which cat we're looking at based on the detected colors
    def __getWhichCat(self, detectedColorBGR, detectedGrayscale):
        Logger.log(LogType.CAMERA, 5, "(Func: __getWhichCat) function invoked")
        # Get values for how different the detected color is from the expected colors
        colorDiffs = []
        for i in range(len(Config.CAT_EXPECTED_COLORS)):
            expectedColorBGR = Config.CAT_EXPECTED_COLORS[i]
            colorDiff = 0
            for j in range(len(expectedColorBGR)):
                colorDiff += abs(expectedColorBGR[j] - detectedColorBGR[j])
            colorDiff += abs( Config.CAT_EXPECTED_GRAYSCALE[i] - detectedGrayscale)
            colorDiffs.append(colorDiff)

        # Determine which was the closest match
        bgrClosestMatchIndex = colorDiffs.index(min(colorDiffs))

        return bgrClosestMatchIndex
    
    
    # Function: updateTrackingNumbers
    # Description: based on what was just detected, update the tracking numbers
    def __updateTrackingNumbers(self, eventNum):
        Logger.log(LogType.CAMERA, 5, "(Func: __updateTrackingNumbers) function invoked")
        self.__trackingInfo[eventNum] += 1
        
        # If a cat has been detected, then reset the NoCat event
        # If a cat has been identified, then reset the NoCat event
        if eventNum >= 0 and (self.__trackingInfo[eventNum] == 1 or self.__trackingInfo[eventNum] == Config.FRAMES_FOR_CONFIRMATION):
            self.__trackingInfo[-1] = 0

        # If the NoCat event goes through, then reset the Cat events
        elif self.__trackingInfo[-1] == Config.FRAMES_FOR_CANCEL:
            for i in range(len(Config.CATS)):
                self.__trackingInfo[i] = 0
            Logger.log(LogType.CAMERA, 1, f'(Func: __updateTrackingNumbers) Cats have not been detected in {Config.FRAMES_FOR_CONFIRMATION} frames -- resetting...')


        if self.__trackingInfo[eventNum] == Config.FRAMES_FOR_CONFIRMATION and eventNum != -1:
            Logger.log(LogType.CAMERA, 1, f'(Func: __updateTrackingNumbers) {Config.CATS[eventNum]} IDENTIFIED')
                

        Logger.log(LogType.CAMERA, 3, f'(Func: __updateTrackingNumbers) Tracking State: {self.__trackingInfo}')


# FOR TESTING THIS CLASS SPECIFICALLY
if __name__ == "__main__":
    cc = CameraController()
    # while True:
    #     catsIdentified = cc.checkCamera()
    #     Logger.log(LogType.CONTROL, 1, f"Cats indentified: {catsIdentified}")
    cc.emailImage("bento.jpg", 1)
