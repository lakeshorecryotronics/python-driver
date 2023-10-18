"""Implements a parent class for temperature controllers that contains shared methods between similar instruments."""

import serial
from .generic_instrument import GenericInstrument, InstrumentException, RegisterBase
from .temperature_controllers_enums import TemperatureControllerEnums


class AlarmSettings:
    """Class used to disable or configure an alarm in conjunction with the set/get_alarm_parameters() method."""

    def __init__(self, high_value, low_value, deadband, latch_enable, audible=None, visible=None, alarm_enable=None):
        """Constructor for AlarmSettings class.

            Args:
                high_value (float):
                    Sets the value the source is checked against to activate the high alarm.
                low_value (float):
                    Sets the value the source is checked against to activate low alarm.
                deadband (float):
                    Sets the value that the source must change outside an alarm.
                    condition to deactivate an unlatched alarm.
                latch_enable (bool):
                    Specifies a latched alarm.
                    False = off, True = on
                audible (bool):
                    Specifies if the internal speaker will beep when an alarm condition occurs.
                    False = off, True = on
                visible (bool):
                    Specifies if the Alarm LED on the instrument front panel will blink when an alarm condition occurs.
                    False = off, True = on
        """
        self.high_value = high_value
        self.low_value = low_value
        self.deadband = deadband
        self.latch_enable = latch_enable
        self.audible = audible
        self.visible = visible
        self.alarm_enable = alarm_enable


class CurveHeader:
    """A class to configure the temperature sensor curve header parameters."""

    def __init__(self, curve_name, serial_number, curve_data_format, temperature_limit, coefficient):
        """Constructor for CurveHeader class.

            Args:
                curve_name (str):
                    Specifies curve name (limit of 15 characters).
                serial_number (str):
                    Specifies curve serial number (limit of 10 characters).
                curve_data_format (IntEnum):
                    Member of the instrument's CurveFormat IntEnum class.
                    Specifies the curve data format.
                temperature_limit (float):
                    Specifies the curve temperature limit in Kelvin.
                coefficient (IntEnum):
                    Member of instrument's CurveTemperatureCoefficient IntEnum class.
                    Specifies the curve temperature coefficient.

        """
        self.curve_name = curve_name
        self.serial_number = serial_number
        self.curve_data_format = curve_data_format
        self.temperature_limit = temperature_limit
        self.coefficient = coefficient


class StandardEventRegister(RegisterBase):
    """Class object representing the standard event register."""

    bit_names = [
        "operation_complete",
        "",
        "query_error",
        "",
        "execution_error",
        "command_error",
        "",
        "power_on"
    ]

    def __init__(self,
                 operation_complete,
                 query_error,
                 execution_error,
                 command_error,
                 power_on):
        self.operation_complete = operation_complete
        self.query_error = query_error
        self.execution_error = execution_error
        self.command_error = command_error
        self.power_on = power_on


class OperationEvent(RegisterBase):
    """Class object representing the status byte register LSB to MSB."""

    bit_names = [
        "alarm",
        "sensor_overload",
        "loop_2_ramp_done",
        "loop_1_ramp_done",
        "new_sensor_reading",
        "autotune_process_completed",
        "calibration_error",
        "processor_communication_error"
    ]

    def __init__(self,
                 alarm,
                 sensor_overload,
                 loop_2_ramp_done,
                 loop_1_ramp_done,
                 new_sensor_reading,
                 autotune_process_completed,
                 calibration_error,
                 processor_communication_error):
        self.alarm = alarm
        self.sensor_overload = sensor_overload
        self.loop_2_ramp_done = loop_2_ramp_done
        self.loop_1_ramp_done = loop_1_ramp_done
        self.new_sensor_reading = new_sensor_reading
        self.autotune_process_completed = autotune_process_completed
        self.calibration_error = calibration_error
        self.processor_communication_error = processor_communication_error


