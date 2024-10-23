import customtkinter as ctk
import os

from utils import event_system, EventType

class SerialNumberWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # Set the custom icon
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.abspath(os.path.join(script_dir, "..", "images", "icons", "eltorqueicon_develop.ico"))
        
        self.iconbitmap(icon_path)
        self.title("Enter Serial Number")
        self.geometry("400x200")
        self.resizable(False, False)


        self.serial_number = None  # Initialize serial_number attribute

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)

        # Instruction label
        self.label = ctk.CTkLabel(self, text="Please scan the serial number:")
        self.label.grid(row=0, column=0, pady=10)

        # Serial number entry
        self.serial_number_var = ctk.StringVar()
        self.serial_number_entry = ctk.CTkEntry(
            self, 
            textvariable=self.serial_number_var, 
            width=300
        )
        self.serial_number_entry.grid(row=1, column=0, pady=10)
        
        # Ensure the entry widget is focused and ready to receive input
        self.after(200, lambda: self.serial_number_entry.focus_force())

        # Error message label
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=2, column=0, pady=5)

        # Submit button
        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_serial_number)
        self.submit_button.grid(row=3, column=0, pady=10)

        # Close button
        self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.close_button.grid(row=4, column=0, pady=10)

        # Bind Enter key to submit_serial_number
        self.serial_number_entry.bind('<Return>', lambda event: self.submit_serial_number())

    def submit_serial_number(self):
        serial_number = self.serial_number_var.get()
        if self.is_valid_serial_number(serial_number):
            self.serial_number = serial_number
            event_system.dispatch_event(EventType.SERIAL_NUMBER_CONFIRMED, {"serial_number": serial_number})
            self.destroy()
        else:
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Invalid serial number entered.", "level": "ERROR"})
            self.error_label.configure(text="Invalid serial number. Please try again.")

    def is_valid_serial_number(self, serial_number):
        # Placeholder for validation logic
        return bool(serial_number)
