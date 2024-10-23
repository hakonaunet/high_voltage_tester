import customtkinter as ctk
from utils import event_system, EventType, LogLevel, MAIN_COLOR
import time
from enum import Enum, auto


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

        # Create a frame for buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, padx=(10, 8), pady=(0, 10), sticky="ew")
        
        # Add debug level selection button
        self.debug_level_button = ctk.CTkButton(
            self.button_frame,
            text="Debug Levels",
            command=self.show_debug_level_selection
        )
        self.debug_level_button.pack(side="left", padx=5)
        
        # Move clear button to button frame
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            command=self.clear_log
        )
        self.clear_button.pack(side="right", padx=5)
        
        # Initialize log storage
        self.logs = []
        self.max_logs = max_logs
        self.show_debug = False  # Initialize the show_debug flag
        self.active_debug_levels = {LogLevel.INFO, LogLevel.WARNING, LogLevel.ERROR}
        
        # Register event listeners using EventType Enum
        event_system.register_listener(EventType.LOG_EVENT, self.handle_log_event)
        event_system.register_listener(EventType.DEBUG_LEVELS_CHANGED, self.handle_debug_levels_changed)

    def show_debug_level_selection(self):
        from ui.widgets.debug_level_window import DebugLevelWindow
        DebugLevelWindow(self, self.active_debug_levels)
    
    def handle_debug_levels_changed(self, data):
        self.active_debug_levels = data.get("levels", {LogLevel.INFO, LogLevel.WARNING, LogLevel.ERROR})
    
    def clear_log(self):
        """Clears the debugger log."""
        self.logs = []
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("0.0", "Debugger Panel\n\n")
        self.textbox.configure(state="disabled")

    def log(self, message, level):
        if isinstance(level, str):
            level = LogLevel.from_string(level)
        
        if level not in self.active_debug_levels:
            return
            
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level.name}] {message}\n"
        
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

    # Removed handle_debug_event method

    def destroy(self):
        """Override destroy to unregister event listeners and theme callback."""
        event_system.unregister_listener(EventType.LOG_EVENT, self.handle_log_event)
        event_system.unregister_listener(EventType.DEBUG_LEVELS_CHANGED, self.handle_debug_levels_changed)
        # Removed unregistration for EventType.DEBUG_EVENT
        super().destroy()
