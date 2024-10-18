import customtkinter
from ui.main_window import MainWindow
from hardware.ni_usb_6525 import NiUsb6525
from test_logic.test_runner import TestRunner

def main():
    ni_usb_6525 = NiUsb6525()
    test_runner = TestRunner(ni_usb_6525)
    app = MainWindow(test_runner)
    
    def clean_exit():
        """Handles the cleanup process before application exit."""
        try:
            ni_usb_6525.close()
        except Exception as e:
            print(f"Error closing NiUsb6525: {e}")
        try:
            test_runner.close()
        except Exception as e:
            print(f"Error closing TestRunner: {e}")
        try:
            app.destroy()
        except Exception as e:
            print(f"Error destroying app: {e}")
            
    app.protocol("WM_DELETE_WINDOW", clean_exit) # Register the clean_exit function to the window close event
    app.mainloop()

if __name__ == "__main__":
    main()
