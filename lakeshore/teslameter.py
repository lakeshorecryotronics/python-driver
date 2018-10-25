"""Implements functionality unique to the Lake Shore F41 and F71 Teslameters."""

import re
from .xip_instrument import XIPInstrument


class Teslameter(XIPInstrument):
    """A XIP Instrument subclass that establishes Teslameter-specific parameters and methods"""

    vid_pid = [(0x1FB9, 0x0405), (0x1FB9, 0x0406)]

    def __init__(self, serial_number=None,
                 com_port=None, baud_rate=115200, flow_control=True,
                 timeout=2.0,
                 ip_address=None):
        # Call the parent init, then fill in values specific to the Teslameter
        XIPInstrument.__init__(self, serial_number, com_port, baud_rate, flow_control, timeout, ip_address)

    def get_buffered_data(self, length_of_time_in_seconds, sample_rate_in_ms=None):
        """Returns an array of parsed field strength and input state data"""

        # Make the amount of time a whole number
        length_of_time_in_seconds = round(length_of_time_in_seconds, 2)

        # Set the sample rate
        if sample_rate_in_ms is not None:
            self.command("SENSE:AVERAGE:COUNT " + str(sample_rate_in_ms / 10))
        else:
            sample_rate_in_ms = 10 * int(self.query("SENSE:AVERAGE:COUNT?"))

        # Clear the buffer by querying it
        self.query('FETC:BUFF:DC?', check_errors=False)

        buffered_data = []

        # Loop until the designated amount of time has been reached
        while True:
            response = self.query('FETC:BUFF:DC?', check_errors=False)

            # Ignore the response if it contains no data
            if ';' in response:

                # If it does contain data, split the data apart and then separate each value and add it to the array.
                parsed = response.rstrip(';').split(';')
                for point in parsed:
                    buffered_data.append(re.split('-|T|:|\+|,', point))

                    # Check to see if time is up. If so, return the data.
                    if len(buffered_data) * sample_rate_in_ms >= length_of_time_in_seconds * 1000:
                        return buffered_data
