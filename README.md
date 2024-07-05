# Image Cropper App

## Description

The Image Cropper App is a simple GUI application for cropping images. It is built using Python's Tkinter library for the GUI and OpenCV for image processing. The application allows users to load an image, select a cropping area, and save the cropped image in 1080x1035 pixels resolution. For this app version program allow to upload image with at least 6000x4000 pixels (straight out of camera image).

## Features

- Load an image from the filesystem.
- Draw a cropping rectangle on the image.
- Crop the image based on the selected area.
- Display the cropped image in a new window.
- Save the cropped image with a specified filename.

## Requirements

- Python 3.x
- OpenCV
- Pillow
- screeninfo

## Installation

1. Clone the repository or download the code files.

2. Install the required Python libraries using pip:
    ```bash
    pip install opencv-python pillow screeninfo
    ```

## Usage

1. Run the application:
    ```bash
    python main.py
    ```

2. Load an image by clicking the "Load Image" button and selecting an image file. The image must have a minimum resolution of 6000x4000 pixels.

3. Draw a cropping rectangle by clicking and dragging the mouse over the image.

4. Click the "Crop Image" button to crop the image. The cropped image will be displayed in a new window.

5. Save the cropped image by clicking the "Save" button in the cropped image window.

