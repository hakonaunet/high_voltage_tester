# main_window.py

import os
import customtkinter as ctk
from ui.widgets import MenuBar  # Import the MenuBar class
from ui.main_frame import MainFrame  # Import the MainFrame class
from utils import MAIN_COLOR  # Import the MAIN_COLOR constant

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the theme file
theme_path = os.path.join(current_dir, "themes", "et_green_develop.json")

# Set the default color theme using the constructed path
ctk.set_default_color_theme(theme_path)

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("High Voltage Tester")
        self.geometry("1600x900")
        
        # Get the absolute path to the icon file
        icon_path = os.path.abspath("ui/images/icons/eltorqueicon_develop.ico")  # Ensure this is a valid .ico file
        self.iconbitmap(icon_path)

        # Attach the menu bar
        self.menu_bar = MenuBar(self)

        # Create and attach the main frame
        self.main_frame = MainFrame(self)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
