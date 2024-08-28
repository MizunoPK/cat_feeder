from ControlCenter import ControlCenter
from Config import Config
import os
os.system("sudo killall pigpiod")
os.system("sudo pigpiod")

# Main function - sets up a ControlCenter object and lets it do its thing
if __name__ == "__main__":
    cc = ControlCenter()
    try:
        cc.run()
    except:
        os.system("sudo killall pigpiod")
        cc.shutDown()