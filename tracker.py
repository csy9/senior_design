#!/usr/bin/python2

import numpy as np
import cv2 as cv

class Tracker():

def track(filename):
    # Open file
    video = cv.VideoCapture(filename)
    w = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv.CAP_PROP_FPS)
    ok, frame = video.read()
    frame = cv.resize(frame, (0,0), fx=0.5, fy=0.5)

    # Set up tracker
    tracker = cv.TrackerMIL_create()
    box = cv.selectROI(frame, False)
    ok = tracker.init(frame, box)

    # Set up output file
    fourcc = cv.VideoWriter_fourcc(*'X264')
    out = cv.VideoWriter('output.avi', fourcc, fps, (w/2, h/2))

    while True:
        ok, frame = video.read()
        if not ok:
            break

        # Update tracking frame
        frame = cv.resize(frame, (0,0), fx=0.5, fy=0.5)
        ok, box = tracker.update(frame)

        # Draw bounding box
        if ok:
            x,y,w,h = map(int, box)
            img = cv.rectangle(frame, (x,y), (x+w,y+h), 255, 2)
        else:
            img = cv.putText(frame, 'Tracking failure detected', (100,80),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)

#         cv.imshow('img', img)
        out.write(img)
        if (cv.waitKey(60) & 0xff == 27):
            break


if __name__ == '__main__':
    # Open file for tracking
    filename = 'vid.mov'
    bgSub(filename)
