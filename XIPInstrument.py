import serial
from serial.tools.list_ports import comports


class XIPInstrument:
    """Parent class that implements functionality shared by all XIP instruments"""

    def __init__(self):
        # Initialize values common to all XIP instruments
        self.baud_rate = 115200
        self.usb_timeout = 2
        self.flow_control = True
        self.device_serial = None
        self.serial_parameters = None
        self.vid_pid = None

    def connect_usb(self, com_port=None,
                    baud_rate=None,
                    timeout=None,
                    flow_control=None):
        """Establishes a serial USB connection with optional arguments"""

        # Update the serial parameters if they are passed into the method
        if baud_rate:
            self.baud_rate = baud_rate
        if timeout:
            self.usb_timeout = timeout
        if flow_control:
            self.flow_control = flow_control

        self.serial_parameters = {'baudrate': self.baud_rate,
                                  'timeout': self.usb_timeout,
                                  'parity': serial.PARITY_NONE,
                                  'rtscts': self.flow_control
                                  }

        # Scan the ports for devices matching the VID and PID combos of the instrument
        for port in comports():
            if (port.vid, port.pid) in self.vid_pid:
                # If the com port argument is passed, check for a match
                if port.device == com_port or com_port is None:
                    # Establish a connection with device using the instrument's serial communications parameters
                    self.device_serial = serial.Serial(port.device, **self.serial_parameters)

                    return

        # TODO: Raise an error when no matching instruments are found

    def disconnect_usb(self):
        """Disconnects the USB connection"""
        self.device_serial.close()
        self.device_serial = None

    def usb_command(self, command):
        """Sends a command over the serial USB connection"""
        self.device_serial.write(command.encode('ascii') + b'\n')

    def usb_query(self, query):
        """Queries over the serial USB connection"""

        self.usb_command(query)
        response = self.device_serial.readline().decode('ascii').rstrip('\r\n')

        # TODO: Raise an error when the instrument times out

        return response
