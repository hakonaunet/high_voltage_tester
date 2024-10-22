# test_runner.py
import threading
import time
import json
import socket

from test_logic import event_system
from test_logic.sub_test import SubTest

# Import the new HardwareClient
from hardware.hardware_client import HardwareClient

from ui.widgets.serial_number_window import SerialNumberWindow 

class TestRunner:
    def __init__(self, hardware_client: HardwareClient):
        self.hardware_client = hardware_client
        self.serial_number = None
        self.is_running = False
        self.results = []
        self.current_position = 0
        self.batch_info = None  # Add this
        
        # Register event listeners for batch information
        event_system.register_listener('batch_info_confirmed', self.handle_batch_info_confirmed)
        event_system.register_listener('batch_info_cleared', self.handle_batch_info_cleared)

    def handle_batch_info_confirmed(self, data):
        self.batch_info = data.get('batch_info')

    def handle_batch_info_cleared(self, data):
        self.batch_info = None

    def run_tests(self):
        event_system.dispatch_event("test_started")
        if self.is_running:
            event_system.dispatch_event("error_occurred", {"error_message": "Test already running."})
            return
        if not self.batch_info:
            event_system.dispatch_event("error_occurred", {"error_message": "Batch information not set."})
            return
        
        event_system.dispatch_event("progress_update", {"position": 0})
        serial_number = self.get_serial_number()
        if serial_number:
            event_system.dispatch_event("log_event", {"message": f"Submitted serial number: {serial_number}.", "level": "INFO"})
            event_system.dispatch_event("serial_number_confirmed", {"serial_number": serial_number})
        else:
            event_system.dispatch_event("error_occurred", {"error_message": "Serial number not provided."})
            return
        
        self.serial_number = serial_number
        self.is_running = True
        self.results = []
        threading.Thread(target=self._execute_tests, daemon=True).start()

    def get_serial_number(self):
        # Instantiate and display the SerialNumberWindow
        serial_window = SerialNumberWindow(None)  # Replace 'None' with the appropriate parent if necessary
        serial_window.grab_set()  # Make the window modal
        serial_window.wait_window()  # Wait for the window to close
        return serial_window.serial_number

    def _execute_tests(self):
        try:
            # Check connection with hardware client
            if not self.hardware_client.check_connection():
                event_system.dispatch_event("log_event", {
                    "message": "Hardware connection check failed. Test execution aborted.",
                    "level": "ERROR"
                })
                event_system.dispatch_event("test_terminated", {})
                return

            event_system.dispatch_event("log_event", {
                "message": "Hardware connection confirmed. Starting test execution.",
                "level": "INFO"
            })

            event_system.dispatch_event("progress_update", {"position": 1})
            self.current_position = 1

            sub_tests = [
                SubTest(1, 500), SubTest(2, 500), SubTest(3, 500),
                SubTest(4, 1600), SubTest(5, 1600), SubTest(6, 1600)
            ]

            for i, sub_test in enumerate(sub_tests, start=1):
                if not self.is_running:
                    break
                if i > self.current_position:
                    self.current_position = i
                    event_system.dispatch_event("progress_update", {"position": i})
                
                status = sub_test.run()
                self.results.append(sub_test.get_result())
                
                if status == "ERROR":
                    break


            if self.is_running:
                self._upload_results()
                event_system.dispatch_event("progress_update", {"position": 7})

            event_system.dispatch_event("test_terminated")
        except Exception as e:
            event_system.dispatch_event("error_occurred", {"error_message": str(e)})
        finally:
            self.is_running = False

    def _upload_results(self):
        event_system.dispatch_event("log_event", {"message": "Uploading results to the database.", "level": "INFO"})
        # Perform upload
        # You can access self.results and self.batch_info here to upload the data

    def stop_tests(self):
        if self.is_running:
            self.is_running = False
            event_system.dispatch_event("log_event", {"message": "Test execution stopped by user.", "level": "WARNING"})

    def get_results(self):
        return self.results

    def close(self):
        # Implement any necessary cleanup for TestRunner
        pass
