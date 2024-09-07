#!/usr/bin/env python3
########################################################################
# Filename    : Sweep.py
# Description : Servo sweep
# Author      : www.freenove.com
# modification: 2023/05/12
########################################################################
import os
# os.system("sudo pigpiod")
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
import time

my_factory = PiGPIOFactory() 
myGPIO=21
SERVO_DELAY_SEC = 0.01 
myCorrection=0.0
maxPW=(2.5+myCorrection)/1000
minPW=(0.5-myCorrection)/1000
servo =  AngularServo(myGPIO,initial_angle=0,min_angle=0, max_angle=270,min_pulse_width=minPW,max_pulse_width=maxPW,pin_factory=my_factory)

def loop():
    while True:
        for angle in range(0, 271, 1):   # make servo rotate from 0 to 180 deg
            servo.angle = angle
            time.sleep(SERVO_DELAY_SEC)
        time.sleep(3)
        for angle in range(270, -1, -1): # make servo rotate from 180 to 0 deg
            servo.angle = angle
            time.sleep(SERVO_DELAY_SEC)
        time.sleep(3)

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        servo.close()
        # os.system("sudo killall pigpiod")
        print("Ending program")