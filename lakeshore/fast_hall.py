"""Implements functionality unique to the Lake Shore M91 Fast Hall"""

from .xip_instrument import XIPInstrument, RegisterBase, StatusByteRegister, StandardEventRegister


def generate_scpi_command(beginning, default_arguments, non_default_arguments):
    """Compiles a SCPI command string based on the default and non default arguments.

        Args:
            beginning (str):
                The first part of the SCPI command that is unqiue to a specific function and measurement type

            default_arguments (list):
                List of arguments that have a default value of 'DEF', but can be another value

            non_default_arguments (list):
                List of arguments that do NOT have a default value of 'DEF'
    """
    final_command = ""

    # Add non default arguments to final command string
    for arg in non_default_arguments:
        if final_command == "":
            final_command += str(arg)
        else:
            final_command += "," + str(arg)

    # If not all default arguments are DEF, then add each argument to the final command string
    if any(args != 'DEF' for args in default_arguments):
        for arg in default_arguments:
            if arg is True or arg is False:
                arg = int(arg)
            if final_command == "":
                final_command += str(arg)
            else:
                final_command += "," + str(arg)

    return beginning + final_command


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
    def run_contact_check_vdp_auto(self,
                                   max_current='DEF',
                                   max_voltage='DEF',
                                   number_of_points='DEF',
                                   min_r_squared='DEF'):
        """Automatically determines excitation value and ranges. Then runs contact check on all 4 pairs.

            Args:
                max_current (float):
                    A 'not to exceed' output current value for the auto algorithm to use MIN= 1 uA MAX = 100 mA
                    Default = 100 mA

                max_voltage (float):
                    A 'not to exceed' output voltage value for the auto algorithm to use MIN = 1 V MAX = 10 V
                    Default = 10 V

                number_of_points (int):
                     The number of points to measure between the excitation start and end. MIN = 2 MAX = 100
                     Default = 11

                min_r_squared (float):
                    The minimum R^2 desired DEFault = 0.9999
        """
        non_default_args = []
        default_args = [max_current, max_voltage, number_of_points, min_r_squared]
        self.command(generate_scpi_command("CCHECK:START ", default_args, non_default_args))

    def run_contact_check_vdp_manual(self,
                                     excitation_type,
                                     excitation_value_start,
                                     excitation_value_end,
                                     compliance_limit,
                                     number_of_points,
                                     excitation_range='AUTO',
                                     measurement_range='AUTO',
                                     min_r_squared='DEF',
                                     blanking_time='DEF'):
        """Performs a contact check measurement on contact pairs 1-2, 2-3, 3-4, and 4-1.

            Args:
                excitation_type (str):
                    * Excitation types are as follows:
                    * "VOLTAGE"
                    * "CURRENT"

                excitation_value_start (float):
                    The starting excitation value For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_value_end (float):
                    The ending excitation value For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_range (float):
                    For voltage excitation 0 to 10.0 V For current excitation 0 to 100e-3 A AUTO sets the range to the
                    best fit range for a given excitation value

                measurement_range (float):
                    For voltage excitation, specify the current measurement range 0 to 100e-3 A For current excitation,
                    specify the voltage measurement range 0 to 10.0 V

                compliance_limit (float):
                    For voltage excitation, specify the current limit 100e-9 to 100e-3 A For current excitation,
                    specify the voltage compliance 1.00 to 10.0 V

                number_of_points (int):
                    The number of points to measure between the excitation start and end. 0-100

                min_r_squared (float):
                    The minimum R^2 desired DEFault = 0.9999.

                blanking_time (float):
                    The time in seconds to wait for hardware to settle before gathering readings. 0.5 ms to 300 s with a
                    resolution of 0.1 ms. Can also be represented by the following string types:
                    * "DEF" = 2 ms
                    * "MIN" = 0.5 ms
                    * "MAX" = 300 s
                """
        non_default_args = [excitation_type, excitation_value_start, excitation_value_end, excitation_range,
                            measurement_range, compliance_limit, number_of_points]
        default_args = [min_r_squared, blanking_time]
        self.command(generate_scpi_command("CCHECK:START:MANUAL ", default_args, non_default_args))

    def run_contact_check_hbar(self,
                               excitation_type,
                               excitation_value_start,
                               excitation_value_end,
                               compliance_limit,
                               number_of_points,
                               excitation_range='AUTO',
                               measurement_range='AUTO',
                               min_r_squared='DEF',
                               blanking_time='DEF'):
        """Performs a contact check measurement on contact pairs 5-6, 5-1, 5-2, 5-3, 5-4, and 6-1

            Args:
                excitation_type (string):
                    excitation types are as follows:
                        * "VOLTAGE"
                        * "CURRENT"

                excitation_value_start (float):
                    The starting excitation value For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_value_end (float):
                    The ending excitation value For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_range (float):
                    For voltage excitation 0 to 10.0 V For current excitation 0 to 100e-3 A AUTO sets the range to the
                    best fit range for a given excitation value

                measurement_range (float):
                    For voltage excitation, specify the current measurement range 0 to 100e-3 A For current excitation,
                    specify the voltage measurement range 0 to 10.0 V

                compliance_limit (float):
                    For voltage excitation, specify the current limit 100e-9 to 100e-3 A For current excitation,
                    specify the voltage compliance 1.00 to 10.0 V

                number_of_points (int):
                    The number of points to measure between the excitation start and end. 0-100

                min_r_squared (float):
                    The minimum R^2 desired DEFault = 0.9999.

                blanking_time (float):
                    The time in seconds to wait for hardware to settle before gathering readings. 0.5 ms to 300 s with a
                    resolution of 0.1 ms. Can also be represented by the following string types:
                    * "DEF" = 2 ms
                    * "MIN" = 0.5 ms
                    * "MAX" = 300 s
                """
        non_default_args = [excitation_type, excitation_value_start, excitation_value_end, excitation_range,
                            measurement_range, compliance_limit, number_of_points]
        default_args = [min_r_squared, blanking_time]
        self.command(generate_scpi_command("CCHECK:HBAR:START ", default_args, non_default_args))

    def run_fasthall_vdp(self,
                         excitation_type,
                         excitation_value,
                         compliance_limit,
                         user_defined_field,
                         excitation_range='AUTO',
                         excitation_measurement_range='AUTO',
                         measurement_range='AUTO',
                         max_number_of_samples='DEF',
                         resistivity='DEF',
                         blanking_time='DEF',
                         number_of_averaging_voltage_samples='DEF',
                         sample_thickness='DEF',
                         min_hall_voltage_snr='DEF'):
        """Performs a FastHall measurement.

            Args:
                excitation_type:
                    * Excitation types are as follows:
                    * "VOLTAGE"
                    * "CURRENT"
                excitation_value (float):
                    For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_range (float):
                    For voltage excitation 0 to 10.0 V For current excitation 0 to 100e-3 A AUTO sets the range to the
                    best fit range for a given excitation value Note: The hardware will be configured to best meet the
                    desired range.

                excitation_measurement_range (float):
                    For voltage excitation 0 to 10.0 V For current excitation 0 to 100e-3 A AUTO sets the measurement
                    range to the best fit range for a given excitation value Note: The hardware will be configured to
                    best meet the desired range.

                measurement_range (float):
                    For voltage excitation, specify the current measurement range 0 to 100e-3 A For current excitation,
                    specify the voltage measurement range 0 to 10.0 V Note: The hardware will be configured to best meet
                    the desired range

                compliance_limit (float):
                    For voltage excitation, specify the current limit 100e-9 to 100e-3 A For current excitation,
                    specify the voltage compliance 1.00 to 10.0 V

                user_defined_field (float):
                    The field, in units of Tesla, the sample is being subjected to. Used for calculations

                max_number_of_samples (int):
                    When minimumSnr is omitted or INFinity, the total number of samples to average 1 - 1000 When
                    minimumSnr is specified, the maximum number of samples to average 10 - 1000 DEFault = 100

                resistivity (float):
                    The resistivity of the sample in units of Ohm*Meters (bulk) of Ohms Per Square (sheet).DEFault = NaN

                blanking_time (float):
                    The time in seconds to wait for hardware to settle before gathering readings. 0.5 ms to 300 s with a
                    resolution of 0.1 ms. Can also be represented by the following string types:
                    * "DEF" = 2 ms
                    * "MIN" = 0.5 ms
                    * "MAX" = 300 s

                number_of_averaging_voltage_samples (int):
                    The number of voltage compensation samples to average. Only applied for excitation type voltage.
                    1 - 120 DEFault = 60

                sample_thickness (float):
                    Thickness of the sample in meters. 0 to 10E-3 m DEFault = 0 m

                min_hall_voltage_snr (float):
                    The desired signal to noise ratio of the measurement calculated using average hall voltage / error
                    of mean 1 - 1000, or infinity DEFault = 30
        """
        non_default_args = [excitation_type, excitation_value, excitation_range,
                            excitation_measurement_range, measurement_range, compliance_limit, user_defined_field]
        default_args = [max_number_of_samples, resistivity, blanking_time, number_of_averaging_voltage_samples,
                        sample_thickness, min_hall_voltage_snr]
        self.command(generate_scpi_command("FASTHALL:START ", default_args, non_default_args))

    def run_fasthall_vdp_link(self,
                              user_defined_field,
                              measurement_range='DEF',
                              max_number_of_samples='DEF',
                              min_hall_voltage_snr='DEF',
                              number_of_averaging_voltage_samples='DEF',
                              sample_thickness='DEF'):
        """Performs a FastHall measurement that uses the last run contact check measurement's excitation type,
        compliance limit, blanking time, excitation range, and the largest absolute value of the start and end
        excitation values along with the last run resistivity measurement's resistivity average and sample thickness.

            Args:
                user_defined_field (float):
                    The field, in units of Tesla, the sample is being subjected to. Used for calculations

                measurement_range (float):
                    For voltage excitation, specify the current measurement range 0 to 100e-3 A For current excitation,
                    specify the voltage measurement range 0 to 10.0 V Note: The hardware will be configured to best meet
                    the desired range

                max_number_of_samples (int):
                    When minimumSnr is omitted or INFinity, the total number of samples to average 1 - 1000 When
                    minimumSnr is specified, the maximum number of samples to average 10 - 1000 DEFault = 100

                min_hall_voltage_snr (float):
                    The desired signal to noise ratio of the measurement calculated using average hall voltage / error
                    of mean 1 - 1000, or infinity DEFault = 30

                number_of_averaging_voltage_samples (int):
                    The number of voltage compensation samples to average. Only applied for excitation type voltage.
                    1 - 120 DEFault = 60

                sample_thickness (float):
                    Thickness of the sample in meters. 0 to 10E-3 m DEFault =  use last run resistivity measurement's
                    sample thickness
        """
        non_default_args = [user_defined_field]
        default_args = [measurement_range, max_number_of_samples, min_hall_voltage_snr,
                        number_of_averaging_voltage_samples, sample_thickness]
        self.command(generate_scpi_command("FASTHALL:START:LINK ", default_args, non_default_args))

    # Four Wire Run Method
    def run_four_wire(self,
                      contact_point1,
                      contact_point2,
                      contact_point3,
                      contact_point4,
                      excitation_type,
                      excitation_value,
                      compliance_limit,
                      excitation_range='AUTO',
                      measurement_range='AUTO',
                      excitation_measurement_range='AUTO',
                      blanking_time='DEF',
                      max_number_of_samples='DEF',
                      min_snr='DEF',
                      excitation_reversal='DEF'):
        """Performs a Four wire measurement. Excitation is sourced from Contact Point 1 to Contact Point 2. Voltage is
        measured/sensed between contact point 3 and contact point 4.

            Args:
                contact_point1 (int):
                    Excitation +. Valid contact points are: 1, 2, 3, 4, 5, or 6. Cannot be the same as Contact Point 2.

                contact_point2 (int):
                    Excitation -. Valid contact points are: 1, 2, 3, 4, 5, or 6. Cannot be the same as Contact Point 1.

                contact_point3 (int):
                    Voltage Measure/Sense +. Valid contact points are: 1, 2, 3, 4, 5, or 6. Cannot be the same as
                    Contact Point 4.

                contact_point4 (int):
                    Voltage Measure/Sense -. Valid contact points are: 1, 2, 3, 4, 5, or 6. Cannot be the same as
                    Contact Point 3.

                excitation_type (str):
                    * Excitation types are as follows:
                    * "VOLTAGE"
                    * "CURRENT"

                excitation_value (float):
                    For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_range (float):
                    For voltage excitation 0 to 10.0 V For current excitation 0 to 100e-3 A AUTO sets the range to the
                    best fit range for a given excitation value Note: The hardware will be configured to best meet the
                    desired range.

                measurement_range (float):
                    For voltage excitation, specify the current measurement range 0 to 100e-3 A For current excitation,
                    specify the voltage measurement range 0 to 10.0 V Note: The hardware will be configured to best meet
                    the desired range

                excitation_measurement_range (float):
                    For voltage excitation 0 to 10.0 V For current excitation 0 to 100e-3 A AUTO sets the measurement
                    range to the best fit range for a given excitation value Note: The hardware will be configured to
                    best meet the desired range.

                compliance_limit (float):
                    For voltage excitation, specify the current limit 100e-9 to 100e-3 A For current excitation,
                    specify the voltage compliance 1.00 to 10.0 V

                blanking_time (float):
                    The time in seconds to wait for hardware to settle before gathering readings. 0.5 ms to 300 s with a
                    resolution of 0.1 ms. Can also be represented by the following string types:
                    * "DEF" = 2 ms
                    * "MIN" = 0.5 ms
                    * "MAX" = 300 s

                max_number_of_samples (int):
                    When minimumSnr is omitted or INFinity, the total number of samples to average 1 - 1000 When
                    minimumSnr is specified, the maximum number of samples to average 10 - 1000 DEFault = 100

                min_snr (float):
                    The desired signal to noise ratio of the measured resistance, calculated using measurement
                    average / error of mean 1 - 1000, or INFinity DEFault = 30

                excitation_reversal (bool):
                    1 = Reverse the excitation to generate the resistance. 0 = no excitation reversal
        """
        non_default_args = [contact_point1, contact_point2, contact_point3, contact_point4, excitation_type,
                            excitation_value, excitation_range, measurement_range, excitation_measurement_range,
                            compliance_limit]
        default_args = [blanking_time, max_number_of_samples, min_snr, excitation_reversal]
        self.command(generate_scpi_command("FWIRE:START ", default_args, non_default_args))

    # DC Hall Run Methods
    def run_dc_hall_vdp(self,
                        excitation_type,
                        excitation_value,
                        compliance_limit,
                        number_of_samples,
                        user_defined_field,
                        excitation_range='AUTO',
                        excitation_measurement_range='AUTO',
                        measurement_range='AUTO',
                        with_field_reversal='DEF',
                        resistivity='DEF',
                        blanking_time='DEF',
                        sample_thickness='DEF'):

        """Performs a DC hall measurement for a Hall Bar sample.

            Args:
                excitation_type (string):
                    * Excitation types are as follows:
                    * "VOLTAGE"
                    * "CURRENT"

                excitation_value (float):
                    For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_range (float):
                    For voltage excitation 0 to 10.0 V For current excitation 0 to 100e-3 A AUTO sets the range to the
                    best fit range for a given excitation value Note: The hardware will be configured to best meet the
                    desired range.

                excitation_measurement_range (float):
                    For voltage excitation 0 to 10.0 V For current excitation 0 to 100e-3 A AUTO sets the measurement
                    range to the best fit range for a given excitation value Note: The hardware will be configured to
                    best meet the desired range.

                measurement_range (float):
                    For voltage excitation, specify the current measurement range 0 to 100e-3 A For current excitation,
                    specify the voltage measurement range 0 to 10.0 V Note: The hardware will be configured to best meet
                    the desired range

                compliance_limit (float):
                    For voltage excitation, specify the current limit 100e-9 to 100e-3 A For current excitation,
                    specify the voltage compliance 1.00 to 10.0 V

                number_of_samples (int):
                    the number of samples to average 1-1000

                user_defined_field (float):
                    The field, in units of Tesla, the sample is being subjected to. Used for calculations

                with_field_reversal (bool):
                     Specifies whether or not to apply reversal field. Default = true

                resistivity (float):
                    The resistivity of the sample in units of Ohm*Meters (bulk) of Ohms Per Square (sheet). Used for
                    calculations. Measure this value using the RESistivity SCPI subsystem. Defaults to not a number
                    which will propagate through calculated values. DEFault = NaN

                blanking_time (float):
                    The time in seconds to wait for hardware to settle before gathering readings. 0.5 ms to 300 s with a
                    resolution of 0.1 ms. Can also be represented by the following string types:
                    * "DEF" = 2 ms
                    * "MIN" = 0.5 ms
                    * "MAX" = 300 s

                sample_thickness (float):
                    Thickness of the sample in meters. 0 to 10E-3 m DEFault =  use last run resistivity measurement's
                    sample thickness

        """
        non_default_args = [excitation_type, excitation_value, excitation_range, excitation_measurement_range,
                            measurement_range, compliance_limit, number_of_samples, user_defined_field]
        default_args = [with_field_reversal, resistivity, blanking_time, sample_thickness]
        self.command(generate_scpi_command("HALL:DC:START ", default_args, non_default_args))

    def run_dc_hall_hbar(self,
                         excitation_type,
                         excitation_value,
                         compliance_limit,
                         number_of_samples,
                         user_defined_field,
                         excitation_range='AUTO',
                         excitation_measurement_range='AUTO',
                         measurement_range='AUTO',
                         with_field_reversal='DEF',
                         resistivity='DEF',
                         blanking_time='DEF',
                         sample_thickness='DEF'):
        """Performs a DC hall measurement for a Hall Bar sample.

            Args:
                excitation_type (str):
                    * Excitation types are as follows:
                    * "VOLTAGE"
                    * "CURRENT"

                excitation_value (float):
                    For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_range (float):
                    For voltage excitation 0 to 10.0 V For current excitation 0 to 100e-3 A AUTO sets the range to the
                    best fit range for a given excitation value Note: The hardware will be configured to best meet the
                    desired range.

                excitation_measurement_range (float):
                    For voltage excitation 0 to 10.0 V For current excitation 0 to 100e-3 A AUTO sets the measurement
                    range to the best fit range for a given excitation value Note: The hardware will be configured to
                    best meet the desired range.

                measurement_range (float):
                    For voltage excitation, specify the current measurement range 0 to 100e-3 A For current excitation,
                    specify the voltage measurement range 0 to 10.0 V Note: The hardware will be configured to best meet
                    the desired range

                compliance_limit (float):
                    For voltage excitation, specify the current limit 100e-9 to 100e-3 A For current excitation,
                    specify the voltage compliance 1.00 to 10.0 V

                number_of_samples (int):
                    the number of samples to average 1-1000

                user_defined_field (float):
                    The field, in units of Tesla, the sample is being subjected to. Used for calculations

                with_field_reversal (bool):
                     Specifies whether or not to apply reversal field. Default = true

                resistivity (float):
                    The resistivity of the sample in units of Ohm*Meters (bulk) of Ohms Per Square (sheet). Used for
                    calculations. Measure this value using the RESistivity SCPI subsystem. Defaults to not a number
                    which will propagate through calculated values. DEFault = NaN

                blanking_time (float):
                    The time in seconds to wait for hardware to settle before gathering readings. 0.5 ms to 300 s with a
                    resolution of 0.1 ms. Can also be represented by the following string types:
                    * "DEF" = 2 ms
                    * "MIN" = 0.5 ms
                    * "MAX" = 300 s

                sample_thickness:
                    Thickness of the sample in meters. 0 to 10E-3 m DEFault =  use last run resistivity measurement's
                    sample thickness
        """
        non_default_args = [excitation_type, excitation_value, excitation_range, excitation_measurement_range,
                            measurement_range, compliance_limit, number_of_samples, user_defined_field]
        default_args = [with_field_reversal, resistivity, blanking_time, sample_thickness]
        self.command(generate_scpi_command("HALL:HBAR:DC:START ", default_args, non_default_args))

    # Resistivity Measurement Methods
    def run_resistivity_vdp(self,
                            excitation_type,
                            excitation_value,
                            compliance_limit,
                            excitation_range='AUTO',
                            excitation_measurement_range='AUTO',
                            measurement_range='AUTO',
                            max_number_of_samples='DEF',
                            blanking_time='DEF',
                            sample_thickness='DEF',
                            min_snr='DEF'):
        """Performs a resistivity measurement on a Van der Pauw sample.

            Args:
                excitation_type (str):
                    * Excitation types are as follows:
                    * "VOLTAGE"
                    * "CURRENT"

                excitation_value (float):
                    For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_range (float):
                    For voltage excitation 0 to 10.0 V For current excitation 0 to 100e-3 A AUTO sets the range to the
                    best fit range for a given excitation value Note: The hardware will be configured to best meet the
                    desired range.

                excitation_measurement_range (float):
                    For voltage excitation 0 to 10.0 V For current excitation 0 to 100e-3 A AUTO sets the measurement
                    range to the best fit range for a given excitation value Note: The hardware will be configured to
                    best meet the desired range.

                measurement_range (float):
                    For voltage excitation, specify the current measurement range 0 to 100e-3 A For current excitation,
                    specify the voltage measurement range 0 to 10.0 V Note: The hardware will be configured to best meet
                    the desired range

                compliance_limit (float):
                    For voltage excitation, specify the current limit 100e-9 to 100e-3 A For current excitation,
                    specify the voltage compliance 1.00 to 10.0 V

                max_number_of_samples (float):
                    When minimumSnr is omitted or INFinity, the total number of samples to average 1 - 1000 When
                    minimumSnr is specified, the maximum number of samples to average 10 - 1000 DEFault = 100

                blanking_time (float):
                    The time in seconds to wait for hardware to settle before gathering readings. 0.5 ms to 300 s with a
                    resolution of 0.1 ms. Can also be represented by the following string types:
                    * "DEF" = 2 ms
                    * "MIN" = 0.5 ms
                    * "MAX" = 300 s

                sample_thickness (float):
                    Thickness of the sample in meters. 0 to 10E-3 m DEFault =  use last run resistivity measurement's
                    sample thickness

                min_snr:
                    The desired signal to noise ratio of the measured resistance, calculated using measurement
                    average / error of mean 1 - 1000, or INFinity DEFault = 30
        """
        non_default_args = [excitation_type, excitation_value, excitation_range, excitation_measurement_range,
                            measurement_range, compliance_limit]
        default_args = [max_number_of_samples, blanking_time, sample_thickness, min_snr]
        self.command(generate_scpi_command("RESISTIVITY:START ", default_args, non_default_args))

    def run_resistivity_vdp_link(self,
                                 measurement_range='DEF',
                                 sample_thickness='DEF',
                                 min_snr='DEF',
                                 max_number_of_samples='DEF',):
        """Performs a resistivity measurement that uses the last run contact check measurement's excitation type,
        compliance limit, blanking time, excitation range, and the largest absolute value of the start and end
        excitation values.

            Args:
                measurement_range (float):
                    For voltage excitation, specify the current measurement range 0 to 100e-3 A For current excitation,
                    specify the voltage measurement range 0 to 10.0 V Note: The hardware will be configured to best meet
                    the desired range

                sample_thickness (float):
                        Thickness of the sample in meters. 0 to 10E-3 m DEFault =  use last run resistivity
                        measurement's sample thickness

                min_snr (float):
                        The desired signal to noise ratio of the measured resistance, calculated using measurement
                        average / error of mean 1 - 1000, or INFinity DEFault = 30

                max_number_of_samples (int):
                    When minimumSnr is omitted or INFinity, the total number of samples to average 1 - 1000 When
                    minimumSnr is specified, the maximum number of samples to average 10 - 1000 DEFault = 100
        """
        non_default_args = []
        default_args = [measurement_range, sample_thickness, min_snr, max_number_of_samples]
        self.command(generate_scpi_command("RESISTIVITY:START:LINK ", default_args, non_default_args))

    def run_resistivity_hbar(self,
                             excitation_type,
                             excitation_value,
                             compliance_limit,
                             width,
                             separation,
                             excitation_range='AUTO',
                             excitation_measurement_range='AUTO',
                             measurement_range='AUTO',
                             max_number_of_samples='DEF',
                             blanking_time='DEF',
                             sample_thickness='DEF',
                             min_snr='DEF'):
        """Performs a resistivity measurement on a hall bar sample.

            Args:
                excitation_type (str):
                    * Excitation types are as follows:
                    * "VOLTAGE"
                    * "CURRENT"

                excitation_value (float):
                    For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_range (float):
                    For voltage excitation 0 to 10.0 V For current excitation 0 to 100e-3 A AUTO sets the range to the
                    best fit range for a given excitation value Note: The hardware will be configured to best meet the
                    desired range.

                excitation_measurement_range (float):
                    For voltage excitation 0 to 10.0 V For current excitation 0 to 100e-3 A AUTO sets the measurement
                    range to the best fit range for a given excitation value Note: The hardware will be configured to
                    best meet the desired range.

                measurement_range (float):
                    For voltage excitation, specify the current measurement range 0 to 100e-3 A For current excitation,
                    specify the voltage measurement range 0 to 10.0 V Note: The hardware will be configured to best meet
                    the desired range

                compliance_limit (float):
                    For voltage excitation, specify the current limit 100e-9 to 100e-3 A For current excitation,
                    specify the voltage compliance 1.00 to 10.0 V

                width (float):
                    the width of the sample in meters. Greater than 0.

                separation (float):
                    the distance between the sample's arms in meters. Greater than 0

                max_number_of_samples (int):
                    When minimumSnr is omitted or INFinity, the total number of samples to average 1 - 1000 When
                    minimumSnr is specified, the maximum number of samples to average 10 - 1000 DEFault = 100

                blanking_time (float):
                    The time in seconds to wait for hardware to settle before gathering readings. 0.5 ms to 300 s with a
                    resolution of 0.1 ms. Can also be represented by the following string types:
                    * "DEF" = 2 ms
                    * "MIN" = 0.5 ms
                    * "MAX" = 300 s

                sample_thickness (float):
                    Thickness of the sample in meters. 0 to 10E-3 m DEFault =  use last run resistivity measurement's
                    sample thickness

                min_snr (float):
                    The desired signal to noise ratio of the measured resistance, calculated using measurement
                    average / error of mean 1 - 1000, or INFinity DEFault = 30

        """
        non_default_args = [excitation_type, excitation_value, excitation_range, excitation_measurement_range,
                            measurement_range, compliance_limit, width, separation]
        default_args = [max_number_of_samples, blanking_time, sample_thickness, min_snr]
        self.command(generate_scpi_command("RESISTIVITY:HBAR:START ", default_args, non_default_args))

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
