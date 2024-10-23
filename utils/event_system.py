from enum import Enum
import threading

class EventType(Enum):
    LOG_EVENT = "log_event"
    SUB_TEST_STARTED = "sub_test_started"
    # ... other non-log event types ...

class EventSystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventSystem, cls).__new__(cls)
            cls._instance.listeners = {}
            cls._instance.lock = threading.Lock()
        return cls._instance

    def register_listener(self, event_type: EventType, callback):
        with self._instance.lock:
            if event_type not in self._instance.listeners:
                self._instance.listeners[event_type] = []
            self._instance.listeners[event_type].append(callback)

    def unregister_listener(self, event_type: EventType, callback):
        with self._instance.lock:
            if event_type in self._instance.listeners:
                self._instance.listeners[event_type].remove(callback)
                if not self._instance.listeners[event_type]:
                    del self._instance.listeners[event_type]

    def dispatch_event(self, event_type: EventType, data=None):
        with self._instance.lock:
            listeners = self._instance.listeners.get(event_type, []).copy()
        for callback in listeners:
            callback(data)

# Initialize the singleton instance
event_system = EventSystem()
