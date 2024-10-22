from ui.widgets.stylized_frame import StylizedFrame
from ui.widgets.headings import Heading2
from ui.widgets import StylizedButton
from test_logic.event_system import event_system

class ControlFrame(StylizedFrame):
    def __init__(self, parent, test_runner, hardware_client):
        super().__init__(parent)

        self.test_runner = test_runner
        self.hardware_client = hardware_client  # Ensure hardware_client is passed correctly

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        for i in range(1, 6):
            self.grid_rowconfigure(i, weight=1)

        # Add heading
        self.heading = Heading2(self, text="Test Controls")
        self.heading.grid(row=0, column=0, pady=(20, 10), padx=10, sticky="ew")

        # Add buttons
        self.start_button = StylizedButton(
            self, 
            text="Start Test", 
            command=self.start_test
        )
        self.start_button.grid(row=1, column=0, pady=(20, 5), padx=10)

        self.stop_button = StylizedButton(
            self, 
            text="Stop Test", 
            command=self.stop_test
        )
        self.stop_button.grid(row=2, column=0, pady=(20, 5), padx=10)

        self.reset_button = StylizedButton(
            self, 
            text="Reset Test", 
            command=self.reset_test
        )
        self.reset_button.grid(row=3, column=0, pady=(20, 10), padx=10)

    def start_test(self):
        self.test_runner.run_tests()

    def stop_test(self):
        self.test_runner.stop_tests()

    def reset_test(self):
        # Implement reset functionality
        event_system.dispatch_event("log_event", {"message": "Resetting tests.", "level": "INFO"})
        self.test_runner.stop_tests()
        self.test_runner.results = []
        self.test_runner.is_running = False
        self.test_runner.serial_number = None
        # Optionally, reset hardware state
        self.test_runner.ni_usb_6525.set_all_relays_off()
