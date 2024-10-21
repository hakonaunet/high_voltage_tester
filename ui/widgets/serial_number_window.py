import customtkinter as ctk
import threading
import sys

# Modify the import path based on your project structure
from hardware.hardware_client import HardwareClient

class SerialNumberWindow(ctk.CTkToplevel):
    def __init__(self, parent, hardware_client):
        super().__init__(parent)
        self.title("Scan Serial Number")
        self.geometry("400x200")
        self.resizable(False, False)

        self.hardware_client = hardware_client  # Use the passed hardware_client

        # Instruction label
        self.label = ctk.CTkLabel(self, text="Please scan the QR code using the scanner.")
        self.label.pack(pady=20)

        # Serial number display
        self.serial_number_var = ctk.StringVar()
        self.serial_number_entry = ctk.CTkEntry(
            self, 
            textvariable=self.serial_number_var, 
            state="readonly", 
            width=300
        )
        self.serial_number_entry.pack(pady=10)

        # Scan button
        self.scan_button = ctk.CTkButton(self, text="Scan", command=self.start_scan)
        self.scan_button.pack(pady=10)

        # Close button
        self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.close_button.pack(pady=10)

    def start_scan(self):
        self.scan_button.configure(state="disabled")
        threading.Thread(target=self.scan_serial_number, daemon=True).start()

    def scan_serial_number(self):
        response = self.hardware_client.get_serial_number()
        if response.get('status') == 'success':
            serial_number = response.get('serial_number')
            self.serial_number_var.set(serial_number)
        else:
            self.serial_number_var.set("Scan failed. Please try again.")
        self.scan_button.configure(state="normal")

if __name__ == "__main__":
    app = ctk.CTk()
    hardware_client = HardwareClient()
    window = SerialNumberWindow(app, hardware_client)
    window.mainloop()
