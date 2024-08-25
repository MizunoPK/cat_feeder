from CameraController import CameraController
from Logger import Logger
from LogType import LogType
from Config import Config
import os
if Config.SERVOS_ACTIVE or Config.ULTRASONIC_ACTIVE: os.system("sudo pigpiod")
import cv2

# Class: ControlCenter
# Description:
#       The brain of the cat feeder system
#       Uses the controllers to ensure the feeders are working properly
# Logs:
#       5: All function invocations
class ControlCenter:

    def __init__(self):
        Logger.log(LogType.CONTROL, 5, "__init__ function has been invoked")

        self.cameraController = CameraController()


    # Function: run
    # Description: run the main loop
    def run(self):
        Logger.log(LogType.CONTROL, 5, "run function has been invoked")

    
    # Function: shutDown
    # Description: Shut down all processes
    def shutDown(self):
        Logger.log(LogType.CONTROL, 1, "----- SHUTTING DOWN SYSTEM -----")
        os.system("sudo killall pigpiod")

if __name__ == "__main__":
    cc = ControlCenter()
    cc.run()