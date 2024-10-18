import customtkinter as ctk
from test_logic import event_system
from utils import MAIN_COLOR
import time

class DebuggerPanel(ctk.CTkFrame):
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DebuggerPanel, cls).__new__(cls)
        return cls._instance

    def __init__(self, parent, max_logs=500):
        if self._initialized:
            return
        self._initialized = True

        super().__init__(
            parent, 
            corner_radius=15, 
            fg_color=("gray88", "gray17"), 
            border_width=2, 
            border_color=MAIN_COLOR
        )
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialize the textbox for the debugger panel
        self.textbox = ctk.CTkTextbox(
            self, 
            corner_radius=15, 
            fg_color=("gray88", "gray17"), 
            border_width=2, 
            border_color=MAIN_COLOR
        )
        self.textbox.grid(row=0, column=0, padx=(10, 8), pady=(10, 10), sticky="nsew")
        
        # Set initial content
        self.textbox.insert("0.0", "Debugger Panel\n\n")
        self.textbox.configure(state="disabled")  # Make it read-only

        # Add a clear button
        self.clear_button = ctk.CTkButton(self, text="Clear", command=self.clear_log)
        self.clear_button.grid(row=1, column=0, padx=(10, 8), pady=(0, 10), sticky="e")

        # Initialize log storage
        self.logs = []
        self.max_logs = max_logs

        # Register event listeners
        event_system.register_listener("log_event", self.handle_log_event)
        event_system.register_listener("test_started", self.handle_test_started)
        event_system.register_listener("error_occurred", self.handle_error_occurred)
        # Add more listeners as needed

    def clear_log(self):
        """Clears the debugger log."""
        self.logs = []
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("0.0", "Debugger Panel\n\n")
        self.textbox.configure(state="disabled")

    def log(self, message, level="INFO"):
        """Add a log message to the debugger panel."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        # Manage log size
        if len(self.logs) >= self.max_logs:
            self.logs.pop(0)  # Remove the oldest log entry

        self.logs.append(log_entry)

        # Update the textbox
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")  # Clear current content
        self.textbox.insert("0.0", "Debugger Panel\n\n" + "".join(self.logs))
        self.textbox.see("end")  # Scroll to the bottom
        self.textbox.configure(state="disabled")

    def handle_log_event(self, data):
        message = data.get('message', 'No message provided.')
        level = data.get('level', 'INFO')
        self.log(message, level)

    def handle_test_started(self, data):
        test_name = data.get('test_name', 'Unnamed Test')
        self.log(f"{test_name} started", "INFO")
        # Trigger UI updates or animations related to test start

    def handle_error_occurred(self, data):
        error_message = data.get('error_message', 'An error occurred.')
        self.log(error_message, "ERROR")
        # Trigger UI updates or animations related to errors

    def update_theme(self, new_theme):
        """Update the theme of the debugger panel."""
        if new_theme == "dark":
            self.configure(fg_color="gray17")
            self.textbox.configure(fg_color="gray17")
        else:
            self.configure(fg_color="gray88")
            self.textbox.configure(fg_color="gray88")

    def destroy(self):
        """Override destroy to unregister event listeners."""
        event_system.unregister_listener("log_event", self.handle_log_event)
        event_system.unregister_listener("test_started", self.handle_test_started)
        event_system.unregister_listener("error_occurred", self.handle_error_occurred)
        super().destroy()
