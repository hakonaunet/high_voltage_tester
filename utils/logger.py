import os
import time
from utils.event_system import event_system, EventType

class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.log_directory = os.path.join(os.getcwd(), "log_files")
        os.makedirs(self.log_directory, exist_ok=True)
        start_time = time.strftime("%Y%m%d_%H%M%S")
        self.log_file_path = os.path.join(self.log_directory, f"HV_tester_log_{start_time}.txt")
        self._initialize_log_file()
        
        # Register the log_event listener
        event_system.register_listener(EventType.LOG_EVENT, self.handle_log_event)

    def _initialize_log_file(self):
        with open(self.log_file_path, 'w') as log_file:
            log_file.write("Log File Created\n")
            log_file.write(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    def handle_log_event(self, data):
        message = data.get('message', 'No message provided.')
        level = data.get('level', 'INFO')
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        self._write_log(log_entry)

    def _write_log(self, log_entry):
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(log_entry)

    def __del__(self):
        # Unregister the listener when the Logger is destroyed
        event_system.unregister_listener(EventType.LOG_EVENT, self.handle_log_event)

# Initialize the Logger instance at program start
logger = Logger()
