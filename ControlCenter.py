from CameraController import CameraController
from Logger import Logger
from LogType import LogType
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

if __name__ == "__main__":
    cc = ControlCenter()
    cc.run()