'''
Jawline:
Points 0-16: Jawline, starting from the left side of the face (0) and moving to the right side (16).

Right Eyebrow:
Points 17-21: Right eyebrow.

Left Eyebrow:
Points 22-26: Left eyebrow.

Nose Bridge:
Points 27-30: Nose bridge.

Nose Base:
Points 31-35: Bottom of the nose.

Right Eye:
Points 36-41: Right eye.

Left Eye:
Points 42-47: Left eye.

Outer Lips:
Points 48-59: Outer lips.

Inner Lips:
Points 60-67: Inner lips.
'''

import cv2
import dlib
import math
import numpy as np

# Open a video capture object (camera index 0)
cap = cv2.VideoCapture(0)

# Initialize a list to store points for each part of the face
facial_points_list = []

def loadModel():
    # Make the variables global
    global detector, predictor

    # Load the pre-trained face detection model from dlib
    detector = dlib.get_frontal_face_detector()

    # Load the facial landmarks predictor
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def loadImageToOverlay(imageName):
    # Load your image with transparency using cv2.IMREAD_UNCHANGED flag
    image_to_overlay = cv2.imread(str("assets/" + imageName), cv2.IMREAD_UNCHANGED)
    return image_to_overlay

def videoCaptureToGrayScale(cap):
    # Read the frame from the camera
    ret, frame = cap.read()

    # Break if error
    if not ret:
        print("ERROR???")

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces using the dlib face detector
    faces = detector(gray)

    return faces, gray, frame

def extractCoordinatesOfFacialLandmarks(faces, gray):

    for i, face in enumerate(faces, 1):
        landmarks = predictor(gray, face)

        # Extract points of all the landmarks
        all_points = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(68)], dtype=np.int32)
        # Extract points of the jawline (index 0 to 16)
        jawline = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(0, 16)], dtype=np.int32)
        # Extract points of the right eyebrow (index 17 to 21)
        right_eyebrow = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(17, 21)], dtype=np.int32)
        # Extract points of the left eyebrow (index 22 to 26)
        left_eyebrow = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(22, 26)], dtype=np.int32)
        # Extract points of the nose bridge (index 27 to 30)
        nose_bridge = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(27, 30)], dtype=np.int32)
        # Extract points of the nose base (index 31 to 35)
        nose_base = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(31, 35)], dtype=np.int32)
        # Extract points of the right eye (index 36 to 41)
        right_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 41)], dtype=np.int32)
        # Extract points of the left eye (index 42 to 47)
        left_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 47)], dtype=np.int32)
        # Extract points of the outer lips (index 48 to 59)
        outer_lips = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(48, 59)], dtype=np.int32)
        # Extract points of the inner lips (index 60 to 67)
        inner_lips = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(60, 67)], dtype=np.int32)

        # Extract tip of nose coordinates
        tip_of_nose = (landmarks.part(30).x, landmarks.part(30).y)
        # Extract middle of the eyes coordiantes
        middle_of_eyes = (landmarks.part(27).x, landmarks.part(27).y)

        # Extract edges of the face
        x, y, w, h = face.left(), face.top(), face.width(), face.height()

    return x, y, w, h, middle_of_eyes, tip_of_nose

def overlayImageEyes(background, foreground, x_face, y_face, rotation_angle, scale_factor=1.85):
    bg_h, bg_w, bg_channels = background.shape
    
    # Scale up the foreground image
    foreground_scaled = cv2.resize(foreground, None, fx=scale_factor, fy=scale_factor)
    fg_h, fg_w, fg_channels = foreground_scaled.shape

    # Flip the image vertically
    foreground_scaled = cv2.flip(foreground_scaled, 0)

    # Calculate offsets based on the face coordinate point
    x_offset = int(x_face - fg_w / 2)
    y_offset = int(y_face - fg_h / 2) - 1

    # Ensure the overlay image does not extend beyond the background image
    x_offset = max(0, min(bg_w - fg_w, x_offset))
    y_offset = max(0, min(bg_h - fg_h, y_offset))

    w = min(fg_w, bg_w - x_offset)
    h = min(fg_h, bg_h - y_offset)

    if w < 1 or h < 1: return

    # Rotate the foreground image
    M = cv2.getRotationMatrix2D((fg_w / 2, fg_h / 2), -2 * rotation_angle, 1)
    foreground_rotated = cv2.warpAffine(foreground_scaled, M, (fg_w, fg_h))

    # Clip foreground and background images to the overlapping regions
    foreground_cropped = foreground_rotated[:h, :w]
    background_subsection = background[y_offset:y_offset + h, x_offset:x_offset + w]

    # Separate alpha and color channels from the foreground image
    foreground_colors = foreground_cropped[:, :, :3]
    alpha_channel = foreground_cropped[:, :, 3] / 255  # 0-255 => 0.0-1.0

    # Construct an alpha_mask that matches the image shape
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

    # Combine the background with the overlay image weighted by alpha
    composite = background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask

    # Overwrite the section of the background image that has been updated
    background[y_offset:y_offset + h, x_offset:x_offset + w] = composite

    return background

def calculate_rotation_angle(nose_middle, eye_middle):

    # Use atan2 function to calculate face rotation https://en.wikipedia.org/wiki/Atan2
    delta_y_nose_eye = nose_middle[1] - eye_middle[1]
    delta_x_nose_eye = nose_middle[0] - eye_middle[0]
    radians = math.atan2(delta_y_nose_eye, delta_x_nose_eye)

    return math.degrees(radians)

loadModel()

errorCount = 0

while True:
    faces, gray, frame = videoCaptureToGrayScale(cap)

    # Clear the list of lip points for each new frame
    facial_points_list = []

    try:
        x, y, w, h, middle_of_eyes, tip_of_nose = extractCoordinatesOfFacialLandmarks(faces, gray)
    # Catch the error if no face is detected
    except UnboundLocalError:
        # Incriment the error counter and print error count
        errorCount += 1
        print(f"no face detected {errorCount}")
        # Blank the screen
        frame[:] = 0
        cv2.imshow('Testing time owo', frame)
        cv2.waitKey(1)
        continue

    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.circle(frame, middle_of_eyes, 2, (0, 0, 255), 2)

    rotation_angle = calculate_rotation_angle(tip_of_nose, middle_of_eyes)
    print("Rotation Angle:", rotation_angle)

    # Getting the image to overlay
    image = loadImageToOverlay("swag.png")

    frame = overlayImageEyes(frame, image, middle_of_eyes[0], middle_of_eyes[1], rotation_angle)
    
    # Display the result
    cv2.imshow('Testing time owo', frame)

    # Break the loop if 'Esc' key is pressed
    if cv2.waitKey(1) == 27:
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
