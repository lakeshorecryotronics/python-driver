"""Implements functionality unique to the Lake Shore 155 Precision Source"""

from .xip_instrument import XIPInstrument


class OperationRegister:
    """Class object representing the operation status register"""

    bit_names = [
        "",
        "",
        "",
        "",
        "",
        "waiting_for_trigger_event",
        "waiting_for_ARM_event",
        "",
        "",
        "",
        "trigger_model_is_idle",
        "",
        "interlock_is_open"
    ]
    
    def __init__(self,
                 waiting_for_trigger_event,
                 waiting_for_ARM_event,
                 trigger_model_is_idle,
                 interlock_is_open):
        self.waiting_for_trigger_event = waiting_for_trigger_event
        self.waiting_for_ARM_event = waiting_for_ARM_event
        self.trigger_model_is_idle = trigger_model_is_idle
        self.interlock_is_open = interlock_is_open


class QuestionableRegister:
    """Class object representing the questionable status register"""

    bit_names = [
        "voltage_source_in_current_limit",
        "current_source_in_voltage_compliance",
        "",
        "",
        "",
        "",
        "",
        "",
        "calibration_error",
        "inter_processor_communication_error"
    ]
    
    def __init__(self,
                 voltage_source_in_current_limit,
                 current_source_in_voltage_compliance,
                 calibration_error,
                 inter_processor_communication_error):
        self.voltage_source_in_current_limit = voltage_source_in_current_limit
        self.current_source_in_voltage_compliance = current_source_in_voltage_compliance
        self.calibration_error = calibration_error
        self.inter_processor_communication_error = inter_processor_communication_error


class PrecisionSource(XIPInstrument):
    """A class object representing a Lake Shore 155 precision I/V source"""

    vid_pid = [(0x1FB9, 0x0103)]

    def __init__(self, serial_number=None,
                 com_port=None, baud_rate=115200, flow_control=False,
                 timeout=2.0,
                 ip_address=None):
        # Call the parent init, then fill in values specific to the 155
        XIPInstrument.__init__(self, serial_number, com_port, baud_rate, flow_control, timeout, ip_address)
        self.operation_register = OperationRegister
        self.questionable_register = QuestionableRegister
