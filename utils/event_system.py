from enum import Enum, auto
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
    DEBUG_LEVELS_CHANGED = "debug_levels_changed"
    # Add any other necessary event types here

class LogLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()

    @classmethod
    def from_string(cls, level_str: str):
        try:
            return cls[level_str.upper()]
        except KeyError:
            raise ValueError(f"Invalid log level: {level_str}. Must be one of {[level.name for level in cls]}")

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
        
        # Validate log level if this is a log event
        if event_type == EventType.LOG_EVENT and data:
            level = data.get('level')
            if not isinstance(level, LogLevel):
                raise TypeError(f"Log level must be an instance of LogLevel enum, not {type(level)}. "
                              f"Use LogLevel.LEVEL_NAME instead of string values.")
        
        with self._instance.lock:
            listeners = self._instance.listeners.get(event_type, []).copy()
        for callback in listeners:
            callback(data)

# Initialize the singleton instance
event_system = EventSystem()
