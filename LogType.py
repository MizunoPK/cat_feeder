from enum import Enum

# Defines the types of Logs that can occur
class LogType(Enum):
    ControlCenter = "CONTROL CENTER"
    FEEDER = "FEEDER"
    CAMERA = "CAMERA CONTROLLER"
    SERVO = "SERVO CONTROLLER"
    ULTRASONIC = "ULTRASONIC CONTROLLER"