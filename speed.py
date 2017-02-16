import datetime
import imutils
import time
import cv2
import numpy as np
import sys

# construct the argument parser and parse the arguments


focal_const = 1.10825
width = float(sys.argv[1])*1.10825

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
        #1.4
        if car_in_frame and variation > .1:
            frame_count = frame_count + 1
        elif not car_in_frame and variation > .1:
            car_in_frame = True
            frame_count = 1
        elif car_in_frame:
            if frame_count > 10:
                print(frame_count)
                print(width)
                print((frame_count/30.0))
                meters_per_second = width/(frame_count/30.0)
                miles_per_hour = ((meters_per_second*360000)/160934.4)
                #if miles_per_hour > 20:
                print(str(meters_per_second) + "m/s")
                print(str(miles_per_hour) + "mph")
                frames_to_pass.append(frame_count)

            car_in_frame = False
            frame_count = 0
        frames_list.pop()
        prev_frame = frame
        
    frames_list.insert(0,frameDeltaAvg)
