import os
import tkinter as tk
from PIL import Image, ImageTk

class TestImageDisplay(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test Image Display")
        self.geometry("400x400")

        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()

        try:
            image_path = os.path.join(os.path.dirname(__file__), "..", "ui", "images", "eltorque_logo_text.png")
            image_path = os.path.abspath(image_path)
            print(f"Loading test image from: {image_path}")
            pil_image = Image.open(image_path)
            pil_image = pil_image.resize((200, 50), Image.Resampling.LANCZOS)  # Adjust size as needed
            self.test_image = ImageTk.PhotoImage(pil_image)
            self.image_id = self.canvas.create_image(200, 300, image=self.test_image, anchor="center")
            print("Test image loaded successfully.")
        except Exception as e:
            print(f"Error loading test image: {e}")

        # Optionally, add a placeholder rectangle
        self.canvas.create_rectangle(150, 250, 250, 350, outline="red", width=2)

if __name__ == "__main__":
    app = TestImageDisplay()
    app.mainloop()