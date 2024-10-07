import customtkinter as ctk
from ui.widgets.stylized_frame import StylizedFrame
from ui.widgets.stylized_label import StylizedLabel
from ui.widgets import InvertedCTkProgressBar  

class ProgressFrame(StylizedFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure grid with padding
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(corner_radius=40)
        
        # Add Inverted Progress Bar
        self.progress_bar = InvertedCTkProgressBar(
            self, 
            corner_radius=15, 
            width=30, 
            border_width=2, 
            orientation="vertical"
        )
        self.progress_bar.grid(padx=10, pady=10, sticky="nsew")
        
        # Configure the progress bar for determinate mode
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(0)  # Start at 0%

    def destroy(self):
        """Override destroy to stop the progress bar animation."""
        super().destroy()
