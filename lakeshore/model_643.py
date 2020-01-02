"""Implements functionality unique to the Lake Shore Model 643 electromagnet magnet power supply"""
import serial

from .generic_instrument import GenericInstrument


class Model643(GenericInstrument):
    """A class object representing the Lake Shore Model 643 electromagnet magnet power supply"""

    vid_pid = [(0x1FB9, 0x0601)]

    def __init__(self,
                 serial_number=None,
                 com_port=None,
                 baud_rate=57600,
                 data_bits=7,
                 stop_bits=1,
                 parity=serial.PARITY_ODD,
                 flow_control=False,
                 handshaking=False,
                 timeout=2.0,
                 ip_address=None,
                 tcp_port=7777,
                 **kwargs):

        # Call the parent init, then fill in values specific to the 121
        GenericInstrument.__init__(self, serial_number, com_port, baud_rate, data_bits, stop_bits, parity, flow_control,
                                   handshaking, timeout, ip_address, tcp_port, **kwargs)
