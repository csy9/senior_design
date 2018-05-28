#!/usr/bin/python2

import os
import subprocess
import cv2 as cv

class Tracker(object):
    def __init__(self, filename):
        """ Initializes MIL tracker object on a stream of images named filename """
        self.filename = filename
        # Take initial image (at 1/4th size) and save dimensions
        img = self._capture()
        self.h = img.shape[0]
        self.w = img.shape[1]

        # Initialize tracker
        box = cv.selectROI(img, False)
        self.tracker = cv.TrackerMedianFlow_create()
        self.tracker.init(img, box)

        # Create window for displaying images to
        self.window = cv.namedWindow('window', cv.WINDOW_AUTOSIZE)

    def _capture(self):
        """ Capture image and save to 'img.jpg'; read result """
        # Capture new image
        cmd = ['gphoto2', '--capture-image-and-download', '--force-overwrite',
               '--filename', self.filename]
        subprocess.check_output(cmd)
        # Open color image and return data, scaled back in each dimension
        img = cv.imread(self.filename, 1)
        return cv.resize(img, (0,0), fx=0.2, fy=0.2)

    def track(self):
        """ Capture an image and update the location of the tracked object """
        # Update tracking frame
        frame = self._capture()
        ok, box = self.tracker.update(frame)
        print ok, box

        # Draw bounding box
        if ok:
            x,y,w,h = map(int, box)
            img = cv.rectangle(frame, (x,y), (x+w,y+h), 255, 2)
        else:
            img = cv.putText(frame, 'Tracking failure detected', (100,80),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)

        # Draw frame and return box coords
        cv.imshow('window', img)
        if ok:
            return (x, y, w, h)
        else:
            return None


if __name__ == '__main__':
    # Open file for tracking
    filename = 'img.jpg'
    # Start tracking
    tracker = Tracker(filename)
    while True:
        tracker.track()
        if (cv.waitKey(60) & 0xff == 27):
            break
