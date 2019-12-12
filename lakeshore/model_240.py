"""Implements functionality unique to the Lake Shore model 240 temperature monitor"""
import serial

from .generic_instrument import GenericInstrument


class Model240(GenericInstrument):
    """A class object representing the Lake Shore model 240 temperature monitor"""

    vid_pid = [(0x1FB9, 0x0205)]

    def __init__(self,
                 serial_number=None,
                 com_port=None,
                 baud_rate=115200,
                 data_bits=8,
                 stop_bits=1,
                 parity=serial.PARITY_NONE,
                 flow_control=False,
                 handshaking=False,
                 timeout=2.0,
                 ip_address=None,
                 tcp_port=7777,
                 **kwargs):

        # Call the parent init, then fill in values specific to the 121
        GenericInstrument.__init__(serial_number, com_port, baud_rate, data_bits, stop_bits, parity, flow_control,
                                   handshaking, timeout, ip_address, tcp_port, **kwargs)
