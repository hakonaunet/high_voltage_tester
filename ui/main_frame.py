# main_frame.py

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from test_logic.test_runner import TestRunner
from ui.widgets import MetersFrame, RotatingLogo, DebuggerPanel
from ui.middle_frame import MiddleFrame
from ui.progress_frame import ProgressFrame
from utils import get_theme_background, event_system

class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, test_runner, hardware_client):
        super().__init__(parent)

        self.test_runner = test_runner
        self.hardware_client = hardware_client

        bg_color = get_theme_background()
        super().__init__(parent, fg_color=bg_color)
        self.pack(fill="both", expand=True)

        # Register the callback with AppearanceModeTracker
        ctk.AppearanceModeTracker.add(self.update_theme)

        # Configure grid for main_frame
        self.grid_columnconfigure((0, 2, 3), weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Add rotating logo to main_frame
        self.rotating_logo = RotatingLogo(self, size=500, display_text=True, text_above_logo=True)
        self.rotating_logo.grid(row=0, column=0, pady=(25, 0), sticky="nw")

        # Initialize DebuggerPanel instead of directly adding a CTkTextbox
        self.debugger_panel = DebuggerPanel(self)
        self.debugger_panel.grid(row=1, column=0, padx=(10, 8), pady=(10, 10), sticky="nsew")

        # Replace the middle_frame creation with the new MiddleFrame class
        self.middle_frame = MiddleFrame(self, self.test_runner, self.hardware_client)
        self.middle_frame.grid(row=0, column=1, rowspan=3, pady=(10, 10), sticky="nsew")

        self.progress_frame = ProgressFrame(self)
        self.progress_frame.grid(row=0, column=2, rowspan=2, padx=(8, 0), pady=(10, 10), sticky="nsew")

        # Add meters to main_frame
        self.meters_frame = MetersFrame(self)
        self.meters_frame.grid(row=0, column=3, rowspan=3, sticky="nsew")

    def destroy(self):
        """Override destroy to unregister the theme callback."""
        ctk.AppearanceModeTracker.remove(self.update_theme)  # Corrected
        super().destroy()

    def update_theme(self, new_theme):
        """
        Updates the background color based on the current theme.
        This method is called automatically when the theme changes.
        """
        bg_color = get_theme_background(new_theme)
        self.configure(fg_color=bg_color)

        self.meters_frame.update_theme(new_theme)  # Ensure child frames also update
        self.rotating_logo.update_theme(new_theme)  # Ensure RotatingLogo updates

        self.middle_frame.update_theme(new_theme)  # Add this line to update the MiddleFrame

        # If there are other widgets or elements that need theme updates, handle them here

        self.debugger_panel.update_theme(new_theme)  # Ensure DebuggerPanel updates

    def update_debugger(self, data):
        message = data.get('message', '')
        level = data.get('level', 'INFO')
        # Assume you have access to the DebuggerPanel instance
        self.debugger_panel.log(message, level)

    def handle_error(self, data):
        error_message = data.get('error_message', 'An unexpected error occurred.')
        # Log the error and notify the user
        self.debugger_panel.log(error_message, "ERROR")
        # Optionally, display a popup or notification
        CTkMessagebox(title="Error", message=error_message, icon="cancel")

if __name__ == "__main__":
    # Initialize the main application window
    ctk.set_appearance_mode("system")  # Set to use system theme initially
    ctk.set_default_color_theme("blue")
    
    app = ctk.CTk()
    app.title("Meters Dashboard")
    app.geometry("600x1000")  # Adjust the window size as needed
    app.configure(fg_color=get_theme_background())  # Set initial background color
    
    # Initialize AppearanceModeTracker
    ctk.AppearanceModeTracker.init_appearance_mode()
    
    # Create and place the MainFrame
    main_frame = MainFrame(app)
    
    # Start the application's event loop
    app.mainloop()