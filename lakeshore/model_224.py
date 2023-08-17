"""Implements functionality unique to the Lake Shore Model 224 temperature monitor."""

import serial
from .generic_instrument import GenericInstrument, InstrumentException, RegisterBase
from .model_224_enums import Model224Enums
from .temperature_controllers import StandardEventRegister


class Model224AlarmParameters:
    """Class used to disable or configure an alarm in conjunction with the set/get_alarm_parameters() method."""

    def __init__(self, high_value, low_value, deadband, latch_enable, audible=None, visible=None):
        """Constructor for Model224AlarmParameters class.

            Args:
                high_value (float):
                    Sets the value the source is checked against to activate the high alarm.
                low_value (float):
                    Sets the value the source is checked against to activate low alarm.
                deadband (float):
                    Sets the value that the source must change outside an alarm
                    condition to deactivate an unlatched alarm.
                latch_enable (bool):
                    Specifies a latched alarm (False = off, True = on).
                audible (bool):
                    Specifies if the internal speaker will beep when an alarm condition
                    occurs (False = off, True = on). Optional parameter.
                visible (bool):
                    Specifies if the Alarm LED on the instrument front panel will blink
                    when an alarm condition occurs (False = off, True = on). Optional parameter.

        """
        self.high_value = high_value
        self.low_value = low_value
        self.deadband = deadband
        self.latch_enable = latch_enable
        self.audible = audible
        self.visible = visible


class Model224InputSensorSettings:
    """Class representing the parameters of a sensor in one of the instrument's inputs."""

    def __init__(self,
                 sensor_type,
                 preferred_units,
                 sensor_range=None,
                 autorange_enabled=False,
                 compensation=False):
        """Constructor for the Model224InputSensorSettings class.

            Args:
                sensor_type (Model224InputSensorType or int):
                    Specifies what type of sensor is being used at the input.
                preferred_units (Model224InputSensorUnits or int):
                    Specifies the preferred units used for sensor readings and alarm set-points when displayed.
                sensor_range (IntEnum):
                    Specifies the range of the sensor.
                    Optional if auto range is enabled.
                autorange_enabled (bool):
                    Defines if autorange is enabled.
                    Not applicable for diode sensors.
                    Defaults to false. Optional parameter.
                compensation (bool):
                    Defines if thermal input compensation is on or off.
                    Not applicable for diode sensors.
                    Defaults to false. Optional parameter.

        """
        self.sensor_type = sensor_type
        self.sensor_range = sensor_range
        self.preferred_units = preferred_units
        self.autorange_enabled = autorange_enabled
        self.compensation = compensation


class Model224CurveHeader:
    """A class that configures the user curve header and corresponding parameters."""

    def __init__(self, curve_name, serial_number, curve_data_format, temperature_limit, coefficient):
        """Constructor for Model224CurveHeader class.

            Args:
                curve_name (str):
                    Specifies curve name (limit of 15 characters).
                serial_number (str):
                    Specifies curve serial number (limit of 10 characters).
                curve_data_format (Model224CurveFormat):
                    Specifies the curve data format.
                temperature_limit (float):
                    Specifies the curve temperature limit in Kelvin.
                coefficient (Model224CurveTemperatureCoefficients):
                    Specifies the curve temperature coefficient.

        """

        self.curve_name = curve_name
        self.serial_number = serial_number
        self.curve_data_format = curve_data_format
        self.temperature_limit = temperature_limit
        self.coefficient = coefficient


Model224StandardEventRegister = StandardEventRegister


class Model224ServiceRequestRegister(RegisterBase):
    """Class object representing the Service Request Enable register."""
    bit_names = [
        "",
        "",
        "",
        "",
        "message_available",
        "event_summary",
        ""
        "operation_summary"
    ]

    def __init__(self,
                 message_available,
                 event_summary,
                 operation_summary):
        self.message_available = message_available
        self.event_summary = event_summary
        self.operation_summary = operation_summary


