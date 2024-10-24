import socket
import json
import threading

from utils import event_system, EventType, LogLevel
from .ni_usb_6525 import RelayController

class HardwareClient:
    def __init__(self, host='192.168.0.2', port=65432):
        self.host = host
        self.port = port
        self.socket = None
        self.use_backup_relay = False
        self.backup_relay = RelayController()
        self.relay_timers = {}  # For managing relay timers

        event_system.register_listener(EventType.VERIFY_RASPBERRY_PI_CONNECTION, self.check_connection)
        event_system.register_listener(EventType.DEFAULT_RELAY_SELECTED, self.set_default_relay)
        event_system.register_listener(EventType.SET_HIPOT_VOLTAGE, self.set_hipot_voltage)
        event_system.register_listener(EventType.SET_RELAYS, self.set_relays)
    
    def close(self):
        """Closes the socket connection if it's open and cancels relay timers."""
        # Cancel all relay timers
        for timer in self.relay_timers.values():
            timer.cancel()
        self.relay_timers.clear()

        if self.socket:
            try:
                self.socket.close()
                event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Hardware client closed.", "level": LogLevel.INFO})
            except Exception as e:
                event_system.dispatch_event(EventType.LOG_EVENT, {"message": f"Error closing HardwareClient socket: {e}", "level": LogLevel.ERROR})
            finally:
                self.socket = None

    def send_command(self, command):
        try:
            if not self.socket:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
            self.socket.sendall(json.dumps(command).encode())
            data = self.socket.recv(1024)
            response = json.loads(data.decode())
            return response
        except ConnectionError as e:
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": f"Connection error: {e}", "level": LogLevel.ERROR})
            return {'status': 'error', 'message': 'Connection failed'}
        except Exception as e:
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": f"Unexpected error: {e}", "level": LogLevel.ERROR})
            return {'status': 'error', 'message': 'Unexpected error occurred'}

    def check_connection(self, event_data=None):  # Add event_data parameter with default None
        command = {'command': 'check_connection'}
        debug_level = event_data.get('level', LogLevel.DEBUG) if event_data else LogLevel.DEBUG
        response = self.send_command(command)
        if response['status'] == 'success' and response['message'] == 'Connection established':
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Connection to Raspberry Pi server verified.", "level": debug_level})
            return True
        else:
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Connection to Raspberry Pi server failed.", "level": LogLevel.ERROR})
            return False

    def initialize(self):
        if self.check_connection():
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Hardware client initialized.", "level": LogLevel.INFO})
            return True
        else:
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Hardware client initialization failed.", "level": LogLevel.ERROR})
            return False

    def set_relays(self, event_data):
        relay_indices = event_data.get("relays")
        timeout = event_data.get("timeout", 10)
        state = event_data.get("state")
        # Ensure relay_indices is a tuple of integers
        if isinstance(relay_indices, int):
            relay_indices = (relay_indices,)
        elif isinstance(relay_indices, (list, tuple)):
            if not all(isinstance(i, int) and 0 <= i <= 7 for i in relay_indices):
                error_msg = "Relay indices must be integers between 0 and 7."
                event_system.dispatch_event(EventType.LOG_EVENT, {"message": error_msg, "level": LogLevel.ERROR})
                raise ValueError(error_msg)
        else:
            error_msg = "Parameter 'relay_indices' must be an integer or a tuple/list of integers."
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": error_msg, "level": LogLevel.ERROR})
            raise TypeError(error_msg)

        # Convert state to boolean
        if isinstance(state, str):
            state = state.lower()
            if state == 'open':
                state = True
            elif state == 'closed':
                state = False
            else:
                error_msg = "State must be 'open', 'closed', True, or False."
                event_system.dispatch_event(EventType.LOG_EVENT, {"message": error_msg, "level": LogLevel.ERROR})
                raise ValueError(error_msg)
        elif isinstance(state, bool):
            pass  # state is already a boolean, no conversion needed
        else:
            error_msg = "State must be a boolean or a string ('open' or 'closed')."
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": error_msg, "level": LogLevel.ERROR})
            raise TypeError(error_msg)

        # Send command to the appropriate relay controller
        if self.use_backup_relay:
            # Use backup relay
            self.backup_relay.set_relay_state(relay_indices, state)
        else:
            # Send command to server
            command = {
                'command': 'set_relays',
                'relay_indices': relay_indices,
                'state': state
            }
            self.send_command(command)

        # Safety feature: manage timers
        for relay_index in relay_indices:
            if state:  # Relay is being turned ON
                # Cancel existing timer if any
                if relay_index in self.relay_timers:
                    self.relay_timers[relay_index].cancel()
                # Define function to turn off relay after timeout
                def turn_off_relay(relay_index=relay_index):
                    # Turn off the relay
                    if self.use_backup_relay:
                        self.backup_relay.set_relay_state(relay_index, False)
                    else:
                        command = {
                            'command': 'set_relays',
                            'relay_indices': [relay_index],
                            'state': False
                        }
                        self.send_command(command)
                    # Remove timer from dictionary
                    del self.relay_timers[relay_index]
                    event_system.dispatch_event(EventType.LOG_EVENT, {"message": f"Relay {relay_index} automatically turned off after timeout.", "level": LogLevel.WARNING})
                # Start new timer
                t = threading.Timer(timeout, turn_off_relay)
                t.start()
                # Save timer
                self.relay_timers[relay_index] = t
            else:  # Relay is being turned OFF
                # Cancel existing timer if any
                if relay_index in self.relay_timers:
                    self.relay_timers[relay_index].cancel()
                    del self.relay_timers[relay_index]

    def set_hipot_voltage(self, event_data):
        voltage = event_data.get("voltage")
        command = {
            'command': 'set_hipot_voltage',
            'voltage': voltage
        }
        return self.send_command(command)

    def read_current(self):
        command = {'command': 'read_current'}
        return self.send_command(command)

    def get_serial_number(self):
        command = {'command': 'get_serial_number'}
        return self.send_command(command)

    def set_default_relay(self, event_data):
        selected_relay = event_data.get("selected_relay")
        if selected_relay == "Electromechanical":
            self.use_backup_relay = False
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": f"Default relay set to {selected_relay.lower()}.", "level": LogLevel.INFO})
        elif selected_relay == "Solid State":
            self.use_backup_relay = True
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": f"Default relay set to {selected_relay.lower()}.", "level": LogLevel.INFO})
        elif selected_relay is None:
            event_system.dispatch_event(EventType.LOG_EVENT, {"message": "Default relay was not updated.", "level": LogLevel.INFO})

    def stop_tests(self):
        # ... existing code ...
        pass

    # ... other methods ...
