import datetime
import imutils
import time
import cv2
import numpy as np
import sys

# construct the argument parser and parse the arguments


camera = cv2.VideoCapture(1)
time.sleep(0.25)


# initialize the first frame in the video stream
firstFrame = None
# loop over the frames of the video


car_in_frame = False
frame_count = 0
frames_to_pass = []
frames_list = []
prev_frame = None

while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    (grabbed, frame) = camera.read()
    # if the frame could not be grabbed, then we have reached the end
        # of the video
        #if not grabbed:
         #   break

        # resize the frame, convert it to grayscale, and blur it
        #frame = imutils.resize(frame, width=500)

    if prev_frame is None:
        prev_frame = frame
        continue

        # compute the absolute difference between the current frame and
        # first frame
    frameDelta = cv2.absdiff(prev_frame, frame)
    frameDeltaAvg = np.average(frameDelta)
    if len(frames_list) > 10:
        variation = np.std(frames_list)/np.average(frames_list)
        print(variation)
        prev_frame = frame
        frames_list.pop()
        
    frames_list.insert(0,frameDeltaAvg)
