"""Implements functionality unique to the Lake Shore M91 Fast Hall"""

from .xip_instrument import XIPInstrument, RegisterBase, StatusByteRegister, StandardEventRegister


def generate_scpi_run_string(start_string, arguments):
    argument_string = ""
    for count in arguments:
        if str(count) != 'None':
            if argument_string == "":
                argument_string = str(count)
            else:
                argument_string += "," + str(count)
    return start_string + argument_string


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


class ContactCheckManualParameters:
    """Class object representing parameters used for manual Contact Check run methods"""
    def __init__(self,
                 excitation_type,
                 excitation_start_value,
                 excitation_end_value,
                 compliance_limit,
                 excitation_range='AUTO',
                 measurement_range='AUTO',
                 number_of_points='DEF',
                 min_r_squared='DEF',
                 blanking_time='DEF'):

        self.excitation_type = excitation_type
        self.excitation_start_value = excitation_start_value
        self.excitation_end_value = excitation_end_value
        self.excitation_range = excitation_range
        self.measurement_range = measurement_range
        self.compliance_limit = compliance_limit
        self.number_of_points = number_of_points
        self.min_r_squared = min_r_squared
        self.blanking_time = blanking_time


class ContactCheckOptimizedParameters:
    """Class object representing parameters used for optimized Contact Check run methods"""
    def __init__(self,
                 max_current='DEF',
                 max_voltage='DEF',
                 number_of_points='DEF',
                 min_r_squared='DEF'):

        self.max_current = max_current
        self.max_voltage = max_voltage
        self.number_of_points = number_of_points
        self.min_r_squared = min_r_squared


class FastHallManualParameters:
    """Class object representing parameters used for running manual FastHall measurements"""
    def __init__(self,
                 excitation_type,
                 excitation_value,
                 user_defined_field,
                 compliance_limit,
                 excitation_range='AUTO',
                 excitation_measurement_range='AUTO',
                 measurement_range='AUTO',
                 max_samples='DEF',
                 resistivity='DEF',
                 blanking_time='DEF',
                 averaging_samples='DEF',
                 sample_thickness='DEF',
                 min_hall_voltage='DEF'):

        self.excitation_type = excitation_type
        self.excitation_value = excitation_value
        self.excitation_range = excitation_range
        self.excitation_measurement_range = excitation_measurement_range
        self.measurement_range = measurement_range
        self.compliance_limit = compliance_limit
        self.user_defined_field = user_defined_field
        self.max_samples = max_samples
        self.resistivity = resistivity
        self.blanking_time = blanking_time
        self.averaging_samples = averaging_samples
        self.sample_thickness = sample_thickness
        self.min_hall_voltage = min_hall_voltage


class FastHallOptimizedParameters:
    """Class object representing parameters used for running optimized FastHall measurements"""
    def __init__(self,
                 user_defined_field,
                 measurement_range='DEF',
                 max_samples='DEF',
                 min_hall_voltage='DEF',
                 averaging_samples='DEF',
                 sample_thickness='DEF'):

        self.user_defined_field = user_defined_field
        self.measurement_range = measurement_range
        self.max_samples = max_samples
        self.min_hall_voltage = min_hall_voltage
        self.averaging_samples = averaging_samples
        self.sample_thickness = sample_thickness



class FourWireParameters:
    """Class object representing parameters used for running Four Wire measurements"""
    def __init__(self,
                 contact_point1,
                 contact_point2,
                 contact_point3,
                 contact_point4,
                 excitation_type,
                 excitation_value,
                 compliance_limit,
                 excitation_range='AUTO',
                 excitation_measurement_range='AUTO',
                 measurement_range='AUTO',
                 blanking_time='DEF',
                 max_samples='DEF',
                 min_snr='DEF',
                 excitation_reversal='DEF'):

        self.contact_point1 = contact_point1
        self.contact_point2 = contact_point2
        self.contact_point3 = contact_point3
        self.contact_point4 = contact_point4
        self.excitation_type = excitation_type
        self.excitation_value = excitation_value
        self.excitation_range = excitation_range
        self.excitation_measurement_range = excitation_measurement_range
        self.measurement_range = measurement_range
        self.compliance_limit = compliance_limit
        self.blanking_time = blanking_time
        self.max_samples = max_samples
        self.min_snr = min_snr
        self.excitation_reversal = excitation_reversal


