# test_runner.py
import threading
import time
import json
import socket

from test_logic import event_system
from test_logic.sub_test import SubTest

# Import the new HardwareClient
from hardware.hardware_client import HardwareClient

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

    def run_tests(self, serial_number):
        if self.is_running:
            event_system.dispatch_event("error_occurred", {"error_message": "Test already running."})
            return
        if not self.batch_info:
            event_system.dispatch_event("error_occurred", {"error_message": "Batch information not set."})
            return
        self.serial_number = serial_number
        self.is_running = True
        self.results = []
        threading.Thread(target=self._execute_tests, daemon=True).start()

    def _execute_tests(self):
        try:
            event_system.dispatch_event("progress_update", {"position": 0})
            self.current_position = 0

            sub_tests = [
                SubTest(1, 500), SubTest(2, 500), SubTest(3, 500),
                SubTest(4, 1600), SubTest(5, 1600), SubTest(6, 1600)
            ]

            for i, sub_test in enumerate(sub_tests, start=1):
                if not self.is_running:
                    break
                
                status = sub_test.run()
                self.results.append(sub_test.get_result())
                
                if status == "ERROR":
                    break

                if i > self.current_position:
                    self.current_position = i
                    event_system.dispatch_event("progress_update", {"position": i})

                time.sleep(2)  # 2-second cooldown between sub-tests

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

    def run_test(self):
        try:
            event_system.dispatch_event("test_started", {"test_name": "Full Test Suite"})
            
            for i, voltage in enumerate(self.voltages, start=1):
                sub_test = SubTest(i, voltage)
                result = sub_test.run()
                self.results.append(sub_test.get_result())
                
                if result != "SUCCESS":
                    event_system.dispatch_event("test_terminated", {})
                    return False
            
            event_system.dispatch_event("test_completed", {})
            return True
        except Exception as e:
            error_message = f"Error in test runner: {str(e)}"
            event_system.dispatch_event("error_occurred", {"error_message": error_message})
            event_system.dispatch_event("test_terminated", {})
            return False
