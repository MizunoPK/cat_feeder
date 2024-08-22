from CameraController import CameraController
from Logger import Logger
from LogType import LogType
import cv2

# Class: ControlCenter
# Description:
#       The brain of the cat feeder system
#       Uses the controllers to ensure the feeders are working properly
class ControlCenter:

    def __init__(self):
        self.cameraController = CameraController()


    # Function: run
    # Description: run the main loop
    def run(self):
        control = cv2.imread("cv/control.jpg")
        bento = cv2.imread("cv/bento.jpg")
        nori = cv2.imread("cv/nori.jpg")
        both = cv2.imread("cv/both.jpg")
        sequence = [both]
        # sequence = [
        #     control,
        #     control,
        #     bento,
        #     bento,
        #     nori,
        #     bento,
        #     bento,
        #     bento,
        #     bento,
        #     control,
        #     control,
        #     bento,
        #     bento,
        #     bento,
        #     bento,
        #     bento,
        #     bento,
        #     control,
        #     control,
        #     control,
        #     nori,
        #     control,
        #     control,
        #     control,
        #     control,
        #     control,
        #     control,
        #     control,
        # ]
        
        for readImg in sequence:
            catsIdentified = self.cameraController.checkCamera(img=readImg)
            Logger.log(LogType.ControlCenter, 1, f"Cats indentified: {catsIdentified}")

if __name__ == "__main__":
    cc = ControlCenter()
    cc.run()