import datetime
import imutils
import time
import cv2
import numpy as np
import sys

#ratio between camera's feild of view and distance from the plane to the camera. In reality this might not be constant, but it certainly won't be the limiting factor in precision.

focal_const = 1.10825

#takes distance from camera as an argument and determines width of feild of view useing the ratio. 
width = float(sys.argv[1])*1.10825

camera = cv2.VideoCapture(1)
time.sleep(0.25)


# initialize the first frame in the video stream
firstFrame = None


# loop over the frames of the video
car_in_frame = False
frame_count = 0
frames_to_pass = []

prev_frame = None

while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    (grabbed, frame) = camera.read()
    
    if prev_frame is None:
        prev_frame = frame
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(prev_frame, frame)
    frameDeltaAvg = np.average(frameDelta)

    if car_in_frame and frameDeltaAvg > 3:
        frame_count = frame_count + 1
    elif not car_in_frame and frameDeltaAvg > 3:
        car_in_frame = True
        frame_count = 1
    elif car_in_frame:
        if frame_count > 5:
            print(frame_count)
            print(width)
            print((frame_count/30.0))
            meters_per_second = width/(frame_count/30.0)
            miles_per_hour = ((meters_per_second*360000)/160934.4)
            if miles_per_hour > 1:
                print(str(meters_per_second) + "m/s")
                print(str(miles_per_hour) + "mph")
                frames_to_pass.append(frame_count)
            
        car_in_frame = False
        frame_count = 0

    prev_frame = frame