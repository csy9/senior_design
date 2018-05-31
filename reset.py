#! /usr/bin/python2

from Motor import Motor
from time import sleep

motor = Motor()

# Set forward position
motor.move(True, 0.4)
try:
    while True:
        pass
except KeyboardInterrupt:
    motor.stop()

# Set backwards position
motor.move(False, 0.8)
try:
    while True:
        pass
except KeyboardInterrupt:
    motor.stop()
