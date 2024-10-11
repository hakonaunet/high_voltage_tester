import threading
from test_logic import event_system
from test_logic.sub_test import SubTest

class TestRunner:
    def __init__(self):
        self.serial_number = None
        self.is_running = False
        self.results = []

    def run_tests(self, serial_number):
        if self.is_running:
            event_system.emit("error_occurred", {"error_message": "Test already running."})
            return

        self.serial_number = serial_number
        self.is_running = True
        self.results = []
        threading.Thread(target=self._execute_tests).start()

    def _execute_tests(self):
        try:
            event_system.emit("test_started", {"test_name": "Initial Setup"})
            # Setup initial hardware configurations

            sub_tests = [
                SubTest(1, 500), SubTest(2, 500), SubTest(3, 500),
                SubTest(4, 1600), SubTest(5, 1600), SubTest(6, 1600)
            ]

            for sub_test in sub_tests:
                if not self.is_running:
                    break
                
                status = sub_test.run()
                self.results.append(sub_test.get_result())
                
                if status == "ERROR":
                    break

            if self.is_running:
                self._upload_results()

            event_system.emit("log_event", {"message": "All tests completed.", "level": "INFO"})
        except Exception as e:
            event_system.emit("error_occurred", {"error_message": str(e)})
        finally:
            self.is_running = False

    def _upload_results(self):
        event_system.emit("log_event", {"message": "Uploading results to the database.", "level": "INFO"})
        # Perform upload
        # You can access self.results here to upload the data

    def stop_tests(self):
        if self.is_running:
            self.is_running = False
            event_system.emit("log_event", {"message": "Test execution stopped by user.", "level": "WARNING"})

    def get_results(self):
        return self.results