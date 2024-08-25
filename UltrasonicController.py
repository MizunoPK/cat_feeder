from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from Config import Config
from Logger import Logger
from LogType import LogType

# Class: UltrasonicController
# Description:
#       Controls the behavior of the ultrasonic sensors
#       Determines when a cat is/isn't feeding
# Logs:
#       1: Distance measurements
#       2: All function invokations
class UltrasonicController:

    def __init__(self, boxNum):
        self.__boxNum = boxNum
        Logger.log(LogType.ULTRASONIC, 2, f"(func: __init__, box: {self.__boxNum}) function invoked")

        trigPin = Config.ULTRASONIC_TRIG_PINS[boxNum]
        echoPin = Config.ULTRASONIC_ECHO_PINS[boxNum]
        if Config.ULTRASONIC_ACTIVE:
            my_factory = PiGPIOFactory() 
            self.__sensor = DistanceSensor(echo=echoPin, trigger=trigPin, max_distance=1, pin_factory=my_factory)


    # Function: isDetectingObject
    # Description: returns boolean whether or not the senor is detecting something
    def isDetectingObject(self):
        Logger.log(LogType.ULTRASONIC, 2, f"(func: isDetectingObject, box: {self.__boxNum}) function invoked")

        if Config.ULTRASONIC_ACTIVE:
            distance = self.__sensor.distance * 100
            objectDetected = (distance) <= Config.ULTRASONIC_MAX_DISTANCE

            Logger.log(LogType.ULTRASONIC, 1, f"(func: isDetectingObject, box: {self.__boxNum}) Distance measured: {distance} cm --- Object Detected = {objectDetected}")

            return objectDetected
        return False