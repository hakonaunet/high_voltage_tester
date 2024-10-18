import socket
import json
import threading

from test_logic import event_system

class HardwareClient:
    def __init__(self, host='192.168.0.2', port=65432):
        self.host = host
        self.port = port

    def send_command(self, command):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(json.dumps(command).encode())
                data = s.recv(1024)
            response = json.loads(data.decode())
            return response
        except ConnectionError as e:
            event_system.dispatch_event("error_occurred", {"error_message": f"Connection error: {e}"})
            return {'status': 'error', 'message': 'Connection failed'}

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
