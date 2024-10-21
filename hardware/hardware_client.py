import socket
import json
import threading

from test_logic import event_system

class HardwareClient:
    def __init__(self, host='192.168.0.2', port=65432):
        self.host = host
        self.port = port
        self.socket = None

    def close(self):
        """Closes the socket connection if it's open."""
        if self.socket:
            try:
                self.socket.close()
                print("HardwareClient socket closed successfully.")
            except Exception as e:
                print(f"Error closing HardwareClient socket: {e}")
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
            event_system.dispatch_event("error_occurred", {"error_message": f"Connection error: {e}"})
            return {'status': 'error', 'message': 'Connection failed'}
        except Exception as e:
            event_system.dispatch_event("error_occurred", {"error_message": f"Unexpected error: {e}"})
            return {'status': 'error', 'message': 'Unexpected error occurred'}

    def check_connection(self):
        command = {'command': 'check_connection'}
        response = self.send_command(command)
        if response['status'] == 'success' and response['message'] == 'Connection established':
            print("Connection to server confirmed.")
            return True
        else:
            print("Failed to confirm connection to server.")
            return False

    def initialize(self):
        if self.check_connection():
            print("HardwareClient initialized successfully.")
            return True
        else:
            print("HardwareClient initialization failed.")
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

