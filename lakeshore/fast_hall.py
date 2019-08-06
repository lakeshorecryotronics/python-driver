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


class ContactCheckManualParameters:
    """Class object representing parameters used for manual Contact Check run methods."""
    def __init__(self,
                 excitation_type,
                 excitation_start_value,
                 excitation_end_value,
                 compliance_limit,
                 number_of_points,
                 excitation_range='AUTO',
                 measurement_range='AUTO',
                 min_r_squared=0.9999,
                 blanking_time=2e-3):
        """The constructor for ContackCheckManualParameters class.
            Args:
                excitation_type (str):
                    * The excitation type used for the measurement. Options are:
                    * "CURRENT"
                    * "VOLTAGE"

                excitation_start_value (float):
                    The starting excitation value For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_end_value (float):
                    The ending excitation value For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_range (float or str):
                    * Excitation range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - volts in the range of 0 to 10.0V: voltage excitation
                        - amps in the range of -100e-3 to 100e-3 A: current excitation

                measurement_range (float or str):
                    * Measurement range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - amps in the range of 0 to 100e-3A: voltage excitation
                        - volts in the range of 0 to 10.0V: current excitation

                compliance_limit (float):
                    For voltage excitation, specify the current limit 100e-9 to 100e-3 A For current excitation,
                    specify the voltage compliance 1.00 to 10.0 V

                number_of_points (int):
                    The number of points to measure between the excitation start and end. 0 - 100

                min_r_squared (float):
                    The minimum R^2 desired. Default is 0.9999.

                blanking_time (float or str):
                    * The time in seconds to wait for hardware to settle before gathering readings. Range of time is
                      0.5 ms - 300 s with a resolution of 0.1 ms. Options are:
                    * "DEF" (Default) = 2 ms
                    * "MIN" = 0.5 ms
                    * "MAX" = 300 s
                    * floating point number of seconds
        """
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
                 max_current=100e-3,
                 max_voltage=10,
                 number_of_points=11,
                 min_r_squared=0.9999):
        """The constructor for ContactCheckOptimizedParameters class.
            Args:
                max_current(float or str):
                    * A 'not to exceed' output current value for the auto algorithm to use. Options are:
                    * "MIN" = 1 uA
                    * "MAX" = 100 mA
                    * "DEF" (Default) = 100 mA
                    * floating point number of amps

                max_voltage(float or str):
                    * A 'not to exceed' output voltage value for the auto algorithm to use. Options are:
                    * "MIN" = 1 V
                    * "MAX" = 10 V
                    * "DEF" (Default) = 10 V
                    * floating point number of volts

                number_of_points(int or str):
                    * The number of points to measure between the excitation start and end. Options are:
                    * "MIN" = 2
                    * "MAX" = 100
                    * "DEF" (Default) = 11
                    * integer number of points

                min_r_squared(float):
                    The minimum R^2 desired. Default is 0.9999.
        """
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
                 max_samples=100,
                 resistivity='"NaN"',
                 blanking_time=2e-3,
                 averaging_samples=60,
                 sample_thickness=0,
                 min_hall_voltage_snr=30):
        """The constructor for FastHallManualParameters class
            Args:
                excitation_type (str):
                    * The excitation type used for the measurement. Options are:
                    * "CURRENT"
                    * "VOLTAGE"

                excitation_value(float):
                    For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_range (float or str):
                    * Excitation range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - volts in the range of 0 to 10.0V for voltage excitation,
                        - amps in the range of -100e-3 to 100e-3 A for current excitation

                excitation_measurement_range (float or str):
                    * Excitation measurement range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - volts in the range of 0 to 10.0V: voltage excitation
                        - amps in the range of -100e-3 to 100e-3 A: current excitation

                measurement_range (float or str):
                    * Measurement range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - amps in the range of 0 to 100e-3A: voltage excitation
                        - volts in the range of 0 to 10.0V: current excitation

                compliance_limit (float):
                    For voltage excitation, specify the current limit 100e-9 to 100e-3 A For current excitation,
                    specify the voltage compliance 1.00 to 10.0 V

                user_defined_field (float):
                    The field, in units of Tesla, the sample is being subjected to. Used for calculations.

                max_samples(int):
                    When minimumSnr is omitted or Infinity ('INF'), the total number of samples to average 1 - 1000 When
                    minimumSnr is specified, the maximum number of samples to average 10 - 1000. Default is 100

                resistivity (float):
                    The resistivity of the sample in units of Ohm*Meters (bulk) of Ohms Per Square (sheet). Used for
                    calculations. Measure this value using the RESistivity SCPI subsystem. Defaults to 'Nan' (not a
                    number) which will propagate through calculated values


                blanking_time (float or str):
                    * The time in seconds to wait for hardware to settle before gathering readings. Range of time is
                      0.5 ms - 300 s with a resolution of 0.1 ms. Options are:
                    * "DEF" (Default) = 2 ms
                    * "MIN" = 0.5 ms
                    * "MAX" = 300 s
                    * floating point number in seconds

                averaging_samples (int):
                    The number of voltage compensation samples to average. Only applied for excitation type voltage.
                    1 - 120. Default is 60.

                sample_thickness (float):
                    Thickness of the sample in meters. 0 to 10E-3 m Default is 0 m

                min_hall_voltage_snr (float or str):
                    * The desired signal to noise ratio of the measurement calculated using average hall voltage / error
                      of mean 1 - 1000. Options are:
                    * "INF" (Infinity)
                    * "DEF" (Default) = 30
                    * floating point number to represent the ratio
        """
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
        self.min_hall_voltage_snr = min_hall_voltage_snr


