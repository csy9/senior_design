#!/usr/bin/python2

import numpy as np
import cv2 as cv

def bgSub(filename):
    # Open file
    vc = cv.VideoCapture(filename)
    # Set up subtractor
    fgbg = cv.createBackgroundSubtractorMOG2(detectShadows = False)

    while True:
        ret, frame = vc.read()
        frame = cv.resize(frame, (0,0), fx=0.5, fy=0.5)
        fgmask = fgbg.apply(frame)
        cv.imshow('frame', fgmask)
        if (cv.waitKey(30) & 0xff) == 27:
            break

    vc.release()
    cv.destroyAllWindows()


def meanshift(filename):
    # Open file
    vc = cv.VideoCapture(filename)
    ret, frame = vc.read()
    frame = cv.resize(frame, (0,0), fx=0.5, fy=0.5)

    # Define initial tracking rectangle
    r,c,h,w = 143, 392, 25, 15
    track_window = (c,r,w,h)

    # Set up ROI for tracking
    roi = frame[r:r+h, c:c+w]
    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv_roi, np.array((0.,60.,32.)), np.array((180.,255.,255.)))
    roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0,180])
    cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)

    # Set up termination criteria
    term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )

    # Loop through each frame of video
    while True:
        ret, frame = vc.read()
        if ret:
            # Perform manipulations
            frame = cv.resize(frame, (0,0), fx=0.5, fy=0.5)
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            dst = cv.calcBackProject([hsv], [0], roi_hist, [0,180], 1)

            # Apply meanshift to get to the new target location
            ret, track_window = cv.meanShift(dst, track_window, term_crit)

            # Draw on image
            x,y,w,h = track_window
            img = cv.rectangle(frame, (x,y), (x+w,y+h), 255, 2)
            cv.imshow('img', img)

            if (cv.waitKey(60) & 0xff == 27):
                break
        else:
            break

    # Release video streams
    vc.release()
    cv.destroyAllWindows()


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
