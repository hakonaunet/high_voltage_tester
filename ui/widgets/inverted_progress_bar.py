import math
import time
import random

import customtkinter as ctk

class InvertedCTkProgressBar(ctk.CTkProgressBar):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._animation_delay = 16  # Delay in milliseconds (~60 FPS)
        self._is_animating = False
        self._animation_after_id = None
        self._target_value = None
        self._start_value = None
        self._change_in_value = None
        self._animation_start_time = None
        self._animation_duration = 1000  # Duration in milliseconds
        self.positions = [0, 0.036, 0.218, 0.402, 0.582, 0.762, 0.947, 1]

        self.after(1, lambda: self.animation_loop())

    def _draw(self, no_color_updates=False):
        # Call the parent class's _draw method to set up the canvas
        super()._draw(no_color_updates)

        # Determine the orientation for drawing
        if self._orientation.lower() == "horizontal":
            orientation = "w"
        elif self._orientation.lower() == "vertical":
            orientation = "s"  # Keep the orientation as 's' (south)
        else:
            orientation = "w"

        if self._mode == "determinate":
            # Invert the progress values for top-to-bottom fill
            progress_value_1 = 1 - self._determinate_value
            progress_value_2 = 1.0
            requires_recoloring = self._draw_engine.draw_rounded_progress_bar_with_border(
                self._apply_widget_scaling(self._current_width),
                self._apply_widget_scaling(self._current_height),
                self._apply_widget_scaling(self._corner_radius),
                self._apply_widget_scaling(self._border_width),
                progress_value_1,
                progress_value_2,
                orientation
            )
        else:  # indeterminate mode
            # Adjust progress values for inverted indeterminate mode
            progress_value = (math.sin(self._indeterminate_value * math.pi / 40) + 1) / 2
            progress_value = 1 - progress_value  # Invert the progress value
            progress_value_1 = max(0.0, progress_value - (self._indeterminate_width / 2))
            progress_value_2 = min(1.0, progress_value + (self._indeterminate_width / 2))
            requires_recoloring = self._draw_engine.draw_rounded_progress_bar_with_border(
                self._apply_widget_scaling(self._current_width),
                self._apply_widget_scaling(self._current_height),
                self._apply_widget_scaling(self._corner_radius),
                self._apply_widget_scaling(self._border_width),
                progress_value_1,
                progress_value_2,
                orientation
            )

        if not no_color_updates or requires_recoloring:
            # Update colors if necessary
            self._canvas.configure(bg=self._apply_appearance_mode(self._bg_color))
            self._canvas.itemconfig(
                "border_parts",
                fill=self._apply_appearance_mode(self._border_color),
                outline=self._apply_appearance_mode(self._border_color)
            )
            self._canvas.itemconfig(
                "inner_parts",
                fill=self._apply_appearance_mode(self._fg_color),
                outline=self._apply_appearance_mode(self._fg_color)
            )
            self._canvas.itemconfig(
                "progress_parts",
                fill=self._apply_appearance_mode(self._progress_color),
                outline=self._apply_appearance_mode(self._progress_color)
            )
        

    def on_click(self, event):
        # Generate a random value between 0 and 1
        random_value = random.uniform(0, 1)
        
        # Call animate_to with the random value
        self.go_to(random_value)
        
        # Reset the 3-second timer
        if self.reset_timer_id is not None:
            self.after_cancel(self.reset_timer_id)
        self.reset_timer_id = self.after(3000, self.go_to_zero)

    def smooth_easing(self, t):
        return 4 * t * t * t if t < 0.5 else 1 - ((-2 * t + 2) ** 3) / 2
    
    def go_to(self, target_value):
        duration = 1000  # duration in milliseconds
        start_time = None
        start_value = self.get()
        change_in_value = target_value - start_value
        
        def animate():
            nonlocal start_time
            if start_time is None:
                start_time = time.perf_counter()
            elapsed_time = (time.perf_counter() - start_time) * 1000  # in milliseconds
            t = min(elapsed_time / duration, 1)  # Ensure t <= 1

            easing = self.smooth_easing(t)
            current_value = start_value + easing * change_in_value
            self.set(current_value)
            self.current_value = current_value

            if t < 1:
                self.after(16, animate)  # roughly 60 frames per second
            else:
                self.set(target_value)  # Ensure we end at the exact target value
                self.current_value = target_value
        
        animate()
    
    def go_to_zero(self):
        self.go_to(0)
    
    def go_to_random_position(self):
        random_value = random.uniform(0, 1)
        self.go_to(random_value)

    def go_to_test_position(self, position):
        self.go_to(self.positions[position])

    def animation_loop(self):
        delay = 0
        for position in self.positions:
            self.after(delay, lambda pos=position: self.go_to(pos))
            delay += 1000  # Increase delay for each position
        self.after(delay + 100, self.animation_loop)  # Schedule the next loop
