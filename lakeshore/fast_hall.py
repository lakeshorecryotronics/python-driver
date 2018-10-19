"""Implements functionality unique to the Lake Shore M91 Fast Hall"""

from .xip_instrument import XIPInstrument


class FastHall(XIPInstrument):
    """A class object representing a Lake Shore M91 Fast Hall controller"""

    vid_pid = [(0x1FB9, 0x0704)]

    # TODO: update register enums once they are finalized
    operation_status_register = [
        "",
        "Settling",
        "Ranging",
        "Measurement complete",
        "Waiting for trigger",
        "",
        "Field control ramping",
        "Field measurement enabled",
        "Transient"
    ]

    questionable_status_register = [
        "Source in compliance or at current limit",
        "",
        "Field control slew rate limit",
        "Field control at voltage limit",
        "Current measurement overload",
        "Voltage measurement overload",
        "Invalid probe",
        "Invalid calibration",
        "Inter-processor communication error",
        "Field measurement communication error",
        "Probe EEPROM read error",
        "R^2 less than minimum allowable"
    ]

    def __init__(self, serial_number=None,
                 com_port=None, baud_rate=115200, flow_control=True,
                 timeout=2.0,
                 ip_address=None):
        # Call the parent init, then fill in values specific to FastHall
        XIPInstrument.__init__(self, serial_number, com_port, baud_rate, flow_control, timeout, ip_address)
