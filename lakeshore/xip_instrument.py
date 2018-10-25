"""This module implements a parent class that contains all functionality shared by Lake Shore XIP instruments."""

import re
from time import sleep

import serial
from serial.tools.list_ports import comports
import socket


class XIPInstrumentConnectionException(Exception):
    """Names a new type of exception specific to instrument connectivity."""
    pass


class XIPInstrument:
    """Parent class that implements functionality shared by all XIP instruments"""

    vid_pid = []

    def __init__(self, serial_number, com_port, baud_rate, timeout, flow_control, ip_address):
        # Initialize values common to all XIP instruments
        self.device_serial = None
        self.device_tcp = None

        if serial_number is None and com_port is None and ip_address is None:
            self.connect_usb(serial_number, com_port, baud_rate, timeout, flow_control)
        if serial_number is not None or com_port is not None:
            self.connect_usb(serial_number, com_port, baud_rate, timeout, flow_control)

        if ip_address is not None:
            self.connect_tcp(ip_address, timeout)

        # Query the instrument identification information and store the firmware version and model number in variables
        idn_response = self.query('*IDN?', check_errors=False).split(',')
        self.firmware_version = idn_response[3]
        self.model_number = idn_response[1]

    def __del__(self):
        if self.device_serial is not None:
            self.device_serial.close()
        if self.device_tcp is not None:
            self.device_tcp.close()

    def command(self, command, check_errors=True):
        """Sends a SCPI command to the instrument"""

        if check_errors:
            # Do a query which will automatically check the errors.
            self.query(command)
        else:
            # Send command to the instrument over serial.
            self._usb_command(command)

    def query(self, query, check_errors=True):
        """Sends a SCPI query to the instrument and returns the response"""

        # Append the query with an additional error buffer query.
        if check_errors:
            query += ";:SYSTem:ERRor:ALL?"

        # Query the instrument over serial.
        response = self._usb_query(query)

        if check_errors:
            # Split the responses to each query, remove the last response which is to the error buffer query,
            # and check whether it contains an error
            response_list = re.split(''';(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', response)
            error_response = response_list.pop()
            self._error_check(error_response)
            response = ';'.join(response_list)

        return response

    @staticmethod
    def _error_check(error_response):
        """Evaluates the instrument response"""

        # If the error buffer returns an error, raise an exception with that includes the error.
        if "No error" not in error_response:
            raise XIPInstrumentConnectionException("SCPI command error(s): " + error_response)

    def connect_tcp(self, ip_address, timeout):
        """Establishes a TCP connection with the instrument on the specified IP address"""
        self.device_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.device_tcp.settimeout(timeout)
        self.device_tcp.connect((ip_address, 8888))

    def disconnect_tcp(self):
        """Disconnects the TCP connection"""
        self.device_tcp.close()
        self.device_tcp = None

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

                        # Send the instrument a line break, wait 100ms, and clear the input buffer so that
                        # any leftover communications from a prior session don't gum up the works
                        self.device_serial.write(b'\n')
                        sleep(0.1)
                        self.device_serial.reset_input_buffer()

                        break
        else:
            raise XIPInstrumentConnectionException("No instrument found with given parameters")

    def disconnect_usb(self):
        """Disconnects the USB connection"""
        self.device_serial.close()
        self.device_serial = None

    def _tcp_command(self, command):
        """Sends a command over the TCP connection"""
        self.device_tcp.send(command.encode('utf-8') + b'\n')

    def _tcp_query(self, query):
        """Queries over the TCP connection"""
        self.tcp_command(query)

        total_response = ""

        # Continuously receive data from the buffer until a line break
        while True:
            # sleep(0.01)
            response = self.device_tcp.recv(4096).decode('utf-8')

            # Add received information to the response
            total_response += response

            # Return the response once it ends with a line break
            if total_response.endswith("\r\n"):
                return total_response.rstrip()

    def _usb_command(self, command):
        """Sends a command over the serial USB connection"""
        self.device_serial.write(command.encode('ascii') + b'\n')

    def _usb_query(self, query):
        """Queries over the serial USB connection"""

        self._usb_command(query)
        response = self.device_serial.readline().decode('ascii')

        # If nothing is returned, raise a timeout error.
        if not response:
            raise XIPInstrumentConnectionException("Communication timed out")

        # Remove the line break the end of the response before returning it.
        return response.rstrip()
