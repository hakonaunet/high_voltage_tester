import time
from test_logic import event_system

class SubTest:
    def __init__(self, test_number, voltage):
        self.test_number = test_number
        self.voltage = voltage
        self.current = None
        self.status = None

    def run(self):
        try:
            event_system.emit("test_started", {"test_name": f"Sub-test {self.test_number}"})
            event_system.emit("log_event", {"message": f"Setting hi-pot tester to {self.voltage}V", "level": "INFO"})
            
            # Simulate hardware configuration and measurement
            time.sleep(2)
            
            # Simulate reading current (replace with actual hardware interface)
            self.current = self._simulate_current_measurement()
            
            event_system.emit("log_event", {"message": f"Measured current: {self.current:.2f} mA", "level": "INFO"})
            
            # Evaluate test result (replace with actual criteria)
            if 0.1 <= self.current <= 1.0:
                self.status = "SUCCESS"
                event_system.emit("log_event", {"message": f"Sub-test {self.test_number} passed.", "level": "INFO"})
            else:
                self.status = "FAILURE"
                event_system.emit("log_event", {"message": f"Sub-test {self.test_number} failed.", "level": "WARNING"})
            
            return self.status

        except Exception as e:
            self.status = "ERROR"
            error_message = f"Error in sub-test {self.test_number}: {str(e)}"
            event_system.emit("error_occurred", {"error_message": error_message})
            event_system.emit("log_event", {"message": error_message, "level": "ERROR"})
            return self.status

    def _simulate_current_measurement(self):
        # Replace this with actual hardware interface
        import random
        return random.uniform(0.05, 1.5)

    def get_result(self):
        return {
            "test_number": self.test_number,
            "voltage": self.voltage,
            "current": self.current,
            "status": self.status
        }