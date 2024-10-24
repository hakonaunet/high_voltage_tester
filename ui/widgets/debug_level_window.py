import customtkinter as ctk
from utils.event_system import LogLevel, event_system, EventType

class DebugLevelWindow(ctk.CTkToplevel):
    def __init__(self, parent, current_levels=None):
        super().__init__(parent)
        
        self.title("Debug Level Selection")
        self.geometry("300x255")
        self.resizable(False, False)
        
        # Initialize variables
        self.debug_levels = {level: ctk.BooleanVar(value=level in (current_levels or [])) 
                           for level in LogLevel}
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Create main label
        self.label = ctk.CTkLabel(
            self,
            text="Select Debug Levels to Display:",
            font=("Arial", 14, "bold")
        )
        self.label.grid(row=0, column=0, pady=(20, 10))
        
        # Create frame for checkboxes
        checkbox_frame = ctk.CTkFrame(self, fg_color="transparent")
        checkbox_frame.grid(row=1, column=0, sticky="nsew")
        
        # Create checkboxes for each debug level
        for i, level in enumerate(reversed(list(LogLevel))):
            checkbox = ctk.CTkCheckBox(
                checkbox_frame,
                text=level.name,
                variable=self.debug_levels[level],
            )
            checkbox.grid(row=i, column=0, pady=5, padx=(113, 0), sticky="w")
        
        # Create apply button
        self.apply_button = ctk.CTkButton(
            self,
            text="Apply",
            command=self.apply_settings
        )
        self.apply_button.grid(row=2, column=0, pady=20)
        
    def apply_settings(self):
        selected_levels = {level for level, var in self.debug_levels.items() 
                         if var.get()}
        event_system.dispatch_event(
            EventType.LOG_EVENT,
            {
                "message": f"Debug levels updated to: {[level.name for level in selected_levels]}",
                "level": LogLevel.INFO
            }
        )
        event_system.dispatch_event(
            EventType.DEBUG_LEVELS_CHANGED,
            {"levels": selected_levels}
        )
        self.destroy()

