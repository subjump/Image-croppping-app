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

## Code Explanation

- `ImageCropperApp`: Main class for the image cropping application.
  - `__init__(self, root)`: Initializes the GUI components and binds events.
  - `center_window(self, window, width, height)`: Centers the application window on the screen.
  - `load_image(self)`: Loads an image from the filesystem.
  - `display_image(self)`: Displays the loaded image on the canvas.
  - `update_scaled_image(self)`: Resizes the image to fit within the window.
  - `draw_image_on_canvas(self)`: Draws the resized image on the canvas.
  - `reset_canvas(self)`: Resets the canvas and clears any drawings.
  - `on_button_press(self, event)`: Handles the event when the mouse button is pressed on the canvas.
  - `on_mouse_drag(self, event)`: Handles the event when the mouse is dragged over the canvas.
  - `on_button_release(self, event)`: Handles the event when the mouse button is released on the canvas.
  - `crop_image(self)`: Crops the image based on the selected rectangle.
  - `show_cropped_image(self, cropped_image)`: Displays the cropped image in a new window.
  - `save_image(self, cropped_image)`: Saves the cropped image to the filesystem.
  - `on_window_resize(self, event)`: Redraws the image on the canvas when the window is resized.
