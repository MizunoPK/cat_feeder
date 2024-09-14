from Config import Config
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
import time
import threading
from Logger import Logger
from LogType import LogType
from enum import Enum

# Class: ServoController
# Description:
#       Controls the behavior of the servos
#       Makes the servos move and sends signals when movement is done
# Logs:
#       1: Box finishes opening/closing
#       2: Open/close functions invoked
#       3: getState results
#       4: Errors
#       5: All function invocations
#       6: All rotate info
class ServoController():
    class State(Enum):
        OPEN = 1
        OPENING = 2
        CLOSED = 3
        CLOSING = 4

    def __init__(self, boxNum):
        self.__boxNum = boxNum

        Logger.log(LogType.SERVO, 5, f"(func: __init__, box: {self.__boxNum}) function invoked")

        # Set up info needed by servos
        self.__closeAngle = 90 if Config.SERVO_SIDES[boxNum] == "L" else 135
        self.__openAngle = 0 if Config.SERVO_SIDES[boxNum] == "L" else 225
        if Config.SERVOS_ACTIVE:
            myCorrection=0.0
            maxPW=(2.5+myCorrection)/1000
            minPW=(0.5-myCorrection)/1000
            my_factory = PiGPIOFactory() 
            
            # Save the Servo info
            gpio = Config.SERVO_GPIO_SLOTS[boxNum]
            self.__servo =  AngularServo(gpio, initial_angle=self.__closeAngle, min_angle=0, max_angle=270, min_pulse_width=minPW, max_pulse_width=maxPW, pin_factory=my_factory)
            self.__servo.angle = self.__closeAngle
        
        self.__state = self.State.CLOSED

        # Establish threading info
        self.__thread = None
        self.__threadDoneEvent = None

    # Function: shutDown
    # Description: Shut down the servo
    def shutDown(self):
        Logger.log(LogType.SERVO, 5, f"(func: shutDown, box: {self.__boxNum}) function invoked")
        self.__servo.close()

    # Function: getState
    # Description: check on the state of the servo, if it is open, opening, closed, or closing
    def getState(self):
        Logger.log(LogType.SERVO, 5, f"(func: getState, box: {self.__boxNum}) function invoked")

        # If the rotate thread has finished...
        if self.__threadDoneEvent is not None and self.__threadDoneEvent.is_set():
            # clean up the thread
            self.__thread.join()
            self.__thread = None
            self.__threadDoneEvent = None

            # Update the state
            self.__state = self.State.OPEN if self.__state == self.State.OPENING else self.State.CLOSED

        Logger.log(LogType.SERVO, 3, f"(func: getState, box: {self.__boxNum}) - current state: {self.__state.name}")
        return self.__state


    # Functions: open & close
    # Description: call the thread starting function for opening or closing the box
    def open(self):
        Logger.log(LogType.SERVO, 2, f"(func: __open, box: {self.__boxNum}) function invoked")
        self.__state = self.State.OPENING
        self.__startThread(True)
    def close(self):
        Logger.log(LogType.SERVO, 2, f"(func: __close, box: {self.__boxNum}) function invoked")
        self.__state = self.State.CLOSING
        self.__startThread(False)


    # Function: startThread
    # Description: Start up a thread for opening/closing the box
    def __startThread(self, opening):
        Logger.log(LogType.SERVO, 5, f"(func: __startThread, box: {self.__boxNum}) function invoked")

        # Use a thread to open/close the box
        self.__threadDoneEvent = threading.Event()
        self.__thread = threading.Thread(target=self.__rotate, args=(self.__threadDoneEvent, opening))
        self.__thread.start()


    # Function: rotate
    # Description: Use a thread to rotate the box to open/close
    def __rotate(self, event, opening):
        try:
            Logger.log(LogType.SERVO, 5, f"(func: __rotate, box: {self.__boxNum}) function invoked")

            startAngle = self.__closeAngle if opening else self.__openAngle
            endAngle = self.__openAngle if opening else self.__closeAngle
            movementDir = 1 if endAngle > startAngle else -1
            angleRange = range(startAngle, endAngle + movementDir, movementDir)
            Logger.log(LogType.SERVO, 4, f"(func: __rotate, box: {self.__boxNum}) Range Data: Start: {startAngle}, End: {endAngle}, Dir: {movementDir}")
            for angle in angleRange:
                if Config.SERVOS_ACTIVE:
                    self.__servo.angle = angle
                time.sleep(Config.SERVO_DELAY_SEC)

            newState = "OPEN" if opening else "CLOSED"
            Logger.log(LogType.SERVO, 1, f"(func: __rotate, box: {self.__boxNum}) New State: {newState}")

            event.set()
        except:
            Logger.log(LogType.SERVO, 4, f"(func: __rotate, box: {self.__boxNum}) Error occurred when trying to rotate the servo - possibly due to program closing. Ending thread.")


# FOR TESTING THIS CLASS SPECIFICALLY
if __name__ == "__main__":
    try:
        sc = ServoController(1)
        sc.getState()
        #while True:
        sc.open()
        while sc.getState() != ServoController.State.OPEN:
            time.sleep(0.25)
        time.sleep(5)
        #break
        sc.close()
        while sc.getState() != ServoController.State.CLOSED:
            time.sleep(0.25)
        time.sleep(5)
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        sc.shutDown()
        print("Ending program")