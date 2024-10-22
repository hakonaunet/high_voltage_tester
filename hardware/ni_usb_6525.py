"""
This module serves as a backup to operate a NI USB 6525 relay in case the primary electromechanical
relay connected to the Raspberry Pi fails.
"""

import time

import nidaqmx
from nidaqmx.constants import LineGrouping
from nidaqmx.system import System

class RelayController:
    def __init__(self, device_name='Dev1'):
        self.device_name = device_name
        self.task = nidaqmx.Task()
        # Initialize the digital output channels for all 8 relays
        self.task.do_channels.add_do_chan(
            f'{device_name}/port0/line0:7', line_grouping=LineGrouping.CHAN_PER_LINE)
        self.state = [False] * 8  # Initial state: all relays OFF (open)
        print(f"RelayController initialized for device '{self.device_name}'.")

    def set_relay_state(self, relay_indices, state):
        # Ensure relay_indices is a tuple of integers
        if isinstance(relay_indices, int):
            relay_indices = (relay_indices,)
        elif isinstance(relay_indices, (list, tuple)):
            if not all(isinstance(i, int) and 0 <= i <= 7 for i in relay_indices):
                raise ValueError("Relay indices must be integers between 0 and 7.")
        else:
            raise TypeError("Parameter 'relay_indices' must be an integer or a tuple/list of integers.")

        # Validate state
        if state.lower() == 'open':
            relay_state = False
        elif state.lower() == 'closed':
            relay_state = True
        else:
            raise ValueError("State must be 'open' or 'closed'.")

        # Update the state of specified relays
        for index in relay_indices:
            self.state[index] = relay_state

        # Write the new state to the device
        self.task.write(self.state)
        print(f"Set relay(s) {relay_indices} to {'ON (closed)' if relay_state else 'OFF (open)'}.")

    def turn_on_all_relays(self):
        self.state = [True] * 8
        self.task.write(self.state)
        print("All relays turned ON (closed).")

    def turn_off_all_relays(self):
        self.state = [False] * 8
        self.task.write(self.state)
        print("All relays turned OFF (open).")

    def check_device_connection(self):
        system = System.local()
        device_names = [device.name for device in system.devices]
        if self.device_name in device_names:
            print(f"Device '{self.device_name}' is connected.")
            return True
        else:
            print(f"Device '{self.device_name}' is NOT connected.")
            return False

    def close(self):
        self.task.close()
        print("RelayController task closed.")

    def __del__(self):
        # Ensure the task is closed when the object is deleted
        try:
            self.task.close()
        except Exception:
            pass

# Example usage:
if __name__ == "__main__":
    controller = RelayController()

    # Confirm communication with the device
    if controller.check_device_connection():
        # Turn on all relays
        controller.turn_on_all_relays()
        time.sleep(1)

        # Turn off all relays
        controller.turn_off_all_relays()
        time.sleep(1)

        # Set relay 0 and 1 to closed, others remain open
        controller.set_relay_state((0, 1), 'closed')
        time.sleep(1)

        # Set relay 0 to open
        controller.set_relay_state(0, 'open')
        time.sleep(1)

    # Close the controller
    controller.close()
