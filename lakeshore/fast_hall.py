"""Implements functionality unique to the Lake Shore M91 Fast Hall"""

from .xip_instrument import XIPInstrument, RegisterBase, StatusByteRegister, StandardEventRegister


# TODO: update register enums once they are finalized
class FastHallOperationRegister(RegisterBase):
    """Class object representing the operation status register"""

    bit_names = [
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

    def __init__(self,
                 settling,
                 ranging,
                 measurement_complete,
                 waiting_for_trigger,
                 field_control_ramping,
                 field_measurement_enabled,
                 transient):
        self.settling = settling
        self.ranging = ranging
        self.measurement_complete = measurement_complete
        self.waiting_for_trigger = waiting_for_trigger
        self.field_control_ramping = field_control_ramping
        self.field_measurement_enabled = field_measurement_enabled
        self.transient = transient


class FastHallQuestionableRegister(RegisterBase):
    """Class object representing the questionable status register"""

    bit_names = [
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
        "probe_eeprom_read_error",
        "r2_less_than_minimum_allowable"
    ]

    def __init__(self,
                 source_in_compliance_or_at_current_limit,
                 field_control_slew_rate_limit,
                 field_control_at_voltage_limit,
                 current_measurement_overload,
                 voltage_measurement_overload,
                 invalid_probe,
                 invalid_calibration,
                 inter_processor_communication_error,
                 field_measurement_communication_error,
                 probe_eeprom_read_error,
                 r2_less_than_minimum_allowable):
        self.source_in_compliance_or_at_current_limit = source_in_compliance_or_at_current_limit
        self.field_control_slew_rate_limit = field_control_slew_rate_limit
        self.field_control_at_voltage_limit = field_control_at_voltage_limit
        self.current_measurement_overload = current_measurement_overload
        self.voltage_measurement_overload = voltage_measurement_overload
        self.invalid_probe = invalid_probe
        self.invalid_calibration = invalid_calibration
        self.inter_processor_communication_error = inter_processor_communication_error
        self.field_measurement_communication_error = field_measurement_communication_error
        self.probe_eeprom_read_error = probe_eeprom_read_error
        self.r2_less_than_minimum_allowable = r2_less_than_minimum_allowable


class FastHall(XIPInstrument):
    """A class object representing a Lake Shore M91 Fast Hall controller"""

    vid_pid = [(0x1FB9, 0x0705)]

    def __init__(self,
                 serial_number=None,
                 com_port=None,
                 baud_rate=921600,
                 flow_control=True,
                 timeout=2.0,
                 ip_address=None,
                 tcp_port=7777,
                 **kwargs):

        # Call the parent init, then fill in values specific to FastHall
        XIPInstrument.__init__(self, serial_number, com_port, baud_rate, flow_control, timeout, ip_address, tcp_port, **kwargs)
        self.status_byte_register = StatusByteRegister
        self.standard_event_register = StandardEventRegister
        self.operation_register = FastHallOperationRegister
        self.questionable_register = FastHallQuestionableRegister

    #Status Methods
    def get_contact_check_running_status(self):
        """Indicates if the contact check measurement is running."""
        return bool(self.query("CCHECK:RUNNING?"))

    def get_fasthall_running_status(self):
        """Indicates if the FastHall measurement is running"""
        return bool(self.query("FASTHALL:RUNNING?"))

    def get_four_wire_running_status(self):
        """Indicates if the four wire measurement is running"""
        return bool(self.query("FWIRE:RUNNING?"))

    def get_resistivity_running_status(self):
        """Indicates if the resistivity measurement is running"""
        return bool(self.query("RESISTIVITY:RUNNING?"))

    def get_dc_hall_running_status(self):
        """Indicates if the DC Hall measurement is running"""
        return bool(self.query("HALL:DC:RUNNING?"))

    def get_dc_hall_waiting_status(self):
        """Indicates if the DC hall measurement is running."""
        return bool(self.query("HALL:DC:WAITING?"))

    def continue_dc_hall(self):
        """Continues the DC hall measurement if it's in a waiting state """
        self.command("HALL:DC:CONTINUE")

    # Reset Methods
    def reset_contact_check_measurement(self):
        """Resets the measurement to a not run state, canceling any running measurement"""
        self.command("CCHECK:RESET")

    def reset_fasthall_measurement(self):
        """Resets the measurement to a not run state, canceling any running measurement"""
        self.command("FASTHALL:RESET")

    def reset_four_wire_measurement(self):
        """Resets the measurement to a not run state, canceling any running measurement"""
        self.command("FWIRE:RESET")

    def reset_dc_hall_measurement(self):
        """Resets the measurement to a not run state, canceling any running measurement"""
        self.command("HALL:DC:RESET")

    def reset_resistivity_measurement(self):
        """Resets the measurement to a not run state, canceling any running measurement"""
        self.command("RESISTIVITY:RESET")

    def reset_measurement_settings(self):
        """Resets all measurement settings to their default"""
        self.command("SYSTEM:PRESET")

    def factory_reset(self):
        """Resets all system information such as settings, wi-fi connections, date and time, etc"""
        self.command("SYSTEM:FACTORYRESET")

