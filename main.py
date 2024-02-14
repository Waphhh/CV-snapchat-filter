import cv2
import dlib
import math
import numpy as np
import filters as ft
import tkinter as tk
import gui

root = tk.Tk()

def tkinter_thread_func(root):
    errorWindow = gui.errorButton()
    root.destroy()
    errorWindow.mainloop()

# Open a video capture object (camera index 0)
cap = cv2.VideoCapture(0)

detector, predictor = ft.loadModel()

errorCount = 0

errorFlag = False

while True:
    faces, gray, frame = ft.videoCaptureToGrayScale(cap, detector)

    if len(faces) == 0:
        errorCount += 1
        print(f"no face detected {errorCount}")
        if errorCount % 20 == 0:
            errorFlag = True

    if errorFlag:
        tkinter_thread_func(root)
        print("test")
        root = tk.Tk()
        errorFlag = False
        continue

    else:
        for face in faces:

            x, y, w, h, middle_of_eyes, tip_of_nose = ft.extractCoordinatesOfFacialLandmarks(face, gray, predictor)

            rotation_angle = ft.calculate_rotation_angle(tip_of_nose, middle_of_eyes)

            # Getting the image to overlay
            eyeImage = ft.loadImageToOverlay("mask.png")
            noseImage = ft.loadImageToOverlay("red_nose.png")

            frame = ft.overlayImage(frame, eyeImage, middle_of_eyes[0], middle_of_eyes[1], rotation_angle, 1, 20)
            frame = ft.overlayImage(frame, noseImage, tip_of_nose[0], tip_of_nose[1], rotation_angle, 0.4)
            
            frame = ft.overlaySSTLogo(frame)

    # Display the result
    cv2.imshow('PhotoBooth', frame)

    # Break the loop if 'Esc' key is pressed
    if cv2.waitKey(1) == 27:
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