class FastHallOptimizedParameters:
    """Class object representing parameters used for running optimized FastHall measurements"""
    def __init__(self,
                 user_defined_field,
                 measurement_range='AUTO',
                 max_samples=100,
                 min_hall_voltage_snr=30,
                 averaging_samples=60,
                 sample_thickness='DEF'):
        """The constructor for FastHallOptimizedParameters class
            Args:
                user_defined_field (float):
                    The field, in units of Tesla, the sample is being subjected to. Used for calculations.

                measurement_range (float or str):
                    For voltage excitation, specify the current measurement range 0 to 100e-3 A For current
                    excitation, specify the voltage measurement range 0 to 10.0 V. Defaults to 'AUTO'

                max_samples(int):
                    When minimumSnr is omitted or Infinity ('INF'), the total number of samples to average 1 - 1000
                    When minimumSnr is specified, the maximum number of samples to average 10 - 1000 Defaults to 100

                min_hall_voltage_snr (float or str):
                    * The desired signal to noise ratio of the measurement calculated using average hall voltage / error
                      of mean 1 - 1000. Options are:
                    * "INF" (Infinity)
                    * "DEF" (Default) = 30
                    * floating point number to represent the ratio

                averaging_samples (int):
                    The number of voltage compensation samples to average. Only applied for excitation type voltage.
                    1 - 120. Defaults to 60

                sample_thickness (float):
                    Thickness of the sample in meters. 0 to 10E-3 m Default is the last run resistivity measurement's
                    sample thickness.
        """
        self.user_defined_field = user_defined_field
        self.measurement_range = measurement_range
        self.max_samples = max_samples
        self.min_hall_voltage_snr = min_hall_voltage_snr
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
                 blanking_time=2e-3,
                 max_samples=100,
                 min_snr=30,
                 excitation_reversal=True):
        """The constructor for FourWireParameter class.
            Args:
                contact_point1 (int):
                    Excitation +. Valid contact points are: 1, 2, 3, 4, 5, or 6. Cannot be the same as Contact Point 2.

                contact_point2 (int):
                    Excitation - Valid contact points are: 1, 2, 3, 4, 5, or 6. Cannot be the same as Contact Point 1.

                contact_point3 (int):
                    Voltage Measure/Sense +. Valid contact points are: 1, 2, 3, 4, 5, or 6. Cannot be the same as
                    Contact Point 4.

                contact_point4 (int):
                    Voltage Measure/Sense -. Valid contact points are: 1, 2, 3, 4, 5, or 6. Cannot be the same as
                    Contact Point 3.

                excitation_type (str):
                    * The excitation type used for the measurement. Options are:
                    * "CURRENT"
                    * "VOLTAGE"

                excitation_value(float):
                    For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_range (float or str):
                    * Excitation range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - volts in the range of 0 to 10.0V for voltage excitation,
                        - amps in the range of -100e-3 to 100e-3 A for current excitation

                excitation_measurement_range (float or str):
                    * Excitation measurement range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - volts in the range of 0 to 10.0V: voltage excitation
                        - amps in the range of -100e-3 to 100e-3 A: current excitation

                measurement_range (float or str):
                    * Measurement range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - amps in the range of 0 to 100e-3A: voltage excitation
                        - volts in the range of 0 to 10.0V: current excitation

                compliance_limit (float):
                    For voltage excitation, specify the current limit 100e-9 to 100e-3 A For current excitation,
                    specify the voltage compliance 1.00 to 10.0 V

                blanking_time (float or str):
                    * The time in seconds to wait for hardware to settle before gathering readings. Range of time is
                      0.5 ms - 300 s with a resolution of 0.1 ms. Options are:
                    * "DEF" (Default)= 2 ms
                    * "MIN" = 0.5 ms
                    * "MAX" = 300 s
                    * floating point number in seconds

                max_samples(int):
                    When minimumSnr is omitted or Infinity, the total number of samples to average 1 - 1000 When
                    minimumSnr is specified, the maximum number of samples to average 10 - 1000. Default is 100

                min_snr (float or str):
                    * The desired signal to noise ratio of the measurement resistance, calculated using measurement
                      average / error of mean 1 - 1000. Options are:
                    * "INF" (Infinity)
                    * "DEF" (Default)= 30
                    * floating point number to represent the ratio

                excitation_reversal (bool):
                    True = Reverse the excitation to generate the resistance. False = no excitation reversal
        """
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
        self.excitation_reversal = str(int(excitation_reversal))


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
                 with_field_reversal=True,
                 resistivity='"NaN"',
                 blanking_time=2e-3,
                 sample_thickness=0):
        """The constructor for DCHallParameters.
            Args:
                excitation_type (str):
                    * The excitation type used for the measurement. Options are:
                    * "CURRENT"
                    * "VOLTAGE"

                excitation_value(float):
                    For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_range (float or str):
                    * Excitation range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - volts in the range of 0 to 10.0V for voltage excitation,
                        - amps in the range of -100e-3 to 100e-3 A for current excitation

                excitation_measurement_range (float or str):
                    * Excitation measurement range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - volts in the range of 0 to 10.0V: voltage excitation
                        - amps in the range of -100e-3 to 100e-3 A: current excitation

                measurement_range (float or str):
                    * Measurement range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - amps in the range of 0 to 100e-3A: voltage excitation
                        - volts in the range of 0 to 10.0V: current excitation

                compliance_limit (float):
                    For voltage excitation, specify the current limit 100e-9 to 100e-3 A For current excitation,
                    specify the voltage compliance 1.00 to 10.0 V

                averaging_samples(int):
                    The number of samples to average 1-1000

                user_defined_field(float):
                    The field, in units of Tesla, the sample is being subjected to. Used for calculations.

                with_field_reversal (bool):
                    Specifies whether or not to apply reversal field. Default is true

                resistivity(float):
                    The resistivity of the sample in units of Ohm*Meters (bulk) of Ohms Per Square (sheet). Used for
                    calculations. Measure this value using the RESistivity SCPI subsystem. Defaults to 'NaN' (not a
                    number) which will propagate through calculated values.

                blanking_time (float or str):
                    * The time in seconds to wait for hardware to settle before gathering readings. Range of time is
                      0.5 ms - 300 s with a resolution of 0.1 ms. Options are:
                    * "DEF" (Default) = 2 ms
                    * "MIN" = 0.5 ms
                    * "MAX" = 300 s
                    * floating point number in seconds

                sample_thickness (float):
                    Thickness of the sample in meters. 0 to 10e-3 m. Default is 0m
            """

        self.excitation_type = excitation_type
        self.excitation_value = excitation_value
        self.excitation_range = excitation_range
        self.excitation_measurement_range = excitation_measurement_range
        self.measurement_range = measurement_range
        self.compliance_limit = compliance_limit
        self.averaging_samples = averaging_samples
        self.user_defined_field = user_defined_field
        self.with_field_reversal = str(int(with_field_reversal))
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
                 max_samples=100,
                 blanking_time=2e-3,
                 sample_thickness=0,
                 min_snr=30,
                 **kwargs):
        """The constructor for ResistivityManualParameters class.
            Args:
                excitation_type (str):
                    * The excitation type used for the measurement. Options are:
                    * "CURRENT"
                    * "VOLTAGE"

                excitation_value(float):
                    For voltage -10.0 to 10.0 V For current -100e-3 to 100e-3 A

                excitation_range (float or str):
                    * Excitation range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - volts in the range of 0 to 10.0V for voltage excitation,
                        - amps in the range of -100e-3 to 100e-3 A for current excitation

                excitation_measurement_range (float or str):
                    * Excitation measurement range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - volts in the range of 0 to 10.0V: voltage excitation
                        - amps in the range of -100e-3 to 100e-3 A: current excitation

                measurement_range (float or str):
                    * Measurement range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - amps in the range of 0 to 100e-3A: voltage excitation
                        - volts in the range of 0 to 10.0V: current excitation

                compliance_limit (float):
                    For voltage excitation, specify the current limit 100e-9 to 100e-3 A For current excitation,
                    specify the voltage compliance 1.00 to 10.0 V

                max_samples(int):
                    When minimumSnr is omitted or Infinity ('INF'), the total number of samples to average 1 - 1000 When
                    minimumSnr is specified, the maximum number of samples to average 10 - 1000. Default is 100

                blanking_time (float or str):
                    * The time in seconds to wait for hardware to settle before gathering readings. Range of time is
                      0.5 ms - 300 s with a resolution of 0.1 ms. Options are:
                    * "DEF" (Default) = 2 ms
                    * "MIN" = 0.5 ms
                    * "MAX" = 300 s
                    * floating point number in seconds

                averaging_samples (int):
                    The number of voltage compensation samples to average. Only applied for excitation type voltage.
                    1 - 120. Default is 60

                sample_thickness (float):
                    Thickness of the sample in meters. 0 to 10E-3 m. Default is 0 m

                min_snr (float or str):
                    * The desired signal to noise ratio of the measurement calculated using average resistivity / error
                      of mean 1 - 1000. Options are:
                    * "INF" (Infinity)
                    * "DEF" (Default) = 30
                    * floating point number to represent the ratio

            Kwargs:
                width(float):
                    The width of the sample in meters. Greater than 0

                separation(float):
                    The distance between the sample's arms in meters. Greater than 0
            """

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
                 measurement_range='AUTO',
                 sample_thickness=0,
                 min_snr=30,
                 max_samples=100):
        """The constructor for ResistivityOptimizedParameters class.
            Args:
                measurement_range (float or str):
                    * Measurement range based on the excitation type. Options are:
                    * "AUTO": sets the range to the best fit range for a given excitation value
                    * floating point number of
                        - amps in the range of 0 to 100e-3A: voltage excitation
                        - volts in the range of 0 to 10.0V: current excitation

                sample_thickness (float):
                    Thickness of the sample in meters. 0 to 10E-3 m. Default is 0 m

                min_snr (float or str):
                    * The desired signal to noise ratio of the measurement calculated using average resistivity / error
                      of mean 1 - 1000. Options are:
                    * "INF" (Infinity)
                    * "DEF" (Default)= 30
                    * floating point number to represent the ratio

                max_samples(int):
                    When minimumSnr is omitted or Infinity ('INF'), the total number of samples to average 1 - 1000 When
                    minimumSnr is specified, the maximum number of samples to average 10 - 1000 Default is 100
        """

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

    def run_contact_check_vdp_measurement_auto(self, settings):
        """Automatically determines excitation value and ranges. Then runs contact check on all 4 pairs.

            Args:
                settings(ContactCheckOptimizedParameters):
        """
        command_string = "CCHECK:START " + \
                         str(settings.max_current) + "," + \
                         str(settings.max_voltage) + "," + \
                         str(settings.number_of_points) + "," + \
                         str(settings.min_r_squared)
        self.command(command_string)

    def run_contact_check_vdp_measurement_manual(self, settings):
        """Performs a contact check measurement on contact pairs 1-2, 2-3, 3-4, and 4-1.

            Args:
                settings(ContactCheckManualParameters):
                """
        command_string = "CCHECK:START:MANUAL " + \
                         str(settings.excitation_type) + "," + \
                         str(settings.excitation_start_value) + "," + \
                         str(settings.excitation_end_value) + "," + \
                         str(settings.excitation_range) + "," + \
                         str(settings.measurement_range) + "," + \
                         str(settings.compliance_limit) + "," + \
                         str(settings.number_of_points) + "," + \
                         str(settings.min_r_squared) + "," + \
                         str(settings.blanking_time)
        self.command(command_string)

    def run_contact_check_hbar_measurement(self, settings):
        """Performs a contact check measurement on contact pairs 5-6, 5-1, 5-2, 5-3, 5-4, and 6-1

            Args:
                settings(ContactCheckManualParameters):
                """
        command_string = "CCHECK:HBAR:START " + \
                         str(settings.excitation_type) + "," + \
                         str(settings.excitation_start_value) + "," + \
                         str(settings.excitation_end_value) + "," + \
                         str(settings.excitation_range) + "," + \
                         str(settings.measurement_range) + "," + \
                         str(settings.compliance_limit) + "," + \
                         str(settings.number_of_points) + "," + \
                         str(settings.min_r_squared) + "," + \
                         str(settings.blanking_time)
        self.command(command_string)

    def run_fasthall_vdp_measurement(self, settings):
        """Performs a FastHall measurement.

            Args:
                settings (FastHallManualParameters):
            """
        command_string = "FASTHALL:START " + \
                         str(settings.excitation_type) + "," + \
                         str(settings.excitation_value) + "," + \
                         str(settings.excitation_range) + "," + \
                         str(settings.excitation_measurement_range) + "," + \
                         str(settings.measurement_range) + "," + \
                         str(settings.compliance_limit) + "," + \
                         str(settings.user_defined_field) + "," + \
                         str(settings.max_samples) + "," + \
                         str(settings.resistivity) + "," + \
                         str(settings.blanking_time) + "," + \
                         str(settings.averaging_samples) + "," + \
                         str(settings.sample_thickness) + "," + \
                         str(settings.min_hall_voltage_snr)
        self.command(command_string)

    def run_fasthall_vdp_measurement_optimized(self, settings):
        """Performs a FastHall (measurement that uses the last run contact check measurement's excitation type,
        compliance limit, blanking time, excitation range, and the largest absolute value of the start and end
        excitation values along with the last run resistivity measurement's resistivity average and sample thickness.

            Args:
                settings (FastHallOptimizedParameters)
        """
        command_string = "FASTHALL:START:LINK " + \
                         str(settings.user_defined_field) + "," + \
                         str(settings.measurement_range) + "," + \
                         str(settings.max_samples) + "," + \
                         str(settings.min_hall_voltage_snr) + "," + \
                         str(settings.averaging_samples) + "," + \
                         str(settings.sample_thickness)
        self.command(command_string)

    def run_four_wire_measurement(self, settings):
        """Performs a Four wire measurement. Excitation is sourced from Contact Point 1 to Contact Point 2. Voltage is
        measured/sensed between contact point 3 and contact point 4.

            Args:
                settings(FourWireParameters)
        """
        command_string = "FWIRE:START " + \
                         str(settings.contact_point1) + "," + \
                         str(settings.contact_point2) + "," + \
                         str(settings.contact_point3) + "," + \
                         str(settings.contact_point4) + "," + \
                         str(settings.excitation_type) + "," + \
                         str(settings.excitation_value) + "," + \
                         str(settings.excitation_range) + "," + \
                         str(settings.excitation_measurement_range) + "," + \
                         str(settings.measurement_range) + "," + \
                         str(settings.compliance_limit) + "," + \
                         str(settings.blanking_time) + "," + \
                         str(settings.max_samples) + "," + \
                         str(settings.min_snr) + "," + \
                         str(settings.excitation_reversal)
        self.command(command_string)

    def run_dc_hall_vdp_measurement(self, settings):

        """Performs a DC hall measurement for a Hall Bar sample.

            Args:
                settings(DCHallParameters)

        """
        command_string = "HALL:DC:START " + \
                         str(settings.excitation_type) + "," + \
                         str(settings.excitation_value) + "," + \
                         str(settings.excitation_range) + "," + \
                         str(settings.excitation_measurement_range) + "," + \
                         str(settings.measurement_range) + "," + \
                         str(settings.compliance_limit) + "," + \
                         str(settings.averaging_samples) + "," + \
                         str(settings.user_defined_field) + "," + \
                         str(settings.with_field_reversal) + "," + \
                         str(settings.resistivity) + "," + \
                         str(settings.blanking_time) + "," + \
                         str(settings.sample_thickness)
        self.command(command_string)

    def run_dc_hall_hbar_measurement(self, settings):
        """Performs a DC hall measurement for a Hall Bar sample.

            Args:
                settings(DCHallParameters)
        """
        command_string = "HALL:HBAR:DC:START " + \
                         str(settings.excitation_type) + "," + \
                         str(settings.excitation_value) + "," + \
                         str(settings.excitation_range) + "," + \
                         str(settings.excitation_measurement_range) + "," + \
                         str(settings.measurement_range) + "," + \
                         str(settings.compliance_limit) + "," + \
                         str(settings.averaging_samples) + "," + \
                         str(settings.user_defined_field) + "," + \
                         str(settings.with_field_reversal) + "," + \
                         str(settings.resistivity) + "," + \
                         str(settings.blanking_time) + "," + \
                         str(settings.sample_thickness)
        self.command(command_string)

    def run_resistivity_vdp_measurement(self, settings):
        """Performs a resistivity measurement on a Van der Pauw sample.

            Args:
                settings(ResistivityManualParameters)
        """
        command_string = "RESISTIVITY:START " + \
                         str(settings.excitation_type) + "," + \
                         str(settings.excitation_value) + "," + \
                         str(settings.excitation_range) + "," + \
                         str(settings.excitation_measurement_range) + "," + \
                         str(settings.measurement_range) + "," + \
                         str(settings.compliance_limit) + "," + \
                         str(settings.max_samples) + "," + \
                         str(settings.blanking_time) + "," + \
                         str(settings.sample_thickness) + "," + \
                         str(settings.min_snr)
        self.command(command_string)

    def run_resistivity_vdp_measurement_optimized(self, settings):
        """Performs a resistivity measurement that uses the last run contact check measurement's excitation type,
        compliance limit, blanking time, excitation range, and the largest absolute value of the start and end
        excitation values.

            Args:
                settings(ResistivityOptimizedParameters)
        """
        command_string = "RESISTIVITY:START:LINK " + \
                         str(settings.measurement_range) + "," + \
                         str(settings.sample_thickness) + "," + \
                         str(settings.min_snr) + "," + \
                         str(settings.max_samples)
        self.command(command_string)

    def run_resistivity_hbar_measurement(self, settings):
        """Performs a resistivity measurement on a hall bar sample.

            Args:
                settings(ResistivityManualParameters)

        """
        command_string = "RESISTIVITY:HBAR:START " + \
                         str(settings.excitation_type) + "," + \
                         str(settings.excitation_value) + "," + \
                         str(settings.excitation_range) + "," + \
                         str(settings.excitation_measurement_range) + "," + \
                         str(settings.measurement_range) + "," + \
                         str(settings.compliance_limit) + "," + \
                         str(settings.width) + "," + \
                         str(settings.separation) + "," + \
                         str(settings.max_samples) + "," + \
                         str(settings.blanking_time) + "," + \
                         str(settings.sample_thickness) + "," + \
                         str(settings.min_snr)
        self.command(command_string)

    def get_contact_check_setup_results(self):
        """Returns an object representing the setup results of the last run Contact Check measurement"""

        # Parse the query string into a list of individual result values
        results = self.query('CCHECK:RESULT?').rsplit(',')

        # Generate a  Contact Check settings object using the setup result values as the initialization parameters
        settings = ContactCheckManualParameters(excitation_type=results[2],
                                                excitation_start_value=float(results[3]),
                                                excitation_end_value=float(results[4]),
                                                excitation_range=float(results[5]),
                                                measurement_range=float(results[6]),
                                                compliance_limit=float(results[7]),
                                                number_of_points=int(results[8]),
                                                min_r_squared=float(results[9]),
                                                blanking_time=float(results[10]))
        return settings

    def get_contact_check_measurement_results(self):
        """Returns a dictionary representing the results of the last run Contact Check measurement"""

        # Parse the query string into a list of individual result values
        result_values = self.query('CCHECK:RESULT?').rsplit(',')

        # Remove the setup result values
        del result_values[0:11]

        # Split the list of values into a list of subsets with length 7, representing the measurements per contact pair
        measurements_list = [result_values[i:i+7] for i in range(0, len(result_values), 7)]

        # Pop off the remaining three values (packed in one list) that represent the overload status values
        overload_status_list = measurements_list.pop()

        # Initialize the dictionary to be empty
        results = {}

        # Number of groupings (length of the list) correlates to the number of contact pairs. 4-Van der Pauw, 6-Hall Bar
        contact_pairs = ['contact_pair_A_', 'contact_pair_B_', 'contact_pair_C_', 'contact_pair_D_']
        if len(measurements_list) == 6:
            contact_pairs.extend(['contact_pair_E_', 'contact_pair_F_'])

        # Loop through each contact pair to add every measurement and its corresponding value to the results dictionary
        for pair, pair_measurements in zip(contact_pairs, measurements_list):
            pair_results = {
                pair + 'offset': float(pair_measurements[0]),
                pair + 'slope': float(pair_measurements[1]),
                pair + 'r_squared': float(pair_measurements[2]),
                pair + 'r_squared_passed': bool(int(pair_measurements[3])),
                pair + 'in_compliance': bool(int(pair_measurements[4])),
                pair + 'voltage_overload': bool(int(pair_measurements[5])),
                pair + 'current_overload': bool(int(pair_measurements[6]))
            }
            results.update(pair_results)

        # Add the overload status information to the results dictionary
        overload_status_results = {
            'in_compliance': bool(int(overload_status_list[0])),
            'voltage_overload': bool(int(overload_status_list[1])),
            'current_overload': bool(int(overload_status_list[2]))
        }
        results.update(overload_status_results)

        return results

    def get_fasthall_setup_results(self):
        """Returns an object representing the setup results of the last run FastHall measurement"""

        # Parse the query string into a list of individual result values
        results = self.query('FASTHALL:RESULT?').rsplit(',')

        # Generate a FastHall settings object using the setup result values as the initialization parameters
        settings = FastHallManualParameters(excitation_type=results[2],
                                            excitation_value=float(results[3]),
                                            excitation_range=float(results[4]),
                                            excitation_measurement_range=float(results[5]),
                                            measurement_range=float(results[6]),
                                            compliance_limit=float(results[7]),
                                            max_samples=int(results[8]),
                                            user_defined_field=float(results[9]),
                                            resistivity=float(results[10]),
                                            blanking_time=float(results[11]),
                                            averaging_samples=int(results[12]),
                                            sample_thickness=float(results[13]),
                                            min_hall_voltage_snr=float(results[14]))
        return settings

    def get_fasthall_measurement_results(self):
        """Returns a dictionary representing the results of the last run FastHall measurement"""

        # Parse the query string into a list of individual result values
        result_values = self.query('FASTHALL:RESULT?').rsplit(',')

        # Generate a dictionary by assigning specific result values to the corresponding result names
        results = {'hall_voltage_average': float(result_values[15]),
                   'hall_voltage_standard_error': float(result_values[16]),
                   'hall_voltage_snr': float(result_values[17]),
                   'carrier_type': result_values[18],
                   'P_type_count': int(result_values[19]),
                   'N_type_count': int(result_values[20]),
                   'carrier_concentration_average': float(result_values[21]),
                   'sheet_carrier_concentration_average': float(result_values[22]),
                   'carrier_concentration_standard_error': float(result_values[23]),
                   'sheet_carrier_concentration_standard_error': float(result_values[24]),
                   'hall_coefficient_average': float(result_values[25]),
                   'sheet_hall_coefficient_average':  float(result_values[26]),
                   'hall_coefficient_standard_error': float(result_values[27]),
                   'sheet_hall_coefficient_standard_error': float(result_values[28]),
                   'mobility_average': float(result_values[29]),
                   'mobility_standard_error': float(result_values[30]),
                   'in_compliance': bool(int(result_values[31])),
                   'voltage_overload': bool(int(result_values[32])),
                   'current_overload': bool(int(result_values[33]))}
        return results

    def get_four_wire_setup_results(self):
        """Returns an object representing the setup results of the last run Four Wire measurement"""

        # Parse the query string into a list of individual result values
        results = self.query('FWIRE:RESULT?').rsplit(',')

        # Generate a Four Wire settings object using the setup result values as the initialization parameters
        settings = FourWireParameters(contact_point1=int(results[2]),
                                      contact_point2=int(results[3]),
                                      contact_point3=int(results[4]),
                                      contact_point4=int(results[5]),
                                      excitation_type=results[6],
                                      excitation_value=float(results[7]),
                                      excitation_range=float(results[8]),
                                      excitation_measurement_range=float(results[9]),
                                      measurement_range=float(results[10]),
                                      compliance_limit=float(results[11]),
                                      blanking_time=float(results[12]),
                                      max_samples=int(results[13]),
                                      min_snr=float(results[14]),
                                      excitation_reversal=bool(int(results[15])))
        return settings

    def get_four_wire_measurement_results(self):
        """Returns a dictionary representing the results of the last run Four Wire measurement"""

        # Parse the query string into a list of individual result values
        result_values = self.query('FWIRE:RESULT?').rsplit(',')

        # Generate a dictionary by assigning specific result values to the corresponding result names
        results = {'resistance_average': float(result_values[16]),
                   'resistance_standard_error': float(result_values[17]),
                   'voltage_average': float(result_values[18]),
                   'voltage_standard_error': float(result_values[19]),
                   'current_average': float(result_values[20]),
                   'current_standard_error': float(result_values[21]),
                   'in_compliance': bool(int(result_values[22])),
                   'voltage_overload': bool(int(result_values[23])),
                   'current_overload': bool(int(result_values[24]))}
        return results

    def get_dc_hall_setup_results(self):
        """Returns a dictionary representing the setup results of the last run Hall measurement"""

        # Parse the query string into a list of individual result values
        results = self.query('HALL:DC:RESULT?').rsplit(',')

        # Generate a DC Hall settings object using the setup result values as the initialization parameters
        settings = DCHallParameters(excitation_type=results[2],
                                    excitation_value=float(results[3]),
                                    excitation_range=float(results[4]),
                                    excitation_measurement_range=float(results[5]),
                                    measurement_range=float(results[6]),
                                    compliance_limit=float(results[7]),
                                    averaging_samples=int(results[8]),
                                    user_defined_field=float(results[9]),
                                    resistivity=float(results[10]),
                                    blanking_time=float(results[11]),
                                    sample_thickness=float(results[12]))
        return settings

    def get_dc_hall_measurement_results(self):
        """Returns a dictionary representing the results of the last run Hall measurement"""

        # Parse the query string into a list of individual result values
        result_values = self.query('HALL:DC:RESULT?').rsplit(',')

        # Generate a dictionary by assigning specific result values to the corresponding result names
        results = {'hall_voltage_average': float(result_values[13]),
                   'hall_voltage_standard_error': float(result_values[14]),
                   'hall_coefficient_average': float(result_values[15]),
                   'sheet_hall_coefficient_average': float(result_values[16]),
                   'hall_coefficient_standard_error': float(result_values[17]),
                   'sheet_hall_coefficient_standard_error': float(result_values[18]),
                   'carrier_type': result_values[19],
                   'P_type_count': int(result_values[20]),
                   'N_type_count': int(result_values[21]),
                   'carrier_concentration_average': float(result_values[22]),
                   'sheet_carrier_concentration_average': float(result_values[23]),
                   'carrier_concentration_standard_error': float(result_values[24]),
                   'standard_carrier_concentration_standard_error': float(result_values[25]),
                   'mobility_average': float(result_values[26]),
                   'mobility_standard_error': float(result_values[27]),
                   'in_compliance': bool(int(result_values[28])),
                   'voltage_overload': bool(int(result_values[29])),
                   'current_overload': bool(int(result_values[30]))
                   }
        return results

    def get_resistivity_setup_results(self):
        """Returns an object representing the setup results of the last run Resistivity measurement"""

        # Parse the query string into a list of individual result values
        results = self.query('RESISTIVITY:RESULT?').rsplit(',')

        # Generate a Resistivity settings object using the setup result values as the initialization parameters
        settings = ResistivityManualParameters(excitation_type=results[2],
                                               excitation_value=float(results[3]),
                                               excitation_range=float(results[4]),
                                               excitation_measurement_range=float(results[5]),
                                               measurement_range=float(results[6]),
                                               compliance_limit=float(results[7]),
                                               max_samples=int(results[8]),
                                               blanking_time=float(results[9]),
                                               sample_thickness=float(results[10]),
                                               min_snr=float(results[11]))
        return settings

    def get_resistivity_measurement_results(self):
        """Returns a dictionary representing the results of the last run Resistivity measurement"""

        # Parse the query string into a list of individual result values
        result_values = self.query('RESISTIVITY:RESULT?').rsplit(',')

        # Generate a dictionary by assigning specific result values to the corresponding result names
        results = {
            'resistivity_average': float(result_values[12]),
            'sheet_resistivity_average': float(result_values[13]),
            'resistivity_standard_error': float(result_values[14]),
            'sheet_resistivity_standard_error': float(result_values[15]),
            'resistivity_snr': float(result_values[16]),
            'geometry_A_resistivity_average': float(result_values[17]),
            'geometry_A_sheet_resistivity_average': float(result_values[18]),
            'geometry_A_resistivity_standard_error': float(result_values[19]),
            'geometry_A_sheet_resistivity_standard_error': float(result_values[20]),
            'geometry_A_F_value': float(result_values[21]),
            'geometry_B_resistivity_average': float(result_values[22]),
            'geometry_B_sheet_resistivity_average': float(result_values[23]),
            'geometry_B_resistivity_standard_error': float(result_values[24]),
            'geometry_B_sheet_resistivity_standard_error': float(result_values[25]),
            'geometry_B_F_value': float(result_values[26]),
            'in_compliance': bool(int(result_values[27])),
            'voltage_overload': bool(int(result_values[28])),
            'current_overload': bool(int(result_values[29]))
        }
        return results

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
