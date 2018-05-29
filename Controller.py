#! /usr/bin/python2
# Raspberry Pi Interface
# Senior Design Group 4
# Casey O'Neill

# import Pi
from Tracker import Tracker
import cv2 as cv
import numpy as np

class Controller(object):
    """ Implementation of discrete controller for the magnet. """
    def __init__(self, Kp=1, Ki=0, Kd=0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral = 0
        self.dt = 1
        self.prev_err = 0

        # Wait to get tracking info
        self.tracker = Tracker('img.jpg')
        self.template = self._getTemplate()

        # Set initial midpoint
        x,y,w,h = self.tracker.initbox
        self.prevmidpoint = ((x + x+w)/2, (y + y+h)/2)

#     def _getTemplate(self):
#         """ Capture image and obtain thresholded mask for the trajectory template """
#         # Read image
#         img = self.tracker._capture()
#         # Convert to HSV
#         hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
#         # mask of green (36,0,0) ~ (70, 255,255)
#         mask = cv.inRange(hsv, (36, 0, 0), (70, 255,255))
#         # slice the green
#         imask = mask > 0
#         green = np.zeros_like(img, np.uint8)
#         green[imask] = img[imask]
#         return green

    def _getTemplate(self):
        """ Capture image and obtain thresholded mask for the trajectory template """
        # Read image
        img = self.tracker._capture()
        # Get satisfying template
        win = cv.namedWindow('win', cv.WINDOW_AUTOSIZE)
        cv.imshow('win', img)
        cv.waitKey(0)
        while True:
            # Prompt for circle center
            center = raw_input('Center of circle ("x,y"):')
            cx, cy = map(int, center.split(','))
            radius = raw_input('Radius of circle:')
            # Draw circle
            cpy = img.copy()
            cv.circle(cpy, (cx, cy), int(radius), (0,0,255), 1)
            cv.imshow('win', cpy)
            cv.waitKey(0)
            # Ask if it's all good
            ok = raw_input('Is it ok?')
            if ok == 'y':
                break

        return cpy

 

    def _findError(self):
        # Get tracking information
        ret = self.tracker.update()
        if ret:
            # x,y - upper left coordinates
            x, y, w, h = ret
            # Find midpoint of bounding box
            midpoint = ((x + x+w)/2, (y + y+h)/2)
            # Compute slope to figure out desired dimension of error
            slope = (midpoint[1] - self.prevmidpoint[1]) / float(midpoint[0] - self.prevmidpoint[0])

            # Moving primarily down; compute lateral error
            if slope > 1:
                templatepos = self.template
            else:
                templatepos = self.template


    def pid(self):
        """ Update PID controller """
        err = self._findError()
        self.integral += error * self.dt
        derivative = (err - self.prev_err) / self.dt
        self.prev_err = err
        return self.Kp*err + self.Ki*self.integral + self.Kd*derivative

if __name__ == "__main__":
    controller = Controller()