class Model224StatusByteRegister(RegisterBase):
    """Class object representing the status byte register."""
    bit_names = [
        "",
        "",
        "",
        "",
        "message_available",
        "event_summary",
        "master_summary_status"
        "operation_summary"
    ]

    def __init__(self,
                 message_available,
                 event_summary,
                 master_summary_status,
                 operation_summary):
        self.message_available = message_available
        self.event_summary = event_summary
        self.master_summary_status = master_summary_status
        self.operation_summary = operation_summary


class Model224ReadingStatusRegister(RegisterBase):
    """Class object representing the reading status of an input.

        While not a literal register, the return of an int representation of multiple booleans makes it convenient to
        represent this functionality as a register.
    """
    bit_names = [
        "invalid_reading",
        "",
        "",
        "",
        "temperature_under_range",
        "temperature_over_range",
        "sensor_units_zero",
        "sensor_units_over_range"
    ]

    def __init__(self,
                 invalid_reading,
                 temperature_under_range,
                 temperature_over_range,
                 sensor_units_zero,
                 sensor_units_over_range):
        self.invalid_reading = invalid_reading
        self.temperature_under_range = temperature_under_range
        self.temperature_over_range = temperature_over_range
        self.sensor_units_zero = sensor_units_zero
        self.sensor_units_over_range = sensor_units_over_range


