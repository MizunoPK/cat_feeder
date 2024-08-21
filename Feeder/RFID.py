#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        print("Place your tag to write")
        id = reader.read()
        print(id)
finally:
        GPIO.cleanup()