class DCHallParameters:
    """Class object representing parameters used for running DC Hall measurements"""
    def __init__(self,
                 excitation_type,
                 excitation_value,
                 compliance_limit,
                 averaging_samples,
                 user_defined_field,
                 excitation_range='AUTO',
                 excitation_measurement_range='AUTO',
                 measurement_range='AUTO',
                 with_field_reversal='DEF',
                 resistivity='DEF',
                 blanking_time='DEF',
                 sample_thickness='DEF'):

        self.excitation_type = excitation_type
        self.excitation_value = excitation_value
        self.excitation_range = excitation_range
        self.excitation_measurement_range = excitation_measurement_range
        self.measurement_range = measurement_range
        self.compliance_limit = compliance_limit
        self.averaging_samples = averaging_samples
        self.user_defined_field = user_defined_field
        self.with_field_reversal = with_field_reversal
        self.resistivity = resistivity
        self.blanking_time = blanking_time
        self.sample_thickness = sample_thickness


class ResistivityManualParameters:
    """Class object representing parameters used for running manual Resistivity measurements"""
    def __init__(self,
                 excitation_type,
                 excitation_value,
                 compliance_limit,
                 excitation_range='AUTO',
                 excitation_measurement_range='AUTO',
                 measurement_range='AUTO',
                 max_samples='DEF',
                 blanking_time='DEF',
                 sample_thickness='DEF',
                 min_snr='DEF',
                 **kwargs):

        self.excitation_type = excitation_type
        self.excitation_value = excitation_value
        self.excitation_range = excitation_range
        self.excitation_measurement_range = excitation_measurement_range
        self.measurement_range = measurement_range
        self.compliance_limit = compliance_limit
        self.width = kwargs.get('width')
        self.separation = kwargs.get('separation')
        self.max_samples = max_samples
        self.blanking_time = blanking_time
        self.sample_thickness = sample_thickness
        self.min_snr = min_snr


