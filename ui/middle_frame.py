import customtkinter as ctk
from utils import MAIN_COLOR
from ui.widgets.bordered_label import BorderedLabel
from ui.test_status_frame import TestStatusFrame
from ui.widgets.stylized_frame import StylizedFrame
from ui.widgets.headings import Heading1
from ui.control_frame import ControlFrame
from ui.left_frame import LeftFrame

class MiddleFrame(StylizedFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure grid
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(tuple(i for i in range(1, 4)), weight=1)
        self.grid_columnconfigure(tuple(j for j in range(3)), weight=1)
        
        # Add headline
        self.headline = Heading1(
            self,
            text="HIGH VOLTAGE TESTER"
        )
        self.headline.grid(row=0, column=0, columnspan=3, pady=(20, 10), sticky="n")
        
        # Add left frame in the 2x2 top-left grid space
        self.left_frame = LeftFrame(self)
        self.left_frame.grid(row=1, column=0, rowspan=2, columnspan=2, padx=(10, 5), pady=(10, 5), sticky="nsew")
        
        # Add Control frame
        self.control_frame = ControlFrame(self)
        self.control_frame.grid(row=1, column=2, rowspan=2, padx=(5, 10), pady=(10, 5), sticky="nsew")
        
        # Use the new TestStatusFrame
        self.test_status_frame = TestStatusFrame(self)
        self.test_status_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=(5, 10), sticky="nsew")
    
    def update_theme(self, new_theme: str):
        # Add theme update logic if needed
        pass