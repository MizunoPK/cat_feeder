from Config import Config
from Logger import Logger
from LogType import LogType
from enum import Enum

# Class: BoxController
# Description: Handles opening and closing the box
#               Manages the ServoController and UltrasonicController
class BoxController():
    class BoxState(Enum):
        OPEN = 0
        CLOSE = 1
        OPENING = 2
        CLOSING = 3
    pass