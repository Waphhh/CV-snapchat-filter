# CV-snapchat-filter

A simple "snapchat" filter using openCV to detect facial landmarks to pinpoint placements for the assets to be placed on the face

### DISCLAIMER

This program runs into a lot of memory issues mainly due to tkinter, a lot of memory is advised, common errors:
* trace trap
* bus error
* segmentation fault
If those occur try again but slower

#### Distribution of labour

Main logical flow and video capturing and editting done by Raphael
UI elements and sourcing of assets done by vernon

### Requirements

```sh
pip install -r requirements.txt
```

Navigate into the directory where this is located

Then run main.py

```sh
python3 main.py
```

### How to use

When you run main.py, just select your props and theme and the camera will open.
Once you are satisfied with the pose, press the esc key to save.
The image will save to the captures file and be opened, press esc again to close it.

### Acknowledgements

Assets were taken from various places
no_photo.png was taken from flaticon