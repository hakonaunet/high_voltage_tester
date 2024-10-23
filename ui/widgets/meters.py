import time
import random
import threading

import customtkinter as ctk
from tkdial import Meter

from utils import get_theme_background, MAIN_COLOR, Colors, TestConstants
from ui.widgets.bordered_label import BorderedLabel
from utils import event_system


class MeterWidget(ctk.CTkFrame):
    """
    A custom widget that encapsulates the Meter and its label.
    Handles animations and color changes based on test progress.
    """
    def __init__(self, parent, label_text, test_number, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.test_number = test_number
        self.is_running = False
        self.blink_job = None

        # Get the parent frame's background color
        parent_bg = get_theme_background()
        self.configure(fg_color=parent_bg, corner_radius=0)
        
        # Initialize default border color
        self.default_border_color = Colors.GRAY.value  # Assuming Colors enum has GRAY
        
        # Replace the CTkButton with BorderedLabel
        self.label = BorderedLabel(
            self,
            text=label_text,
            width=0,
            border_color=self.default_border_color
        )
        self.label.pack(side="left", padx=(0, 10), fill="none")
        
        self.meter = Meter(
            self,
            radius=130,
            start=0,
            end=6,
            border_width=2,
            major_divisions=40,
            minor_divisions=0.1,
            fg="black",
            text_color="white",
            start_angle=270,
            end_angle=-300,
            text_font="DS-Digital 10",
            scale_color="white",
            needle_color="white",
            axis_color=MAIN_COLOR,
            border_color=MAIN_COLOR,
            text="mA",
            state="Unbind",
            scroll_steps=0,
            bg=parent_bg
        )
        
        try:
            self.meter.configure(bg=parent_bg)
        except TypeError:
            if hasattr(self.meter, 'canvas'):
                self.meter.canvas.configure(bg=parent_bg)
            else:
                event_system.dispatch_event("error_occurred", {"error_message": "Unable to set Meter background. Check if 'canvas' attribute exists."})
        
        self.meter.set_mark(int(TestConstants.CURRENT_CUT_OFF.value*10), 60, "red")
        self.meter.set(0)
        self.current_value = 0
        
        self.meter.pack(side="left", pady=0)
        
        self.reset_timer_id = None
        
        self.meter.bind("<Button-1>", self.on_click)
        
        ctk.AppearanceModeTracker.add(self.update_theme)
        
        # Register event listeners
        event_system.register_listener("progress_update", self.on_progress_update)
        event_system.register_listener("error_occurred", self.on_error_occurred)

        self.test_status = None

    def on_progress_update(self, event_data):
        """
        Handles progress updates to start test animations.
        """
        position = event_data.get("position")
        if position == self.test_number:
            self.start_test()

    def on_error_occurred(self, event_data):
        """
        Handles errors by setting the border to red.
        """
        self.end_test("ERROR")

    def start_test(self):
        """
        Initiates the test state with blinking yellow borders.
        """
        if self.is_running:
            return  # Avoid multiple starts
        self.is_running = True
        self.test_status = "running"
        self.blink_border(Colors.GRAY.value, "yellow")

    def end_test(self, result):
        """
        Ends the test and updates the border color based on the result.
        """
        self.is_running = False
        self.test_status = result
        if self.blink_job:
            self.after_cancel(self.blink_job)
            self.blink_job = None

        if result == "SUCCESS":
            self.label.configure(border_color=MAIN_COLOR)
        elif result in ["FAILURE", "ERROR"]:
            self.label.configure(border_color=Colors.NEON_RED.value)

    def blink_border(self, color1, color2):
        """
        Animates the border color between two colors.
        """
        current_color = self.label.cget("border_color")
        next_color = color2 if current_color == color1 else color1
        self.label.configure(border_color=next_color)
        
        if self.test_status in ["running", "error"]:
            self.blink_job = self.after(500, self.blink_border, color1, color2)

    def update_theme(self, new_theme):
        """
        Updates the background color and other theme-dependent properties.
        This method is called automatically when the theme changes.
        """
        bg_color = get_theme_background(new_theme)
        self.configure(fg_color=bg_color)
        
        # Update Meter's background
        try:
            self.meter.configure(bg=bg_color)
        except TypeError:
            if hasattr(self.meter, 'canvas'):
                self.meter.canvas.configure(bg=bg_color)
        
        # Update label color based on theme and test status
        if self.test_status is None:
            border_color = self.default_border_color
        elif self.test_status == "SUCCESS":
            border_color = MAIN_COLOR
        elif self.test_status in ["FAILURE", "ERROR"]:
            border_color = Colors.NEON_RED.value
        else:  # running
            border_color = self.label.cget("border_color")  # Keep current color
        
        self.label.configure(
            text_color="white" if new_theme.lower() == "dark" else "black",
            fg_color="transparent",
            border_color=border_color
        )
        
        self.meter.border_color = MAIN_COLOR  # Using the constant
        self.meter.configure(fg=self.meter.fg)  # Reconfigure to apply changes

    def on_click(self, event):
        """
        Handles click events to trigger meter animations.
        """
        self.go_to_random_position()
        
        # Reset the 3-second timer
        if self.reset_timer_id is not None:
            self.after_cancel(self.reset_timer_id)
        self.reset_timer_id = self.after(3000, self.go_to_zero)

    def smooth_easing(self, t):
        return 4 * t * t * t if t < 0.5 else 1 - ((-2 * t + 2) ** 3) / 2

    def go_to(self, target_value):
        duration = 1000  # duration in milliseconds
        start_time = None
        start_value = self.current_value
        change_in_value = target_value - start_value
        
        def animate():
            nonlocal start_time
            if start_time is None:
                start_time = time.perf_counter()
            elapsed_time = (time.perf_counter() - start_time) * 1000  # in milliseconds
            t = min(elapsed_time / duration, 1)  # Ensure t <= 1

            easing = self.smooth_easing(t)
            current_value = start_value + easing * change_in_value
            self.meter.set(current_value)
            self.current_value = current_value

            if t < 1:
                self.after(16, animate)  # roughly 60 frames per second
            else:
                self.meter.set(target_value)  # Ensure we end at the exact target value
                self.current_value = target_value

        animate()
    
    def go_to_zero(self):
        self.go_to(0)
    
    def go_to_random_position(self):
        random_value = random.uniform(0, 6)
        self.go_to(random_value)
    

    def destroy(self):
        """Override destroy to unregister callbacks."""
        ctk.AppearanceModeTracker.remove(self.update_theme)
        event_system.unregister_listener("progress_update", self.on_progress_update)
        event_system.unregister_listener("error_occurred", self.on_error_occurred)
        if self.blink_job:
            self.after_cancel(self.blink_job)
        super().destroy()


class MetersFrame(ctk.CTkFrame):
    """
    A frame that contains a 6x1 stack of MeterWidgets with labels.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=("#f0f0f0", "#1f1f1f"), **kwargs)  # Initialize first
        
        # Configure grid layout with 6 rows and 2 columns
        for row in range(6):
            self.grid_rowconfigure(row, weight=1)
        self.grid_columnconfigure(0, weight=0)  # Column for labels
        self.grid_columnconfigure(1, weight=1)  # Column for meters
        
        # Create and place six MeterWidgets
        self.meter_widgets = []
        for row in range(6):
            label_text = f"Test #{row + 1}"
            meter_widget = MeterWidget(self, label_text, test_number=row + 1)
            meter_widget.grid(row=row, column=0, columnspan=2, padx=(10,10), pady=0, sticky="nsew")
            self.meter_widgets.append(meter_widget)
    
        event_system.register_listener("sub_test_concluded", self.on_sub_test_concluded)
        event_system.register_listener("test_started", self.on_test_started)
    def on_sub_test_concluded(self, event_data):
        """
        Handles sub-test conclusion to update the meter's status.
        """
        test_number = event_data.get("test_number")
        status = event_data.get("status")
        current = event_data.get("current")
        self.meter_widgets[test_number - 1].end_test(status)
        self.meter_widgets[test_number - 1].go_to(current)

    def on_test_started(self, event_data):
        """
        Handles test start to reset all meters and their border colors.
        """
        for meter_widget in self.meter_widgets:
            meter_widget.go_to_zero()
            meter_widget.label.configure(border_color=Colors.GRAY.value)
            meter_widget.test_status = None  # Reset the test status

    def update_theme(self, new_theme):
        """
        Updates the theme for all MeterWidgets within the frame.
        """
        for meter_widget in self.meter_widgets:
            meter_widget.update_theme(new_theme)
    
    def destroy(self):
        """
        Override destroy to unregister the theme callback.
        """
        ctk.AppearanceModeTracker.remove(self.update_theme)
        event_system.unregister_listener("sub_test_concluded", self.on_sub_test_concluded)
        for meter_widget in self.meter_widgets:
            meter_widget.destroy()
        super().destroy()


if __name__ == "__main__":
    # Example usage of MetersFrame
    app = ctk.CTk()
    app.title("Meters Dashboard")
    app.geometry("600x1000")  # Adjust the window size as needed
    app.configure(fg_color="#242424")  # Set a dark background color
    
    # Create and place the MetersFrame
    meters_frame = MetersFrame(app)
    meters_frame.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Start the application's event loop
    app.mainloop()
