# menubar.py

import customtkinter as ctk
from CTkMenuBar import CTkMenuBar, CustomDropdownMenu  # Ensure this module is accessible
from test_logic import event_system
from .relay_selection_window import RelaySelectionWindow

class MenuBar:
    def __init__(self, master):
        self.master = master  # Reference to the main CTk instance
        self.menu = CTkMenuBar(master)
        self.create_menu()
    
    def create_menu(self):
        # Create menu buttons
        file_menu = self.menu.add_cascade("File")
        edit_menu = self.menu.add_cascade("Edit")
        settings_menu = self.menu.add_cascade("Settings")
        about_menu = self.menu.add_cascade("About")

        # Create dropdown for 'File' menu
        dropdown_file = CustomDropdownMenu(widget=file_menu)
        dropdown_file.add_option(option="Open", command=lambda: print("Open"))
        dropdown_file.add_option(option="Save", command=lambda: print("Save"))
        dropdown_file.add_separator()
        sub_export = dropdown_file.add_submenu("Export As")
        sub_export.add_option(option=".TXT", command=lambda: print("Export as TXT"))
        sub_export.add_option(option=".PDF", command=lambda: print("Export as PDF"))

        # Create dropdown for 'Edit' menu
        dropdown_edit = CustomDropdownMenu(widget=edit_menu)
        dropdown_edit.add_option(option="Cut", command=lambda: print("Cut"))
        dropdown_edit.add_option(option="Copy", command=lambda: print("Copy"))
        dropdown_edit.add_option(option="Paste", command=lambda: print("Paste"))

        # Create dropdown for 'Settings' menu
        dropdown_settings = CustomDropdownMenu(widget=settings_menu)
        dropdown_settings.add_option(option="Preferences", command=lambda: print("Preferences"))
        sub_theme = dropdown_settings.add_submenu("Theme")
        sub_theme.add_option(option="Light", command=self.set_light_theme)
        sub_theme.add_option(option="Dark", command=self.set_dark_theme)
        dropdown_settings.add_option(option="Select default relay", command=self.on_select_default_relay)

        # Create dropdown for 'About' menu
        dropdown_about = CustomDropdownMenu(widget=about_menu)
        dropdown_about.add_option(option="Hello World", command=lambda: print("About"))

    def set_light_theme(self):
        """Set the appearance mode to Light and notify all widgets."""
        ctk.set_appearance_mode("Light")

    def set_dark_theme(self):
        """Set the appearance mode to Dark and notify all widgets."""
        ctk.set_appearance_mode("Dark")

    def on_select_default_relay(self):
        # Create and display the relay selection window
        relay_window = RelaySelectionWindow(self.master)
        self.master.wait_window(relay_window)  # Wait for the window to be closed

        # Get the user's selection
        selected_relay = relay_window.result

        event_system.dispatch_event("default_relay_selected", {"selected_relay": selected_relay})
# Example usage
if __name__ == "__main__":
    app = ctk.CTk()  # Initialize the main CTk window
    app.geometry("600x400")
    app.title("CustomTkinter MenuBar Example")

    menu_bar = MenuBar(app)
    app.configure(menu=menu_bar.menu)  # Attach the menu to the main window

    app.mainloop()
