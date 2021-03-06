#! /usr/bin/python2
# Control Program (Error correcting)
# Senior Design Group 4
# Casey O'Neill

import cv2 as cv
from math import sqrt, exp
from Motor import Motor
from Tracker import Tracker

class Controller(object):
    """ Implementation of discrete controller for the magnet. """
    def __init__(self, cx=None, cy=None, rad=None):
        self.cx = cx
        self.cy = cy
        self.rad = rad

        # Add Raspberry Pi device
        self.motor = Motor()

        # Initialize tracker, get template/trackpoint
        self.tracker = Tracker('img.jpg')
        if rad is None:
            raw_input('Hit enter to specify template...')
            self._getTemplate()
        raw_input('Hit enter to specify tracking object...')
        self.tracker.setTrackpoint()

        # Make video output writer
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        self.out = cv.VideoWriter('output.avi', fourcc, 1.0, 
                                  (self.tracker.w, self.tracker.h))

    def _getTemplate(self):
        """ Capture image and obtain circle parameters for the trajectory template """
        # Read image
        img = self.tracker._capture()
        # Get satisfying template
        cv.imshow('win', img)
        cv.waitKey(0)
        while True:
            # Prompt for circle center
            center = raw_input('Center of circle ("x,y"): ')
            cx, cy = map(int, center.split(','))
            radius = raw_input('Radius of circle: ')
            # Draw circle
            cpy = img.copy()
            cv.circle(cpy, (cx, cy), int(radius), (0,0,255), 1)
            cv.imshow('win', cpy)
            cv.waitKey(0)
            # Ask if it's all good
            ok = raw_input('Is it ok? (y/n): ')
            if ok == 'y':
                break

        # Write template image, save circle parameters
        cv.imwrite('template.jpg', cpy)
        self.cx = cx
        self.cy = cy
        self.rad = int(radius)

    def distance(self, x, y):
        """ Distance between a point (x,y) and the nearest point
            on the template circle.
        """
        dx = self.cx - x
        dy = self.cy - y
        return abs(sqrt(dx**2 + dy**2) - self.rad)

    def outside(self, x, y):
        """ True if point (x,y) is outside the template circle.
            False otherwise. Magnet should be moved close if True.
        """
        dx = self.cx - x
        dy = self.cy - y
        dc = abs(sqrt(dx**2 + dy**2))
        return dc > self.rad

    def control(self):
        """ Control the motor position to guide magnet along trajectory. """
        # Update box position and compute midpoint
        img, box = self.tracker.update()

        if box is not None:
            # Compute midpoint of box
            x, y, w, h = box
            mx = (x + float(x+w)) / 2
            my = (y + float(y+h)) / 2

            # Compute distance to template, Logistically normalize it to (0,1)
            direc = self.outside(mx, my)
            dist = self.distance(mx, my)
            speed = 1.0 / (1 + exp(-0.1*(dist-50)))
            print 'outside: {0}, dist: {1:.2f}'.format(direc, dist)

            # Move the motor
            self.motor.bump(direc, speed, 1)
            print 'Done moving motor.'

            # Write error to image
            cv.putText(img, 'Error: ' + ('+' if direc else '-') + '{0:.4f}'.format(speed),
                       (40,40), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)
        else:
            # Stop the motor until we regain tracking
            print 'Lost tracking, stopping motor.'
            self.motor.stop()

        # Write image
        cv.circle(img, (self.cx, self.cy), self.rad, (0,0,255), 2)
        self.out.write(img)


if __name__ == "__main__":
    controller = Controller(180, 110, 350)
    try:
        while True:
            controller.control()
    except KeyboardInterrupt:
        controller.motor.finish()
        exit()
