import tkinter as tk
from tkinter import filedialog, messagebox
from screeninfo import get_monitors
from image_cropper import ImageCropper
import utils


class ImageCropperApp:
    def __init__(self, root):
        """
        Initializes the ImageCropperApp, setting up the UI components and event bindings.
        """
        self.root = root
        self.root.title("Image Cropper")
        self.root.geometry("800x600")
        utils.center_window(self.root, 800, 600)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, cursor="cross")
        self.canvas.pack(fill="both", expand=True)

        self.cropper = ImageCropper(self.canvas, get_monitors()[0])

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill="x", side=tk.BOTTOM, pady=10)

        self.load_button = tk.Button(self.button_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.crop_button = tk.Button(self.button_frame, text="Crop Image",
                                     command=self.cropper.crop_image, state=tk.DISABLED)
        self.crop_button.pack(side=tk.RIGHT, padx=10)

        self.canvas.bind("<ButtonPress-1>", self.cropper.on_button_press)
        self.canvas.bind("<B1-Motion>", self.cropper.on_mouse_drag)

        self.root.bind("<Configure>", self.on_window_resize)

    def load_image(self):
        """
        Loads an image file(.jpg, .jpeg) and displays it on the canvas.
        """
        self.cropper.reset_canvas()
        self.cropper.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg")]
        )
        if self.cropper.image_path:
            try:
                self.cropper.load_image()
                self.crop_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

    def on_window_resize(self, _event):
        """
        Redraws the image on canvas when the window is resized.
        """
        self.cropper.draw_image_on_canvas()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropperApp(root)
    root.mainloop()
