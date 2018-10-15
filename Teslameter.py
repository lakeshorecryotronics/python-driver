from XIPInstrument import XIPInstrument


class Teslameter(XIPInstrument):
    """A XIP Instrument subclass that establishes Teslameter-specific parameters and methods"""

    def __init__(self):
        # Call the parent init, then fill in values specific to the Teslameter
        XIPInstrument.__init__(self)
        self.baud_rate = 115200
        self.usb_timeout = 2
        self.flow_control = True
        self.vid_pid = [(0x1FB9, 0x0405), (0x1FB9, 0x0406)]
