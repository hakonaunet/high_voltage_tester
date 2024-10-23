# test_runner.py
import threading
import time
import json
import socket

from utils.event_system import event_system, EventType  # {{ edit_1 }}
from test_logic.sub_test import SubTest
from hardware.hardware_client import HardwareClient
from ui.widgets.serial_number_window import SerialNumberWindow 
from utils.constants import TestConstants

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
        event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Test started.", "level": "INFO"})  # {{ edit_2 }}
        if self.is_running:
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Test already running.", "level": "ERROR"})  # {{ edit_3 }}
            return
        if not self.batch_info:
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Batch information not set.", "level": "ERROR"})  # {{ edit_4 }}
            return
        
        event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Progress update: Position 0.", "level": "INFO"})  # {{ edit_5 }}
        serial_number = self.get_serial_number()
        if serial_number:
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": f"Submitted serial number: {serial_number}.", "level": "INFO"})  # {{ edit_6 }}
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": f"Serial number confirmed: {serial_number}.", "level": "INFO"})  # {{ edit_7 }}
        else:
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Serial number not provided.", "level": "ERROR"})  # {{ edit_8 }}
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
                event_system.dispatch_event(EventType.LOG_EVENT, {
                    "message": "Hardware connection check failed. Test execution aborted.",
                    "level": "ERROR"
                })  # {{ edit_9 }}
                event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Test terminated.", "level": "INFO"})  # {{ edit_10 }}
                return

            event_system.dispatch_event(EventType.LOG_EVENT, {
                "message": "Hardware connection confirmed. Starting test execution.",
                "level": "INFO"
            })  # {{ edit_11 }}

            event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Progress update: Position 1.", "level": "INFO"})  # {{ edit_12 }}
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
                    event_system.dispatch_event(EventType.LOG_EVENT, {"message": f"Progress update: Position {i}.", "level": "INFO"})  # {{ edit_13 }}
                
                status = sub_test.run()
                self.results.append(sub_test.get_result())
                if (i != len(sub_tests)):
                    time.sleep(TestConstants.PAUSE_TIME.value)
                if status == "ERROR":
                    break


            if self.is_running:
                self._upload_results()
                event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Progress update: Position 7.", "level": "INFO"})  # {{ edit_14 }}

            event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Test terminated.", "level": "INFO"})  # {{ edit_15 }}
        except Exception as e:
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": str(e), "level": "ERROR"})  # {{ edit_16 }}
        finally:
            self.is_running = False

    def _upload_results(self):
        event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Uploading results to the database.", "level": "INFO"})  # {{ edit_17 }}
        # Perform upload
        # You can access self.results and self.batch_info here to upload the data

    def stop_tests(self):
        if self.is_running:
            self.is_running = False
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Test execution stopped by user.", "level": "WARNING"})  # {{ edit_18 }}

    def get_results(self):
        return self.results

    def close(self):
        # Implement any necessary cleanup for TestRunner
        pass
