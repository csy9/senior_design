#! /usr/bin/python2
# Raspberry Pi Motor Interface
# Senior Design Group 4
# Casey O'Neill

import RPi.GPIO as gpio
from time import sleep

class Motor(object):
    """ Class designed for use on a Raspberry Pi 2.
        Simplifies use cases of having a single PWM and Digital pin for motor.
    """
    def __init__(self, digpin=11, pwmpin=12, pwmfreq=5000):
        """ digout expect an integer pin number.
            pwmpin expects an integer pin number.
            pwmfreq expects a valid frequency.
        """
        # Use the Pi's pin numbering scheme
        gpio.setmode(gpio.BOARD)

        # Initialize digital output pin (direction)
        self.digpin = digpin
        gpio.setup(digpin, gpio.OUT)
        gpio.output(digpin, False)

        # Initialize pwm output pin (speed)
        self.pwmpin = pwmpin
        gpio.setup(pwmpin, gpio.OUT)
        self.pwm = gpio.PWM(pwmpin, pwmfreq)
        self.pwm.start(0)

    def __del__(self):
        """ Switch ports back to inputs before leaving, for safety. """
        self.pwm.stop()
        gpio.cleanup()

    def readDirection(self):
        """ Read current direction. """
        return gpio.input(self.digpin)

    def setDirection(self, direction):
        """ Set digital output to True/False (true -> towards tank) """
        if direction != gpio.input(self.digpin):
            gpio.output(self.digpin, direction)
            sleep(0.5)

    def changeDirection(self):
        """ Change the direction of the motor. """
        gpio.output(self.digpin, not gpio.input(self.digpin))
        sleep(0.5)

    def setSpeed(self, speed):
        """ Set PWM output to specified duty cycle.
            Maps (0,1) -> (20,60) for safety.
        """
        scaled = int(40*speed + 20)
        self.pwm.ChangeDutyCycle(scaled)

    def move(self, direction, speed):
        """ Set direction and speed. """
        self.setDirection(direction)
        sleep(0.1)
        self.setSpeed(speed)

    def stop(self):
        """ Stop moving the motor. """
        self.pwm.ChangeDutyCycle(0)
