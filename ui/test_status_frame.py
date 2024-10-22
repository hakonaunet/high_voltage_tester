import customtkinter as ctk

from utils import MAIN_COLOR, TestConstants
from ui.widgets.bordered_label import BorderedLabel
from ui.widgets.stylized_frame import StylizedFrame
from ui.widgets.stylized_label import StylizedLabel
from ui.widgets.headings import Heading2
from test_logic.event_system import event_system

class TestStatusFrame(StylizedFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.highest_current = 0.0

        # Configure grid
        self.grid_columnconfigure(tuple(range(4)), weight=1)
        self.grid_rowconfigure(tuple(range(3)), weight=1)

        # Add Test Status headline
        self.test_status_headline = Heading2(
            self,
            text="Test Status"
        )
        self.test_status_headline.grid(row=0, column=0, columnspan=4, padx=10, pady=(20, 10), sticky="ew")

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
        self.serial_button.grid(row=1, column=1, sticky="e", padx=5, pady=(10, 0))
        
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
        self.voltage_button.grid(row=1, column=3, sticky="e", padx=(5, 20), pady=(10, 0))

        # Add Highest measured current label and button
        self.highest_current_label = StylizedLabel(
            self,
            text="Highest current measured:"
        )
        self.highest_current_label.grid(row=2, column=0, sticky="w", padx=(20, 5), pady=(10, 0))
        
        self.highest_current_button = BorderedLabel(
            self,
            text=""
        )
        self.highest_current_button.grid(row=2, column=1, sticky="e", padx=5, pady=(10, 0))

        # Add Maximum current threshold label and button
        self.max_current_label = StylizedLabel(
            self,
            text="Maximum current threshold:"
        )
        self.max_current_label.grid(row=2, column=2, sticky="w", padx=(5, 5), pady=(10, 0))
        
        self.max_current_button = BorderedLabel(
            self,
            text=""
        )
        self.max_current_button.grid(row=2, column=3, sticky="e", padx=(5, 20), pady=(10, 0))
        
        event_system.register_listener("test_started", self.on_test_started)
        event_system.register_listener("sub_test_started", self.on_sub_test_started)
        event_system.register_listener("sub_test_concluded", self.on_sub_test_concluded)
        event_system.register_listener("serial_number_confirmed", self.on_serial_number_confirmed)

    def on_test_started(self, event_data):
        self.serial_button.configure(text="")
        self.voltage_button.configure(text="")
        self.highest_current = 0.0
        self.highest_current_button.configure(text="")
        self.max_current_button.configure(text=f"{TestConstants.CURRENT_CUT_OFF.value}mA")
    
    def on_sub_test_started(self, event_data):
        voltage = event_data.get("voltage")
        self.voltage_button.configure(text=f"{voltage}V")
    
    def on_sub_test_concluded(self, event_data):
        current = event_data.get("current")
        if current > self.highest_current:
            self.highest_current = current
            self.highest_current_button.configure(text=f"{self.highest_current:.3f}mA")
    
    def on_serial_number_confirmed(self, event_data):
        serial_number = event_data.get("serial_number")
        self.serial_button.configure(text=serial_number)
