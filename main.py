import cv2
import dlib
import math
import numpy as np
import filters as ft
import tkinter as tk
import time
import gui
import os
import sys

# wierd reccursions occur that exceed the default limit
# this just lets it occur
sys.setrecursionlimit(1000000000)

assetData = {

    "head": [
        {
            "name": "mask.png",
            "scaleFactor": 1,
            "offset": 20
        },
        {
            "name": "swag.png",
            "scaleFactor": 1.8,
            "offset": 0
        },
        {
            "name": "birthday_hat.png",
            "scaleFactor": 0.6,
            "offset": 300
        },
        None
    ],

    "nose": [
        {
            "name": "red_nose.png",
            "scaleFactor": 0.4,
            "offset": 0
        },
        {
            "name": "pig_nose.png",
            "scaleFactor": 0.15,
            "offset": 0
        },
        {
            "name": "nose.png",
            "scaleFactor": 0.058,
            "offset": 0
        },
        None
    ]
}

def errorGUI():
    errorWindow = gui.errorButton()
    errorWindow.mainloop()

# Paths to images
headImagesPaths = ["assets/mask.png", "assets/swag.png", "assets/birthday_hat.png", "assets/no_photo.png"]
noseImagesPaths = ["assets/red_nose.png", "assets/pig_nose.png", "assets/nose.png", "assets/no_photo.png"]
themesPaths = ["assets/SST_logo.png", "assets/colors.png", "assets/invert.png", "assets/no_photo.png"]

rows = 2
cols = 2

root = gui.ImageGrid(headImagesPaths, rows, cols)
root.mainloop()
selected_head = root.return_selected_image()

root = None

root = gui.ImageGrid(noseImagesPaths, rows, cols)
root.mainloop()
selected_nose = root.return_selected_image()

headData = assetData["head"][selected_head]
noseData = assetData["nose"][selected_nose]

# clear up some memory
root = None

tk.NoDefaultRoot()

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
        errorGUI()
        errorFlag = False
        continue
    else:
        for face in faces:

            x, y, w, h, middle_of_eyes, tip_of_nose = ft.extractCoordinatesOfFacialLandmarks(face, gray, predictor)

            rotation_angle = ft.calculate_rotation_angle(tip_of_nose, middle_of_eyes)

            # headImage = ft.loadImageToOverlay("swag.png")
            # frame = ft.overlayImage(frame, headImage, middle_of_eyes[0], middle_of_eyes[1], rotation_angle, 1.8, 0)

            if headData != None:
                headImage = ft.loadImageToOverlay(headData["name"])
                frame = ft.overlayImage(frame, headImage, middle_of_eyes[0], middle_of_eyes[1], rotation_angle, headData["scaleFactor"], headData["offset"])

            if noseData != None:
                noseImage = ft.loadImageToOverlay(noseData["name"])            
                frame = ft.overlayImage(frame, noseImage, tip_of_nose[0], tip_of_nose[1], rotation_angle, noseData["scaleFactor"], noseData["offset"])

    # Always put the sst logo 
    frame = ft.overlaySSTLogo(frame)

    # Display the result
    cv2.imshow('PhotoBooth', frame)

    # Break the loop if 'Esc' key is pressed
    if cv2.waitKey(1) == 27:
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()

fileNameInitial = "Captures/captured photo.jpg"
fileName = fileNameInitial

count = 1

while os.path.exists(fileName):
    fileName = fileNameInitial
    fileName = fileName.split('.')
    fileName[-2] += f' ({count})'
    fileName = '.'.join(fileName)
    count += 1

cv2.imwrite(fileName, frame)

time.sleep(0.5)

saved_image = cv2.imread(fileName)
cv2.imshow('Saved Image', saved_image)
cv2.waitKey(0)
