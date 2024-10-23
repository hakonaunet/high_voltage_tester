import math
import os
import time

import tkinter as tk
import numpy as np
import customtkinter as ctk
from PIL import Image, ImageTk  # Ensure Pillow is installed

from utils import get_theme_background, MAIN_COLOR, event_system, EventType

class RotatingLogo(ctk.CTkFrame):
    def __init__(self, master=None, size=200, padding_percentage=-0.02, display_text=False, text_above_logo=False):
        super().__init__(master)
        self.size = size
        self.padding_percentage = padding_percentage
        self.display_text = display_text
        self.text_above_logo = text_above_logo

        # Base positions for the logo and text
        self.base_x = self.size / 2
        self.base_y = self.size / 2
        self.configure(fg_color=get_theme_background())

        # Initialize model parameters
        self.outer_vertices_2d = self.create_custom_polygon(2.0, 1.5, 0.5)
        self.inner_vertices_2d = self.create_custom_polygon(1.0, 0.75, 0.25)

        # Center the polygons
        self.center_polygons()

        # Calculate depth based on distance between outer and inner polygons
        self.depth = self.calculate_depth(self.outer_vertices_2d, self.inner_vertices_2d)

        # Extrude the polygons to create prisms
        self.outer_vertices = self.extrude_polygon(self.outer_vertices_2d, self.depth)
        self.inner_vertices = self.extrude_polygon(self.inner_vertices_2d, self.depth)

        # Initialize edges
        self.outer_edges = self.create_edges(len(self.outer_vertices_2d))
        self.inner_edges = self.create_edges(len(self.inner_vertices_2d), offset=len(self.outer_vertices))

        # Compute model extent for scaling
        self.compute_model_scale()

        # Initialize Canvas
        self.canvas = tk.Canvas(
            self,
            width=self.size,
            height=self.size,
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.configure(bg=get_theme_background())

        # Edge color
        self.edge_color = MAIN_COLOR

        # Rotation parameters
        self.current_rotation_q = np.array([1.0, 0.0, 0.0, 0.0])  # Identity quaternion
        self.rotation_duration = 1.5  # seconds
        self.wait_duration = 1.5  # seconds
        self.continuous_rotation = False  # Set to False by default

        # Animation variables
        self.rotation_start_q = np.array([1.0, 0.0, 0.0, 0.0])
        self.rotation_target_q = None
        self.rotation_start_time = None
        self.rotation_end_time = None
        self.waiting = False
        self.wait_start_time = None

        # Easing functions
        self.easing_functions = {
            "Linear": self.linear_easing,
            "Smooth": self.smooth_easing
        }
        self.current_easing = "Smooth"

        # Set background color according to the theme
        self.update_theme(ctk.get_appearance_mode())

        # Register the callback with AppearanceModeTracker
        ctk.AppearanceModeTracker.add(self.update_theme)

        # Load and prepare the text image if display_text is True
        if self.display_text:
            self.load_text_image()

        # Bind click event to the canvas
        self.canvas.bind("<Button-1>", self.on_click)
        # Bind hover events to change cursor
        self.canvas.bind("<Enter>", self.on_hover_enter)
        self.canvas.bind("<Leave>", self.on_hover_leave)
        self.reset_timer_id = None

        # Start animation
        self.after(0, self.update_animation)

        # Register event listeners
        event_system.register_listener(EventType.SUB_TEST_STARTED, self.go_to_random_position)
        event_system.register_listener(EventType.TEST_TERMINATED, self.return_to_default_position)

    def destroy(self):
        """Override destroy to unregister the theme callback."""
        ctk.AppearanceModeTracker.remove(self.update_theme)
        super().destroy()

    def on_click(self, event):
        """
        Handles click events to trigger the Easter egg actions.
        Alternates between rotating and moving the logo.
        Resets the timer on each click.
        """
        self.go_to_random_position()
        
        # Reset the 3-second timer
        if self.reset_timer_id is not None:
            self.after_cancel(self.reset_timer_id)
        self.reset_timer_id = self.after(3000, self.return_to_default_position)
    
    def compute_model_scale(self):
        # Combine all vertices from both the outer and inner models
        all_vertices = self.outer_vertices + self.inner_vertices

        # Compute the maximum distance from the origin to any vertex (bounding radius)
        max_distance = max(math.sqrt(x**2 + y**2 + z**2) for x, y, z in all_vertices)

        # Calculate the scaling factor to fit the model within the canvas
        padding = self.size * abs(self.padding_percentage)
        self.model_scale = (self.size / 2 - padding) / max_distance

        # Store the model's height in units for text positioning
        y_values = [y for x, y, z in all_vertices]
        self.model_height_in_units = max(y_values) - min(y_values)

    # Model creation methods
    def create_custom_polygon(self, W, H, C):
        vertices = [
            [0, C],
            [0, H],
            [W - C, H],
            [W, H - C],
            [W, 0],
            [C, 0]
        ]
        return vertices

    def center_polygons(self):
        outer_centroid = self.calculate_centroid(self.outer_vertices_2d)
        inner_centroid = self.calculate_centroid(self.inner_vertices_2d)

        self.outer_vertices_2d = [
            [x - outer_centroid[0], y - outer_centroid[1]]
            for x, y in self.outer_vertices_2d
        ]

        self.inner_vertices_2d = [
            [x - inner_centroid[0], y - inner_centroid[1]]
            for x, y in self.inner_vertices_2d
        ]

    def calculate_centroid(self, vertices):
        x_list = [vertex[0] for vertex in vertices]
        y_list = [vertex[1] for vertex in vertices]
        n = len(vertices)
        return [sum(x_list) / n, sum(y_list) / n]

    def calculate_depth(self, outer_vertices, inner_vertices):
        distances = [
            math.sqrt((ov[0] - iv[0])**2 + (ov[1] - iv[1])**2)
            for ov, iv in zip(outer_vertices, inner_vertices)
        ]
        return sum(distances) / len(distances)

    def extrude_polygon(self, vertices_2d, depth):
        vertices = [[x, y, -depth / 2] for x, y in vertices_2d] + \
                   [[x, y, depth / 2] for x, y in vertices_2d]
        return vertices

    def create_edges(self, num_vertices, offset=0):
        edges = []
        for i in range(num_vertices):
            edges.append((offset + i, offset + (i + 1) % num_vertices))
        for i in range(num_vertices):
            edges.append((offset + i + num_vertices, offset + ((i + 1) % num_vertices) + num_vertices))
        for i in range(num_vertices):
            edges.append((offset + i, offset + i + num_vertices))
        return edges

    # Rotation methods
    def quaternion_from_axis_angle(self, axis, angle):
        axis = np.array(axis) / np.linalg.norm(axis)
        s = math.sin(angle / 2)
        return np.concatenate(([math.cos(angle / 2)], s * axis))

    def quaternion_multiply(self, q1, q2):
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        return np.array([
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2
        ])

    def quaternion_conjugate(self, q):
        w, x, y, z = q
        return np.array([w, -x, -y, -z])

    def rotate_point(self, q, point):
        p = np.concatenate(([0.0], point))
        q_conj = self.quaternion_conjugate(q)
        return self.quaternion_multiply(self.quaternion_multiply(q, p), q_conj)[1:]

    def quaternion_slerp(self, q0, q1, t):
        cos_half_theta = np.dot(q0, q1)
        if cos_half_theta < 0:
            q1 = -q1
            cos_half_theta = -cos_half_theta
        if abs(cos_half_theta) >= 1.0:
            return q0
        sin_half_theta = math.sqrt(1.0 - cos_half_theta * cos_half_theta)
        if sin_half_theta < 0.001:
            return (1 - t) * q0 + t * q1
        half_theta = math.acos(cos_half_theta)
        return (math.sin((1 - t) * half_theta) / sin_half_theta) * q0 + \
               (math.sin(t * half_theta) / sin_half_theta) * q1

    # Easing functions
    def linear_easing(self, t):
        return t

    def smooth_easing(self, t):
        return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2

    # Drawing method
    def draw_model(self):
        self.canvas.delete('edges')

        vertices = self.outer_vertices + self.inner_vertices
        edges = self.outer_edges + self.inner_edges
        rotation_q = self.current_rotation_q
        projected_points = [
            (
                self.base_x + self.project_point(self.rotate_point(rotation_q, v))[0] * self.model_scale,
                self.base_y - self.project_point(self.rotate_point(rotation_q, v))[1] * self.model_scale
            )
            for v in vertices
        ]

        line_width = max(1, int(self.size * 0.015))
        for edge in edges:
            start, end = edge
            x0, y0 = projected_points[start]
            x1, y1 = projected_points[end]
            self.canvas.create_line(
                x0, y0, x1, y1,
                fill=self.edge_color,
                width=line_width,
                capstyle=tk.ROUND,
                joinstyle=tk.ROUND,
                tags=("edges",)
            )

        if self.display_text and hasattr(self, 'text_image_id'):
            self.canvas.tag_raise("text_image")

    def project_point(self, point):
        x, y, z = point
        return (x, y)  # Orthographic projection

    # Animation methods
    def update_animation(self):
        current_time = time.time()
        if self.waiting:
            if current_time - self.wait_start_time >= self.wait_duration:
                self.waiting = False
                if self.continuous_rotation:
                    self.start_new_rotation(current_time)
        else:
            if self.rotation_start_time is None:
                if self.continuous_rotation:
                    self.start_new_rotation(current_time)
                # Removed the else block to ensure draw_model is called even if not rotating
            else:
                t = (current_time - self.rotation_start_time) / self.rotation_duration
                if t >= 1.0:
                    self.current_rotation_q = self.rotation_target_q
                    self.waiting = True
                    self.wait_start_time = current_time
                else:
                    easing_func = self.easing_functions[self.current_easing]
                    t_eased = easing_func(t)
                    self.current_rotation_q = self.quaternion_slerp(
                        self.rotation_start_q,
                        self.rotation_target_q,
                        t_eased
                    )

        # Always draw the model, even if not rotating
        self.draw_model()

        # Always show text if display_text is True
        if self.display_text and hasattr(self, 'text_image_id'):
            self.canvas.itemconfigure("text_image", state='normal')

        self.after(16, self.update_animation)

    def start_new_rotation(self, current_time=None):
        if current_time is None:
            current_time = time.time()
        self.rotation_start_time = current_time
        self.rotation_end_time = self.rotation_start_time + self.rotation_duration
        self.rotation_start_q = self.current_rotation_q

        u1, u2, u3 = np.random.uniform(0, 1, 3)
        q1 = np.sqrt(1 - u1) * np.sin(2 * math.pi * u2)
        q2 = np.sqrt(1 - u1) * np.cos(2 * math.pi * u2)
        q3 = np.sqrt(u1) * np.sin(2 * math.pi * u3)
        q4 = np.sqrt(u1) * np.cos(2 * math.pi * u3)
        self.rotation_target_q = np.array([q4, q1, q2, q3])

    def return_to_default_position(self, data=None):
        """
        Resets the rotating logo to its default position.

        :param data: Optional data passed by the event system.
        """
        self.rotation_start_q = self.current_rotation_q
        self.rotation_target_q = np.array([1.0, 0.0, 0.0, 0.0])
        self.rotation_start_time = time.time()
        self.rotation_end_time = self.rotation_start_time + self.rotation_duration
        self.waiting = False
        self.continuous_rotation = False

    def go_to_random_position(self, data=None):
        self.rotation_start_q = self.current_rotation_q
        u1, u2, u3 = np.random.uniform(0, 1, 3)
        q1 = np.sqrt(1 - u1) * np.sin(2 * math.pi * u2)
        q2 = np.sqrt(1 - u1) * np.cos(2 * math.pi * u2)
        q3 = np.sqrt(u1) * np.sin(2 * math.pi * u3)
        q4 = np.sqrt(u1) * np.cos(2 * math.pi * u3)
        self.rotation_target_q = np.array([q4, q1, q2, q3])
        self.rotation_start_time = time.time()
        self.rotation_end_time = self.rotation_start_time + self.rotation_duration
        self.waiting = False
        self.continuous_rotation = False

    def set_easing(self, easing_type):
        if easing_type in self.easing_functions:
            self.current_easing = easing_type
        else:
            raise ValueError(f"Easing type '{easing_type}' is not supported.")

    def set_continuous_rotation(self, continuous):
        self.continuous_rotation = continuous
        if continuous and self.waiting:
            self.waiting = False
            self.start_new_rotation()

    def update_theme(self, new_theme):
        """
        Updates the background color based on the current theme.
        This method is called automatically when the theme changes.
        """
        bg_color = get_theme_background(new_theme)
        self.configure(fg_color=bg_color)
        self.canvas.configure(bg=bg_color)
        
        # Update other theme-dependent elements if necessary
        # For example, updating edge color based on theme
        # self.edge_color = '#ffffff' if ctk.get_appearance_mode() == "Dark" else '#000000'
        self.draw_model()

    def get_light_mode_bg(self):
        return "#ffffff"

    def get_dark_mode_bg(self):
        return "#2b2b2b"

    def on_hover_enter(self, event):
        """Change cursor to pointer when hovering over the logo."""
        self.canvas.config(cursor="hand2")

    def on_hover_leave(self, event):
        """Change cursor back to default when leaving the logo area."""
        self.canvas.config(cursor="")

    def load_text_image(self):
        try:
            image_path = os.path.join(os.path.dirname(__file__), "..", "images", "eltorque_logo_text.png")
            image_path = os.path.abspath(image_path)
            pil_image = Image.open(image_path)
            
            # Convert image to have an alpha channel if not present
            if pil_image.mode != "RGBA":
                pil_image = pil_image.convert("RGBA")
            
            # Calculate new dimensions while maintaining aspect ratio
            aspect_ratio = pil_image.width / pil_image.height
            new_width = int(self.size * 0.9)
            new_height = int(new_width / aspect_ratio)
            
            pil_image = pil_image.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS
            )
            self.text_image = ImageTk.PhotoImage(pil_image)
            
            # Set text position based on text_above_logo
            if self.text_above_logo:
                text_y_position = new_height // 2  # Top of the canvas
            else:
                text_y_position = self.size - (new_height // 2)  # Bottom of the canvas
            
            self.text_image_id = self.canvas.create_image(
                self.size // 2,  # Center horizontally
                text_y_position,
                image=self.text_image,
                anchor="center",
                tags=("text_image",)
            )
            # Ensure the text image is visible
            self.canvas.itemconfigure("text_image", state='normal')
        except Exception as e:
            print(f"Error loading text image: {e}")
            self.display_text = False  # Disable text display if image fails to load

# Main execution
if __name__ == "__main__":
    ctk.set_appearance_mode("system")  # Use system theme initially
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("3D Rotating Logo")

    def get_background_color():
        appearance_mode = ctk.get_appearance_mode()
        return "#2b2b2b" if appearance_mode == "dark" else "#ffffff"

    window_bg = get_background_color()
    root.configure(bg=window_bg)

    # Initialize AppearanceModeTracker
    ctk.AppearanceModeTracker.init_appearance_mode()

    # Create an instance of RotatingLogo with display_text enabled
    logo_size = 1000  # Example size
    rotating_logo = RotatingLogo(master=root, size=logo_size, display_text=True)
    rotating_logo.pack(pady=20)

    # Create UI elements
    def toggle_continuous_rotation():
        rotating_logo.set_continuous_rotation(continuous_rotation_var.get())

    def return_to_default():
        rotating_logo.return_to_default_position()

    def go_to_random():
        rotating_logo.go_to_random_position()

    def set_easing(choice):
        rotating_logo.set_easing(easing_var.get())

    def toggle_dark_mode():
        if dark_mode_var.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
        # AppearanceModeTracker will automatically notify registered callbacks

    # Controls frame
    controls_frame = ctk.CTkFrame(root)
    controls_frame.pack(pady=10)

    continuous_rotation_var = tk.BooleanVar(value=False)  # Set default to False
    continuous_rotation_check = ctk.CTkCheckBox(
        controls_frame, text="Perform continuous rotations",
        variable=continuous_rotation_var,
        command=toggle_continuous_rotation
    )
    continuous_rotation_check.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    return_to_default_button = ctk.CTkButton(
        controls_frame, text="Return to default position",
        command=return_to_default
    )
    return_to_default_button.grid(row=0, column=1, padx=5, pady=5)

    go_to_random_button = ctk.CTkButton(
        controls_frame, text="Go to random position",
        command=go_to_random
    )
    go_to_random_button.grid(row=0, column=2, padx=5, pady=5)

    easing_var = tk.StringVar(value="Smooth")
    easing_option = ctk.CTkOptionMenu(
        controls_frame, values=["Linear", "Smooth"], variable=easing_var,
        command=set_easing
    )
    easing_option.grid(row=0, column=3, padx=5, pady=5)
    easing_option.set("Smooth")

    dark_mode_var = tk.BooleanVar(value=False)
    dark_mode_check = ctk.CTkCheckBox(
        controls_frame, text="Dark Mode",
        variable=dark_mode_var,
        command=toggle_dark_mode
    )
    dark_mode_check.grid(row=0, column=4, padx=5, pady=5)

    root.mainloop()