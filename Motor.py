#! /usr/bin/python2
# Raspberry Pi Motor Interface
# Senior Design Group 4
# Casey O'Neill

from time import sleep
import RPi.GPIO as gpio

class Motor(object):
    """ Class designed for use on a Raspberry Pi 2.
        Simplifies use cases of having a single PWM and Digital pin for motor.
    """
    def __init__(self, digpin=11, pwmpin=12, pwmfreq=50):
        """ digout expect an integer pin number.
            pwmpin expects an integer pin number.
            pwmfreq expects a valid frequency.
        """
        # Use the Pi's pin numbering scheme
        gpio.setmode(gpio.BOARD)

        # Initialize digital output pin (direction)
        self.digpin = digpin
        gpio.setup(digpin, gpio.OUT)
#         gpio.output(digpin, False)

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

    def changeDirection(self):
        """ Change the direction of the motor. """
        gpio.output(self.digpin, not gpio.input(self.digpin))

    def setSpeed(self, speed):
        """ Set PWM output to specified duty cycle.
            Maps (0,1) -> (40,60) for safety.
        """
        scaled = int(20*speed + 40)
        self.pwm.ChangeDutyCycle(scaled)

    def move(self, direction, speed):
        """ Set direction and speed.
            The pauses are to avoid crossing signals with the shitty H bridge.
        """
        self.setDirection(direction)
        sleep(0.1)
        self.setSpeed(speed)
        sleep(0.1)

    def stop(self):
        """ Stop moving the motor. """
        self.pwm.ChangeDutyCycle(0)

    def bump(self, direction, speed, duration):
        """ Move for a specified amount of time. """
        self.move(direction, speed)
        sleep(duration)
        self.stop()

    def wiggle(self):
        """ Every day we stray further from god's light """
        sleep(0.1)
        self.move(True, 0.5)
        sleep(0.5)
        self.move(False, 0.5)
        sleep(0.5)
        self.stop()
        self.setDirection(True)


    def finish(self):
        """ Finish using the motor. """
        self.pwm.stop()
