"""
This module serves as a backup to operate a NI USB 6525 relay in case the primary electromechanical
relay connected to the Raspberry Pi fails.
"""

import time
import logging

import nidaqmx
from nidaqmx.constants import LineGrouping
from nidaqmx.system import System
from nidaqmx.errors import DaqError

class RelayController:
    def __init__(self, device_name='Dev1'):
        self.device_name = device_name
        self.task = None
        self.state = [False] * 8  # Initial state: all relays OFF (open)
        self.connected = False  # Flag to indicate device connection status

        try:
            self.task = nidaqmx.Task()
            # Initialize the digital output channels for all 8 relays
            self.task.do_channels.add_do_chan(
                f'{device_name}/port0/line0:7', line_grouping=LineGrouping.CHAN_PER_LINE)
            self.task.write(self.state)
            self.connected = True
            logging.info(f"RelayController initialized for device '{self.device_name}'.")
        except DaqError as e:
            self.connected = False
            logging.error(f"Failed to initialize RelayController for device '{self.device_name}': {e}")
            # Additional handling can be performed here, such as notifying the user or attempting retries

    def set_relay_state(self, relay_indices, state):
        if not self.connected:
            logging.warning("Attempted to set relay state, but RelayController is not connected.")
            return

        # Ensure relay_indices is a tuple of integers
        if isinstance(relay_indices, int):
            relay_indices = (relay_indices,)
        elif isinstance(relay_indices, (list, tuple)):
            if not all(isinstance(i, int) and 0 <= i <= 7 for i in relay_indices):
                raise ValueError("Relay indices must be integers between 0 and 7.")
        else:
            raise TypeError("Parameter 'relay_indices' must be an integer or a tuple/list of integers.")

        # Validate state
        if isinstance(state, str):
            if state.lower() == 'open':
                relay_state = False
            elif state.lower() == 'closed':
                relay_state = True
            else:
                raise ValueError("State must be 'open' or 'closed'.")
        elif isinstance(state, bool):
            relay_state = state
        else:
            raise TypeError("State must be 'open', 'closed', True, or False.")

        # Update the state of specified relays
        for index in relay_indices:
            self.state[index] = relay_state

        try:
            # Write the new state to the device
            self.task.write(self.state)
            logging.info(f"Set relay(s) {relay_indices} to {'ON (closed)' if relay_state else 'OFF (open)'}.")
        except DaqError as e:
            logging.error(f"Failed to set relay state: {e}")
            self.connected = False
            # Handle the disconnection, possibly attempt to reconnect or alert the user

    def turn_on_all_relays(self):
        if not self.connected:
            logging.warning("Attempted to turn on all relays, but RelayController is not connected.")
            return

        self.state = [True] * 8
        try:
            self.task.write(self.state)
            logging.info("All relays turned ON (closed).")
        except DaqError as e:
            logging.error(f"Failed to turn on all relays: {e}")
            self.connected = False

    def turn_off_all_relays(self):
        if not self.connected:
            logging.warning("Attempted to turn off all relays, but RelayController is not connected.")
            return

        self.state = [False] * 8
        try:
            self.task.write(self.state)
            logging.info("All relays turned OFF (open).")
        except DaqError as e:
            logging.error(f"Failed to turn off all relays: {e}")
            self.connected = False

    def check_device_connection(self):
        system = System.local()
        device_names = [device.name for device in system.devices]
        if self.device_name in device_names:
            logging.info(f"Device '{self.device_name}' is connected.")
            self.connected = True
            return True
        else:
            logging.warning(f"Device '{self.device_name}' is NOT connected.")
            self.connected = False
            return False

    def close(self):
        if self.task:
            try:
                self.task.close()
                logging.info("RelayController task closed.")
            except DaqError as e:
                logging.error(f"Failed to close RelayController task: {e}")

    def __del__(self):
        # Ensure the task is closed when the object is deleted
        try:
            if self.task:
                self.task.close()
        except Exception as e:
            logging.error(f"Error during RelayController deletion: {e}")
