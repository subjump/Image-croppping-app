import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from screeninfo import get_monitors


class ImageCropperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")
        self.root.geometry("800x600")
        self.center_window(self.root, 800, 600)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, cursor="cross")
        self.canvas.pack(fill="both", expand=True)

        self.image = None
        self.image_path = None
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.scaled_image = None

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill="x", side=tk.BOTTOM, pady=10)

        self.load_button = tk.Button(self.button_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.crop_button = tk.Button(self.button_frame, text="Crop Image", command=self.crop_image, state=tk.DISABLED)
        self.crop_button.pack(side=tk.RIGHT, padx=10)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.primary_monitor = get_monitors()[0]

        self.root.bind("<Configure>", self.on_window_resize)

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x}+{y}")

    def load_image(self):
        self.reset_canvas()
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif"), ("All files", "*.*")]
        )
        if self.image_path:
            try:
                self.image = cv2.imread(self.image_path)
                if self.image is None:
                    raise ValueError("Could not open or find the image.")

                # Check if the image meets the minimum resolution requirement
                if self.image.shape[1] < 6000 or self.image.shape[0] < 4000:
                    messagebox.showerror("Resolution Error",
                                         "The selected image has insufficient resolution. Please select an image with at least 6000x4000 pixels.")
                    return

                self.display_image()
                self.crop_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

    def display_image(self):
        if self.image is not None:
            self.update_scaled_image()
            self.draw_image_on_canvas()

    def update_scaled_image(self):
        h, w = self.image.shape[:2]

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
        self.canvas.delete("all")
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        if self.rect:
            self.canvas.delete(self.rect)

        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
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

    def on_button_release(self, event):
        pass

    def crop_image(self):
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
        cropped_window = tk.Toplevel(self.root)
        cropped_window.title("Cropped Image")

        # Calculate the scale factors to fit the image within the window
        target_width = self.primary_monitor.width // 2  # Target width of the cropped image window
        target_height = self.primary_monitor.height // 2  # Target height of the cropped image window

        # Get the original dimensions of the cropped image
        original_width, original_height = cropped_image.shape[1], cropped_image.shape[0]

        # Calculate the scale factors
        scale_x = target_width / original_width
        scale_y = target_height / original_height

        # Choose the smaller scale factor to maintain the aspect ratio
        scale = min(scale_x, scale_y)

        # Calculate the new dimensions
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        # Resize the cropped image
        resized_cropped_image = cv2.resize(cropped_image, (new_width, new_height), interpolation=cv2.INTER_AREA)

        cropped_rgb = cv2.cvtColor(resized_cropped_image, cv2.COLOR_BGR2RGB)
        cropped_pil = Image.fromarray(cropped_rgb)
        cropped_image_tk = ImageTk.PhotoImage(image=cropped_pil)

        canvas = tk.Canvas(cropped_window, cursor="cross")
        canvas.pack(fill="both", expand=True, side=tk.TOP)

        canvas.create_image(0, 0, anchor='nw', image=cropped_image_tk)
        canvas.image = cropped_image_tk  # Keep a reference to the image

        button_frame = tk.Frame(cropped_window)
        button_frame.pack(fill="x", side=tk.BOTTOM, pady=10)

        undo_button = tk.Button(button_frame, text="Undo", command=cropped_window.destroy)
        undo_button.pack(side=tk.LEFT, padx=10)

        save_button = tk.Button(button_frame, text="Save", command=lambda: self.save_image(resized_cropped_image))
        save_button.pack(side=tk.RIGHT, padx=10)

        cropped_window.update_idletasks()

        # Set the geometry of the cropped window based on the new dimensions
        x = (self.primary_monitor.width // 2) - (new_width // 2)
        y = (self.primary_monitor.height // 2) - (new_height // 2)
        cropped_window.geometry(f"{new_width}x{new_height}+{x}+{y}")

        cropped_window.mainloop()

    def save_image(self, cropped_image):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if save_path:
            resized_cropped_image = cv2.resize(cropped_image, (1080, 1350), interpolation=cv2.INTER_AREA)
            cv2.imwrite(save_path, resized_cropped_image)
            messagebox.showinfo("Success", "Image saved successfully!")

    def on_window_resize(self, event):
        self.draw_image_on_canvas()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropperApp(root)
    root.mainloop()
