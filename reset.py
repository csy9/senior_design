#! /usr/bin/python2

from Pi import Pi
from time import sleep

pi = Pi()

# Set forward position
pi.move(True, 0.4)
try:
    while True:
        pass
except KeyboardInterrupt:
    pi.stop()

# Set backwards position
pi.move(False, 0.4)
try:
    while True:
        pass
except KeyboardInterrupt:
    pi.stop()
