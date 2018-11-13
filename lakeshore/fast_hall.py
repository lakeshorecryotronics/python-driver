"""Implements functionality unique to the Lake Shore M91 Fast Hall"""

from collections import namedtuple
from .xip_instrument import XIPInstrument

# TODO: update register enums once they are finalized
OPERATION_REGISTER_BIT_NAMES = [
    "",
    "settling",
    "ranging",
    "measurement_complete",
    "waiting_for_trigger",
    "",
    "field_control_ramping",
    "field_measurement_enabled",
    "transient"
]

QUESTIONABLE_REGISTER_BIT_NAMES = [
    "source_in_compliance_or_at_current_limit",
    "",
    "field_control_slew_rate_limit",
    "field_control_at_voltage_limit",
    "current_measurement_overload",
    "voltage_measurement_overload",
    "invalid_probe",
    "invalid_calibration",
    "inter_processor_communication_error",
    "field_measurement_communication_error",
    "probe_EEPROM_read_error",
    "r2_less_than_minimum_allowable"
]

OPERATION_REGISTER_TUPLE = namedtuple('OperationRegister',
                                      [bit_name for bit_name in OPERATION_REGISTER_BIT_NAMES if bit_name != ""])

QUESTIONABLE_REGISTER_TUPLE = namedtuple('QuestionableRegister',
                                         [bit_name for bit_name in QUESTIONABLE_REGISTER_BIT_NAMES if bit_name != ""])


class FastHall(XIPInstrument):
    """A class object representing a Lake Shore M91 Fast Hall controller"""

    vid_pid = [(0x1FB9, 0x0704)]

    def __init__(self, serial_number=None,
                 com_port=None, baud_rate=115200, flow_control=True,
                 timeout=2.0,
                 ip_address=None):
        # Call the parent init, then fill in values specific to FastHall
        XIPInstrument.__init__(self, serial_number, com_port, baud_rate, flow_control, timeout, ip_address)
