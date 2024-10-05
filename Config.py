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
        LogType.CAMERA: 3,
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
        (50.17433207710885, 51.934087165428174, 58.34037871234033, 53.64360966880825),
        (27.75704668865186, 24.434116272008524, 30.86516604265306, 26.73071870510751),
    ] # Values found via GetMedianColorTool for what the expected colors of each cat are - this is (blue, green, red, gray)
    GRAY_UPPER_THRESHOLD = 160 # The upper limit of gray values to accept - anything higher does not contribute to the average color calculations, assuming it is part of white backgrounds
    FRAMES_FOR_CONFIRMATION = 15 # Number of frames that a cat needs to be seen before assuming they are there
    FRAMES_FOR_CANCEL = 8 # Number of frames that a cat needs to not be detected before things get reset
    IMAGE_SCALE = 0.6 # how to scale the image we fetch from the camera
    SAVE_IMAGES = False # whether or not to save images upon identification
    SAVED_IMG_DIRS = ["./data/CatPics/nori", "./data/CatPics/bento"] # Where to save images if we are saving
    MAX_IMGS = 300 # the maximum number of images to save - will delete the oldest once this is reached
    EMAIL_IMAGES = True
    EMAIL = "Mizuno.PK@gmail.com"

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
    ULTRASONIC_COOLDOWN = 15 # seconds until we've decided the cat has definitely left

    # --- BUTTON CONFIG ---
    BUTTON_PIN = [5, 13] # GPIO pin for button
    LED_PIN = [6, 19] # GPIO pin for LED