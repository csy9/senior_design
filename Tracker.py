#! /usr/bin/python2
# Object Tracking Interface
# Senior Design Group 4
# Casey O'Neill

import subprocess
import cv2 as cv

class Tracker(object):
    def __init__(self, filename):
        """ Initializes tracker object on a stream of images named filename """
        self.filename = filename
        self.h = 0
        self.w = 0
        self.initbox = None
        self.tracker = None

    def setTrackpoint(self):
        # Take initial image and save dimensions
        img = self._capture()
        self.h = img.shape[0]
        self.w = img.shape[1]

        # Initialize tracker
        box = cv.selectROI(img, False)
        self.initbox = box
        self.tracker = cv.TrackerMIL_create()
        self.tracker.init(img, box)

        # Create window for displaying images to
        self.window = cv.namedWindow('win', cv.WINDOW_AUTOSIZE)

    def _capture(self):
        """ Capture image and save to 'img.jpg'; read result """
        # Capture new image
        cmd = ['gphoto2', '--capture-image-and-download', '--force-overwrite',
               '--set-config', 'autofocus=1',
               '--filename', self.filename]
        subprocess.check_output(cmd)
        # Open color image and return data, scaled back in each dimension
        img = cv.imread(self.filename, 1)
        return cv.resize(img, (0,0), fx=0.2, fy=0.2)

    def update(self):
        """ Capture an image and update the location of the tracked object """
        # Update tracking frame
        frame = self._capture()
        ok, box = self.tracker.update(frame)
        print 'Object found: ' + str(ok)

        # Draw bounding box
        if ok:
            x,y,w,h = map(int, box)
            img = cv.rectangle(frame, (x,y), (x+w,y+h), 255, 2)
            return (img, (x, y, w, h))
        else:
            img = cv.putText(frame, 'Tracking failure detected', (100,80),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)
            return (img, None)
