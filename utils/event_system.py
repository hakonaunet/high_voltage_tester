from enum import Enum
import threading

class EventType(Enum):
    LOG_EVENT = "log_event"
    SUB_TEST_STARTED = "sub_test_started"
    SUB_TEST_CONCLUDED = "sub_test_concluded"
    BATCH_INFO_CONFIRMED = "batch_info_confirmed"
    BATCH_INFO_CLEARED = "batch_info_cleared"
    SET_HIPOT_VOLTAGE = "set_hipot_voltage"
    SET_RELAYS = "set_relays"
    DEFAULT_RELAY_SELECTED = "default_relay_selected"
    VERIFY_RASPBERRY_PI_CONNECTION = "verify_raspberry_pi_connection"
    TEST_STARTED = "test_started"
    PROGRESS_UPDATE = "progress_update"
    SERIAL_NUMBER_CONFIRMED = "serial_number_confirmed"
    TEST_TERMINATED = "test_terminated"
    # Add any other necessary event types here

class EventSystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventSystem, cls).__new__(cls)
            cls._instance.listeners = {}
            cls._instance.lock = threading.Lock()
        return cls._instance

    def _validate_event_type(self, event_type: EventType) -> None:
        """Validates that the event_type is an instance of EventType enum"""
        if not isinstance(event_type, EventType):
            raise TypeError(f"Event type must be an instance of EventType enum, not {type(event_type)}. "
                          f"Use EventType.EVENT_NAME instead of string values.")

    def register_listener(self, event_type: EventType, callback):
        self._validate_event_type(event_type)
        with self._instance.lock:
            if event_type not in self._instance.listeners:
                self._instance.listeners[event_type] = []
            self._instance.listeners[event_type].append(callback)

    def unregister_listener(self, event_type: EventType, callback):
        self._validate_event_type(event_type)
        with self._instance.lock:
            if event_type in self._instance.listeners:
                self._instance.listeners[event_type].remove(callback)
                if not self._instance.listeners[event_type]:
                    del self._instance.listeners[event_type]

    def dispatch_event(self, event_type: EventType, data=None):
        self._validate_event_type(event_type)
        with self._instance.lock:
            listeners = self._instance.listeners.get(event_type, []).copy()
        for callback in listeners:
            callback(data)

# Initialize the singleton instance
event_system = EventSystem()
