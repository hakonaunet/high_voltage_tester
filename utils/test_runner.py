import threading
import time
from utils import event_system

class TestRunner:
    def __init__(self):
        self.serial_number = None
        self.is_running = False
        # Initialize other necessary components like hardware interfaces

    def run_tests(self, serial_number):
        if self.is_running:
            event_system.emit("error_occurred", {"error_message": "Test already running."})
            return

        self.serial_number = serial_number
        self.is_running = True
        threading.Thread(target=self._execute_tests).start()

    def _execute_tests(self):
        try:
            event_system.emit("test_started", {"test_name": "Initial Setup"})
            # Setup initial hardware configurations

            for i in range(6):
                voltage = 500 if i < 3 else 1600
                event_system.emit("log_event", {"message": f"Setting hi-pot tester to {voltage}V", "level": "INFO"})
                # Set voltage on hi-pot tester
                # Configure relay modules based on test number

                # Simulate test execution
                time.sleep(2)
                # Read results from hardware
                event_system.emit("log_event", {"message": f"Test {i+1} completed successfully.", "level": "INFO"})

            # Upload results to the database
            event_system.emit("log_event", {"message": "Uploading results to the database.", "level": "INFO"})
            # Perform upload

            event_system.emit("log_event", {"message": "All tests completed successfully.", "level": "INFO"})
        except Exception as e:
            event_system.emit("error_occurred", {"error_message": str(e)})
        finally:
            self.is_running = False

    def stop_tests(self):
        if self.is_running:
            # Implement logic to safely stop tests
            self.is_running = False
            event_system.emit("log_event", {"message": "Test execution stopped by user.", "level": "WARNING"})