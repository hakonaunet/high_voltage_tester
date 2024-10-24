# menubar.py
from time import sleep
import threading

import customtkinter as ctk
from CTkMenuBar import CTkMenuBar, CustomDropdownMenu

from utils import event_system
from .relay_selection_window import RelaySelectionWindow
from .debug_level_window import DebugLevelWindow
from utils.event_system import event_system, EventType, LogLevel
from ui.debugger_panel import DebuggerPanel
from hardware import HardwareClient

class MenuBar:
    def __init__(self, master):
        self.master = master  # Reference to the main CTk instance
        self.hardware_client = HardwareClient()  # Access the singleton instance
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
        self.relay_test(False)

    def test_backup_relays(self):
        self.relay_test(True)
    
    def relay_test(self, test_backup_relay):
        """Run relay tests in a separate thread to keep the UI responsive."""
        thread = threading.Thread(target=self._relay_test_thread, args=(test_backup_relay,), daemon=True)
        thread.start()
    
    def _relay_test_thread(self, test_backup_relay):
        try:
            original_relay_state = self.hardware_client.use_backup_relay
            self.hardware_client.use_backup_relay = test_backup_relay
            relay_type = "backup solid state" if test_backup_relay else "primary electromechanical"
            countdown = 7
            log_msg = (
                f"Test of the {relay_type} relay started. In {countdown} seconds, all relays will be turned on and off in sequence, "
                "with a 1 second delay between each action."
            )
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": log_msg, "level": LogLevel.INFO})
            sleep(countdown)
            event_system.dispatch_event(EventType.SET_RELAYS, {"relays": [0], "state": True})
            sleep(1)
            for i in range(7):
                event_system.dispatch_event(EventType.SET_RELAYS, {"relays": [i], "state": False})
                sleep(1)
                event_system.dispatch_event(EventType.SET_RELAYS, {"relays": [i+1], "state": True})
                sleep(1)
            event_system.dispatch_event(EventType.SET_RELAYS, {"relays": [7], "state": False})
            self.hardware_client.use_backup_relay = original_relay_state
            log_msg_completion = f"Relay test of the {relay_type} relay completed successfully."
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": log_msg_completion, "level": LogLevel.INFO})
        except Exception as e:
            error_msg = f"An error occurred during relay testing: {e}"
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": error_msg, "level": LogLevel.ERROR})
            # Restore the original relay state in case of an error
            self.hardware_client.use_backup_relay = original_relay_state

# Example usage
if __name__ == "__main__":
    app = ctk.CTk()  # Initialize the main CTk window
    app.geometry("600x400")
    app.title("CustomTkinter MenuBar Example")

    menu_bar = MenuBar(app)
    app.configure(menu=menu_bar.menu)  # Attach the menu to the main window

    app.mainloop()
