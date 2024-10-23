import time
import random
from utils import event_system, EventType, TestConstants, test_number_to_relays, LogLevel

class SubTest:
    def __init__(self, test_number, voltage):
        self.test_number = test_number
        self.voltage = voltage
        self.current = None
        self.status = None

    def run(self):
        try:
            # Dispatch SUB_TEST_STARTED event
            event_system.dispatch_event(EventType.SUB_TEST_STARTED, {
                "test_number": self.test_number,
                "voltage": self.voltage
            })

            # Log setting hi-pot voltage
            event_system.dispatch_event(EventType.LOG_EVENT, {
                "message": f"Setting hi-pot tester to {self.voltage}V",
                "level": LogLevel.INFO
            })
            event_system.dispatch_event(EventType.SET_HIPOT_VOLTAGE, {"voltage": self.voltage})

            relays = test_number_to_relays[self.test_number]
            # Log setting relays to open before measurement
            event_system.dispatch_event(EventType.LOG_EVENT, {
                "message": f"Setting relays {relays} to open before measurement",
                "level": LogLevel.INFO
            })
            event_system.dispatch_event(EventType.SET_RELAYS, {
                "relays": relays,
                "timeout": 10,
                "state": True
            })

            # Simulate test runtime
            time.sleep(TestConstants.RUNTIME.value)
            
            # Simulate reading current (replace with actual hardware interface)
            self.current = self._simulate_current_measurement()
            
            # Log measured current
            event_system.dispatch_event(EventType.LOG_EVENT, {
                "message": f"Measured current: {self.current:.2f} mA",
                "level": LogLevel.INFO
            })

            # Evaluate test result
            if 0 <= self.current <= TestConstants.CURRENT_CUT_OFF.value:
                self.status = "SUCCESS"
                event_system.dispatch_event(EventType.LOG_EVENT, {
                    "message": f"Sub-test {self.test_number} passed.",
                    "level": LogLevel.INFO
                })
            else:
                self.status = "FAILURE"
                event_system.dispatch_event(EventType.LOG_EVENT, {
                    "message": f"Sub-test {self.test_number} failed.",
                    "level": LogLevel.WARNING
                })

            # Log setting relays to closed after measurement
            event_system.dispatch_event(EventType.LOG_EVENT, {
                "message": f"Setting relays {relays} to closed after measurement",
                "level": LogLevel.INFO
            })
            event_system.dispatch_event(EventType.SET_RELAYS, {"relays": relays, "state": False})

            # Dispatch SUB_TEST_CONCLUDED event
            event_system.dispatch_event(EventType.SUB_TEST_CONCLUDED, {
                "test_number": self.test_number,
                "status": self.status,
                "current": self.current
            })

            return self.status

        except Exception as e:
            self.status = "ERROR"
            error_message = f"Error in sub-test {self.test_number}: {str(e)}"
            
            # Replace ERROR_OCCURRED with LOG_EVENT at ERROR level
            event_system.dispatch_event(EventType.LOG_EVENT, {
                "message": error_message,
                "level": LogLevel.ERROR
            })
            
            # Dispatch SUB_TEST_CONCLUDED event for error case
            event_system.dispatch_event(EventType.SUB_TEST_CONCLUDED, {
                "test_number": self.test_number,
                "status": self.status,
                "current": self.current  # This might be None in case of an error
            })
            
            return self.status

    def _simulate_current_measurement(self):
        # Replace this with actual hardware interface
        return random.uniform(0.0, 6)

    def get_result(self):
        return {
            "test_number": self.test_number,
            "voltage": self.voltage,
            "current": self.current,
            "status": self.status
        }
