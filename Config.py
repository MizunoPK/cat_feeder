from LogType import LogType

# Class: Config 
# Description: Outlines the configuration variables that change how the system behaves
#              Change values here to refine the control of the system
class Config:
    # --- CAT CONFIGURATION ---
    # Any of the following cat-related arrays should follow the same ordering
    #   as what is defined here
    CATS = ["Bento", "Nori"]

    # --- LOGGER CONFIGURATION ---
    LOG_LEVELS = {
        LogType.CONTROL: 5,
        LogType.BOX: 5,
        LogType.CAMERA: 3,
        LogType.SERVO: 5,
        LogType.ULTRASONIC: 5,
        LogType.BUTTON: 5
    }

    # --- BOX CONFIG ---
    BOX_GRACE_PERIOD = 15 # number of seconds to keep the box open before restarting detection efforts

    # --- CAMERA CONFIGURATION ---
    SHOW_VIDEO = True # Whether or not to display the camera frames as they are read
    DRAW_ON_IMAGE = True # Whether or not to draw on the image
    STEP_THROUGH_VIDEO = False # Whether or not to step through the video or play it continuously
    CAMERA_DETECTION_THRESHOLD = 0.6  # threshold to detect an object - this is how confident on a scale of 0-1 that the found object is a cat
    COLOR_THRESHOLD = 40  # threshold to say this is nori vs bento - scale of 0-255 where 0 is closer to black
    CAT_EXPECTED_COLORS = [
        (52.608725110231134, 53.92688031612082, 58.60149969408517), 
        (76.24038825720217, 89.1908922191514, 101.39967529554147)
    ] # Values found via GetMedianColorTool for what the expected colors of each cat are
    FRAMES_FOR_CONFIRMATION = 10 # Number of frames that a car needs to be seen before assuming they are there

    # --- SERVO CONFIG ---
    SERVOS_ACTIVE = True # Whether or not servos are plugged in and useable
    SERVO_GPIO_SLOTS = [18, 24] # The gpio slots being used by the servos - should correspond to the cat order
    SERVO_SIDES = ["L", "R"]
    SERVO_DELAY_SEC = 0.01 # The delay between incrementing the angle of the servo

    # --- ULTRASONIC CONFIG
    ULTRASONIC_ACTIVE = True # Whether or not the sensors are plugged in and ready
    ULTRASONIC_TRIG_PINS = [20, 16] # The gpio slots being used by the ultrasonic trig pins - should correspond to the cat order
    ULTRASONIC_ECHO_PINS = [21, 12] # The gpio slots being used by the ultrasonic echo pins - should correspond to the cat order
    ULTRASONIC_MAX_DISTANCE = 15 # Maximum distance we check for - measured in cm
    ULTRASONIC_COOLDOWN = 15 # seconds until we've decided the cat has definitely left

    # --- BUTTON CONFIG ---
    BUTTON_PIN = [23,17] # GPIO pin for button
    LED_PIN = [4,27] # GPIO pin for LED