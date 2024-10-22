import socket
import json
import threading

from test_logic import event_system
from .ni_usb_6525 import RelayController
class HardwareClient:
    def __init__(self, host='192.168.0.2', port=65432):
        self.host = host
        self.port = port
        self.socket = None
        self.use_backup_relay = False
        self.backup_relay = RelayController()

        event_system.register_listener("default_relay_selected", self.set_default_relay)

    def close(self):
        """Closes the socket connection if it's open."""
        if self.socket:
            try:
                self.socket.close()
                event_system.dispatch_event("log_event", {"message": "Hardware client closed.", "level": "INFO"})
            except Exception as e:
                event_system.dispatch_event("log_event", {"message": f"Error closing HardwareClient socket: {e}", "level": "ERROR"})
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
            event_system.dispatch_event("log_event", {"message": f"Connection error: {e}", "level": "ERROR"})
            return {'status': 'error', 'message': 'Connection failed'}
        except Exception as e:
            event_system.dispatch_event("log_event", {"message": f"Unexpected error: {e}", "level": "ERROR"})
            return {'status': 'error', 'message': 'Unexpected error occurred'}

    def check_connection(self):
        command = {'command': 'check_connection'}
        response = self.send_command(command)
        if response['status'] == 'success' and response['message'] == 'Connection established':
            event_system.dispatch_event("log_event", {"message": "Connection established.", "level": "INFO"})
            return True
        else:
            event_system.dispatch_event("log_event", {"message": "Connection failed.", "level": "ERROR"})
            return False

    def initialize(self):
        if self.check_connection():
            event_system.dispatch_event("log_event", {"message": "Hardware client initialized.", "level": "INFO"})
            return True
        else:
            event_system.dispatch_event("log_event", {"message": "Hardware client initialization failed.", "level": "ERROR"})
            return False

    def open_relay(self, relay_number):
        command = {
            'command': 'open_relay',
            'relay_number': relay_number
        }
        return self.send_command(command)

    def close_relay(self, relay_number):
        command = {
            'command': 'close_relay',
            'relay_number': relay_number
        }
        return self.send_command(command)

    def set_hipot_voltage(self, voltage):
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
        elif selected_relay == "Solid State":
            self.use_backup_relay = True
        event_system.dispatch_event("log_event", {"message": f"Default relay set to {selected_relay.lower()}.", "level": "INFO"})
