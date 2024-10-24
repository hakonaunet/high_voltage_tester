# menubar.py

import customtkinter as ctk
from CTkMenuBar import CTkMenuBar, CustomDropdownMenu  # Ensure this module is accessible
from utils import event_system
from .relay_selection_window import RelaySelectionWindow
from .debug_level_window import DebugLevelWindow
from utils.event_system import event_system, EventType, LogLevel
from ui.debugger_panel import DebuggerPanel

class MenuBar:
    def __init__(self, master):
        self.master = master  # Reference to the main CTk instance
        self.menu = CTkMenuBar(master)
        self.create_menu()
    
    def create_menu(self):
        # Create menu buttons
        settings_menu = self.menu.add_cascade("Settings")
        troubleshooting_menu = self.menu.add_cascade("Troubleshooting")
        about_menu = self.menu.add_cascade("About")

        # Create dropdown for 'Settings' menu
        dropdown_settings = CustomDropdownMenu(widget=settings_menu)
        sub_theme = dropdown_settings.add_submenu("Theme")
        sub_theme.add_option(option="Light", command=self.set_light_theme)
        sub_theme.add_option(option="Dark", command=self.set_dark_theme)
        dropdown_settings.add_option(option="Select default relay", command=self.on_select_default_relay)
        dropdown_settings.add_option(option="Debug levels", command=self.on_select_debug_levels)

        # Create dropdown for 'Troubleshooting' menu
        dropdown_troubleshooting = CustomDropdownMenu(widget=troubleshooting_menu)
        dropdown_troubleshooting.add_option(option="Verify Raspberry Pi connection", command=self.verify_raspberry_pi_connection)
        dropdown_troubleshooting.add_option(option="Test primary relays", command=self.test_primary_relays)
        dropdown_troubleshooting.add_option(option="Test backup relays", command=self.test_backup_relays)

        # Create dropdown for 'About' menu
        dropdown_about = CustomDropdownMenu(widget=about_menu)
        dropdown_about.add_option(option="Hello World", command=lambda: print("About"))

    def set_light_theme(self):
        """Set the appearance mode to Light and notify all widgets."""
        ctk.set_appearance_mode("Light")

    def set_dark_theme(self):
        """Set the appearance mode to Dark and notify all widgets."""
        ctk.set_appearance_mode("Dark")
    
    def on_select_debug_levels(self):
        from ui.debugger_panel import DebuggerPanel
        debugger_panel = DebuggerPanel._instance
        if debugger_panel:
            debug_level_window = DebugLevelWindow(self.master, debugger_panel.active_debug_levels)
            self.master.wait_window(debug_level_window)

    def on_select_default_relay(self):
        # Create and display the relay selection window
        relay_window = RelaySelectionWindow(self.master)
        self.master.wait_window(relay_window)  # Wait for the window to be closed

        # Get the user's selection
        selected_relay = relay_window.result

        event_system.dispatch_event(EventType.DEFAULT_RELAY_SELECTED, {"selected_relay": selected_relay})

    def verify_raspberry_pi_connection(self):
        event_system.dispatch_event(EventType.VERIFY_RASPBERRY_PI_CONNECTION, {"level": LogLevel.INFO})

    def test_primary_relays(self):
        pass

    def test_backup_relays(self):
        pass
# Example usage
if __name__ == "__main__":
    app = ctk.CTk()  # Initialize the main CTk window
    app.geometry("600x400")
    app.title("CustomTkinter MenuBar Example")

    menu_bar = MenuBar(app)
    app.configure(menu=menu_bar.menu)  # Attach the menu to the main window

    app.mainloop()
