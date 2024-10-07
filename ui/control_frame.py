import customtkinter as ctk
from ui.widgets.stylized_frame import StylizedFrame
from ui.widgets.headings import Heading2

class ControlFrame(StylizedFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        for i in range(1, 5):
            self.grid_rowconfigure(i, weight=1)

        # Add heading
        self.heading = Heading2(self, text="Test Controls")
        self.heading.grid(row=0, column=0, pady=(20, 10), padx=10, sticky="ew")

        # Add buttons
        self.start_button = ctk.CTkButton(self, text="Start test", corner_radius=15, height=60, font=("Arial", 18, "bold"))
        self.start_button.grid(row=1, column=0, pady=(10, 5), padx=10)

        self.stop_button = ctk.CTkButton(self, text="Stop test", corner_radius=15, height=60, font=("Arial", 18, "bold"))
        self.stop_button.grid(row=2, column=0, pady=5, padx=10)

        self.reset_button = ctk.CTkButton(self, text="Reset test", corner_radius=15, height=60, font=("Arial", 18, "bold"))
        self.reset_button.grid(row=3, column=0, pady=(5, 10), padx=10)