class Model224(Model224Enums, GenericInstrument):
    """A class object representing the Lake Shore Model 224 temperature monitor."""

    vid_pid = [(0x1FB9, 0x0204)]

    def __init__(self,
                 serial_number=None,
                 com_port=None,
                 baud_rate=57600,
                 data_bits=7,
                 stop_bits=1,
                 parity=serial.PARITY_ODD,
                 flow_control=False,
                 handshaking=False,
                 timeout=2.0,
                 ip_address=None,
                 tcp_port=7777,
                 **kwargs):

        # Call the parent init, then fill in values specific to the 224
        GenericInstrument.__init__(self, serial_number, com_port, baud_rate, data_bits, stop_bits, parity, flow_control,
                                   handshaking, timeout, ip_address, tcp_port, **kwargs)

    @staticmethod
    def _error_check(error_code):
        event_register = Model224StandardEventRegister.from_integer(error_code)
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
                check_errors (bool):
                    Chooses whether to check for and raise errors after sending a command. True by default. kwarg.
                    Optional Parameter

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

        response = self.query("*ESE?")
        status_register = Model224StandardEventRegister.from_integer(response)
        return status_register

    def set_standard_event_enable_mask(self, register_mask):
        """Configures values of the standard event enable register bits.

            These values determine which bits propagate to the standard event register.

            Args:
                register_mask (Model224StandardEventRegister):
                    An StandardEventRegister class object with all bits set to a value.

        """

        integer_representation = register_mask.to_integer()
        self.command("*ESE " + str(integer_representation))

    def clear_interface_command(self):
        """Clears the bits of the interface and terminates all pending operations.

            Clears the bits in the Status Byte Register, Standard Event Status Register, and Operation Event Register,
            and terminates all pending operations. Clears the interface, but not the controller.
        """

        self.command("*CLS")

    def reset_instrument(self):
        """Sets controller parameters to power-up settings."""

        self.command("*RST")

    def set_service_request(self, register_mask):
        """Manually enable/disable the mask of the corresponding status-flag bit in the status byte register.

            Args:
                register_mask (Model224ServiceRequestRegister):
                    A Model224ServiceRequestRegister class object with all bits configured.
        """

        integer_representation = register_mask.to_integer()
        self.command("*SRE " + str(integer_representation))

    def get_service_request(self):
        """Returns the status byte register bits and their values as a class instance."""

        response = self.query("*SRE?")
        status_register = Model224ServiceRequestRegister.from_integer(response)
        return status_register

    def get_status_byte(self):
        """Returns the status flag bits as a class instance without resetting the register."""

        response = self.query("*STB?")
        status_flag = Model224StatusByteRegister.from_integer(response)
        return status_flag

    def get_self_test(self):
        """Instrument self test result completed at power up.

            Returns:
                test_errors (bool):
                    True means errors found, and False means no errors found.
        """

        test_errors = bool(int(self.query("*TST?")))
        return test_errors

    def set_wait_to_continue(self):
        """Causes the IEEE-488 interface to hold off until all pending operations have been completed.

            This has the same function as the set_operation_complete() method, except that it does not set the
            Operation Complete event bit in the Event Status Register.
        """

        self.command("*WAI")

    def set_to_factory_defaults(self):
        """Sets all the settings and configurations to their factory default values."""
        self.command("DFLT 99")

    def get_reading_status(self, input_channel):
        """Returns the reading status of any input status flags that may be set.

            Args:
                input_channel (str):
                    The input to check for reading status flags.
                    Options are: A, B, C(1 - 5), D(1 - 5).

            Returns:
                (dict):
                    {"invalid_reading": bool, "temperature_under_range": bool, "temperature_over_range": bool,
                    "sensor_units_zero": bool, "sensor_units_over_range": bool}
        """
        flag_code = int(self.query(f"RDGST? {input_channel}"))
        reading_status = Model224ReadingStatusRegister.from_integer(flag_code)
        return reading_status

    def get_kelvin_reading(self, input_channel):
        """Returns the temperature value in kelvin of either channel.

            Args:
                input_channel:
                    Selects the channel to retrieve measurement.
                    Options are: A, B, C(1 - 5), D(1 - 5).

            Returns:
                (float):
                    The reading of the sensor in kelvin.


        """

        return float(self.query(f"KRDG? {input_channel}"))

    def get_sensor_reading(self, input_channel):
        """Returns the sensor reading in the sensor's units.

            Args:
                input_channel:
                    Selects the channel to retrieve measurement.
                    Options are: Options are: A, B, C(1 - 5), D(1 - 5).

            Returns:
                reading (float):
                    The raw sensor reading in the units of the connected sensor.

        """

        return float(self.query(f"SRDG? {input_channel}"))

    def get_celsius_reading(self, input_channel):
        """Returns the given input's temperature reading in degrees Celsius.

            Args:
                input_channel (str):
                    Selects input to retrieve measurement from.
                    Options are: A, B, C(1 - 5), D(1 - 5).

            Returns:
                (float):
                    Temperature readings in degrees Celsius.
        """
        return float(self.query(f"CRDG? {input_channel}"))

    def get_all_inputs_celsius_reading(self):
        """Returns the temperature reading in degrees Celsius of all the inputs.

            Returns:
                (dict):
                    {"input_a_reading": float, "input_b_reading": float, "input_c1_reading": float,
                    "input_c2_reading": float, "input_c3_reading": float, "input_c4_reading": float,
                    "input_c5_reading": float, "input_d1_reading": float, "input_d2_reading": float,
                    "input_d3_reading": float, "input_d4_reading": float, "input_d5_reading": float}
        """
        reading = self.query("CRDG? 0")
        separated_readings = reading.split(",")
        return {'input_a_reading': float(separated_readings[0]),
                'input_b_reading': float(separated_readings[1]),
                'input_c1_reading': float(separated_readings[2]),
                'input_c2_reading': float(separated_readings[3]),
                'input_c3_reading': float(separated_readings[4]),
                'input_c4_reading': float(separated_readings[5]),
                'input_c5_reading': float(separated_readings[6]),
                'input_d1_reading': float(separated_readings[7]),
                'input_d2_reading': float(separated_readings[8]),
                'input_d3_reading': float(separated_readings[9]),
                'input_d4_reading': float(separated_readings[10]),
                'input_d5_reading': float(separated_readings[11])}

    def set_input_diode_excitation_current(self, input_channel, diode_current):
        """Sets the excitation current of a diode sensor.

            Input must be configured for a diode sensor for command to work. Current defaults to 10uA.

            Args:
                input_channel (str):
                    The input to configure the diode excitation current for.
                diode_current (Model224DiodeExcitationCurrent):
                    The excitation current for the diode sensor.

        """
        self.command(f"DIOCUR {input_channel},{diode_current}")

    def get_input_diode_excitation_current(self, input_channel):
        """Returns the diode excitation current for the given diode sensor.

            Args:
                input_channel (str):
                    The diode sensor input to query the current of.

            Returns:
                diode_current (Model224DiodeExcitationCurrent):
                    A member of the Model224DiodeExcitationCurrent enum class.

        """
        diode_current_int = int(self.query(f"DIOCUR? {input_channel}"))
        return self.DiodeExcitationCurrent(diode_current_int)

    def set_sensor_name(self, channel, sensor_name):
        """Sets a given name to a sensor on the specified channel.

            Args:
                channel (str):
                    Specifies which the sensor to name is on.
                    Options are: A, B, C(1 - 5), D(1 - 5).

                sensor_name(str):
                    Name user wants to give to the sensor on the specified channel.

        """

        self.command(f"INNAME {channel},\"{sensor_name}\"")

    def get_sensor_name(self, channel):
        """Returns the name of the sensor on the specified channel.

            Args:
                channel (str):
                    Specifies which input sensor to retrieve name of.
                    Options are: A, B, C(1 - 5), D(1 - 5).

            Returns:
                name (str):
                    Name associated with the sensor.

        """

        return self.query(f"INNAME? {channel}")

    def set_display_contrast(self, contrast_level):
        """Sets the contrast level for the front panel display.

            Args:
                contrast_level (int):
                    Display contrast for the front panel LCD screen. Options are:
                    1 - 32.

        """

        self.command(f"BRIGT {contrast_level}")

    def get_display_contrast(self):
        """Returns the contrast level of front panel display.

            Returns:
                (int):
                    Contrast level of the front panel LCD screen.

        """

        return int(self.query("BRIGT?"))

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

    def set_led_state(self, state):
        """Sets the front panel LEDs to on or off.

            Args:
                state (bool):
                    Sets the LEDs to functional or nonfunctional. Options are:
                    False for off, True for on.

        """
        self.command(f"LEDS {str(int(state))}")

    def get_led_state(self):
        """Returns whether front panel LEDs are enabled.

            Returns:
                state (bool):
                    Specifies whether front panel LEDs are functional. Returns:
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
        self.command(f"LOCK {str(int(state))},{str(code)}")

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
                min_max_data (dict):
                    {"minimum": float, "maximum": float}

        """
        min_max_data = self.query("MDAT? " + str(input_channel)).split(",")
        min_max_dictionary = {"minimum": float(min_max_data[0]),
                              "maximum": float(min_max_data[1])}
        return min_max_dictionary

    def reset_min_max_data(self):
        """Resets the minimum and maximum input data."""
        self.command("MNMXRST")

    def set_input_curve(self, input_channel, curve_number):
        """Specifies the curve an input uses for temperature conversion.

            Args:
                input_channel (str):
                    Specifies which input to configure.
                curve_number (int):
                    0 = none, 1-20 = standard curves, 21-59 = user curves.

        """
        self.command(f"INCRV {str(input_channel)},{str(curve_number)}")
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
                input_channel (str):
                    Specifies which input to query.

            Returns:
                curve_number (int):
                    0-59.

        """
        return int(self.query(f"INCRV? {str(input_channel)}"))

    def set_website_login(self, username, password):
        """Sets the username and password to connect instrument to website.

            Args:
                username (str):
                    Username to set for login.
                    Must be less than or equal to 15 characters.
                    Method automatically puts quotation marks around string, so they are not needed in the
                    string literal passed into the method.
                password (str):
                    Password to set for login.
                    Must be less than or equal to 15 characters.
                    Method automatically puts quotation marks around string, so they are not needed in the
                    string literal passed into the method.

        """
        self.command("WEBLOG \"" + username + "\",\"" + password + "\"")

    def get_website_login(self):
        """Returns the set username and password for web login for the instrument.

            Returns:
                (dict):
                    {"username": str, "password": str}
        """
        username_password = self.query("WEBLOG?")
        separated_string = username_password.split(",")
        # Remove padded whitespace and quotations in the returned username and password
        username = separated_string[0].strip(' "')
        password = separated_string[1].strip(' "')
        return {"username": username,
                "password": password}

    def set_alarm_parameters(self, input_channel, alarm_enable, alarm_settings=None):
        """Configures the alarm parameters for an input.

            Args:
                input_channel (str):
                    Specifies which input to configure.
                alarm_enable (bool):
                    Specifies whether to turn on the alarm for the input, or turn the alarm off.
                alarm_settings (Model224AlarmParameters):
                    See Model224AlarmParameters class. Optional if alarm_enable is set to False.

        """

        if alarm_enable:
            if alarm_settings.audible is None:
                audible = 0
            else:
                audible = int(alarm_settings.audible)
            if alarm_settings.visible is None:
                visible = 0
            else:
                visible = int(alarm_settings.visible)
            self.command(f"ALARM {input_channel.upper()},{int(alarm_enable)},{alarm_settings.high_value}," +
                        f"{alarm_settings.low_value},{alarm_settings.deadband},{int(alarm_settings.latch_enable)}," +
                        f"{audible},{visible}")
        else:
            self.command("ALARM " + str(input_channel.upper()) + "," + str(int(alarm_enable)) + ",0,0,0,0,0,0")

    def get_alarm_parameters(self, input_channel):
        """Returns the present state of all alarm parameters.

            Args:
                input_channel (str):
                    Specifies which input to configure.

            Returns:
                (dict):
                    {"alarm_enable": bool, "alarm_settings": Model224AlarmParameters}.

        """
        parameters = self.query("ALARM? " + str(input_channel)).split(",")
        alarm_enable = bool(int(parameters[0]))
        alarm_settings = Model224AlarmParameters(float(parameters[1]), float(parameters[2]),
                                                 float(parameters[3]), bool(int((parameters[4]))),
                                                 audible=bool(int(parameters[5])), visible=bool(int(parameters[6])))
        return {'alarm_enable': alarm_enable,
                'alarm_settings': alarm_settings}

    def get_alarm_status(self, input_channel):
        """Returns the high state and low state of the alarm for the specified channel.

            Args:
                input_channel (str):
                    Specifies which input channel to read from.
                    Options are: A, B, C(1 - 5), D(1 - 5).

            Returns:
                (dict):
                    {"high_state": bool, "low_state": bool}

        """
        response = self.query("ALARMST? " + str(input_channel))
        separated_response = response.split(",")
        return {"high_state": bool(int(separated_response[0])),
                "low_state": bool(int(separated_response[1]))}

    def reset_alarm_status(self):
        """Clears the high and low status of all alarms."""
        self.command("ALMRST")

    def set_curve_header(self, curve_number, curve_header):
        """Configures the user curve header.

            Args:
                curve_number (int):
                    Specifies which curve to configure.
                    Options are: 21 - 59.
                curve_header (Model224CurveHeader):
                    A Model224CurveHeader class object containing the desired curve information.

        """
        command_string = (f"CRVHDR {curve_number},{curve_header.curve_name},{curve_header.serial_number}," +
                        f"{curve_header.curve_data_format},{curve_header.temperature_limit},{curve_header.coefficient}")

        self.command(command_string)

    def get_curve_header(self, curve):
        """Returns parameters set on a particular user curve header.

            Args:
                curve (int):
                    Specifies a curve to retrieve.
                    Options are: 21 - 59.

            Returns:
                header (Model224CurveHeader):
                    A Model224CurveHeader class object containing the desired curve information.

        """
        response = self.query(f"CRVHDR? {curve}")
        curve_header = response.split(",")
        header = Model224CurveHeader(str(curve_header[0]),
                                     str(curve_header[1]),
                                     self.CurveFormat(int(curve_header[2])),
                                     float(curve_header[3]),
                                     self.CurveTemperatureCoefficients(int(curve_header[4])))

        return header

    def set_curve_data_point(self, curve, index, sensor_units, temperature):
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

        """
        self.command(f"CRVPT {curve},{index},{sensor_units},{temperature}")

    def get_curve_data_point(self, curve, index):
        """Returns a standard or user curve data point.

            Args:
                curve (int):
                    Specifies which curve to query.
                index (int):
                    Specifies the points index in the curve.

            Returns:
                curve_point (tuple):
                    (sensor_units: float, temp_value: float)).

        """
        curve_point = self.query(f"CRVPT? {curve},{index}").split(",")
        return float(curve_point[0]), float(curve_point[1])

    def delete_curve(self, curve):
        """Deletes the user curve.

            Args:
                curve (int):
                    Specifies a user curve to delete.

        """
        self.command(f"CRVDEL {curve}")

    def generate_and_apply_soft_cal_curve(self, source_curve, curve_number, serial_number, calibration_point_1,
                                          calibration_point_2=(0, 0), calibration_point_3=(0, 0)):
        """Creates a SoftCal curve from 1-3 temperature/sensor points and a standard curve.

            Inputs generated curve into the given curve number.

            Args:
                source_curve (Model224SoftCalSensorTypes):
                    The standard curve to use to generate the SoftCal curve from along with calibration points.
                curve_number (int):
                    The curve number to save the generated curve to.
                    Options are: 21 - 59.
                serial_number (str):
                    Serial number of the user curve.
                    Maximum of 10 characters.
                calibration_point_1 (tuple):
                    Tuple of two floats in the form (temperature_value, sensor_value).
                calibration_point_2 (tuple):
                    Tuple of two floats in the form (temperature_value, sensor_value). Optional Parameter.
                calibration_point_3 (tuple):
                    Tuple of two floats in the form (temperature_value, sensor_value). Optional parameter.

        """
        command_string = (f"SCAL {source_curve},{curve_number},{serial_number}," +
                            f"{calibration_point_1[0]},{calibration_point_1[1]}," +
                            f"{calibration_point_2[0]},{calibration_point_2[1]}," +
                            f"{calibration_point_3[0]},{calibration_point_3[1]}")
        self.command(command_string)

    def get_curve(self, curve):
        """Returns a list of all the data points in a particular curve.

            Args:
                curve (int):
                    Specifies which curve to set.

            Return:
                data_points (list):
                    A list containing every point in the curve represented as a tuple
                    (sensor_units: float, temp_value: float).

        """

        data_points = []
        true_point_index = 0
        for i in range(0, 200):
            point = self.get_curve_data_point(curve, i + 1)
            data_points.append(point)
            if point[0] != 0 or point[1] != 0:
                true_point_index = i

        # Remove all extraneous points
        data_points = data_points[:true_point_index + 1]

        return data_points

    def set_curve(self, curve, data_points):
        """Method to define a user curve using a list of data points.

            Args:
                curve (int):
                    Specifies which curve to set.
                data_points (list):
                    A list containing every point in the curve represented as a tuple
                        (sensor_units: float, temp_value: float).

        """

        self.delete_curve(curve)

        for index, point in data_points:
            self.set_curve_data_point(curve, index + 1, point[0], point[1])

    def get_relay_status(self, relay_channel):
        """Returns whether the specified relay is On or Off.

            Args:
                relay_channel (int):
                    The relay channel to query.
                    Options are: 1 or 2.

            Returns:
                (bool):
                    True if relay is on, False if relay is off.
        """
        return bool(int(self.query(f"RELAYST? {str(relay_channel)}")))

    def set_filter(self, input_channel, filter_enabled, number_of_points=8, filter_reset_threshold=10):
        """Enables or disables a filter for the readings of the specified input channel.

            Filter is a running average that smooths input readings exponentially.

            Args:
                input_channel (str):
                    The input to set or disable a filter for.
                    Options are: A, B, C(1 - 5), D(1 - 5).
                filter_enabled (bool):
                    Enables or disables a filter for the input channel.
                    True for enabled, False for disabled.
                number_of_points (int):
                    Specifies the number of points used for the filter.
                    Inputting a larger number of points will slow down the instrument's response to changes in
                    temperature.
                    Options are: 2 - 64
                    Optional if disabling the filter function.
                filter_reset_threshold (int):
                    Specifies the limit for restarting the filter, represented by a percent of the full scale reading.
                    If raw reading differs from filtered value by more than this threshold, filter averaging resets.
                    Options are: 1% - 10%.
                    Optional if disabling the filter function.

        """
        self.command("FILTER " + str(input_channel) + "," + str(int(filter_enabled)) + "," + str(number_of_points) +
                     "," + str(filter_reset_threshold))

    def get_filter(self, input_channel):
        """Retrieves information about the filter set on the specified input channel.

            Args:
                input_channel (str):
                    The input to query for filter information.
                    Options are: A, B, C(1 - 5), D(1 - 5).

            Returns:
                (dict):
                    {"filter_enabled": bool, "number_of_points": int, "filter_reset_threshold": int}

        """
        filter_information = self.query(f"FILTER? {str(input_channel)}")
        separated_information = filter_information.split(",")
        return {'filter_enabled': bool(int(separated_information[0])),
                'number_of_points': int(separated_information[1]),
                'filter_reset_threshold': int(separated_information[2])}

    def configure_input(self, input_channel, settings):
        """Configures a sensor for measurement input readings.

            Args:
                input_channel (str):
                    The input to configure the input for.
                    Options are: A, B, C(1 - 5), D(1 - 5).

                settings (Model224InputSensorSettings):
                    Object of the Model224InputSensorSettings containing information for sensor setup.

        """
        command_string = (f"INTYPE {input_channel},{settings.sensor_type},{int(settings.autorange_enabled)}," +
                        f"{settings.sensor_range},{int(settings.compensation)},{settings.preferred_units}")
        self.command(command_string)

    def disable_input(self, input_channel):
        """Disables the selected input channel.

            Args:
                input_channel (str):
                    The input to disable.
                    Options are: A, B, C(1 - 5), D(1 - 5).

        """
        # Fill all parameters with 0 to disable
        self.command(f"INTYPE {str(input_channel)},0,0,0,0,0")

    def get_input_configuration(self, input_channel):
        """Returns the configuration settings of the sensor at the specified input channel.

            Args:
                input_channel (str):
                    The input to query.
                    Options are: A, B, C(1 - 5), D(1 - 5).

            Returns:
                (Model224InputSensorSettings):
                    Object of type Model224InputSensorSettings containing information about the sensor at the given
                    input_channel.

        """
        settings_string = self.query(f"INTYPE? {str(input_channel)}")
        separated_settings = settings_string.split(",")
        # Convert sensor_range depending on sensor type
        sensor_type = int(separated_settings[0])
        if sensor_type == 1:
            sensor_range = self.DiodeSensorRange(int(separated_settings[2]))
        elif sensor_type == 2:
            sensor_range = self.PlatinumRTDSensorResistanceRange(int(separated_settings[2]))
        elif sensor_type == 3:
            sensor_range = self.NTCRTDSensorResistanceRange(int(separated_settings[2]))
        else:
            # Sensor is disabled
            sensor_range = None
        # Create object
        return Model224InputSensorSettings(self.InputSensorType(sensor_type),
                                           self.InputSensorUnits(int(separated_settings[4])),
                                           sensor_range,
                                           bool(int(separated_settings[1])),
                                           bool(int(separated_settings[3])))

    def select_remote_interface(self, remote_interface):
        """Selects the remote interface to use for communications.

            Args:
                remote_interface (Model224RemoteInterface):
                    Object of enum type Model224RemoteInterface, representing the type of interface used for
                    communications.

        """
        self.command(f"INTSEL {remote_interface}")

    def get_remote_interface(self):
        """Returns the remote interface being used for communications.

            Returns:
                (Model224RemoteInterface):
                    Object of enum type Model224RemoteInterface representing the interface being used for
                    communications.

        """
        interface_number = int(self.query("INTSEL?"))
        return self.RemoteInterface(interface_number)

    def select_interface_mode(self, interface_mode):
        """Selects the mode for the remote interface being used.

            Args:
                interface_mode (Model224InterfaceMode):
                    Object of enum type Model224InterfaceMode representing the desired communication mode.

        """
        self.command(f"MODE {interface_mode}")

    def get_interface_mode(self):
        """Returns the mode of the remote interface.

            Returns:
                (Model224InterfaceMode):
                    Object of enum type Model224InterfaceMode representing the communication mode.

        """
        mode_number = int(self.query("MODE?"))
        return self.InterfaceMode(mode_number)

    def set_display_field_settings(self, field, input_channel, display_units):
        """Configures a display field in custom display mode.

            Args:
                field (int):
                    Specifies which display field to configure.
                    Options are: 1 - 8.
                input_channel (Model224InputChannel):
                    Defines which input to display.
                display_units (Model224DisplayFieldUnits):
                    Defines which units to display reading in.

        """
        self.command(f"DISPFLD {field},{input_channel},{display_units}")

    def get_display_field_settings(self, field):
        """Returns the settings of a single display field in custom display mode.

            Args:
                field (int):
                    Specifies the display field to query.
                    Options are: 1 - 8.

            Returns:
                (dict):
                    {"input_channel": Model224InputChannel, "display_units": Model224DisplayFieldUnits}

        """
        display_field_settings = self.query("DISPFLD? " + str(field))
        separated_settings = display_field_settings.split(",")
        return {'input_channel': self.InputChannel(int(separated_settings[0])),
                'display_units': self.DisplayFieldUnits(int(separated_settings[1]))}

    def configure_display(self, display_mode, number_of_fields=0):
        """Configures the display of the instrument.

            Args:
                display_mode (Model224DisplayMode):
                    Defines what mode to set the display in.
                    Mode either defines which input to display, or sets up a custom display using display fields.
                number_of_fields (Model224NumberOfFields):
                    Defines the number of display locations to display.
                    Only valid if mode is set to CUSTOM.

        """
        self.command(f"DISPLAY {display_mode},{number_of_fields}")

    def get_display_configuration(self):
        """Returns the mode of the display.

            If display mode is Custom, this method also returns the number of display fields in the custom display.

            Returns:
                (dict):
                    {"display_mode": DisplayMode, "number_of_fields": NumberOfFields}.

        """
        display_settings_string = self.query("DISPLAY?")
        separated_settings = display_settings_string.split(",")
        display_mode = int(separated_settings[0])
        if display_mode != 4:
            return_dictionary = {'display_mode': self.DisplayMode(display_mode),
                                 'number_of_fields': None}
        else:
            number_of_fields = int(separated_settings[1])
            return_dictionary = {'display_mode': self.DisplayMode(display_mode),
                                 'number_of_fields': self.NumberOfFields(number_of_fields)}
        return return_dictionary

    def turn_relay_on(self, relay_number):
        """Turns the specified relay on.

            Args:
                relay_number (int):
                    The relay to turn on. Options are: 1 or 2.

        """
        self.command(f"RELAY {relay_number},1,0,0")

    def turn_relay_off(self, relay_number):
        """Turns the specified relay off.

            Args:
                relay_number (int):
                    The relay to turn off. Options are: 1 or 2.

        """
        self.command(f"RELAY {relay_number},0,0,0")

    def set_relay_alarms(self, relay_number, activating_input_channel, alarm_relay_trigger_type):
        """Sets a relay to turn on and off automatically based on the state of the alarm of the specified input channel.

            Args:
                relay_number (int):
                    The relay to configure. Options are: 1 or 2.
                activating_input_channel (str):
                    Specifies which input alarm activates the relay when the relay is in alarm mode.
                    Only applies if ALARM mode is chosen. Options are: A, B, C(1 - 5), D(1 - 5).
                alarm_relay_trigger_type (Model224RelayControlAlarm):
                    Specifies the type of alarm that triggers the relay.
                    Only applies if ALARM mode is chosen.

        """
        self.command(f"RELAY {relay_number},2,{activating_input_channel},{alarm_relay_trigger_type}")

    def get_relay_alarm_control_parameters(self, relay_number):
        """Returns the relay alarm configuration for either of the two configurable relays.

            Relay must be configured for alarm mode to retrieve parameters.

            Args:
                relay_number (int):
                    Specifies which relay to query. Options are: 1 or 2.

            Return:
                (dict):
                    {"activating_input_channel": str, "alarm_relay_trigger_type": Model224RelayControlAlarm}.

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
                    Specifies which relay to query. Options are: 1 or 2.

            Returns:
                (Model224RelayControlMode):
                    The configured mode of the relay, represented as an object of the enum type
                    Model224RelayControlMode.

        """
        relay_settings = self.query("RELAY? " + str(relay_number))
        split_relay_settings = relay_settings.split(",")
        return self.RelayControlMode(int(split_relay_settings[0]))

    def _get_identity(self):
        return self.query('*IDN?', check_errors=False).split(',')


__all__ = ['Model224', 'Model224AlarmParameters', 'Model224CurveHeader', 'Model224StandardEventRegister',
           'Model224InputSensorSettings', 'Model224ReadingStatusRegister', 'Model224ServiceRequestRegister',
           'Model224StatusByteRegister']
