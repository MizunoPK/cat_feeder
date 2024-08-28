from CameraController import CameraController
from Logger import Logger
from LogType import LogType
from Config import Config
from BoxController import BoxController

# Class: ControlCenter
# Description:
#       The brain of the cat feeder system
#       Uses the controllers to ensure the feeders are working properly
# Logs:
#       1: Shut Down
#       5: All function invocations
class ControlCenter:

    def __init__(self):
        Logger.log(LogType.CONTROL, 5, "__init__ function has been invoked")

        self.__cameraController = CameraController()
        self.__boxes = []
        for boxNum in range(len(Config.CATS)):
            self.__boxes.append(BoxController(boxNum))


    # Function: run
    # Description: run the main loop
    def run(self):
        Logger.log(LogType.CONTROL, 5, "run function has been invoked")

        while True:
            # Determine if we need info from the camera
            needCamera = False
            for box in self.__boxes:
                if box.needsCamera():
                    needCamera = True
                    break

            # Get info from the camera
            catsIdentified = [] if (not needCamera) else self.__cameraController.checkCamera()

            # Process each box
            for catNum in range(len(Config.CATS)):
                catIdentified = catNum in catsIdentified
                self.__boxes[catNum].process(catIdentified)

    
    # Function: shutDown
    # Description: Shut down all processes
    def shutDown(self):
        Logger.log(LogType.CONTROL, 1, "----- SHUTTING DOWN SYSTEM -----")
        for box in self.__boxes:
            box.shutDown()

