"""Implements functionality unique to the Lake Shore F41 and F71 Teslameters."""

from .XIPInstrument import XIPInstrument


class Teslameter(XIPInstrument):
    """A XIP Instrument subclass that establishes Teslameter-specific parameters and methods"""

    vid_pid = [(0x1FB9, 0x0405), (0x1FB9, 0x0406)]

    def __init__(self, serial_number=None, com_port=None, baud_rate=115200, timeout=2.0, flow_control=True):
        # Call the parent init, then fill in values specific to the Teslameter
        XIPInstrument.__init__(self, serial_number, com_port, baud_rate, timeout, flow_control)
