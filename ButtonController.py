from gpiozero import LED, Button
from Config import Config
from Logger import Logger
from LogType import LogType
from time import sleep
import threading

# Class: ButtonController
# Description:
#       Controls the behavior of buttons & leds
#       Lets us manually open the box
# Logs:
#       1: Changing button states
#       2: Clickable info
#       4: All button state results
#       5: All function invokations
class ButtonController:

    def __init__(self, boxNum):
        self.__boxNum = boxNum
        Logger.log(LogType.BUTTON, 5, f"(func: __init__, box: {self.__boxNum}) function invoked")

        self.__button = Button(Config.BUTTON_PIN[boxNum])
        self.__led = LED(Config.LED_PIN[boxNum])
        self._stateChangeable = True
        self.__turnedOn = False


    # Function: isTurnedOn
    # Description: returns boolean whether or not the manual mode has been turned on or not
    def isTurnedOn(self):
        Logger.log(LogType.BUTTON, 5, f"(func: isTurnedOn, box: {self.__boxNum}) function invoked")

        # If we can change state: See if the button has been pressed and change state
        if self._stateChangeable and self.__button.is_active:
            self.__changeState()

        # Return the state
        Logger.log(LogType.BUTTON, 2, f"(func: isTurnedOn, box: {self.__boxNum}) Button state = {self.__turnedOn}")
        return self.__turnedOn


    # Function __changeState
    # Description: change the state to be either turned on or off
    def __changeState(self):
        Logger.log(LogType.BUTTON, 5, f"(func: __changeState, box: {self.__boxNum}) function invoked")
        self.__turnedOn = not self.__turnedOn

        if self.__turnedOn:
            self.__led.on()
        else:
            self.__led.off()

        self.setClickable(False)

        Logger.log(LogType.BUTTON, 1, f"(func: __changeState, box: {self.__boxNum}) State changed to: {self.__turnedOn}")

        
    # Function setClickable
    # Description: set whether the button is clickable or not
    def setClickable(self, clickable):
        Logger.log(LogType.BUTTON, 5, f"(func: setClickable, box: {self.__boxNum}) function invoked")
        
        self._stateChangeable = clickable

        Logger.log(LogType.BUTTON, 2, f"(func: setClickable, box: {self.__boxNum}) Clickable = {clickable}")


if __name__ == "__main__":
    bc = ButtonController(0)
    bc.setClickable(True)
    while not bc.isTurnedOn():
        sleep(0.25)
    while bc.isTurnedOn():
        sleep(0.25)