import time
from test_logic import event_system
from utils.constants import TestConstants
class SubTest:
    def __init__(self, test_number, voltage):
        self.test_number = test_number
        self.voltage = voltage
        self.current = None
        self.status = None

    def run(self):
        try:
            event_system.dispatch_event("sub_test_started", {"test_name": f"Sub-test {self.test_number}", "voltage": self.voltage})
            event_system.dispatch_event("log_event", {"message": f"Setting hi-pot tester to {self.voltage}V", "level": "INFO"})
            
            # Simulate reading current (replace with actual hardware interface)
            self.current = self._simulate_current_measurement()
            
            event_system.dispatch_event("log_event", {"message": f"Measured current: {self.current:.2f} mA", "level": "INFO"})
            
            # Evaluate test result
            if 0 <= self.current <= TestConstants.CURRENT_CUT_OFF.value:
                self.status = "SUCCESS"
                event_system.dispatch_event("log_event", {"message": f"Sub-test {self.test_number} passed.", "level": "INFO"})
            else:
                self.status = "FAILURE"
                event_system.dispatch_event("log_event", {"message": f"Sub-test {self.test_number} failed.", "level": "WARNING"})
            
            # Dispatch the new sub_test_concluded event
            event_system.dispatch_event("sub_test_concluded", {
                "test_number": self.test_number,
                "status": self.status,
                "current": self.current
            })
            
            return self.status

        except Exception as e:
            self.status = "ERROR"
            error_message = f"Error in sub-test {self.test_number}: {str(e)}"
            event_system.dispatch_event("error_occurred", {"error_message": error_message})
            event_system.dispatch_event("log_event", {"message": error_message, "level": "ERROR"})
            
            # Dispatch the new sub_test_concluded event for error case
            event_system.dispatch_event("sub_test_concluded", {
                "test_number": self.test_number,
                "status": self.status,
                "current": self.current  # This might be None in case of an error
            })
            
            return self.status

    def _simulate_current_measurement(self):
        # Replace this with actual hardware interface
        import random
        time.sleep(2)
        return random.uniform(0.0, 6)

    def get_result(self):
        return {
            "test_number": self.test_number,
            "voltage": self.voltage,
            "current": self.current,
            "status": self.status
        }
