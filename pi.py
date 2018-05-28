#! /usr/bin/python2
# Raspberry Pi Interface
# Senior Design Group 4
# Casey O'Neill

import RPi.GPIO as gpio
import time

class Pi(object):
    """ Class designed for use on a Raspberry Pi 2.
        Simplifies use cases of having a single PWM and Digital pin.
    """
    def __init__(self, digouts=[], pwmouts=[]):
        """ digouts expect a list of pairs:
                (int, str)
            where int is a valid pin # and str is 'out' or 'in'.

            pwmouts expects a list of pairs:
                (int, int)
            where the first int is a valid pin #
            and the second is a valid frequency.
        """
        # Use the Pi's pin numbering scheme
        gpio.setmode(gpio.BOARD)

        # List of digital pins
        self.digpins = [pin[0] for pin in digouts]

        # Mapping of pwm pins
        self.pwmpins = {}

        # Initialize all digital outputs
        for (digpin, mode) in digouts:
            if mode == 'in':
                gpio.setup(digpin, gpio.OUT)
            elif mode == 'out':
                gpio.setup(digpin, gpio.IN)
            else:
                raise Exception('Invalid digital pin mode supplid.')

        # Initialize pwm outputs
        for (pwmpin, freq) in pwmouts:
            gpio.setup(pwmpin, gpio.OUT)
            self.pwmpins[pwmpin] = gpio.PWM(pwmpin, freq)

    def setdigout(self, pin, val):
        gpio.setup(pin, val);

    def setpwm(self, pin, dutycycle):
        """ """
        # Ensure a valid duty cycle is supplied
        if dutycycle < 0 or dutycycle > 100:
            raise Exception('Duty cycle value must be between 0 and 100.')
        if pin in self.pwmpins:
            self.pwmpins[pin].ChangeDutyCycle(dutycycle)
        else:
            raise Exception('Supplied pwm pin number not set up for pwm.')

    def pwmstart(self, pin, dutycycle):
        p = self.pwmpins[pin]
        p.start(dutycycle)

if __name__ == "__main__":
    digouts = [(11, 'out')]
    pwmouts = [(12, 500000)]
    pi = Pi(digouts, pwmouts)
    pi.setdigout(11, 1)
    pi.pwmstart(12, 90)
    time.sleep(5)
