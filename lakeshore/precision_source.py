"""Implements functionality unique to the Lake Shore 155 Precision Source"""

from .xip_instrument import XIPInstrument


class PrecisionSource(XIPInstrument):
    """A XIP Instrument subclass that establishes 155 specific parameters and methods"""

    vid_pid = [(0x1FB9, 0x0103)]

    def __init__(self, serial_number=None, com_port=None, baud_rate=115200, timeout=2.0, flow_control=True):
        # Call the parent init, then fill in values specific to the 155
        XIPInstrument.__init__(self, serial_number, com_port, baud_rate, timeout, flow_control)
