from ControlCenter import ControlCenter
from Config import Config
import os

# Main function - sets up a ControlCenter object and lets it do its thing
if __name__ == "__main__":
    if Config.SERVOS_ACTIVE or Config.ULTRASONIC_ACTIVE: os.system("sudo pigpiod")
    cc = ControlCenter()
    try:
        cc.run()
    except:
        os.system("sudo killall pigpiod")
        cc.shutDown()