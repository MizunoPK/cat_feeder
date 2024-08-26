from enum import Enum

# Defines the types of Logs that can occur
class LogType(Enum):
    CONTROL = "CONTROL CENTER"
    BOX = "BOX CONTROLLER"
    CAMERA = "CAMERA CONTROLLER"
    SERVO = "SERVO CONTROLLER"
    ULTRASONIC = "ULTRASONIC CONTROLLER"
    BUTTON = "BUTTON CONTROLLER"