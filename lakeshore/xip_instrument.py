"""This module implements a parent class that contains all functionality shared by Lake Shore XIP instruments."""

import serial
from serial.tools.list_ports import comports


class XIPInstrumentConnectionException(Exception):
    """Names a new type of exception specific to instrument connectivity."""
    pass


class XIPInstrument:
    """Parent class that implements functionality shared by all XIP instruments"""

    vid_pid = []

    def __init__(self, serial_number, com_port, baud_rate, timeout, flow_control):
        # Initialize values common to all XIP instruments
        self.device_serial = None
        self.connect_usb(serial_number, com_port, baud_rate, timeout, flow_control)

        # Query the instrument identification information and store the firmware version and model number in variables
        idn_response = self.query('*IDN?').split(',')
        self.firmware_version = idn_response[3]
        self.model_number = idn_response[1]

    def command(self, command):
        """Sends a SCPI command to the instrument"""

        self._usb_command(command)

    def query(self, query):
        """Sends a SCPI query to the instrument and returns the response"""

        response = self._usb_query(query)

        return response

    def connect_usb(self, serial_number=None, com_port=None, baud_rate=None, timeout=None, flow_control=None):
        """Establishes a serial USB connection with optional arguments"""

        # Scan the ports for devices matching the VID and PID combos of the instrument
        for port in comports():
            if (port.vid, port.pid) in self.vid_pid:
                # If the com port argument is passed, check for a match
                if port.device == com_port or com_port is None:
                    # If the serial number argument is passed, check for a match
                    if port.serial_number == serial_number or serial_number is None:
                        # Establish a connection with device using the instrument's serial communications parameters
                        self.device_serial = serial.Serial(port.device,
                                                           baudrate=baud_rate,
                                                           timeout=timeout,
                                                           parity=serial.PARITY_NONE,
                                                           rtscts=flow_control)

                        break
        else:
            raise XIPInstrumentConnectionException("No instrument found with given parameters")

    def disconnect_usb(self):
        """Disconnects the USB connection"""
        self.device_serial.close()
        self.device_serial = None

    def _usb_command(self, command):
        """Sends a command over the serial USB connection"""
        self.device_serial.write(command.encode('ascii') + b'\n')

    def _usb_query(self, query):
        """Queries over the serial USB connection"""

        self._usb_command(query)
        response = self.device_serial.readline().decode('ascii')

        # If nothing was returned, raise a timeout error
        if not response:
            raise XIPInstrumentConnectionException("The response timed out")

        return response.rstrip('\r\n')
