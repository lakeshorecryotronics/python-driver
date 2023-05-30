"""Implements functionality unique to the Lake Shore F41 and F71 Teslameters."""

from collections import namedtuple
from datetime import datetime

import warnings
import iso8601

from .requires_firmware_version import requires_firmware_version
from .xip_instrument import XIPInstrument, RegisterBase, StatusByteRegister, StandardEventRegister

# A namedtuple object representing a Teslameter measurement buffer data point.
DataPoint = namedtuple("DataPoint", ['elapsed_time', 'time_stamp',
                                     'magnitude', 'x', 'y', 'z',
                                     'field_control_set_point',
                                     'input_state'])


class TeslameterOperationRegister(RegisterBase):
    """Class object representing the operation status register."""

    bit_names = [
        "no_probe",
        "overload",
        "ranging",
        "",
        "",
        "ramp_done",
        "no_data_on_breakout_adapter"
    ]

    def __init__(self,
                 no_probe,
                 overload,
                 ranging,
                 ramp_done,
                 no_data_on_breakout_adapter):
        self.no_probe = no_probe
        self.overload = overload
        self.ranging = ranging
        self.ramp_done = ramp_done
        self.no_data_on_breakout_adapter = no_data_on_breakout_adapter


class TeslameterQuestionableRegister(RegisterBase):
    """Class object representing the questionable status register."""

    bit_names = [
        "x_axis_sensor_error",
        "y_axis_sensor_error",
        "z_axis_sensor_error",
        "probe_eeprom_read_error",
        "temperature_compensation_error",
        "invalid_probe",
        "field_control_slew_rate_limit",
        "field_control_at_voltage_limit",
        "calibration_error",
        "heartbeat_error"
    ]

    def __init__(self,
                 x_axis_sensor_error,
                 y_axis_sensor_error,
                 z_axis_sensor_error,
                 probe_eeprom_read_error,
                 temperature_compensation_error,
                 invalid_probe,
                 field_control_slew_rate_limit,
                 field_control_at_voltage_limit,
                 calibration_error,
                 heartbeat_error):
        self.x_axis_sensor_error = x_axis_sensor_error
        self.y_axis_sensor_error = y_axis_sensor_error
        self.z_axis_sensor_error = z_axis_sensor_error
        self.probe_eeprom_read_error = probe_eeprom_read_error
        self.temperature_compensation_error = temperature_compensation_error
        self.invalid_probe = invalid_probe
        self.field_control_slew_rate_limit = field_control_slew_rate_limit
        self.field_control_at_voltage_limit = field_control_at_voltage_limit
        self.calibration_error = calibration_error
        self.heartbeat_error = heartbeat_error


