"""Implements functionality unique to the Lake Shore 155 Precision Source"""

from collections import namedtuple
from .xip_instrument import XIPInstrument


class PrecisionSource(XIPInstrument):
    """A class object representing a Lake Shore 155 precision I/V source"""

    vid_pid = [(0x1FB9, 0x0103)]

    operation_register = [
        "",
        "",
        "",
        "",
        "",
        "Waiting for trigger event",
        "Waiting for ARM event",
        "",
        "",
        "",
        "Trigger model is idle",
        "",
        "Interlock is open"
    ]

    questionable_register = [
        "Voltage source in current limit",
        "Current source in voltage compliance",
        "",
        "",
        "",
        "",
        "",
        "",
        "Calibration error",
        "Inter-processor communication error"
    ]

    OperationRegister = namedtuple('OperationRegister')

    QuestionableRegister = namedtuple('QuestionableRegister')

    def __init__(self, serial_number=None,
                 com_port=None, baud_rate=115200, flow_control=True,
                 timeout=2.0,
                 ip_address=None):
        # Call the parent init, then fill in values specific to the 155
        XIPInstrument.__init__(self, serial_number, com_port, baud_rate, flow_control, timeout, ip_address)
