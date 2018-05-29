#! /usr/bin/python2
# Raspberry Pi Interface
# Senior Design Group 4
# Casey O'Neill

import RPi.GPIO as gpio
# import time

class Pi(object):
    """ Class designed for use on a Raspberry Pi 2.
        Simplifies use cases of having a single PWM and Digital pin.
    """
    def __init__(self, digpin=11, pwmpin=12, pwmfreq=5000):
        """ digout expect an integer pin number.
            pwmpin expects an integer pin number.
            pwmfreq expects a valid frequency.
        """
        # Use the Pi's pin numbering scheme
        gpio.setmode(gpio.BOARD)
        # Disable dumb warnings #YOLO
        gpio.setwarnings(False)

        # Initialize digital output pin
        self.digpin = digpin
        gpio.setup(digpin, gpio.OUT)

        # Initialize pwm output pin
        self.pwmpin = pwmpin
        gpio.setup(pwmpin, gpio.OUT)
        self.pwm = gpio.PWM(pwmpin, pwmfreq)
        self.pwm.start(0)

    def dig_write(self, val):
        """ Set digital output to True/False (true -> towards tank) """
        gpio.output(self.digpin, val);

    def pwm_write(self, dutycycle):
        """ Set PWM output to specified duty cycle. """
        self.pwm.ChangeDutyCycle(dutycycle)

    def move(self, direction, speed):
        """ Move the motor with the specified parameters.
            This function maps (0,100) -> (0, 75) so that the motor
            doesn't run on full blast and go off the track.
        """
        gpio.output(self.digpin, direction)
        self.pwm.ChangeDutyCycle(75 * (float(speed)/100))

    def stop(self):
        """ Stop moving the motor. """
        self.pwm.ChangeDutyCycle(0)


# if __name__ == "__main__":
#     pi = Pi()
#     pi.move(False, 100)
#     time.sleep(4)
#     pi.stop()
#     time.sleep(2)
#     pi.move(True, 100)
#     time.sleep(4)
