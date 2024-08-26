from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from Config import Config
from Logger import Logger
from LogType import LogType
import time

# Class: UltrasonicController
# Description:
#       Controls the behavior of the ultrasonic sensors
#       Determines when a cat is/isn't feeding
# Logs:
#       1: Change in detecting something
#       2: Cooldown Info
#       3: Distance measurements
#       4: All function invokations
class UltrasonicController:

    def __init__(self, boxNum):
        self.__boxNum = boxNum
        Logger.log(LogType.ULTRASONIC, 4, f"(func: __init__, box: {self.__boxNum}) function invoked")

        self.__detectingSomething = False
        self.__cooldownStartTime = None

        trigPin = Config.ULTRASONIC_TRIG_PINS[boxNum]
        echoPin = Config.ULTRASONIC_ECHO_PINS[boxNum]
        if Config.ULTRASONIC_ACTIVE:
            my_factory = PiGPIOFactory() 
            self.__sensor = DistanceSensor(echo=echoPin, trigger=trigPin, max_distance=1, pin_factory=my_factory)


    # Function: isDetectingObject
    # Description: returns boolean whether or not the senor is detecting something
    def isDetectingObject(self):
        Logger.log(LogType.ULTRASONIC, 4, f"(func: isDetectingObject, box: {self.__boxNum}) function invoked")
        
        # Check on the cooldown
        self.__outOfCooldown()

        if Config.ULTRASONIC_ACTIVE:
            distance = self.__sensor.distance * 100
            objectDetected = (distance) <= Config.ULTRASONIC_MAX_DISTANCE

            Logger.log(LogType.ULTRASONIC, 3, f"(func: isDetectingObject, box: {self.__boxNum}) Distance measured: {distance} cm --- Object Detected = {objectDetected}")

            # Determine if we have changed in detecting something
            if objectDetected != self.__detectingSomething:
                # If we are now detecting something:
                if objectDetected:
                    self.__detectingSomething = True
                    self.__cooldownStartTime = None
                
                # If we are seeing nothing for the first time - start the cooldown
                elif self.__cooldownStartTime is None:
                    self.__cooldownStartTime = time.perf_counter()

                # If we are seeing nothing after the cooldown finishes - change the state
                elif self.__isOffCooldown(): 
                    self.__detectingSomething = False
                    self.__cooldownStartTime = None

        return self.__detectingSomething
    
    # Function: isOffCooldown
    # Description: returns boolean whether or not we are no longer in cooldown
    def __isOffCooldown(self):
        Logger.log(LogType.ULTRASONIC, 4, f"(func: __isOffCooldown, box: {self.__boxNum}) function invoked")

        if self.__cooldownStartTime is None:
            return True
        
        currentTime = time.perf_counter()
        isOffCooldown = False
        if (currentTime - self.__cooldownStartTime) >= Config.ULTRASONIC_COOLDOWN:
            Logger.log(LogType.ULTRASONIC, 2, f"(func: __outOfCooldown, box: {self.__boxNum}) Cooldown Finished")
            isOffCooldown = True
        return isOffCooldown
        

    # Function: resetDetecting
    # Description: Set things up to start detecting as box opens
    def resetDetecting(self):
        Logger.log(LogType.ULTRASONIC, 4, f"(func: isDetectingObject, box: {self.__boxNum}) function invoked")
        self.__detectingSomething = False
        self.__cooldownStartTime = None