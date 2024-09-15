from LogType import LogType

# Class: Config 
# Description: Outlines the configuration variables that change how the system behaves
#              Change values here to refine the control of the system
class Config:
    # --- CAT CONFIGURATION ---
    # Any of the following cat-related arrays should follow the same ordering
    #   as what is defined here
    CATS = ["Nori", "Bento"]

    # --- LOGGER CONFIGURATION ---
    LOG_LEVELS = {
        LogType.CONTROL: 1,
        LogType.BOX: 1,
        LogType.CAMERA: 2,
        LogType.SERVO: 2,
        LogType.ULTRASONIC: 3,
        LogType.BUTTON: 1
    }

    # --- BOX CONFIG ---
    BOX_GRACE_PERIOD = 5 # number of seconds to keep the box open before restarting detection efforts

    # --- CAMERA CONFIGURATION ---
    SHOW_VIDEO = True # Whether or not to display the camera frames as they are read
    DRAW_ON_IMAGE = False # Whether or not to draw on the image
    STEP_THROUGH_VIDEO = False # Whether or not to step through the video or play it continuously
    CAMERA_DETECTION_THRESHOLD = 0.6  # threshold to detect an object - this is how confident on a scale of 0-1 that the found object is a cat
    CAT_EXPECTED_COLORS = [
        (76.15548150658283, 86.24959916710047, 96.65603224760979),
        (51.805574820151676, 51.54244241398648, 54.053270066447325),
    ] # Values found via GetMedianColorTool for what the expected colors of each cat are
    CAT_EXPECTED_GRAYSCALE = [
        117.20612696306127,
        69.85845558563489,
    ] # Values found via GetMedianColorTool for what the expected colors of each cat are
    FRAMES_FOR_CONFIRMATION = 10 # Number of frames that a cat needs to be seen before assuming they are there
    FRAMES_FOR_CANCEL = 20 # Number of frames that a cat needs to not be detected before things get reset
    IMAGE_SCALE = 0.7 # how to scale the image we fetch from the camera
    SAVE_IMAGES = True # whether or not to save images upon identification
    SAVED_IMG_DIRS = ["./data/CatPics/nori", "./data/CatPics/bento"] # Where to save images if we are saving

    # --- SERVO CONFIG ---
    SERVOS_ACTIVE = True # Whether or not servos are plugged in and useable
    SERVO_GPIO_SLOTS = [16, 18] # The gpio slots being used by the servos - should correspond to the cat order
    SERVO_SIDES = ["L","R"]
    SERVO_DELAY_SEC = 0.01 # The delay between incrementing the angle of the servo

    # --- ULTRASONIC CONFIG
    ULTRASONIC_ACTIVE = True # Whether or not the sensors are plugged in and ready
    ULTRASONIC_TRIG_PINS = [21, 24] # The gpio slots being used by the ultrasonic trig pins - should correspond to the cat order
    ULTRASONIC_ECHO_PINS = [20, 23] # The gpio slots being used by the ultrasonic echo pins - should correspond to the cat order
    ULTRASONIC_MAX_DISTANCE = [20, 25] # Maximum distance we check for - measured in cm
    ULTRASONIC_COOLDOWN = 5 # seconds until we've decided the cat has definitely left

    # --- BUTTON CONFIG ---
    BUTTON_PIN = [5, 13] # GPIO pin for button
    LED_PIN = [6, 19] # GPIO pin for LED