import customtkinter as ctk

from utils import MAIN_COLOR
from ui.widgets.bordered_label import BorderedLabel
from ui.widgets.stylized_frame import StylizedFrame
from ui.widgets.stylized_label import StylizedLabel
from ui.widgets.headings import Heading2

class TestStatusFrame(StylizedFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure grid
        self.grid_columnconfigure(tuple(range(6)), weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        # Add Test Status headline
        self.test_status_headline = Heading2(
            self,
            text="Test Status"
        )
        self.test_status_headline.grid(row=0, column=0, columnspan=6, padx=10, pady=(20, 10), sticky="ew")

        # Add Serial no. label and button
        self.serial_label = StylizedLabel(
            self,
            text="Serial no.:"
        )
        self.serial_label.grid(row=1, column=0, sticky="w", padx=(20, 5), pady=(10, 0))
        
        self.serial_button = BorderedLabel(
            self,
            text=""
        )
        self.serial_button.grid(row=1, column=1, sticky="ew", padx=5, pady=(10, 0))
        
        # Add Current voltage label and button
        self.voltage_label = StylizedLabel(
            self,
            text="Provided voltage:"
        )
        self.voltage_label.grid(row=1, column=2, sticky="w", padx=(5, 5), pady=(10, 0))
        
        self.voltage_button = BorderedLabel(
            self,
            text=""
        )
        self.voltage_button.grid(row=1, column=3, sticky="ew", padx=5, pady=(10, 0))

        self.placeholder_label = StylizedLabel(
            self,
            text="Placeholder:"
        )
        self.placeholder_label.grid(row=1, column=4, sticky="w", padx=(5, 5), pady=(10, 0))

        self.placeholder_button = BorderedLabel(
            self,
            text="Placeholder"
        )
        self.placeholder_button.grid(row=1, column=5, sticky="ew", padx=(5, 20), pady=(10, 0))
        
        # Removed progress_bar and test_label_frame