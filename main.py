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

# These 2 libraries used for memory management
import gc
import resource

# # Get memory usage in bytes
# mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

# # Convert to megabytes for easier reading
# mem_usage_mb = mem_usage / (1024 * 1024)

# print(f"Memory usage: {mem_usage_mb:.2f} MB")

# wierd reccursions occur that exceed the default limit
# this just lets it occur
sys.setrecursionlimit(1000000000)

# All the data for each prop
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
            "offset": 150
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

# Opens the gui when no face is detected
def errorGUI():
    errorWindow = gui.errorButton()
    errorWindow.mainloop()

# Paths to images
headImagesPaths = ["assets/mask.png", "assets/swag.png", "assets/birthday_hat.png", "assets/no_photo.png"]
noseImagesPaths = ["assets/red_nose.png", "assets/pig_nose.png", "assets/nose.png", "assets/no_photo.png"]
themesPaths = ["assets/cartoon.jpeg", "assets/sketch.jpeg", "assets/vintage.jpeg", "assets/no_photo.png"]

# Specify grid dimensions for prop selection
rows = 2
cols = 2

# Opening of selection GUI
root = gui.ImageGrid(headImagesPaths, rows, cols)
root.mainloop()
selectedHead = root.return_selected_image() # Handling of choice

# Clear the tk window
root = None

# Short delay
time.sleep(0.5)

# Opening of selection GUI
root = gui.ImageGrid(noseImagesPaths, rows, cols)
root.mainloop()
selectedNose = root.return_selected_image() # Handling of choice

# Clear the tk window
root = None

# Short delay
time.sleep(0.5)

# Opening of selection GUI
root = gui.ImageGrid(themesPaths, rows, cols)
root.mainloop()
selectedTheme = root.return_selected_image() # Handling of choice

# Identifying the choice
headData = assetData["head"][selectedHead]
noseData = assetData["nose"][selectedNose]

# clear up memory
time.sleep(0.5) # Short delay
del root
del headImagesPaths
del noseImagesPaths
del themesPaths

gc.collect()

# Disabling tk default root
tk.NoDefaultRoot()

# Open a video capture object (camera index 0)
cap = cv2.VideoCapture(0)

# Load the model
detector, predictor = ft.loadModel()

# Define error counter
errorCount = 0

# Define error flag
errorFlag = False

while True:
    faces, gray, frame = ft.videoCaptureToGrayScale(cap, detector) # extracting faces, grayscale and frame from the cam footage

    # Checking if no faces are detected
    if len(faces) == 0:
        errorCount += 1
        print(f"no face detected {errorCount}")
        # Checks if for 20 frames no faces have been detected
        if errorCount % 20 == 0:
            errorFlag = True

    # Triggers popup if for 20 frames no faces were detected
    if errorFlag:
        errorGUI()
        errorFlag = False # Reset flag
        continue
    else:
        # Iterating through all faces detected
        for face in faces:

            # Key landmarks of face
            x, y, w, h, middle_of_eyes, tip_of_nose = ft.extractCoordinatesOfFacialLandmarks(face, gray, predictor)

            # Face deegree of rotation
            rotation_angle = ft.calculate_rotation_angle(tip_of_nose, middle_of_eyes)

            # Checks if no prop was selected
            if headData != None:
                # Loads and overlays the prop
                headImage = ft.loadImageToOverlay(headData["name"])
                frame = ft.overlayImage(frame, headImage, middle_of_eyes[0], middle_of_eyes[1], rotation_angle, headData["scaleFactor"], headData["offset"])
            
            # Checks if no prop was selected
            if noseData != None:
                # Loads and overlays the prop
                noseImage = ft.loadImageToOverlay(noseData["name"])            
                frame = ft.overlayImage(frame, noseImage, tip_of_nose[0], tip_of_nose[1], rotation_angle, noseData["scaleFactor"], noseData["offset"])

    # Checks for theme selected and enables it
    if selectedTheme == 0:
        frame = ft.cartooning(frame)
    elif selectedTheme == 1:
        frame = ft.pencilSketchFilter(frame)
    elif selectedTheme == 2:
        frame = ft.vintageTheme(frame)

    # Always put the sst logo 
    frame = ft.overlaySSTLogo(frame)

    # Display the result
    cv2.imshow("PhotoBooth", frame)

    # Break the loop if esc key is pressed
    if cv2.waitKey(1) == 27:
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()

# File name for captures
fileNameInitial = "Captures/captured photo.jpg"
fileName = fileNameInitial

count = 1 # Misc counter

# Renames the file name if it alread exists
while os.path.exists(fileName):
    fileName = fileNameInitial
    fileName = fileName.split(".")
    fileName[-2] += f" ({count})"
    fileName = ".".join(fileName)
    count += 1

# Saves the final frame as an image
cv2.imwrite(fileName, frame)

# Short delay
time.sleep(0.5)

# Opens saved image, esc to close
saved_image = cv2.imread(fileName)
cv2.imshow("Saved image", saved_image)
cv2.waitKey(0)