class ResistivityOptimizedParameters:
    """Class object representing parameters used for running manual Resistivity measurements"""
    def __init__(self,
                 measurement_range='DEF',
                 sample_thickness='DEF',
                 min_snr='DEF',
                 max_samples='DEF'):

        self.measurement_range = measurement_range
        self.sample_thickness = sample_thickness
        self.min_snr = min_snr
        self.max_samples = max_samples


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
        XIPInstrument.__init__(self, serial_number, com_port, baud_rate, flow_control, timeout, ip_address, tcp_port,
                               **kwargs)
        self.status_byte_register = StatusByteRegister
        self.standard_event_register = StandardEventRegister
        self.operation_register = FastHallOperationRegister
        self.questionable_register = FastHallQuestionableRegister

    # Status Methods
    def get_contact_check_running_status(self):
        """Indicates if the contact check measurement is running."""
        return bool(int(self.query("CCHECK:RUNNING?")))

    def get_fasthall_running_status(self):
        """Indicates if the FastHall measurement is running"""
        return bool(int(self.query("FASTHALL:RUNNING?")))

    def get_four_wire_running_status(self):
        """Indicates if the four wire measurement is running"""
        return bool(int(self.query("FWIRE:RUNNING?")))

    def get_resistivity_running_status(self):
        """Indicates if the resistivity measurement is running"""
        return bool(int(self.query("RESISTIVITY:RUNNING?")))

    def get_dc_hall_running_status(self):
        """Indicates if the DC Hall measurement is running"""
        return bool(int(self.query("HALL:DC:RUNNING?")))

    def get_dc_hall_waiting_status(self):
        """Indicates if the DC hall measurement is running."""
        return bool(int(self.query("HALL:DC:WAITING?")))

    def continue_dc_hall(self):
        """Continues the DC hall measurement if it's in a waiting state """
        self.command("HALL:DC:CONTINUE")

    # Contact Check Run Methods

    def run_contact_check_vdp_measurement_auto(self, settings):
        """Automatically determines excitation value and ranges. Then runs contact check on all 4 pairs.

            Args:
                settings(ContactCheckOptimizedParameters):
        """
        parameter_list = settings.__dict__.values()
        scpi_parameter_string = generate_scpi_run_string("CCHECK:START ", parameter_list)
        self.command(scpi_parameter_string)

    def run_contact_check_vdp_measurement_manual(self, settings):
        """Performs a contact check measurement on contact pairs 1-2, 2-3, 3-4, and 4-1.

            Args:
                settings(ContactCheckManualParameters):
                """
        parameter_list = settings.__dict__.values()
        scpi_parameter_string = generate_scpi_run_string("CCHECK:START:MANUAL ", parameter_list)
        self.command(scpi_parameter_string)

    def run_contact_check_hbar_measurement(self, settings):
        """Performs a contact check measurement on contact pairs 5-6, 5-1, 5-2, 5-3, 5-4, and 6-1

            Args:
                settings(ContactCheckManualParameters):
                """
        parameter_list = settings.__dict__.values()
        scpi_parameter_string = generate_scpi_run_string("CCHECK:HBAR:START ", parameter_list)
        self.command(scpi_parameter_string)

    def run_fasthall_vdp_measurement(self, settings):
        """Performs a FastHall measurement.

            Args:
                settings (FastHallManualParameters):
            """
        parameter_list = settings.__dict__.values()
        scpi_parameter_string = generate_scpi_run_string("FASTHALL:START ", parameter_list)
        self.command(scpi_parameter_string)

    def run_fasthall_vdp_measurement_existing_settings(self, settings):
        """Performs a FastHall (wmeasurement that uses the last run contact check measurement's excitation type,
        compliance limit, blanking time, excitation range, and the largest absolute value of the start and end
        excitation values along with the last run resistivity measurement's resistivity average and sample thickness.

            Args:
                settings (FastHallOptimizedParameters)
        """
        parameter_list = settings.__dict__.values()
        scpi_parameter_string = generate_scpi_run_string("FASTHALL:START:LINK ", parameter_list)
        self.command(scpi_parameter_string)

    # Four Wire Run Method
    def run_four_wire_measurement(self, settings):
        """Performs a Four wire measurement. Excitation is sourced from Contact Point 1 to Contact Point 2. Voltage is
        measured/sensed between contact point 3 and contact point 4.

            Args:
                settings(FourWireParameters)
        """
        if settings.excitation_reversal != 'DEF':
            settings.excitation_reversal = str(int(settings.excitation_reversal))

        parameter_list = settings.__dict__.values()
        scpi_parameter_string = generate_scpi_run_string("FWIRE:START ", parameter_list)
        self.command(scpi_parameter_string)

    # DC Hall Run Methods
    def run_dc_hall_vdp_measurement(self, settings):

        """Performs a DC hall measurement for a Hall Bar sample.

            Args:
                settings(DCHallParameters)

        """
        if settings.with_field_reversal != 'DEF':
            settings.with_field_reversal = str(int(settings.with_field_reversal))

        parameter_list = settings.__dict__.values()
        scpi_parameter_string = generate_scpi_run_string("HALL:DC:START ", parameter_list)
        self.command(scpi_parameter_string)

    def run_dc_hall_hbar_measurement(self, settings):
        """Performs a DC hall measurement for a Hall Bar sample.

            Args:
                settings(DCHallParameters)
        """
        if settings.with_field_reversal != 'DEF':
            settings.with_field_reversal = str(int(settings.with_field_reversal))

        parameter_list = settings.__dict__.values()
        scpi_parameter_string = generate_scpi_run_string("HALL:HBAR:DC:START ", parameter_list)
        self.command(scpi_parameter_string)

    # Resistivity Measurement Methods
    def run_resistivity_vdp_measurement(self, settings):
        """Performs a resistivity measurement on a Van der Pauw sample.

            Args:
                settings(ResistivityManualParameters)
        """
        parameter_list = settings.__dict__.values()
        scpi_parameter_string = generate_scpi_run_string("RESISTIVITY:START ", parameter_list)
        self.command(scpi_parameter_string)

    def run_resistivity_vdp_measurement_existing_settings(self, settings):
        """Performs a resistivity measurement that uses the last run contact check measurement's excitation type,
        compliance limit, blanking time, excitation range, and the largest absolute value of the start and end
        excitation values.

            Args:
                settings(ResistivityOptimizedParameters)
        """
        parameter_list = settings.__dict__.values()
        scpi_parameter_string = generate_scpi_run_string("RESISTIVITY:START:LINK ", parameter_list)
        self.command(scpi_parameter_string)

    def run_resistivity_hbar_measurement(self, settings):
        """Performs a resistivity measurement on a hall bar sample.

            Args:
                settings(ResistivityManualParameters)

        """
        parameter_list = settings.__dict__.values()
        scpi_parameter_string = generate_scpi_run_string("RESISTIVITY:HBAR:START ", parameter_list)
        self.command(scpi_parameter_string)

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
