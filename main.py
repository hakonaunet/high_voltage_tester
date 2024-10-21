import customtkinter
from ui.main_window import MainWindow
from test_logic.test_runner import TestRunner
from hardware import HardwareClient

def main():
    hardware_client = HardwareClient()
    test_runner = TestRunner(hardware_client)
    app = MainWindow(test_runner, hardware_client)
    
    def clean_exit():
        """Handles the cleanup process before application exit."""
        try:
            hardware_client.close()
        except Exception as e:
            print(f"Error closing HardwareClient: {e}")
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
