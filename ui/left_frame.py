from ui.widgets.stylized_frame import StylizedFrame
from ui.widgets.headings import Heading2

class LeftFrame(StylizedFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # Add heading
        self.heading = Heading2(self, text="Test Information")
        self.heading.grid(row=0, column=0, pady=(20, 10), padx=10, sticky="ew")
        
        # Add content (placeholder for now)
        # You can add more widgets here as needed