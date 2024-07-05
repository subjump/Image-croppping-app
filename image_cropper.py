import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, filedialog


class ImageCropper:
    def __init__(self, canvas, primary_monitor):
        """
        Initializes the ImageCropper with a canvas and primary monitor.
        """
        self.canvas = canvas
        self.primary_monitor = primary_monitor
        self.image = None
        self.image_path = None
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.scaled_image = None

    def load_image(self):
        """
        Loads an image from the specified path and displays it on the canvas.
        """
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            raise ValueError("Could not open or find the image.")

        if self.image.shape[1] < 6000 or self.image.shape[0] < 4000:
            messagebox.showerror(
                "Resolution Error",
                "The selected image has insufficient resolution. Please select an image with at least 6000x4000 pixels."
            )
            return

        self.display_image()

    def display_image(self):
        """
        Updates and draws the image on the canvas.
        """
        if self.image is not None:
            self.update_scaled_image()
            self.draw_image_on_canvas()

    def update_scaled_image(self):
        """
        Scales the image to fit within the primary monitor's dimensions.
        """
        h, w = self.image.shape[:2]

        # Floor division (//) divides the operands and returns the largest whole number \
        # less than or equal to the result.
        max_width = self.primary_monitor.width // 2
        max_height = self.primary_monitor.height // 2

        if w > max_width or h > max_height:
            scale = min(max_width / w, max_height / h)
            dim = (int(w * scale), int(h * scale))
            resized_img = cv2.resize(self.image, dim, interpolation=cv2.INTER_AREA)
        else:
            resized_img = self.image

        image_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        self.scaled_image = ImageTk.PhotoImage(image=image_pil)

    def draw_image_on_canvas(self):
        """
        Draws the scaled image on the canvas.
        """

        if self.scaled_image:
            self.canvas.delete("all")
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            image_width = self.scaled_image.width()
            image_height = self.scaled_image.height()

            x = (canvas_width - image_width) // 2
            y = (canvas_height - image_height) // 2

            self.canvas.create_image(x, y, anchor='nw', image=self.scaled_image)

    def reset_canvas(self):
        """
        Resets the canvas by clearing all drawn items and resetting variables.
        """
        self.canvas.delete("all")
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

    def on_button_press(self, event):
        """
        Handles the button press event to start drawing a rectangle.
        """
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        if self.rect:
            self.canvas.delete(self.rect)

        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
        """
        Handles the mouse drag event to draw and update the rectangle.
        """
        if not self.rect:
            return

        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        width = end_x - self.start_x
        height = (width * 5) / 4

        if end_y < self.start_y:
            height = -height

        self.end_x = self.start_x + width
        self.end_y = self.start_y + height

        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def crop_image(self):
        """
        Crops the selected area from the image and displays the cropped image in a new window.
        """
        if self.image_path and self.start_x is not None and self.end_x is not None \
                and self.start_y is not None and self.end_y is not None:
            try:
                scale_x = self.image.shape[1] / self.scaled_image.width()
                scale_y = self.image.shape[0] / self.scaled_image.height()

                x1 = int(min(self.start_x, self.end_x) * scale_x)
                x2 = int(max(self.start_x, self.end_x) * scale_x)
                y1 = int(min(self.start_y, self.end_y) * scale_y)
                y2 = int(max(self.start_y, self.end_y) * scale_y)

                cropped_image = self.image[y1:y2, x1:x2]
                cv2.imwrite("cropped_image.jpg", cropped_image)

                self.show_cropped_image(cropped_image)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to crop image: {e}")

    def show_cropped_image(self, cropped_image):
        """
        Displays the cropped image in a new window with options to undo or save.
        """
        cropped_window = tk.Toplevel(self.canvas)
        cropped_window.title("Cropped Image")

        target_width = self.primary_monitor.width // 2
        target_height = self.primary_monitor.height // 2

        original_width, original_height = cropped_image.shape[1], cropped_image.shape[0]

        scale_x = target_width / original_width
        scale_y = target_height / original_height
        scale = min(scale_x, scale_y)

        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        resized_cropped_image = cv2.resize(cropped_image, (new_width, new_height), interpolation=cv2.INTER_AREA)

        cropped_rgb = cv2.cvtColor(resized_cropped_image, cv2.COLOR_BGR2RGB)
        cropped_pil = Image.fromarray(cropped_rgb)
        cropped_image_tk = ImageTk.PhotoImage(image=cropped_pil)

        canvas = tk.Canvas(cropped_window, cursor="arrow")
        canvas.pack(fill="both", expand=True, side=tk.TOP)

        canvas.create_image(0, 0, anchor='nw', image=cropped_image_tk)
        canvas.image = cropped_image_tk

        button_frame = tk.Frame(cropped_window)
        button_frame.pack(fill="x", side=tk.BOTTOM, pady=10)

        undo_button = tk.Button(button_frame, text="Undo", command=cropped_window.destroy)
        undo_button.pack(side=tk.LEFT, padx=10)

        save_button = tk.Button(button_frame, text="Save", command=lambda: self.save_image(resized_cropped_image))
        save_button.pack(side=tk.RIGHT, padx=10)

        cropped_window.update_idletasks()

        x = (self.primary_monitor.width // 2) - (new_width // 2)
        y = (self.primary_monitor.height // 2) - (new_height // 2)
        cropped_window.geometry(f"{new_width}x{new_height}+{x}+{y}")

        cropped_window.mainloop()

    @staticmethod
    def save_image(cropped_image):
        """
        Saves the cropped image to a specified location.
        """
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPG file", "*.jpg")]
        )
        if save_path:
            resized_cropped_image = cv2.resize(cropped_image, (1080, 1350), interpolation=cv2.INTER_AREA)
            cv2.imwrite(save_path, resized_cropped_image)
            messagebox.showinfo("Success", "Image saved successfully!")
