#! /usr/bin/python2
# Raspberry Pi Interface
# Senior Design Group 4
# Casey O'Neill

import RPi.GPIO as gpio

class Pi(object):
    """ Class designed for use on a Raspberry Pi 2.
        Sets everything up and makes it easier to
        control devices with the GPIO pins.
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
        try:
            for (digpin, mode) in digouts:
                if mode == 'in':
                    gpio.setup(digpin, gpio.OUT)
                elif mode == 'out':
                    gpio.setup(digpin, gpio.IN)
                else:
                    raise Exception('Invalid digital pin mode supplid.')
        except:
            raise Exception('Error when initializing digital pin modes. \
                             Verify that the supplied pin numbers are correct.')

        # Initialize pwm outputs
        try:
            for (pwmpin, freq) in pwmouts:
                self.pwmpins[pwmpin] = gpio.pwm(pwmpin, freq)
        except:
            raise Exception('Error when initializing pwm pin modes. \
                             Verify that the supplied pin numbers and \
                             frequencies are correct.')

    def setpwm(self, pin, dutycycle):
        """ """
        # Ensure a valid duty cycle is supplied
        if dutycycle < 0 or dutycycle > 100:
            raise Exception('Duty cycle value must be between 0 and 100.')
        if pin in self.pwmpins:
            self.pwmpins[pin].ChangeDutyCycle(dutycycle)
        else:
            raise Exception('Supplied pwm pin number not set up for pwm.')