class Teslameter(XIPInstrument):
    """A class object representing a Lake Shore F41 or F71 Teslameter."""

    vid_pid = [(0x1FB9, 0x0405), (0x1FB9, 0x0406)]

    def __init__(self,
                 serial_number=None,
                 com_port=None,
                 baud_rate=115200,
                 flow_control=True,
                 timeout=2.0,
                 ip_address=None,
                 tcp_port=7777,
                 **kwargs):

        # Call the parent init, then fill in values specific to the Teslameter
        XIPInstrument.__init__(self, serial_number, com_port, baud_rate, flow_control, timeout, ip_address, tcp_port,
                               **kwargs)
        self.status_byte_register = StatusByteRegister
        self.standard_event_register = StandardEventRegister
        self.operation_register = TeslameterOperationRegister
        self.questionable_register = TeslameterQuestionableRegister

    @requires_firmware_version('1.1.2018091003')
    def stream_buffered_data(self, length_of_time_in_seconds, sample_rate_in_ms):
        """Yield a generator object for the buffered field data.

            Useful for getting the data in real time when doing a lengthy acquisition.

            Args:
                length_of_time_in_seconds (float):
                    The period of time over which to stream the data.
                sample_rate_in_ms (int):
                    The averaging window (sampling period) of the instrument.

            Returns:
               A generator object that returns the data as datapoint tuples.
        """

        # Set the sample rate
        self.command("SENSE:AVERAGE:COUNT " + str(sample_rate_in_ms / 10))

        # Round the length of time to the nearest 10 milliseconds.
        length_of_time_in_seconds = round(length_of_time_in_seconds, 2)

        # Calculate the total number of samples
        total_number_of_samples = int(round(length_of_time_in_seconds * 1000 / sample_rate_in_ms, 0))
        number_of_samples = 0

        # Clear the buffer by querying it
        self.query('FETC:BUFF:DC?', check_errors=False)
        while number_of_samples < total_number_of_samples:
            # Query the buffer.
            response = self.query('FETC:BUFF:DC?', check_errors=False).strip('"')

            # Ignore the response if it contains no data
            if ';' in response:
                # Split apart the response into single data points.
                data_points = response.rstrip(';').split(';')

                for point in data_points:
                    # Split the data point along the delimiter.
                    point_data = point.split(',')

                    # Convert the returned values from strings to appropriate types
                    for count, _ in enumerate(point_data):
                        if count == 0:
                            point_data[count] = iso8601.parse_date(point_data[count])
                        elif count == len(point_data) - 1:
                            point_data[count] = int(point_data[count])
                        else:
                            point_data[count] = float(point_data[count])

                    # If the instrument does not have a field control option, insert zero as the control set point.
                    if len(point_data) == 6:
                        input_state = point_data.pop()
                        point_data.append(0.0)
                        point_data.append(input_state)

                    # Count how many samples have been collected and calculate the elapsed time.
                    number_of_samples += 1
                    elapsed_time_in_seconds = sample_rate_in_ms * number_of_samples / 1000

                    # If we have exceeded the requested number of samples, end the stream.
                    if number_of_samples > total_number_of_samples:
                        break

                    # Unpack the parsed point into a namedtuple and append it to the list
                    new_point = DataPoint(elapsed_time_in_seconds, *point_data)

                    yield new_point

    @requires_firmware_version('1.1.2018091003')
    def get_buffered_data_points(self, length_of_time_in_seconds, sample_rate_in_ms):
        """Returns a list of named tuples that contain the buffered data.

            Args:
                length_of_time_in_seconds (float):
                    The period of time over which to collect the data.
                sample_rate_in_ms (int):
                    The averaging window (sampling period) of the instrument.

            Returns:
               The data as a list of datapoint tuples.
        """
        return list(self.stream_buffered_data(length_of_time_in_seconds, sample_rate_in_ms))

    @requires_firmware_version('1.1.2018091003')
    def log_buffered_data_to_file(self, length_of_time_in_seconds, sample_rate_in_ms, file):
        """Creates or appends a CSV file with the buffered data and excel-friendly timestamps.

            Args:
                length_of_time_in_seconds (float):
                    The period of time over which to collect the data.
                sample_rate_in_ms (int):
                    The averaging window (sampling period) of the instrument.
                file (file_object):
                    Field measurement data will be written to this file object in a CSV format.
        """
        # Open the file and write in header information.
        file.write('time elapsed,date,time,' +
                   'magnitude,x,y,z,field control set point,input state\n')

        data_stream_generator = self.stream_buffered_data(length_of_time_in_seconds, sample_rate_in_ms)

        # Parse the datetime value into a separate date and time.
        for point in data_stream_generator:
            column_values = []
            for count, data in enumerate(point):
                if count != 1:
                    column_values.append(str(data))
                else:
                    column_values.append(datetime.strftime(data, '%m/%d/%Y'))
                    column_values.append(datetime.strftime(data, '%H:%M:%S.%f'))

            file.write(','.join(column_values) + '\n')

    def get_dc_field(self):
        """Returns the DC field reading."""
        return float(self.query("FETCH:DC?"))

    def get_dc_field_xyz(self):
        """Returns the DC field reading."""

        response = self.query("FETCH:DC? ALL")

        xyz_values = [float(channel_value) for channel_value in response.split(",")]

        return tuple(xyz_values)

    def get_rms_field(self):
        """Returns the RMS field reading."""
        return float(self.query("FETCH:RMS?"))

    def get_rms_field_xyz(self):
        """Returns the RMS field reading."""

        response = self.query("FETCH:RMS? ALL")

        xyz_values = [float(channel_value) for channel_value in response.split(",")]

        return tuple(xyz_values)

    def get_frequency(self):
        """Returns the field frequency reading."""
        return float(self.query("FETCH:FREQ?"))

    def get_max_min(self):
        """Returns the maximum and minimum field readings respectively."""

        response = self.query("FETCH:MAX?", "FETCH:MIN?")
        separated_response = response.split(";")

        return float(separated_response[0]), float(separated_response[1])

    def get_max_min_peaks(self):
        """Returns the maximum and minimum peak field readings respectively."""

        response = self.query("FETCH:MAXP?", "FETCH:MINP?")
        separated_response = response.split(";")

        return float(separated_response[0]), float(separated_response[1])

    def reset_max_min(self):
        """Resets the maximum and minimum field readings to the present field reading."""
        self.command("SENS:MRESET")

    def get_temperature(self):
        """Returns the temperature reading."""
        return float(self.query("FETCH:TEMP?"))

    def get_probe_information(self):
        """Returns a dictionary of probe data."""
        probe_data = {"model_number": self.query("PROBE:MODEL?"),
                      "serial_number": self.query("PROBE:SNUM?"),
                      "probe_type": self.query("PROBE:PTYPE?"),
                      "sensor_type": self.query("PROBE:STYPE?"),
                      "sensor_orientation": self.query("PROBE:SOR?"),
                      "number_of_axes": self.query("PROBE:AXES?"),
                      "calibration_date": self.query("PROBE:CALDATE?")}

        return probe_data

    def get_relative_field(self):
        """Returns the relative field value."""
        return float(self.query("FETCH:RELATIVE?"))

    def tare_relative_field(self):
        """Copies the current field reading to the relative baseline value."""
        self.command("SENS:RELATIVE:TARE")

    def get_relative_field_baseline(self):
        """Returns the relative field baseline value."""
        return float(self.query("SENS:RELATIVE:BASELINE?"))

    def set_relative_field_baseline(self, baseline_field):
        """Configures the relative baseline value.

            Args:
                baseline_field (float):
                    A field units value that will act as the zero field for the relative measurement.
        """
        self.command(f"SENS:RELATIVE:BASELINE {str(baseline_field)}")

    def configure_field_measurement_setup(self, mode="DC", autorange=True, expected_field=None, averaging_samples=20):
        """Configures the field measurement settings.

            Args:
                mode (str):
                    Modes are as follows:
                    "DC",
                    "AC" (0.1 - 500 Hz), and
                    "HIFR" (50 Hz - 100 kHz).
                autorange (bool):
                    Chooses whether the instrument automatically selects the best range for the measured value.
                expected_field (float):
                    When autorange is False, the expected_field is the largest field expected to be measured.
                    It sets the lowest instrument field range capable of measuring the value.
                averaging_samples (int):
                    The number of field samples to average. Each sample is 10 milliseconds of field information.

        """
        self.command(f"SENS:MODE {mode}")
        self.command(f"SENS:RANGE:AUTO {str(int(autorange))}")
        if expected_field is not None:
            self.command(f"SENS:RANGE {str(expected_field)}")
        self.command(f"SENS:AVERAGE:COUNT {str(averaging_samples)}")

    def get_field_measurement_setup(self):
        """Returns the mode, autoranging state, range, and number of averaging samples as a dictionary."""
        measurement_setup = {"mode": self.query("SENS:MODE?"),
                             "autorange": bool(int(self.query("SENS:RANGE:AUTO?"))),
                             "expected_field": float(self.query("SENS:RANGE?")),
                             "averaging_samples": int(self.query("SENS:AVERAGE:COUNT?"))}

        return measurement_setup

    def configure_temperature_compensation(self, temperature_source="PROBE", manual_temperature=None):
        """Configures how temperature compensation is applied to the field readings.

            Args:
                temperature_source (str):
                    Determines where the temperature measurement is drawn from. Options are:
                    "PROBE" (Compensation is based on measurement of a thermistor in the probe),
                    "MTEM" (Compensation is based on a manual temperature value provided by the user),
                    "NONE" (Temperature compensation is not applied).
                manual_temperature (float):
                    Sets the temperature provided by the user for MTEMP (manual temperature) source in Celsius.

        """
        self.command(f"SENS:TCOM:TSOURCE {temperature_source}")
        if manual_temperature is not None:
            self.command(f"SENS:TCOM:MTEM {str(manual_temperature)}")

    def get_temperature_compensation_source(self):
        """Returns the source of temperature measurement for field compensation."""
        return self.query("SENS:TCOM:TSOURCE?")

    def get_temperature_compensation_manual_temp(self):
        """Returns the manual temperature setting value in Celsius."""
        return float(self.query("SENS:TCOM:MTEM?"))

    def configure_field_units(self, units="TESLA"):
        """Configures the field measurement units of the instrument.

            Args:
                units (str):
                    A unit of magnetic field. Options are:
                    "TESLA", or
                    "GAUSS".

        """
        self.command(f"UNIT:FIELD {units}")

    def get_field_units(self):
        """Returns the magnetic field units of the instrument."""
        return self.query("UNIT:FIELD?")

    @requires_firmware_version("1.1.2018091003")
    def configure_field_control_limits(self, voltage_limit=10.0, slew_rate_limit=10.0):
        """Configures the limits of the field control output.

            Args:
                voltage_limit (float):
                    The maximum voltage permitted at the field control output. Must be between 0 and 10V.
                slew_rate_limit (float):
                    The maximum rate of change of the field control output voltage in volts per second.

        """
        self.command(f"SOURCE:FIELD:VLIMIT {str(voltage_limit)}")
        self.command(f"SOURCE:FIELD:SLEW {str(slew_rate_limit)}")

    @requires_firmware_version("1.1.2018091003")
    def get_field_control_limits(self):
        """Returns the field control output voltage limit and slew rate limit."""
        limits = {"voltage_limit": float(self.query("SOURCE:FIELD:VLIMIT?")),
                  "slew_rate_limit": float(self.query("SOURCE:FIELD:SLEW?"))}

        return limits

    @requires_firmware_version("1.1.2018091003")
    def configure_field_control_output_mode(self, mode="CLLOOP", output_enabled=True):
        """Configure the field control mode and state.

            Args:
                mode (str):
                    Determines whether the field control is in open or closed loop mode. Options:
                    "CLLOOP" (closed loop control), or
                    "OPLOOP" (open loop control, voltage output).
                output_enabled (bool):
                    Turn the field control voltage output on or off.

        """

        self.command(f"SOURCE:FIELD:MODE {mode}")
        self.command(f"SOURCE:FIELD:STATE {str(int(output_enabled))}")

    @requires_firmware_version("1.1.2018091003")
    def get_field_control_output_mode(self):
        """Returns the mode and state of the field control output."""
        output_state = {"mode": self.query("SOURCE:FIELD:MODE?"),
                        "output_enabled": bool(int(self.query("SOURCE:FIELD:STATE?")))}

        return output_state

    @requires_firmware_version("1.1.2018091003")
    def configure_field_control_pid(self, gain=None, integral=None, ramp_rate=None):
        """Configures the closed loop control parameters of the field control output.

            Args:
                gain (float):
                    Also known as P or Proportional in PID control.
                    This controls how strongly the control output reacts to the present error.
                    Note that the integral value is multiplied by the gain value.
                integral (float):
                    Also known as I or Integral in PID control.
                    This controls how strongly the control output reacts to the past error *history*.
                ramp_rate (float):
                    This value controls how quickly the present field set-point will transition to a new set-point.
                    The ramp rate is configured in field units per second.

        """
        if gain is not None:
            self.command(f"SOURCE:FIELD:CLL:GAIN {str(gain)}")
        if integral is not None:
            self.command(f"SOURCE:FIELD:CLL:INTEGRAL {str(integral)}")
        if ramp_rate is not None:
            self.command(f"SOURCE:FIELD:CLL:RAMP {str(ramp_rate)}")

    @requires_firmware_version("1.1.2018091003")
    def get_field_control_pid(self):
        """Returns the gain, integral, and ramp rate."""
        pid = {"gain": float(self.query("SOURCE:FIELD:CLL:GAIN?")),
               "integral": float(self.query("SOURCE:FIELD:CLL:INTEGRAL?")),
               "ramp_rate": float(self.query("SOURCE:FIELD:CLL:RAMPRATE?"))}

        return pid

    @requires_firmware_version("1.1.2018091003")
    def set_field_control_setpoint(self, setpoint):
        """Sets the field control setpoint value in field units."""
        self.command(f"SOURCE:FIELD:CLL:SETPOINT {str(setpoint)}")

    @requires_firmware_version("1.1.2018091003")
    def get_field_control_setpoint(self):
        """Returns the field control setpoint."""
        return float(self.query("SOURCE:FIELD:CLL:SETPOINT?"))

    @requires_firmware_version("1.1.2018091003")
    def set_field_control_open_loop_voltage(self, output_voltage):
        """Sets the field control open loop voltage."""
        self.command(f"SOURCE:FIELD:OPL:VOLTAGE {str(output_voltage)}")

    @requires_firmware_version("1.1.2018091003")
    def get_field_control_open_loop_voltage(self):
        """Returns the field control open loop voltage."""
        return float(self.query("SOURCE:FIELD:OPL:VOLTAGE?"))

    @requires_firmware_version("1.4.2019061411")
    def set_analog_output(self, analog_output_mode):
        """Configures what signal is provided by the analog output BNC."""
        warnings.warn(
            "set_analog_output will be depreciated in a future version, use set_analog_output_signal instead",
            PendingDeprecationWarning
        )
        self.command(f"SOURCE:AOUT {analog_output_mode}")

    @requires_firmware_version("1.6.2019092002")
    def set_analog_output_signal(self, analog_output_mode):
        """Configures what signal is provided by the analog output BNC.

            Args:
                analog_output_mode (str):
                    Configures what signal is provided by the analog output BNC. Options:
                    "OFF" (output off),
                    "XRAW" (raw amplified X channel Hall voltage),
                    "YRAW" (raw amplified Y channel Hall voltage),
                    "ZRAW" (raw amplified Z channel Hall voltage),
                    "XCOR" (Corrrected X channel field measurement),
                    "YCOR" (Corrected Y channel field measurement),
                    "ZCOR" (Corrected Z channel field measurement), or
                    "MCOR" (Corrected magnitude field measurement)

        """
        self.command(f"SOURCE:AOUT {analog_output_mode}")

    @requires_firmware_version("1.6.2019092002")
    def configure_corrected_analog_output_scaling(self, scale_factor, baseline):
        """Configures the conversion between field reading and analog output voltage.

            Args:
                scale_factor (float):
                    Scale factor in volts per unit field.
                baseline (float):
                    The field value at which the analog output voltage is zero.

        """
        self.command(f"SOURCE:AOUT:SFACTOR {str(scale_factor)}", f"SOURCE:AOUT:BASELINE {str(baseline)}")

    @requires_firmware_version("1.6.2019092002")
    def get_corrected_analog_output_scaling(self):
        """Returns the scale factor and baseline of the corrected analog out."""
        return float(self.query("SOURCE:AOUT:SFACTOR?")), float(self.query("SOURCE:AOUT:BASELINE?"))

    def get_analog_output(self):
        """Returns what signal is being provided by the analog output."""
        warnings.warn(
            "get_analog_output will be depreciated in a future version, use get_analog_output_signal instead",
            PendingDeprecationWarning
        )
        return self.query("SOURCE:AOUT?")

    def get_analog_output_signal(self):
        """Returns what signal is being provided by the analog output."""
        return self.query("SOURCE:AOUT?")

    @requires_firmware_version("1.6.2019092002")
    def enable_high_frequency_filters(self):
        """Applies filtering to the high frequency RMS measurements."""
        self.command("SENSE:FILT 1")

    @requires_firmware_version("1.6.2019092002")
    def disable_high_frequency_filters(self):
        """Turns off filtering of the high frequency mode measurements."""
        self.command("SENSE:FILT 0")

    @requires_firmware_version("1.6.2019092002")
    def set_frequency_filter_type(self, filter_type):
        """Configures which filter is applied to the high frequency measurements.

            Args:
                filter_type (str):
                    Options: "LPASS" (low pass filter), "HPASS" (high pass filter), or "BPASS" (band pass filter).
        """
        self.command(f"SENSE:FILT:TYPE {str(filter_type)}")

    @requires_firmware_version("1.6.2019092002")
    def get_frequency_filter_type(self):
        """Returns the type of filter that is or will be applied to the high frequency measurements."""
        return self.query("SENSE:FILTER:TYPE?")

    @requires_firmware_version("1.6.2019092002")
    def get_low_pass_filter_cutoff(self):
        """Returns the cutoff frequency setting of the low pass filter."""
        return float(self.query("SENSE:FILTER:LPASS:CUTOFF?"))

    @requires_firmware_version("1.6.2019092002")
    def set_low_pass_filter_cutoff(self, cutoff_frequency):
        """Configures the low pass filter cutoff.

            Args:
                cutoff_frequency (float):
                    Options: NONE, F10, F30, F100, F300, F1000, F3000, or F10000
                    F10 = 10 Hz, etc.
        """
        self.command(f"SENSE:FILTER:LPASS:CUTOFF {str(cutoff_frequency)}")

    @requires_firmware_version("1.6.2019092002")
    def get_high_pass_filter_cutoff(self):
        """Returns the cutoff frequency setting of the low pass filter."""
        return float(self.query("SENSE:FILTER:HPASS:CUTOFF?"))

    @requires_firmware_version("1.6.2019092002")
    def set_high_pass_filter_cutoff(self, cutoff_frequency):
        """Configures the high pass filter cutoff.

            Args:
                cutoff_frequency (float):
                    Options: NONE, F10, F30, F100, F300, F1000, F3000, or F10000
                    F10 = 10 Hz, etc.
        """
        self.command(f"SENSE:FILTER:HPASS:CUTOFF {str(cutoff_frequency)}")

    @requires_firmware_version("1.6.2019092002")
    def get_band_pass_filter_center(self):
        """Returns the center of the band pass filter."""
        return float(self.query("SENSE:FILTER:BPASS:CENTER?"))

    @requires_firmware_version("1.6")
    def set_band_pass_filter_center(self, center_frequency):
        """Configures the band pass filter parameters.

            Args:
                center_frequency (float):
                    The frequency at which the gain of the filter is 1.
        """
        self.command(f"SENSE:FILTER:BPASS:CENTER {str(center_frequency)}")

    @requires_firmware_version("1.6.2019092002")
    def enable_qualifier(self):
        """Enables the qualifier."""
        self.command("SENSE:QUALIFIER 1")

    @requires_firmware_version("1.6.2019092002")
    def disable_qualifier(self):
        """Disables the qualifier."""
        self.command("SENSE:QUALIFIER 0")

    @requires_firmware_version("1.6.2019092002")
    def is_qualifier_condition_met(self):
        """Returns whether the qualifier condition is met."""
        return bool(int(self.query("SENSE:QUALIFIER:CONDITION?")))

    @requires_firmware_version("1.6.2019092002")
    def enable_qualifier_latching(self):
        """Enables the qualifier condition latching."""
        self.command("SENSE:QUALIFIER:LATCH 1")

    @requires_firmware_version("1.6.2019092002")
    def disable_qualifier_latching(self):
        """Disables the qualifier condition latching."""
        self.command("SENSE:QUALIFIER:LATCH 0")

    @requires_firmware_version("1.6.2019092002")
    def get_qualifier_latching_setting(self):
        """Returns whether the qualifier latches."""
        return self.query("SENSE:QUALIFIER:LATCH?")

    @requires_firmware_version("1.6.2019092002")
    def set_qualifier_latching_setting(self, latching):
        """Sets whether the qualifier latches.

            Args:
                latching (bool):
                    Determines whether the qualifier latches.
        """
        self.command(f"SENSE:QUALIFIER:LATCH {str(latching)}")

    @requires_firmware_version("1.6.2019092002")
    def reset_qualifier_latch(self):
        """Resets the condition status of the qualifier."""
        self.command("SENSE:QUALIFIER:LRESET")

    @requires_firmware_version("1.6.2019092002")
    def get_qualifier_configuration(self):
        """Returns the threshold mode and field threshold values."""
        response = self.query("SENSE:QUALIFIER:THRESHOLD?")
        elements = response.split(',')
        mode = elements[0]
        threshold_field_low = float(elements[1])
        threshold = (mode, threshold_field_low)
        if len(elements) == 3:
            threshold_field_upper = float(elements[2])
            threshold = (mode, threshold_field_low, threshold_field_upper)
        return threshold

    @requires_firmware_version("1.6.2019092002")
    def configure_qualifier(self, mode, lower_field, upper_field=None):
        """Sets the threshold condition of the qualifier.

            Args:
                mode (str):
                    The type of threshold condition used by the qualifier.
                    Options: "OVER", "UNDER", "BETWEEN", "OUTSIDE", "ABSBETWEEN", or "ABSOUTSIDE".
                lower_field (float):
                    The lower field value threshold used by the qualifier.
                upper_field (float):
                    The upper field value threshold used by the qualifier. Not used for OVER or UNDER.
        """
        if upper_field is None:
            self.command(f"SENSE:QUALIFIER:THRESHOLD {mode},{str(lower_field)}")
        else:
            self.command(f"SENSE:QUALIFIER:THRESHOLD {mode},{str(lower_field)},{str(upper_field)}")


# Create an aliases using the product names
F41 = Teslameter
F71 = Teslameter
