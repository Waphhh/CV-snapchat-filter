import cv2
import dlib
import math
import numpy as np
import filters as ft

# Open a video capture object (camera index 0)
cap = cv2.VideoCapture(0)

# Initialize a list to store points for each part of the face
facial_points_list = []

detector, predictor = ft.loadModel()

errorCount = 0

while True:
    faces, gray, frame = ft.videoCaptureToGrayScale(cap, detector)

    for face in faces:

        try:
            x, y, w, h, middle_of_eyes, tip_of_nose = ft.extractCoordinatesOfFacialLandmarks(face, gray, predictor)
        # Catch the error if no face is detected
        except UnboundLocalError:
            # Incriment the error counter and print error count
            errorCount += 1
            print(f"no face detected {errorCount}")
            # Blank the screen
            frame[:] = 0
            cv2.imshow('PhotoBooth', frame)
            cv2.waitKey(1)
            continue

        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.circle(frame, middle_of_eyes, 2, (0, 0, 255), 2)

        rotation_angle = ft.calculate_rotation_angle(tip_of_nose, middle_of_eyes)
        # print("Rotation Angle:", rotation_angle)

        # Getting the image to overlay
        eyeImage = ft.loadImageToOverlay("wrmask.png")
        noseImage = ft.loadImageToOverlay("red_nose.png")

        frame = ft.overlayImage(frame, eyeImage, middle_of_eyes[0], middle_of_eyes[1], rotation_angle, 0.4)
        frame = ft.overlayImage(frame, noseImage, tip_of_nose[0], tip_of_nose[1], rotation_angle, 0.4)
        
    # Display the result
    cv2.imshow('PhotoBooth', frame)

    # Break the loop if 'Esc' key is pressed
    if cv2.waitKey(1) == 27:
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()