class TemperatureController(GenericInstrument, TemperatureControllerEnums):
    """Base class for all temperature controller instruments."""

    # Initiate instrument specific registers
    status_byte_register = None
    service_request_enable = None

    def __init__(self, serial_number, com_port, baud_rate, timeout, ip_address, tcp_port=None, **kwargs):

        # Call the parent init, then fill in values specific to temperature controllers
        GenericInstrument.__init__(self, serial_number, com_port, baud_rate, 7, 1, serial.PARITY_ODD,
                                   False, False, timeout, ip_address, tcp_port, **kwargs)

    @staticmethod
    def _error_check(error_code):
        event_register = StandardEventRegister.from_integer(error_code)
        if event_register.query_error:
            raise InstrumentException('Query Error')
        if event_register.command_error:
            raise InstrumentException('Command Error: Invalid Command or Query')
        if event_register.execution_error:
            raise InstrumentException('Execution Error: Instrument not able to execute command or query.')

    def command(self, *commands, check_errors=True):
        """Sends an SCPI command or multiple commands to the instrument.

            Args:
                commands (str):
                    A serial command.

            Kwargs:
                check_errors (bool):
                    Chooses whether to check for and raise errors after sending a command. True by default.

        """

        # Group all commands and queries a single string with SCPI delimiters.
        command_string = ";:".join(commands)

        if check_errors:
            self.query(command_string)
        else:
            command_string += ";*OPC?"
            self.query(command_string, check_errors=False)

    def query(self, *queries, check_errors=True):
        """Send a query to the instrument and return the response.

            Args:
                queries (str):
                    A serial query ending in a question mark.

            Returns:
                The instrument query response as a string.

        """

        # Group all commands and queries a single string with SCPI delimiters.
        query_string = ";:".join(queries)

        # Append the query with an additional error buffer query.
        if check_errors:
            query_string += ";*ESR?"

        response = GenericInstrument.query(self, query_string)

        if check_errors:
            response_list = response.split(';')
            error_code = response_list.pop()
            self._error_check(error_code)
            response = ';'.join(response_list)

        return response

    def get_standard_event_enable_mask(self):
        """Returns the names of the standard event enable register bits and their values.

            These values determine which bits propagate to the standard event register.
        """

        response = self.query("*ESE?", check_errors=False)
        return StandardEventRegister.from_integer(response)

    def set_standard_event_enable_mask(self, register_mask):
        """Configures values of the standard event enable register bits.

            These values determine which bits propagate to the standard event register.

            Args:
                register_mask (StandardEventRegister):
                    A StandardEventRegister class object with all bits set to a value.

        """
        integer_representation = register_mask.to_integer()
        self.command(f"*ESE {str(integer_representation)}")

    def clear_interface_command(self):
        """Clears the bits in the SBR, SESR, OER, and terminates all operations.

            Clears the bits in the Status Byte Register, Standard Event Status Register, and Operation Event Register.
            Terminates all pending operations. Clears the interface, but not the controller."""

        self.command("*CLS")

    def reset_instrument(self):
        """Sets controller parameters to power-up settings."""

        self.command("*RST")

    def set_service_request(self, register_mask):
        """Manually enable/disable the mask of the corresponding status-flag bit in the status byte register.

            Args:
                register_mask (service_request_enable):
                    A service_request_enable class object with all bits configured.

        """
        integer_representation = register_mask.to_integer()
        self.command(f"*SRE {str(integer_representation)}")

    def get_service_request(self):
        """Returns the status byte register bits and their values as a class instance."""

        response = self.query("*SRE?")
        return self.service_request_enable.from_integer(response)

    def get_status_byte(self):
        """Returns the status flag bits as a class instance without resetting the register."""

        response = self.query("*STB?")
        return self.status_byte_register.from_integer(response)

    def get_self_test(self):
        """Instrument self test result completed at power up.

            Returns:
                (bool):
                    True = errors found.
                    False = no errors found.

        """
        return bool(int(self.query("*TST?")))

    def get_kelvin_reading(self, input_channel):
        """Returns the temperature value in kelvin of the given channel.

            Args:
                input_channel:
                    Selects the channel to retrieve measurement.

        """
        return float(self.query(f"KRDG? {input_channel}"))

    def get_sensor_reading(self, input_channel):
        """Returns the sensor reading in the sensor's units.

            Returns:
                reading (float):
                    The raw sensor reading in the units of the connected sensor.

        """
        return float(self.query(f"SRDG? {input_channel}"))

    def set_sensor_name(self, input_channel, sensor_name):
        """Sets a given name to a sensor on the specified channel.

            Args:
                input_channel (str or int):
                    Specifies which input_channel channel to read from.
                sensor_name(str):
                    Name user wants to give to the sensor on the specified channel.

        """
        self.command(f"INNAME {input_channel},\"{sensor_name}\"")

    def get_sensor_name(self, input_channel):
        """Returns the name of the sensor on the specified channel.

            Args:
                input_channel (str or int):
                    Specifies which input_channel channel to read from.

            Returns:
                name (str):
                    Name associated with the sensor.

        """
        return self.query(f"INNAME? {input_channel}")

    def set_curve_header(self, curve_number, curve_header):
        """Configures the user curve header.

            Args:
                curve_number:
                    Specifies which curve to configure.
                curve_header (CurveHeader):
                    Instrument's CurveHeader class object containing the desired curve information.

        """
        command_string = (f"CRVHDR {curve_number},\"{curve_header.curve_name}\",\"{curve_header.serial_number}\"," +
                        f"{curve_header.curve_data_format},{curve_header.temperature_limit},{curve_header.coefficient}")
        self.command(command_string)

    def get_curve_header(self, curve_number):
        """Returns parameters set on a particular user curve header.

            Args:
                curve_number (int):
                    Specifies a curve to retrieve.

            Returns:
                (CurveHeader):
                    A CurveHeader class object containing the curve information.

        """
        response = self.query(f"CRVHDR? {curve_number}")
        curve_header = response.split(",")
        return CurveHeader(curve_header[0],
                           curve_header[1],
                           self.CurveFormat(int(curve_header[2])),
                           float(curve_header[3]),
                           self.CurveTemperatureCoefficient(int(curve_header[4])))

    def set_curve_data_point(self, curve, index, sensor_units, temperature, curvature=None):
        """Configures a user curve point.

            Args:
                curve (int or str):
                    Specifies which curve to configure.
                index (int):
                    Specifies the points index in the curve.
                sensor_units (float):
                    Specifies sensor units for this point to 6 digits.
                temperature (float):
                    Specifies the corresponding temperature in Kelvin for this point to 6 digits.
                curvature (float):
                    Specify only if the point is part of a cubic spindle curve.
                    The curvature value scale used to calculate spindle coefficients to 6 digits. Optional parameter.

        """
        if curvature:
            command_string = f"CRVPT {curve},{index},{sensor_units},{temperature},{curvature}"
        else:
            command_string = f"CRVPT {curve},{index},{sensor_units},{temperature}"
        self.command(command_string)

    def get_curve_data_point(self, curve, index):
        """Returns a standard or user curve data point.

            Args:
                curve (int):
                    Specifies which curve to query.
                index (int):
                    Specifies the points index in the curve.

            Returns:
                curve_point (tuple):
                    (sensor_units: float, temp_value: float, curvature_value: float (optional)).

        """
        curve_point = self.query(f"CRVPT? {curve},{index}").split(",")
        curve_point = [float(index) for index in curve_point]
        return tuple(curve_point)

    def get_curve(self, curve):
        """Returns a list of all the data points in a particular curve.

            Args:
                curve (int):
                    Specifies which curve to set.

            Returns:
                data_points (list: tuple):
                    A list containing every point in the curve represented as a tuple.
                    (sensor_units: float, temp_value: float, curvature_value: float (optional)).

        """
        true_point_index = 200
        data_points = []
        for i in range(0, 200):
            point = self.get_curve_data_point(curve, i + 1)
            data_points.append(point)
            if point[0] != 0 or point[1] != 0:
                true_point_index = i

        # Remove all extraneous points
        return data_points[:true_point_index]

    def set_curve(self, curve, data_points):
        """Method to define a user curve using a list of data points.

            Args:
                curve (int):
                    Specifies which curve to set.
                data_points (list):
                    A list containing every point in the curve represented as a tuple.
                    (sensor_units: float, temp_value: float, curvature_value: float (optional)).

        """
        self.delete_curve(curve)

        for index, point in data_points:
            if len(point) > 2:
                self.set_curve_data_point(curve, index + 1, point[0], point[1], point[2])
            else:
                self.set_curve_data_point(curve, index + 1, point[0], point[1])

    def delete_curve(self, curve):
        """Deletes the user curve.

            Args:
                curve (int):
                    Specifies a user curve to delete.

        """
        self.command(f"CRVDEL {curve}")

    def set_alarm_parameters(self, input_channel, alarm_enable, alarm_settings=None):
        """Configures the alarm parameters for an input.

            Args:
                input_channel (str):
                    Specifies which input to configure.
                alarm_enable (bool):
                    Specifies whether to turn on the alarm for the input, or turn the alarm off.
                alarm_settings (AlarmSettings):
                    See AlarmSettings class. Required only if alarm_enable is set to True.

        """
        if alarm_enable:
            command_string = (f"ALARM {input_channel},{int(alarm_enable)},{alarm_settings.high_value}," +
                            f"{alarm_settings.low_value},{alarm_settings.deadband}," +
                            f"{int(alarm_settings.latch_enable)},{int(alarm_settings.audible)},{int(alarm_settings.visible)}")
            self.command(command_string)
        else:
            self.command(f"ALARM {input_channel},{int(alarm_enable)},,,,,,")

    def get_alarm_parameters(self, input_channel):
        """Returns the present state of all alarm parameters.

            Args:
                input_channel (str):
                    Specifies which input to configure.

            Returns:
                alarm_settings (AlarmSettings):
                    See AlarmSettings class.

        """
        parameters = self.query(f"ALARM? {input_channel}").split(",")
        return AlarmSettings(float(parameters[1]), float(parameters[2]),
                             float(parameters[3]), bool(int((parameters[4]))),
                             audible=bool(int(parameters[5])), visible=bool(int(parameters[6])),
                             alarm_enable=bool(int(parameters[0])))

    def get_alarm_status(self, channel):
        """Returns the high state and low state of the alarm for the specified channel.

                Args:
                    channel (str or int)
                        Specifies which input channel to read from.

                Return:
                    (dict):
                        {"high_state": bool, "low_state" bool}

        """
        response = self.query(f"ALARMST? {channel}")
        separated_response = response.split(",")
        return {"high_state_enabled": bool(int(separated_response[0])),
                "low_state_enabled": bool(int(separated_response[1]))}

    def reset_alarm_status(self):
        """Clears the high and low status of all alarms."""
        self.command("ALMRST")

    def _get_analog_output_percentage(self, output):
        """Returns the output percentage of the analog voltage output.

            Args:
                output (int):
                    Specifies which analog voltage output to query.

            Returns:
                (float):
                    Analog voltage heater output percentage.

        """
        return float(self.query(f"AOUT? {output}"))

    def _set_autotune(self, output, mode):
        """Initiates auto-tuning of the heater control loop.

            Args:
                output (int):
                    Specifies the output associated with the loop to be Auto-tuned.
                mode (IntEnum):
                    Specifies the Autotune mode.
                    Member of instrument's AutoTuneMode IntEnum class.

        """
        self.command(f"ATUNE {output},{mode}")

        # Ensure autotune starts without error
        self._autotune_error()

    def _set_contrast_level(self, contrast_level):
        """Sets the display contrast level on the front panel.

            Args:
                contrast_level (int):
                    Contrast value:
                    1 - 32.

        """
        self.command(f"BRIGT {contrast_level}")

    def _get_contrast_level(self):
        """Returns the contrast level of front display."""

        return int(self.query("BRIGT?"))

    def _set_brightness(self, brightness):
        """Method to set the front display brightness.

            Args:
                brightness (IntEnum):
                    A member of the instrument's BrightnessLevel IntEnum class.

        """
        self.command(f"BRIGT {brightness}")

    def _get_brightness(self):
        """Method to query the front display brightness.

            Returns:
                (IntEnum):
                    A member of the instrument's BrightnessLevel IntEnum class.

        """
        return self.BrightnessLevel(int(self.query("BRIGT?")))

    def _get_celsius_reading(self, channel):
        """Returns the temperature in Celsius of any channel.

            Args:
                channel (str):
                    "A" - "D" (in addition, "D1" - "D5" for 3062 option).

        """
        return float(self.query(f"CRDG? {channel}"))

    def _set_diode_excitation_current(self, channel, excitation_current):
        """Sets the excitation current of a specific channel.

            The 10 uA excitation current is the only calibrated excitation current, and is used in
            almost all applications. The Model 336 will default the 10 uA current setting any time the
            input sensor type is changed.

            Args:
                channel (str):
                    Specifies which sensor input to configure:
                    "A" - "D".

                excitation_current (IntEnum):
                    A member of the instrument's DiodeCurrent IntEnum class.

        """
        self.command(f"DIOCUR {channel},{excitation_current}")

    def _get_diode_excitation_current(self, channel):
        """Returns the diode excitation current setting as a string.

            Args:
                channel (str):
                    Specifies which input to return:
                    "A" - "D".

            Returns:
                (IntEnum):
                    A member of the instrument's DiodeCurrent IntEnum class.
                    Diode excitation current.

        """
        response = int(self.query(f"DIOCUR? {channel}"))
        return self.DiodeCurrent(response)

    def set_display_field_settings(self, field, input_channel, display_units):
        """Configures a display field when the display is in custom mode.

            Args:
                field (int):
                    Defines which field of the display is being configured.
                input_channel (IntEnum):
                    Defines which input to display.
                    A member of the instrument's InputChannel IntEnum class.
                display_units (IntEnum):
                    Defines which units to display reading in.
                    A member of the instrument's DisplayUnits IntEnum class.

        """
        self.command(f"DISPFLD {field},{input_channel},{display_units}")

    def get_display_field_settings(self, field):
        """Returns the settings of the specified display field when display is in Custom mode.

            Args:
                field (int)
                    Defines which field of the display to retrieve settings from.

            Returns:
                (dict):
                    See set_display_field_settings method.
                    {"input_channel": IntEnum, "display_units": IntEnum}

        """
        separated_settings = self.query(f"DISPFLD? {field}").split(",")
        return {'input_channel': self.InputChannel(int(separated_settings[0])),
                'display_units': self.DisplayFieldUnits(int(separated_settings[1]))}

    def _set_filter(self, input_channel, filter_enable, data_points, reset_threshold):
        """Configures the input_channel filter parameter.

            Args:
                input_channel (int or str):
                    Specifies which input channel to configure.
                filter_enable (bool):
                    Specified whether the filtering function is enabled or not.
                data_points (int):
                    Specifies how many points the filter function uses:
                    2 - 64.
                reset_threshold (int):
                    Specifies what percent of full scale reading limits the filtering function.
                    When a raw reading differs from a filtered value by more than this threshold,
                    the filter averaging resets.
                    Options are:
                    1% - 10%.

        """
        self.command(f"FILTER {input_channel},{int(filter_enable)},{data_points},{reset_threshold}")

    def _get_filter(self, input_channel):
        """Returns the input_channel filter configuration.

            Args:
                input_channel (int or str):
                    Specifies which input channel to configure.

            Returns:
                (dict)
                    {"filter_enable": bool, "data_points": int, "reset_threshold": int}
                        filter_enable: Specified whether the filtering function is enabled or not.
                        data_points: Specifies how many points the filter function uses.
                        reset_threshold: Specifies what percent of full scale reading limits the filtering function. When a
                        raw reading differs from a filtered value by more than this threshold, the filter averaging
                        resets (1% - 10%).

        """
        filter_settings = self.query(f"FILTER? {input_channel}").split(",")
        return {"filter_enable": bool(int(filter_settings[0])),
                "data_points": int(filter_settings[1]),
                "reset_threshold": int(filter_settings[2])}

    def get_heater_output(self, output):
        """Sample heater output in percent, scale is dependent upon the instrument used and heater configuration.

            Args:
                output (int):
                    Heater output to query.

            Returns:
                (float):
                    percent of full scale current/voltage/power.

        """
        return float(self.query(f"HTR? {output}"))

    def get_heater_status(self, output):
        """Returns the heater error code state, error is cleared upon querying the heater status.

            Args:
                output (int):
                    Specifies which heater output to query (1 or 2).

            Returns:
                (IntEnum):
                    Object of instrument's HeaterError type.

        """
        status_code = int(self.query(f"HTRST? {output}"))
        return self.HeaterError(status_code)

    def set_ieee_488(self, address):
        """Specifies the IEEE address.

            Args:
                address (int):
                    1-30 (0 and 31 reserved).

        """
        self.command(f"IEEE {address}")

    def get_ieee_488(self):
        """Returns the IEEE address set.

            Returns:
                address (int):
                    1-30 (0 and 31 reserved).

        """
        return int(self.query("IEEE?"))

    def set_input_curve(self, input_channel, curve_number):
        """Specifies the curve an input uses for temperature conversion.

            Args:
                input_channel (str or int):
                    Specifies which input to configure.
                curve_number (int):
                    0 = none, 1-20 = standard curves, 21-59 = user curves.

        """
        self.command(f"INCRV {input_channel},{curve_number}")
        # Check that the user mapped an input to a curve (not just set the input to no curve)
        if curve_number != 0:
            # Query the curve mapped to input_channel, if the query returns zero,
            # an invalid curve was selected for the specified input
            set_curve = self.get_input_curve(input_channel)
            if set_curve == 0:
                raise InstrumentException("The specified curve type does not match the configured input type")

    def get_input_curve(self, input_channel):
        """Returns the curve number being used for a given input.

            Args:
                input_channel (str or int):
                    Specifies which input to query.

            Returns:
                curve_number (int):
                    0-59.

        """
        return int(self.query(f"INCRV? {input_channel}"))

    def _set_interface(self, interface):
        """Selects the remote interface for the instrument,

            Args:
                interface (IntEnum):
                    Member of instrument's Interface IntEnum class,

        """
        self.command(f"INTSEL {interface}")

    def _get_interface(self):
        """Returns the remote interface for the instrument.

            Returns:
                (IntEnum):
                    Member of instrument's Interface IntEnum class.

        """
        interface_response = self.query("INTSEL?")
        return self.Interface(int(interface_response))

    def set_led_state(self, state):
        """Sets the front panel LEDs to on or off.

            Args:
                state (bool):
                    Sets the LEDs to functional or nonfunctional.
                    False if disabled, True enabled.

        """
        self.command(f"LEDS {int(state)}")

    def get_led_state(self):
        """Returns whether front panel LEDs are enabled.

            Returns:
                (bool):
                    Specifies whether front panel LEDs are functional.
                    False if disabled, True enabled.

        """
        return bool(int(self.query("LEDS?")))

    def set_keypad_lock(self, state, code):
        """Locks or unlocks front panel keypad (except for alarms and disabling heaters).

            Args:
                state (bool):
                    Sets the keypad to locked or unlocked. Options are:
                    False for unlocked or True for locked.
                code (int):
                    Specifies 3 digit lock-out code. Options are:
                    000 - 999.

        """
        self.command(f"LOCK {int(state)},{code}")

    def get_keypad_lock(self):
        """Returns the state of the keypad lock and the lock-out code.

            Returns:
                (dict):
                    {"state": bool, "code": int}

        """
        output_string = self.query("LOCK?")
        separated_response = output_string.split(",")
        return {'state': bool(int(separated_response[0])),
                'code': int(separated_response[1])}

    def get_min_max_data(self, input_channel):
        """Returns the minimum and maximum data from an input.

            Args:
                input_channel (str):
                    Specifies which input to query.

            Returns:
                (dict):
                    {"minimum": float, "maximum": float}

        """
        min_max_data = self.query(f"MDAT? {input_channel}").split(",")
        return {"minimum": float(min_max_data[0]),
                "maximum": float(min_max_data[1])}

    def reset_min_max_data(self):
        """Resets the minimum and maximum input data."""
        self.command("MNMXRST")

    def set_remote_interface_mode(self, mode):
        """Places the instrument in one of three interface modes.

            Args:
                mode (IntEnum):
                    A member of the instrument's InterfaceMode IntEnum class.

        """
        self.command(f"MODE {mode}")

    def get_remote_interface_mode(self):
        """Returns the state of the interface mode.

            Returns:
                (IntEnum):
                    A member of the instrument's InterfaceMode IntEnum class.

        """
        mode = int(self.query("MODE?"))
        return self.InterfaceMode(mode)

    def set_manual_output(self, output, value):
        """When instrument is in closed loop PID, Zone, or Open Loop modes a manual output may be set.

            Args:
                output (int):
                    Specifies output to configure.
                value (float):
                    Specifies value for manual output in percent.

        """
        self.command(f"MOUT {output},{value}")

    def get_manual_output(self, output):
        """Returns the manual output value in percent.

            Args:
                output (int):
                    Specifies output to query.

            Returns:
                (float):
                    Manual output percent.

        """
        return float(self.query(f"MOUT? {output}"))

    def _set_network_settings(self, dhcp_enable, auto_ip_enable, ip_address, sub_mask, gateway, primary_dns,
                              secondary_dns, pref_host, pref_domain, description):
        """Network class constructor.

            Args:
                dhcp_enable (bool):
                    Enable or disable DHCP.
                auto_ip_enable (bool):
                    Enable or disable dynamically configured link-local addressing (Auto IP).
                ip_address (str):
                    IP address for static configuration.
                sub_mask (str):
                    Subnet mask for static configuration.
                gateway (str):
                    Gateway address for static configuration.
                primary_dns (str):
                    Primary DNS address for static configuration.
                secondary_dns (str):
                    Secondary DNS address for static configuration.
                pref_host (str):
                    Preferred Hostname (15 character maximum).
                pref_domain (str):
                    Preferred Domain name (64 character maximum).
                description (str):
                    Instrument description (32 character maximum).

        """
        command_string = (f"NET {int(dhcp_enable)},{int(auto_ip_enable)},{ip_address}," +
                        f"{sub_mask},{gateway},{primary_dns},{secondary_dns},\"{pref_host}\"," +
                        f"\"{pref_domain}\",\"{description}\"")
        self.command(command_string)

    def _get_network_settings(self):
        """Method to retrieve the IP settings.

            Returns:
                (dict):
                    See set_network_settings arguments.

        """
        network_response = self.query("NET?").split(",")
        return {"dhcp_enable": bool(int(network_response[0])),
                "auto_ip_enable": bool(int(network_response[1])),
                "ip_address": network_response[2],
                "sub_mask": network_response[3],
                "gateway": network_response[4],
                "primary_dns": network_response[5],
                "secondary_dns": network_response[6],
                "pref_host": network_response[7],
                "pref_domain": network_response[8],
                "description": network_response[9]}

    def _get_network_configuration(self):
        """Method to return the configured ethernet parameters.

            Return:
                (dict):
                    {"lan_status": LanStatus, "ip_address": str, "sub_mask": str, "gateway": str, "primary_dns": str,
                        "secondary_dns": str, "hostname" str, "domain": str, "mac_address": str}
                        lan_status: Current status of the ethernet connection. Member of the instrument's LanStatus
                        IntEnum class.
                        ip_address: Configured IP address.
                        sub_mask: Configured subnet mask.
                        gateway: Configured gateway address.
                        primary_dns: Configured primary DNS address.
                        secondary_dns: Configured secondary DNS address.
                        hostname: Assigned hostname.
                        domain: Assigned domain.
                        mac_address: Module MAC address.

        """
        ethernet = self.query("NETID?").split(",")
        return {"lan_status": self.LanStatus(int(ethernet[0])),
                "ip_address": ethernet[1],
                "sub_mask": ethernet[2],
                "gateway": ethernet[3],
                "primary_dns": ethernet[4],
                "secondary_dns": ethernet[5],
                "hostname": ethernet[7],
                "domain": ethernet[8],
                "mac_address": ethernet[6]}

    def _get_operation_condition(self):
        """Returns the names of the operation condition register bits and their values."""

        response = self.query("OPST?")
        return OperationEvent.from_integer(response)

    def _get_operation_event_enable(self):
        """Returns the names of the operation event enable register and their values.

            These values determine which bits propagate to the operation condition register.
        """

        response = self.query("OPSTE?")
        return OperationEvent.from_integer(response)

    def _set_operation_event_enable(self, register_mask):
        """Configures values of the operation event enable register bits.

            These values determine which bits propagate to the standard event register.

            Args:
                register_mask (OperationEvent):
                    An OperationEvent class object with all bits configured true or false.

        """
        integer_representation = register_mask.to_integer()
        self.command(f"OPSTE {integer_representation}")

    def _get_operation_event(self):
        """Returns the names of the operation event register bits and their values."""

        response = self.query("OPSTR?")
        status_register = OperationEvent.from_integer(response)
        return status_register

    def set_heater_pid(self, output, gain, integral, derivative):
        """Configure the closed loop control parameters of the heater output.

            Args:
                output (int):
                    Specifies which output's control loop to configure.
                gain (float):
                    Proportional term in PID control.
                    This controls how strongly the control output reacts to the present error.
                integral (float):
                    Integral term in PID control.
                    This controls how strongly the control output reacts to the past error history.
                derivative (float):
                    Derivative term in PID control.
                    This value controls how quickly the present field set point will transition to a new set-point.
                    The ramp rate is configured in field units per second.

        """
        self.command(f"PID {output},{gain},{integral},{derivative}")

    def get_heater_pid(self, output):
        """Returns the closed loop control parameters of the heater output.

            Args:
                output (int):
                    Specifies which output's control loop to query.

            Returns:
                (dict):
                    {"gain": float, "integral": float, "ramp_rate": float}
                        gain: Proportional term in PID control.
                        integral: Integral term in PID control.
                        ramp_rate: Derivative term in PID control.

        """
        pid_values = self.query(f"PID? {output}")
        pid_values = pid_values.split(",")
        return {"gain": float(pid_values[0]),
                "integral": float(pid_values[1]),
                "ramp_rate": float(pid_values[2])}

    def set_setpoint_ramp_parameter(self, output, ramp_enable, rate_value):
        """Sets the control loop of a particular output.

            Args:
                output (int):
                    Specifies which output's control loop to configure.
                ramp_enable (bool):
                    Specifies whether ramping is off or on (False = Off or True = On).
                rate_value (float):
                    Specifies set-point ramp rate in kelvin per minute.
                    The rate is always positive but will respond to ramps up or down.
                    A rate of 0 is interpreted as infinite, and will respond as if set-point ramping were off.
                    (0.1 to 100)

        """
        self.command(f"RAMP {output},{int(ramp_enable)},{rate_value}")

    def get_setpoint_ramp_parameter(self, output):
        """Returns the control loop parameters of a particular output.

            Args:
                output (int):
                    Specifies which output's control loop to return.

            Returns:
                (dict):
                    {"ramp_enable": bool, "rate_value": float}

        """
        parameters = self.query(f"RAMP? {output}").split(",")
        return {"ramp_enable": bool(int(parameters[0])),
                "rate_value": float(parameters[1])}

    def get_setpoint_ramp_status(self, output):
        """Returns whether the set-point is ramping.

            Args:
                output (int):
                    Specifies which output's control loop to query.

            Returns:
                (bool):
                    Ramp status.
                    False = Not ramping, True = Ramping.

        """
        return bool(int(self.query(f"RAMPST? {output}")))

    def turn_relay_on(self, relay_number):
        """Turns the specified relay on.

            Args:
                relay_number (int):
                    The relay to turn on.
                    Options are:
                    1 or 2.

        """
        self.command(f"RELAY {relay_number},1,,")

    def turn_relay_off(self, relay_number):
        """Turns the specified relay off.

            Args:
                relay_number (int):
                    The relay to turn off.
                    Options are:
                    1 or 2.

        """
        self.command(f"RELAY {relay_number},0,,")

    def set_relay_alarms(self, relay_number, activating_input_channel, alarm_relay_trigger_type):
        """Sets a relay to turn on and off automatically based on the state of the alarm of the specified input channel.

            Args:
                relay_number (int):
                    The relay to configure.
                    Options are:
                    1 or 2.
                activating_input_channel (str or int):
                    Specifies which input alarm activates the relay.
                alarm_relay_trigger_type (RelayControlAlarm):
                    Specifies the type of alarm that triggers the relay.

        """
        self.command(f"RELAY {relay_number},2,{activating_input_channel},{alarm_relay_trigger_type}")

    def get_relay_alarm_control_parameters(self, relay_number):
        """Returns the relay alarm configuration for either of the two configurable relays.

            Relay must be configured for alarm mode to retrieve parameters.

            Args:
                relay_number (int)
                    Specifies which relay to query.
                    Options are:
                    1 or 2.

            Returns:
                (dict):
                    {"activating_input_channel": str, "alarm_relay_trigger_type": RelayControlAlarm}

        """
        relay_config = self.query(f"RELAY? {relay_number}").split(",")
        activating_input_channel = relay_config[1]
        alarm_relay_trigger_type = self.RelayControlAlarm(int(relay_config[2]))
        return {'activating_input_channel': activating_input_channel,
                'alarm_relay_trigger_type': alarm_relay_trigger_type}

    def get_relay_control_mode(self, relay_number):
        """Returns the configured mode of the specified relay.

            Args:
                relay_number (int):
                    Specifies which relay to query.
                    Options are:
                    1 or 2.

            Returns:
                (IntEnum):
                    The configured mode of the relay.
                    Represented as a member of the instrument's RelayControlMode IntEnum class.

        """
        relay_settings = self.query(f"RELAY? {str(relay_number)}")
        split_relay_settings = relay_settings.split(",")
        return self.RelayControlMode(int(split_relay_settings[0]))

    def get_relay_status(self, relay_channel):
        """Returns whether the relay at the specified channel is On or Off.

            Args:
                relay_channel (int):
                    The relay channel to query.

            Returns:
                (bool):
                    True if relay is on, False if relay is off.

        """
        return bool(int(self.query(f"RELAYST? {relay_channel}")))

    def _set_soft_cal_curve_dt_470(self, curve_number, serial_number, calibration_point_1=(4.2, 1.62622),
                                   calibration_point_2=(77.35, 1.02032), calibration_point_3=(305, 0.50691)):
        """Creates a SoftCal curve from any 1-3 temperature/sensor points using the preconfigured DT-470 curve.

            When a calibration point other than one or more the default value(s) is entered a SoftCal curve is
            generated.

            Args:
                curve_number (int):
                    The curve number to save the generated curve to.
                    Options are:  21 - 59.
                serial_number (str):
                    Specifies the curve serial number.
                    Limited to 10 characters.
                calibration_point_1 (tuple):
                    Tuple of two floats in the form (temperature_value, sensor_value). Optional parameter.
                calibration_point_2 (tuple):
                    Tuple of two floats in the form (temperature_value, sensor_value). Optional Parameter.
                calibration_point_3 (tuple):
                    Tuple of two floats in the form (temperature_value, sensor_value). Optional Parameter.

        """
        command_string = (f"SCAL {1},{curve_number},{serial_number},{calibration_point_1[0]}," +
                        f"{calibration_point_1[1]},{calibration_point_2[0]},{calibration_point_2[1]}," +
                        f"{calibration_point_3[0]},{calibration_point_3[1]}")
        self.command(command_string)

    def _set_soft_cal_curve_pt_100(self, curve_number, serial_number, calibration_point_1=(77.35, 20.234),
                                   calibration_point_2=(305, 112.384), calibration_point_3=(480, 178.353)):
        """Creates a SoftCal curve from any 1-3 temperature/sensor points using the preconfigured PT-100 curve.

            When a calibration point other than one or more the default value(s) is entered a SoftCal curve is
            generated.

            Args:
                curve_number (int):
                    The curve number to save the generated curve to.
                    Options are:
                    21 - 59.
                serial_number (str):
                    Specifies the curve serial number.
                    Limited to 10 characters.
                calibration_point_1 (tuple):
                    Tuple of two floats in the form (temperature_value, sensor_value). Optional Parameter.
                calibration_point_2 (tuple):
                    Tuple of two floats in the form (temperature_value, sensor_value). Optional Parameter.
                calibration_point_3 (tuple):
                    Tuple of two floats in the form (temperature_value, sensor_value). Optional Parameter.

        """
        command_string = (f"SCAL {6},{curve_number},{serial_number}," +
                        f"{calibration_point_1[0]},{calibration_point_1[1]}," +
                        f"{calibration_point_2[0]},{calibration_point_2[1]}," +
                        f"{calibration_point_3[0]},{calibration_point_3[1]}")
        self.command(command_string)

    def _set_soft_cal_curve_pt_1000(self, curve_number, serial_number, calibration_point_1=(77.35, 202.34),
                                    calibration_point_2=(305, 1123.84), calibration_point_3=(480, 1783.53)):
        """Creates a SoftCal curve from any 1-3 temperature/sensor points using the preconfigured PT-1000 curve.

            When a calibration point other than one or more the default value(s) is entered a SoftCal curve is
            generated.

            Args:
                curve_number (int):
                    The curve number to save the generated curve to.
                    Options are:
                    21 - 59.
                serial_number (str):
                    Specifies the curve serial number.
                    Limited to 10 characters.
                calibration_point_1 (tuple):
                    Tuple of two floats in the form (temperature_value, sensor_value). Optional Parameter.
                calibration_point_2 (tuple):
                    Tuple of two floats in the form (temperature_value, sensor_value). Optional Parameter.
                calibration_point_3 (tuple):
                    Tuple of two floats in the form (temperature_value, sensor_value). Optional Parameter.

        """
        command_string = (f"SCAL {7},{curve_number},{serial_number}," +
                        f"{calibration_point_1[0]},{calibration_point_1[1]}," +
                        f"{calibration_point_2[0]},{calibration_point_2[1]}," +
                        f"{calibration_point_3[0]},{calibration_point_3[1]}")
        self.command(command_string)

    def set_control_setpoint(self, output, value):
        """Set set-point for specific output's control loop.

            Control settings, that is, P, I, D, and Set-point, are assigned to outputs,
            which results in the settings being applied to the control loop formed by the
            output and its control input.

            Args:
                output (int):
                    Specifies which output's control loop to configure.
                value (float):
                    The value for the set-point (in the preferred units of the control loop sensor).

        """
        self.command(f"SETP {output},{value}")

    def get_control_setpoint(self, output):
        """Returns the value for a given control output.

            Args:
                output (int):
                    Specifies which output's control loop to query (1 or 2).

            Returns:
                value (float):
                    The value for the set-point (in the preferred units of the control loop sensor).

        """
        return float(self.query(f"SETP? {output}"))

    def _get_thermocouple_junction_temp(self):
        """Returns the temperature of the ceramic thermocouple block from the room temperature compensation calculation.

            Returns:
                (float):
                    Temperature of the ceramic thermocouple block (kelvin).

        """
        return float(self.query("TEMP?"))

    def set_temperature_limit(self, input_channel, limit):
        """After a set temperature limit is exceeded, all control outputs will shut down.

            Args:
                input_channel (str or int):
                    Specifies which input to configure.
                limit (float):
                    The temperature limit in kelvin for which to shut down all control outputs when exceeded.
                    A limit of zero will turn the feature off.

        """
        self.command(f"TLIMIT {input_channel},{limit}")

    def get_temperature_limit(self, input_channel):
        """Returns the value of the temperature limit in kelvin.

            Args:
                input_channel (str or int):
                    Specifies which input to query.

        """
        return float(self.query(f"TLIMIT? {input_channel}"))

    def _get_tuning_control_status(self):
        """Returns dictionary of tuning control status values.

            If initial conditions are not met when starting the autotune procedure, causing the
            auto-tuning process to never actually begin, then the error status will be set to 1 and
            the stage status will be stage 00.

            Returns:
                (dict):
                    {"active_tuning_enable": bool, "output": int, "tuning_error": bool, "stage_status": int}
                        active_tuning_enable: False = no active tuning, True = active tuning.
                        output: Heater output of the control loop being tuned.
                        tuning_error: False = no tuning error, True = tuning error.
                        stage_status: Specifies the current stage in the Autotune process. If tuning error occurred,
                        stage status represents stage that failed.

        """
        tuning_status = self.query("TUNEST?").split(",")
        return {"active_tuning_enable": bool(int(tuning_status[0])),
                "output": int(tuning_status[1]),
                "tuning_error": bool(int(tuning_status[2])),
                "stage_status": int(tuning_status[3])}

    def _set_website_login(self, username, password):
        """Sets the username and password for the web interface.

            Args:
                username (str):
                    15 character string representing the website username.
                password (str):
                    15 character string representing the website password.

        """
        self.command(f"WEBLOG \"{username}\",\"{password}\"")

    def _get_website_login(self):
        """Method to return the username and password for the web interface.

            Returns:
                website_login (dict): A dictionary containing 15 character string type items.
                    {"username": str, "password": str}

        """
        login_response = self.query("WEBLOG?").split(",")
        return {"username": login_response[0],
                "password": login_response[1]}

    def _get_identity(self):
        return self.query('*IDN?', check_errors=False).split(',')

    def _autotune_error(self):
        """Method to raise an exception if autotune error has occurred."""

        tuning_status = self.query("TUNEST?").split(",")

        if bool(int(tuning_status[2])):
            raise InstrumentException("An autotune error is present")
