"""Implements functionality unique to the Lake Shore Model 372 AC bridge and temperature controller"""

from .temperature_controllers import TemperatureController


class Model372(TemperatureController):
    """A class object representing the Lake Shore Model 372 AC bridge and temperature controller"""

    vid_pid = [(0x1FB9, 0x0305)]

    def __init__(self,
                 baud_rate,
                 serial_number=None,
                 com_port=None,
                 timeout=2.0,
                 ip_address=None,
                 tcp_port=7777,
                 **kwargs):

        # Call the parent init, then fill in values specific to the 121
        TemperatureController.__init__(self, serial_number, com_port, baud_rate, timeout, ip_address,
                                       tcp_port, **kwargs)
