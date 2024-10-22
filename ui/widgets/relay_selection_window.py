import customtkinter as ctk

from ui.widgets import stylized_button
from utils import Colors, darken_hex_color

class RelaySelectionWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Relay Module Selection")
        self.geometry("600x300")
        self.resizable(False, False)
        self.grab_set()  # Make the window modal
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)  # Handle window close event

        self.result = None  # To store the user's selection

        # Configure grid
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(tuple(range(1, 4)), weight=1)

        # Create the message text
        message_text = (
            "You are about to set which of the two relay modules to use; "
            "the default is an electromechanical relay interfacing with the Raspberry Pi's GPIO pins, "
            "and the backup is a solid state relay connected directly to the PC. "
            "Only proceed to change this setting if you understand the implications."
        )

        # Message Label
        self.label_message = ctk.CTkLabel(
            self, text=message_text, wraplength=560, justify="center", font=("Arial", 14)
        )
        self.label_message.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=20, sticky="nsew")

        # Prompt Label
        self.label_prompt = ctk.CTkLabel(
            self, text="Please select default relay:", font=("Arial", 16, "bold")
        )
        self.label_prompt.grid(row=1, column=0, columnspan=2, pady=(10, 10), sticky="nsew")

        # Electromechanical Relay Button
        self.button_electromechanical = stylized_button.StylizedButton(
            self,
            text="Electromechanical Relay",
            command=self.on_select_electromechanical,
            width=300,
        )
        self.button_electromechanical.grid(row=2, column=0, padx=(20, 10), pady=0, sticky="nsew")

        # Solid State Relay Button
        self.button_solid_state = stylized_button.StylizedButton(
            self,
            text="Solid State Relay",
            command=self.on_select_solid_state,
            fg_color=Colors.NEON_RED.value,
            border_color=Colors.NEON_RED.value,
            hover_color=darken_hex_color(Colors.NEON_RED.value),
            width=300,
        )
        self.button_solid_state.grid(row=2, column=1, padx=(10, 20), pady=0, sticky="nsew")

        # Cancel Button
        self.button_cancel = stylized_button.StylizedButton(
            self,
            text="Cancel",
            command=self.on_cancel,
            fg_color=Colors.ORANGE.value,
            border_color=Colors.ORANGE.value,
            hover_color=darken_hex_color(Colors.ORANGE.value),
        )
        self.button_cancel.grid(row=3, column=0, columnspan=2, padx=(20, 20), pady=(10, 20), sticky="nsew")

    def on_select_electromechanical(self):
        self.result = "Electromechanical"
        self.destroy()

    def on_select_solid_state(self):
        self.result = "Solid State"
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()
