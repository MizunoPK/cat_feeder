from Config import Config
from Logger import Logger
from LogType import LogType
from enum import Enum
import time

from ServoController import ServoController
from UltrasonicController import UltrasonicController
from ButtonController import ButtonController

# Class: BoxController
# Description: Handles opening and closing the box
#               Manages the ServoController and UltrasonicController
# Logs:
#   1: State updates
#   5: All function invocations 
class BoxController():
    class BoxState(Enum):
        WAITING = "WAITING"
        OPENING = "OPENING"
        OPEN = "OPEN"
        OPENED_MANUALLY = "OPENNED MANUALLY"
        CLOSING = "CLOSING"
    

    def __init__(self, boxNum) -> None:
        self.__boxNum = boxNum
        Logger.log(LogType.BOX, 5, f"(func: __init__, box: {self.__boxNum}) function invoked")

        self.__servoController = ServoController(boxNum)
        self.__ultrasonicController = UltrasonicController(boxNum)
        self.__buttonController = ButtonController(boxNum)

        self.__initWaiting()


    def shutDown(self):
        Logger.log(LogType.BOX, 5, f"(func: shutDown, box: {self.__boxNum}) function invoked")
        self.__servoController.shutDown()
        self.__ultrasonicController.shutDown()


    # Function: needsCamera
    # Description: Returns whether or not the box needs the camera currently
    def needsCamera(self):
        return self.__currentState == self.BoxState.WAITING


    # Function: process
    # Description: Given whether or not the corresponding cat is identified, 
    #              process what the box should be doing
    def process(self, catIdentified):
        Logger.log(LogType.BOX, 5, f"(func: process, box: {self.__boxNum} , args: (catIdentified: {catIdentified})) function invoked")

        if self.__currentState == self.BoxState.WAITING:
            self.__processWaiting(catIdentified)
        elif self.__currentState == self.BoxState.OPENING:
            self.__processOpening()
        elif self.__currentState == self.BoxState.OPENED_MANUALLY:
            self.__processOpennedManually()
        elif self.__currentState == self.BoxState.OPEN:
            self.__processOpen(catIdentified)
        elif self.__currentState == self.BoxState.CLOSING:
            return self.__processClosing()

        return False


    # Function: initWaiting
    # Description: init the WAITING state
    def __initWaiting(self):
        Logger.log(LogType.BOX, 5, f"(func: __initWaiting, box: {self.__boxNum}) function invoked")
        Logger.log(LogType.BOX, 1, f"(func: __initWaiting, box: {self.__boxNum}) Setting to WAITING state")
        self.__currentState = self.BoxState.WAITING
        self.__buttonController.setClickable(True)
        return True

    # Function: processWaiting
    # Description: Process the WAITING state
    def __processWaiting(self, catIdentified):
        Logger.log(LogType.BOX, 5, f"(func: __processWaiting, box: {self.__boxNum} , args: (catIdentified: {catIdentified})) function invoked")

        # If the button has been pressed, or a cat has been identified -> move to the OPENNING state
        if self.__buttonController.isTurnedOn() or catIdentified:
            self.__initOpening()


    # Function: initOpening
    # Description: init the Opening state
    def __initOpening(self):
        Logger.log(LogType.BOX, 5, f"(func: __initOpening, box: {self.__boxNum}) function invoked")
        Logger.log(LogType.BOX, 1, f"(func: __initOpening, box: {self.__boxNum}) Setting to OPENNING state")

        self.__currentState = self.BoxState.OPENING
        self.__servoController.open()
        self.__buttonController.setClickable(False)

    # Function: processWaiting
    # Description: Process the OPENING state
    def __processOpening(self):
        Logger.log(LogType.BOX, 5, f"(func: __processOpening, box: {self.__boxNum}) function invoked")

        # Determine if we have finished opening
        if self.__servoController.getState() == ServoController.State.OPEN:
            # If the Button was pressed - then go to the OPENNED_MANUALLY state
            if self.__buttonController.isTurnedOn():
                self.__initOpennedManually()
            # Otherwise, go to the OPEN state
            else:
                self.__initOpen()
            

    # Function: initOpen
    # Description: init the Open state
    def __initOpen(self):
        Logger.log(LogType.BOX, 5, f"(func: __initOpen, box: {self.__boxNum}) function invoked")
        Logger.log(LogType.BOX, 1, f"(func: __initOpen, box: {self.__boxNum}) Setting to OPEN state")

        self.__currentState = self.BoxState.OPEN
        self.__buttonController.setClickable(True)
        self.__ultrasonicController.resetDetecting()


    # Function: processOpen
    # Description: Process the Open state
    def __processOpen(self, catIdentified):
        Logger.log(LogType.BOX, 5, f"(func: __processOpen, box: {self.__boxNum} function invoked")

        # If the button is pressed, then go to the OPENNED_MANUALLY state
        if self.__buttonController.isTurnedOn():
            self.__initOpennedManually()

        # If there is nothing detected by the ultrasonic, 
        # then close the box
        elif not self.__ultrasonicController.isDetectingObject() or not catIdentified:
            self.__initClosing()



    # Function: initOpennedManually
    # Description: init the OPENNED_MANUALLY state
    def __initOpennedManually(self):
        Logger.log(LogType.BOX, 5, f"(func: __initOpennedManually, box: {self.__boxNum}) function invoked")
        Logger.log(LogType.BOX, 1, f"(func: __initOpennedManually, box: {self.__boxNum}) Setting to OPENNED_MANUALLY state")

        self.__currentState = self.BoxState.OPENED_MANUALLY
        self.__buttonController.setClickable(True)


    # Function: processOpennedManually
    # Description: Process the OpennedManually state
    def __processOpennedManually(self):
        Logger.log(LogType.BOX, 5, f"(func: __processOpennedManually, box: {self.__boxNum}) function invoked")

        # Wait for the button to be clicked again, then close the box
        if not self.__buttonController.isTurnedOn():
            self.__initClosing()


    # Function: initClosing
    # Description: init the Closing state
    def __initClosing(self):
        Logger.log(LogType.BOX, 5, f"(func: __initClosing, box: {self.__boxNum}) function invoked")
        Logger.log(LogType.BOX, 1, f"(func: __initClosing, box: {self.__boxNum}) Setting to CLOSING state")

        self.__currentState = self.BoxState.CLOSING
        self.__buttonController.setClickable(False)
        self.__servoController.close()


    # Function: processClosing
    # Description: Process the Closing state
    def __processClosing(self):
        Logger.log(LogType.BOX, 5, f"(func: __processClosing, box: {self.__boxNum}) function invoked")

        # When we finish closing - go to the WAITING state
        if self.__servoController.getState() == ServoController.State.CLOSED:
            return self.__initWaiting()
        return False