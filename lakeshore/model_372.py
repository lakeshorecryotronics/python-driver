"""Implements functionality unique to the Lake Shore Model 372 AC bridge and temperature controller."""
from .model_372_enums import Model372Enums
from .temperature_controllers import TemperatureController, CurveHeader, StandardEventRegister, OperationEvent
from .generic_instrument import RegisterBase

Model372CurveHeader = CurveHeader
Model372OperationEventRegister = OperationEvent
Model372StandardEventRegister = StandardEventRegister


class Model372InputChannelSettings:
    """Class object representing parameters for the channel settings of an self.InputChannel."""

    def __init__(self,
                 enable,
                 dwell_time,
                 pause_time,
                 curve_number,
                 temperature_coefficient=None):
        """The constructor for Model372InputChannelSettings class.

            Args:
                enable (bool):
                    Whether to enable or disable input.
                dwell_time (int):
                    Specifies a value for the auto-scanning dwell time in seconds. Not applicable to control input.
                    Options are: 1 to 200 s.
                pause_time (int):
                    Specifies a value for the change pause time in seconds. Options are:
                    3 to 200 s.
                curve_number (int):
                    Specifies which calibration curve to use on input sensor. Options are:
                    0 (none), or 1 - 59.
                temperature_coefficient (self.CurveTemperatureCoefficient):
                    Sets coefficient for temperature control if no curve is selected.

        """
        self.enable = enable
        self.dwell_time = dwell_time
        self.pause_time = pause_time
        self.curve_number = curve_number
        self.temperature_coefficient = temperature_coefficient


class Model372InputSetupSettings:
    """Class object representing parameters for the sensor and measurement settings of an self.InputChannel."""

    def __init__(self,
                 mode,
                 excitation_range,
                 auto_range,
                 current_source_shunted,
                 units,
                 resistance_range=None):
        """The constructor for Model372InputSetupSettings class.

            Args:
                mode (self.SensorExcitationMode):
                    Determines whether to use current or voltage for sensor excitation.
                excitation_range (IntEnum):
                    The voltage or current (depending on mode) excitation range.
                auto_range (Model372AutoRangeMode):
                    Specifies whether auto range is Off, Auto-ranging Current, or in ROX 102B mode.
                current_source_shunted (bool):
                    Specifies whether the current source is shunted. If current source is shunted,
                    excitation is off. If current source is not shunted, excitation is on.
                units (self.InputSensorUnits):
                    Specifies the preferred units, Kelvin or Ohms, for the sensor.
                resistance_range (Model372MeasurementInputResistance):
                    For measurement inputs only, specifies the measurement input resistance range.

        """
        self.mode = mode
        self.excitation_range = excitation_range
        self.auto_range = auto_range
        self.resistance_range = resistance_range
        self.current_source_shunted = current_source_shunted
        self.units = units


class Model372HeaterOutputSettings:
    """Class object representing parameters to configure Heater Output Settings."""

    def __init__(self,
                 output_mode,
                 input_channel,
                 powerup_enable,
                 reading_filter,
                 delay,
                 polarity=None):
        """The constructor for Model372HeaterOutputSettings class.

            Args:
                output_mode (self.OutputMode):
                    The control or output mode to configure the heater for. Defines how the output is controlled.
                input_channel (self.InputChannel):
                    Which input to control output from in a control loop.
                powerup_enable (bool):
                    Specifies whether output stays on after powerup cycle.
                    True if enabled, False if disabled.
                reading_filter (bool):
                    Specifies whether readings are filtered on unfiltered.
                    True if filtered, False if unfiltered.
                delay (int):
                    Specifies delay in seconds for set-point during AutoScanning. Options are:
                    1 - 255.
                polarity (self.Polarity):
                    Specifies output polarity. Not applicable to warmup heater.

        """
        self.output_mode = output_mode
        self.input_channel = input_channel
        self.powerup_enable = powerup_enable
        self.polarity = polarity
        self.reading_filter = reading_filter
        self.delay = delay


class Model372AlarmParameters:
    """Sets up an alarm for an input channel."""

    def __init__(self,
                 high_value,
                 low_value,
                 deadband,
                 latch_enable,
                 audible=None,
                 visible=None):
        """The constructor for Model372AlarmParameters class.

            Args:
                high_value (int):
                    Sets value for source to be checked against to set high alarm.
                low_value (int):
                    Sets value for source to be checked against to set low alarm.
                deadband (int):
                    Sets value that source must change outside an alarm condition
                    to deactivate an unlatched alarm.
                latch_enable (bool):
                    Specifies if alarm is latched or not.
                audible (bool):
                    Specifies if an alarm is audible or not.
                visible (bool):
                    Specifies if an alarm is visible via LED on front panel or not.

        """
        self.high_value = high_value
        self.low_value = low_value
        self.deadband = deadband
        self.latch_enable = latch_enable
        self.audible = audible
        self.visible = visible


class Model372ControlLoopZoneSettings:
    """Defines the parameters to set up a Control Loop."""

    def __init__(self,
                 upper_bound,
                 p_value,
                 i_value,
                 d_value,
                 manual_output,
                 heater_range,
                 ramp_rate,
                 relay_1,
                 relay_2):
        """The constructor for Model372ControlLoopZoneSettings class.

            Args:
                upper_bound (float):
                    Upper bound setpoint in Kelvin.
                p_value (float):
                    The gain for a PID system. Options are:
                    0.0 - 1000.
                i_value (float):
                    The integral value for a PID system. Options are:
                    0 - 10000.
                d_value (float):
                    The rate for a PID system. Options are:
                    0 - 2500.
                manual_output (float):
                    Percentage full scale manual output.
                heater_range (float or bool):
                    Heater range for the control zone.
                    Entered as a float for the sample heater.
                    Entered as a bool for the warm-up heater.
                ramp_rate (float):
                    Specifies ramp rate for this zone.
                relay_1 (bool):
                    Specifies if relay 1 is on or off.
                    Only applicable if relay is configured in zone mode and relay's control
                    output matches configured output.
                relay_2 (bool):
                    Specifies if relay 2 is on or off.
                    Only applicable if relay is configured in zone mode and relay's control
                    output matches configured output.

        """
        self.upper_bound = upper_bound
        self.p_value = p_value
        self.i_value = i_value
        self.d_value = d_value
        self.manual_output = manual_output
        self.heater_range = heater_range
        self.ramp_rate = ramp_rate
        self.relay_1 = relay_1
        self.relay_2 = relay_2


class Model372ReadingStatusRegister(RegisterBase):
    """Class object representing the reading status of an input.

        While not a literal register, the return of an int representation of multiple booleans makes it convenient to
        represent this functionality as a register.
    """
    bit_names = [
        "current_source_overload",
        "voltage_common_mode_stage_overload",
        "voltage_mixer_stage_overload",
        "voltage_differential_stage_overload",
        "resistance_over",
        "resistance_under",
        "temperature_over",
        "temperature_under"
    ]

    def __init__(self,
                 current_source_overload,
                 voltage_common_mode_stage_overload,
                 voltage_mixer_stage_overload,
                 voltage_differential_stage_overload,
                 resistance_over,
                 resistance_under,
                 temperature_over,
                 temperature_under):
        self.current_source_overload = current_source_overload
        self.voltage_common_mode_stage_overload = voltage_common_mode_stage_overload
        self.voltage_mixer_stage_overload = voltage_mixer_stage_overload
        self.voltage_differential_stage_overload = voltage_differential_stage_overload
        self.resistance_over = resistance_over
        self.resistance_under = resistance_under
        self.temperature_over = temperature_over
        self.temperature_under = temperature_under


class Model372StatusByteRegister(RegisterBase):
    """Class representing the status byte register."""
    bit_names = [
        "warmup_heater_ramp_done",
        "valid_reading_control_input",
        "valid_reading_measurement_input",
        "alarm",
        "sensor_overload",
        "event_summary",
        "request_service_master_summary_status",
        "sample_heater_ramp_done"
    ]

    def __init__(self,
                 warmup_heater_ramp_done,
                 valid_reading_control_input,
                 valid_reading_measurement_input,
                 alarm,
                 sensor_overload,
                 event_summary,
                 request_service_master_summary_status,
                 sample_heater_ramp_done):
        self.warmup_heater_ramp_done = warmup_heater_ramp_done
        self.valid_reading_control_input = valid_reading_control_input
        self.valid_reading_measurement_input = valid_reading_measurement_input
        self.alarm = alarm
        self.sensor_overload = sensor_overload
        self.event_summary = event_summary
        self.request_service_master_summary_status = request_service_master_summary_status
        self.sample_heater_ramp_done = sample_heater_ramp_done


class Model372ServiceRequestEnable(RegisterBase):
    """Class representing the status byte register."""
    bit_names = [
        "warmup_heater_ramp_done",
        "valid_reading_control_input",
        "valid_reading_measurement_input",
        "alarm",
        "sensor_overload",
        "event_summary",
        "",
        "sample_heater_ramp_done"
    ]

    def __init__(self,
                 warmup_heater_ramp_done,
                 valid_reading_control_input,
                 valid_reading_measurement_input,
                 alarm,
                 sensor_overload,
                 event_summary,
                 sample_heater_ramp_done):
        self.warmup_heater_ramp_done = warmup_heater_ramp_done
        self.valid_reading_control_input = valid_reading_control_input
        self.valid_reading_measurement_input = valid_reading_measurement_input
        self.alarm = alarm
        self.sensor_overload = sensor_overload
        self.event_summary = event_summary
        self.sample_heater_ramp_done = sample_heater_ramp_done


class Model372DigitalOutputRegister(RegisterBase):
    """Class representing the digital output register."""
    bit_names = [
        "d_1",
        "d_2",
        "d_3",
        "d_4",
        "d_5",
    ]

    def __init__(self, d_1, d_2, d_3, d_4, d_5):
        self.d_1 = d_1
        self.d_2 = d_2
        self.d_3 = d_3
        self.d_4 = d_4
        self.d_5 = d_5


class Model372(Model372Enums, TemperatureController):
    """A class object representing the Lake Shore Model 372 AC bridge and temperature controller."""

    vid_pid = [(0x1FB9, 0x0305)]

    # Initialize registers
    _status_byte_register = Model372StatusByteRegister
    _service_request_enable = Model372ServiceRequestEnable

    def __init__(self,
                 baud_rate,
                 serial_number=None,
                 com_port=None,
                 timeout=2.0,
                 ip_address=None,
                 tcp_port=7777,
                 **kwargs):

        # Call the parent init, then fill in values specific to the 372
        TemperatureController.__init__(self, serial_number, com_port, baud_rate, timeout, ip_address,
                                       tcp_port, **kwargs)
        # Disable emulation upon initialization
        self._disable_emulation_mode()

    def clear_interface(self):
        """Clears the interface.

            Clears all bits in the status byte register and the standard event status register. Does not clear the
            instrument.
        """
        self.command("*CLS")

    def reset_instrument(self):
        """Resets the instrument to power-up settings and parameters."""
        self.command("*RST")

    def _disable_emulation_mode(self):
        """Disables software emulation for the Model 370. The rest of the driver does not support emulation mode."""
        self.command("EMUL 0")

    def set_display_settings(self, mode, number_of_fields="", displayed_info=""):
        """Sets which parameters to display and how to display them.

            Args:
                mode (self.DisplayMode):
                    Sets the input to monitor on the display, or configures display for custom.
                number_of_fields (self.DisplayFields):
                    Configures the number of display fields to include in a custom display.
                displayed_info (self.DisplayInfo):
                    Determines whether to display information about the loop of the active scan channel or
                    a specific heater in the bottom left of the display in custom mode.

        """
        self.command(f"DISPLAY {mode},{number_of_fields},{displayed_info}")

    def get_display_mode(self):
        """Returns the current mode of the display.

            Returns:
                (self.DisplayMode):
                    Enumerated object representing the current mode of the display.

        """
        settings_string = self.query("DISPLAY?")
        separated_settings = settings_string.split(",")
        return self.DisplayMode(int(separated_settings[0]))

    def get_custom_display_settings(self):
        """Returns the settings of the display in custom mode.

            Returns:
                (dict):
                    mode: self.DisplayMode,
                    number_of_fields: self.DisplayFields,
                    displayed_info: self.DisplayInfo

        """
        settings_string = self.query("DISPLAY?")
        separated_settings = settings_string.split(",")
        return {'mode': self.DisplayMode(int(separated_settings[0])),
                'number_of_fields': self.DisplayFields(int(separated_settings[1])),
                'displayed_info': self.DisplayInfo(int(separated_settings[2]))}

    def get_resistance_reading(self, input_channel):
        """Returns the input reading in Ohms.

            Args:
                input_channel (str or int):
                    Specifies which input channel to read from. Options are:
                    1-16, or "A" (for control input).

            Returns:
                (float):
                    Sensor reading in Ohms.

        """
        return float(self.query(f"RDGR? {str(input_channel)}"))

    def get_quadrature_reading(self, input_channel):
        """Returns the imaginary part of the reading in Ohms. Only valid for measurement inputs.

            Args:
                input_channel (int):
                    Specifies which input channel to read from. Options are:
                    1-16.

            Returns:
                (float):
                    The imaginary part of the sensor reading, in Ohms.
        """
        return float(self.query(f"QRDG? {str(input_channel)}"))

    def get_all_input_readings(self, input_channel):
        """Returns the kelvin reading, resistance reading, and, if a measurement input, the quadrature reading.

            Args:
                input_channel (str or int):
                    Specifies which input channel to read from. Options are:
                    1-16, or "A" (for control input).

            Returns:
                (dict):
                    * If measurement input:
                        * {kelvin: float, resistance: float, power: float, quadrature: float)
                    * If control input:
                        * {kelvin: float, resistance: float, power: float}

        """
        if input_channel == "A":
            readings = {"kelvin": self.get_kelvin_reading(input_channel),
                        "resistance": self.get_resistance_reading(input_channel),
                        "power": self.get_excitation_power(input_channel)}
        else:
            readings = {"kelvin": self.get_kelvin_reading(input_channel),
                        "resistance": self.get_resistance_reading(input_channel),
                        "power": self.get_excitation_power(input_channel),
                        "quadrature": self.get_quadrature_reading(input_channel)}

        return readings

    def get_input_setup_parameters(self, input_channel):
        """Returns the settings on the specified input.

            Args:
                input_channel (str or int):
                    Specifies which input channel to read from. Options are:
                    1-16, or "A" (control input).

            Returns:
                input_sensor_settings (Model372InputSetupSettings):
                    object of Model372InputSetupSettings representing the parameters of the excitation of the sensor
                    on the specified channel

        """
        sensor_settings = self.query(f"INTYPE? {str(input_channel)}")
        separated_settings = sensor_settings.split(",")
        # Determine which enum to use to interpret excitation value:
        if input_channel == "A":
            excitation_range = self.ControlInputCurrentRange(int(separated_settings[1]))
            resistance_range = None
        # Check if excitation mode is voltage or current
        elif int(separated_settings[0]) == self.SensorExcitationMode.VOLTAGE:
            excitation_range = self.MeasurementInputVoltageRange(int(separated_settings[1]))
            resistance_range = self.MeasurementInputResistance(int(separated_settings[3]))
        else:
            excitation_range = self.MeasurementInputCurrentRange(int(separated_settings[1]))
            resistance_range = self.MeasurementInputResistance(int(separated_settings[3]))

        input_sensor_settings = Model372InputSetupSettings(self.SensorExcitationMode(int(separated_settings[0])),
                                                           excitation_range,
                                                           self.AutoRangeMode(int(separated_settings[2])),
                                                           bool(int(separated_settings[4])),
                                                           self.InputSensorUnits(int(separated_settings[5])),
                                                           resistance_range)
        return input_sensor_settings

    def configure_input(self, input_channel, settings):
        """Sets the desired setup settings on the specified input.

            Args:
                input_channel (str or int):
                    Specifies which input channel to read from. Options are:
                    1-16, or "A" (control input).
                settings (Model372InputSetupSettings):
                    Object of Model372InputSetupSettings representing the parameters of the excitation of the sensor
                    on the specified channel.

        """
        # Handle control input not setting resistance range
        if input_channel == "A":
            resistance_range = 0
        else:
            resistance_range = format(settings.resistance_range)
        # Format command string
        command_string = (f"INTYPE {str(input_channel)},{str(format(settings.mode))}," +
                         f"{str(format(settings.excitation_range))},{str(format(settings.auto_range))}," +
                         f"{str(resistance_range)},{str(int(settings.current_source_shunted))}," +
                         f"{str(format(settings.units))}")
        self.command(command_string)

    def disable_input(self, input_channel):
        """Disables the desired input channel.

            Args:
                input_channel (str or int):
                    Specifies which input channel to disable. Options are:
                    1-16, or "A" (control input).

        """
        self.command(f"INSET {str(input_channel)},0,0,0,0,0")

    def get_input_channel_parameters(self, input_channel):
        """Returns the settings on the specified input channel.

                Args:
                    input_channel (str or int):
                        Specifies which input channel to read from. Options are:
                        1-16, or "A" (control input).

                Returns:
                    input_channel_settings (Model372InputChannelSettings):
                        Contains variables representing the different channel settings parameters.

        """
        input_parameters = self.query(f"INSET? {str(input_channel)}")
        separated_parameters = input_parameters.split(",")
        temperature_coefficient = self.CurveTemperatureCoefficient(int(separated_parameters[4]))
        input_channel_settings = Model372InputChannelSettings(bool(int(separated_parameters[0])),
                                                              int(separated_parameters[1]),
                                                              int(separated_parameters[2]),
                                                              int(separated_parameters[3]),
                                                              temperature_coefficient)
        return input_channel_settings

    def set_input_channel_parameters(self, input_channel, settings):
        """Sets the desired channel settings on the specified input channel.

            Args:
                input_channel (str or int):
                    Specifies which input channel to read from. Options are:
                    1-16, or
                    "A" (control input).
                settings (Model372InputChannelSettings):
                    Defines how to set the various parameters.

        """
        if settings.temperature_coefficient is None:
            temperature_coefficient = ""
        else:
            temperature_coefficient = format(settings.temperature_coefficient)
        command_string = (f"INSET {str(input_channel)},{str(int(settings.enable))}," +
                         f"{str(settings.dwell_time)},{str(settings.pause_time)}," +
                         f"{str(settings.curve_number)},{str(temperature_coefficient)}")
        self.command(command_string)

    def get_analog_heater_output(self, output_channel):
        """Returns the output of the warm-up or analog/still heater.

            Args:
                output_channel (int):
                    Specifies which heater to read from. Options:
                        1 output 1 (warm up heater), or
                        2 output 2 (analog heater).

            Returns:
                reading (float):
                    Output of the analog heater being queried.

        """
        return float(self.query(f"AOUT? {str(output_channel)}"))

    def all_off(self):
        """Recreates the front panel safety feature of shutting off all heaters."""
        self.command("RANGE 0,0")
        self.command("RANGE 1,0")
        self.command("RANGE 2,0")

    def set_heater_output_range(self, output_channel, heater_range):
        """Sets the output range.

            Args:
                output_channel (int):
                    Specifies which heater to set. Options:
                    0: sample heater,
                    1: output 1 (warm up heater), or
                    2: output 2 (analog heater).
                heater_range (Enum or bool):
                    Specifies the range of the output. Options:
                    Sample Heater (Enum) - Object of type self.SampleHeaterOutputRange.
                    Warmup Heater/Still Heater (bool) - False: output off, True: output on.

        """
        if output_channel == 0:
            range_value = format(heater_range)
        else:
            range_value = int(heater_range)

        self.command(f"RANGE {str(output_channel)},{str(range_value)}")

    def get_heater_output_range(self, output_channel):
        """Return's the range of the output on a given channel.

            Args:
                output_channel (int):
                    Specifies which heater to read from. Options:
                    0: sample heater,
                    1: output 1 (warm up heater), or
                    2: output 2 (analog heater).

            Returns:
                heater_range (bool or Enum):
                    If channel 1 or 2, returns bool for if output is on or off.
                    If channel 0, an object of enum type SampleHeaterOutputRange.

        """
        key = int(self.query(f"RANGE? {str(output_channel)}"))
        if output_channel == 0:
            output_range = self.SampleHeaterOutputRange(key)
        else:
            output_range = bool(key)

        return output_range

    # Filter methods different from in temperature_instrument
    def set_filter(self, input_channel, state, settle_time, window):
        """Sets a filter for the specified input channel.

            Args:
                input_channel (str or int):
                    Specifies which input channel to read from. Options are:
                    0 (all channels/measurement inputs),
                    1-16, or
                    "A" (control input).
                state (bool):
                    Specifies whether to turn filter on or off. Options are:
                    False for off, or
                    True for on.
                settle_time (float):
                    Specifies filter settle time. Options are:
                    1 - 200 s.
                window (float):
                    Specifies what percent of full scale reading limits the filtering function. Options are:
                    1 - 80.

        """

        self.command(f"FILTER {str(input_channel)},{str(int(state))},{str(settle_time)},{str(window)}")

    def get_filter(self, input_channel):
        """Returns information about the filter set on the specified channel.

            Args:
                input_channel (str or int):
                    Specifies which input channel to read from. Options are:
                    1-16, or "A" (control input).

            Returns:
                state (bool):
                    Specifies whether to turn filter on or off.
                settle_time (int):
                    Specifies filter settle time.
                window (int):
                    Specifies what percent of full scale reading limits the filtering function.

        """
        output_string = self.query(f"FILTER? {str(input_channel)}")
        separated_response = output_string.split(",")
        return {"state": bool(int(separated_response[0])),
                "settle_time": int(separated_response[1]),
                "window": int(separated_response[2])}

    def set_ieee_interface_parameter(self, address):
        """Sets the IEEE address of the instrument.

            Args:
                address (int):
                    Specifies the IEEE address. Options are:
                    1 - 30.

        """
        self.command(f"IEEE 0,0,{str(address)}")

    def get_ieee_interface_parameter(self):
        """Returns the IEEE address of the instrument.

            Returns:
                address (int):
                    The IEEE address.

        """
        return int(self.query("IEEE?"))

    def get_excitation_power(self, input_channel):
        """Returns the most recent power calculation for the selected input channel.

            Args:
                input_channel (str or int):
                    Specifies which input channel to read from. Options are:
                    1-16, or
                    "A" (control input).

            Returns:
                power (float):
                    Most recent power calculation for the input being queried.

        """
        return float(self.query(f"RDGPWR? {str(input_channel)}"))

    def get_heater_output_settings(self, output_channel):
        """Returns the mode and settings of the given output channel.

            Args:
                output_channel (int):
                    Specifies which heater to read from. Options:
                    0: sample heater,
                    1: output 1 (warm up heater), or
                    2: output 2 (analog heater).

            Returns:
                outputmode_settings (Model372HeaterOutputSettings):
                    Object of class Model372HeaterOutputSettings whose variables are set to reflect the
                    current output settings of the queried heater.

        """
        output_mode = self.query(f"OUTMODE? {str(output_channel)}")
        separated_response = output_mode.split(",")
        # Handle special case of control input not being an int
        if separated_response[1] == "A":
            input_channel = self.InputChannel('A')
        else:
            input_channel = self.InputChannel(int(separated_response[1]))

        return Model372HeaterOutputSettings(self.OutputMode(int(separated_response[0])),
                                            input_channel,
                                            bool(int(separated_response[2])),
                                            bool(int(separated_response[4])),
                                            int(separated_response[5]),
                                            self.Polarity(int(separated_response[3])))

    def configure_heater(self, output_channel, settings):
        """Sets up a heater output.

            Analog heaters (outputs 1 and 2) might need to configure further settings in configure_analog_heater.

            Args:
                output_channel (int):
                    Specifies which heater to read from. Options:
                    0: sample heater,
                    1: output 1 (warm up heater), or
                    2: output 2 (analog heater).
                settings (Model372HeaterOutputSettings):
                    Defines how to set the output mode settings.

        """
        if settings.polarity is None:
            polarity = 0
        else:
            polarity = format(settings.polarity)

        # Format input_channel since it does not use IntEnum
        if isinstance(settings.input_channel, self.InputChannel):
            input_channel = settings.input_channel.value
        else:
            input_channel = settings.input_channel

        command_string = (f"OUTMODE {str(output_channel)}," +
                         f"{str(format(settings.output_mode))}," +
                         f"{str(input_channel)}," +
                         f"{str(int(settings.powerup_enable))}," +
                         f"{str(polarity)}," +
                         f"{str(int(settings.reading_filter))}," +
                         f"{str(settings.delay)}")

        self.command(command_string)

    def set_common_mode_reduction(self, state):
        """Sets common mode reduction to given state for all measurement channels.

            Args:
                state (bool):
                    Sets CMR to enabled or disable. Options are:
                    False (for disable), or
                    True (for enable).

        """
        self.command(f"CMR {str(int(state))}")

    def get_common_mode_reduction(self):
        """Returns whether CMR is set for measurement channels.

            Returns:
                False (boolean) if CMR is disabled, or
                True (boolean) if CMR is enabled.

        """
        return bool(int(self.query("CMR?")))

    def set_scanner_status(self, input_channel, status):
        """Sets the scanner to the specified channel, and enables or disables auto scan.

            Args:
                input_channel (int):
                    Specifies which measurement input to set the scanner to. Options are:
                    1 - 16.
                status (bool):
                    Specifies whether to turn auto scan feature on. Options are:
                    False (disable), True (enable).

        """
        self.command(f"SCAN {str(input_channel)},{str(int(status))}")

    def get_scanner_status(self):
        """Returns which channel the scanner is on and whether the auto scan feature is enabled.

            Returns:
                input_channel (int):
                    The measurement channel the scanner is currently on.

                status (bool):
                    True if auto-scan in on, or
                    False if auto-scan is off.

        """
        response = self.query("SCAN?")
        separated_response = response.split(",")
        return {"input_channel": int(separated_response[0]),
                "status": bool(int(separated_response[1]))}

    def set_alarm_beep(self, status):
        """Enables or disables a beep for alarms.

            Args:
                status (bool):
                    False (for disable), or
                    True (for enable).

        """
        self.command(f"BEEP {str(int(status))}")

    def get_alarm_beep_status(self):
        """Returns whether beep for alarms is enabled or disabled.

            Returns
                status (bool):
                    True (beep is enabled), or
                    False (beep is disabled).

        """
        return bool(int(self.query("BEEP?")))

    def set_still_output(self, power):
        """Sets the still output of the still/analog heater to power% of full power.

            Heater gets configured for still mode if not currently configured.

            Args:
                power (float):
                    Specifies the percent of full power for still output. Options are:
                    0 - 100.

        """
        settings = self.get_heater_output_settings(2)
        settings.output_mode = self.OutputMode.STILL
        self.configure_heater(2, settings)
        self.command(f"STILL {str(power)}")

    def get_still_output(self):
        """Returns the percent of full power being outputted by still heater in still mode.

            Returns:
                    power (float):
                        Percent of full power being outputted by heater.

        """
        return float(self.query("STILL?"))

    def set_warmup_output(self, auto_control, current):
        """Sets up the warmup output to continuous control at the percent current specified.

            Configures the warmup heater for continuous control mode from the control input.

            Args:
                auto_control (bool):
                    Specifies whether to turn on auto control. Options are:
                    False for auto off, or
                    True for continuous.

                current (float):
                    Specifies percent of full current to apply to external output. Options are:
                    0 - 100

        """
        settings = self.get_heater_output_settings(1)
        settings.output_mode = self.OutputMode.WARMUP
        self.configure_heater(1, settings)
        self.command(f"WARMUP {str(int(auto_control))},{str(current)}")

    def get_warmup_output(self):
        """Returns the control setting and percent current outputted in the warmup heater in warmup mode.

            Returns:
                auto_control (bool):
                    Specifies whether to turn on auto control. Returns:
                    False for auto off, or
                    True for continuous

                current (float):
                    Specifies percent of full current to apply to external output.

        """
        output_string = self.query("WARMUP?")
        separated_response = output_string.split(",")
        return {'auto_control': bool(int(separated_response[0])),
                'current': float(separated_response[1])}

    def set_setpoint_kelvin(self, output_channel, setpoint):
        """Sets the control set-point in Kelvin. Changes input parameters so preferred units are Kelvin.

            Args:
                output_channel (int):
                    Specifies which heater to set a set-point. Options are:
                    0: sample heater, or
                    1: output 1 (warm up heater).

                setpoint (float):
                    Specifies the set-point the heater ramps to, in Kelvin.

        """
        # First, get control input from OUTMODE settings to change preferred units
        outmode_settings = self.get_heater_output_settings(output_channel)
        control_input = outmode_settings.input_channel.value
        settings = self.get_input_setup_parameters(control_input)
        settings.units = self.InputSensorUnits.KELVIN
        self.configure_input(control_input, settings)
        # Set setpoint now that units are configured properly
        self.command(f"SETP {str(output_channel)},{str(setpoint)}")

    def set_setpoint_ohms(self, output_channel, setpoint):
        """Sets the control set-point in Ohms. Changes input parameters so preferred units are Ohms.

            Args:
                output_channel (int):
                    Specifies which heater to set a set-point. Options are:
                    0: sample heater, or
                    1: output 1 (warm up heater).

                setpoint (float):
                    Specifies the set-point the heater ramps to, in Kelvin.

        """

        # First, get control input from OUTMODE settings to change preferred units
        outmode_settings = self.get_heater_output_settings(output_channel)
        control_input = outmode_settings.input_channel.value
        # Change settings to change preferred units to Ohms
        settings = self.get_input_setup_parameters(control_input)
        settings.units = self.InputSensorUnits.OHMS
        self.configure_input(control_input, settings)
        # Set setpoint
        self.command(f"SETP {str(output_channel)},{str(setpoint)}")

    def get_setpoint_kelvin(self, output_channel):
        """Returns the set-point for the given output channel in kelvin.

            Changes the control input's preferred units to Kelvin as a result.

            Args:
                output_channel (int):
                    Specifies which heater to set a set-point. Options are:
                    0: sample heater, or
                    1: output 1 (warm up heater).

            Returns:
                setpoint (float):
                    Set-point of the output in Kelvin.

        """
        outmode_settings = self.get_heater_output_settings(output_channel)
        control_input = outmode_settings.input_channel.value
        settings = self.get_input_setup_parameters(control_input)
        settings.units = self.InputSensorUnits.KELVIN
        self.configure_input(control_input, settings)
        return float(self.query(f"SETP? {str(output_channel)}"))

    def get_setpoint_ohms(self, output_channel):
        """Returns the set-point for the given output channel in kelvin.

            Changes the control input's preferred units to Kelvin as a result.

            Args:
                output_channel (int):
                    Specifies which heater to set a set-point. Options are:
                    0: sample heater, or
                    1: output 1 (warm up heater).

            Returns:
                setpoint (float):
                    Set-point of the output in Ohms.

        """
        outmode_settings = self.get_heater_output_settings(output_channel)
        control_input = outmode_settings.input_channel.value
        settings = self.get_input_setup_parameters(control_input)
        settings.units = self.InputSensorUnits.OHMS
        self.configure_input(control_input, settings)
        return float(self.query(f"SETP? {str(output_channel)}"))

    def get_excitation_frequency(self, input_channel):
        """Returns the excitation frequency in Hz for either the measurement or control inputs.

            Args:
                input_channel (int or str):
                    Specifies which input to get frequency from. Options are:
                    0 : measurement inputs, or
                    "A" : control input.

            Returns:
                frequency (Enum):
                    The excitation frequency in Hz, returned as an object of self.InputFrequency Enum type.

        """
        key = int(self.query(f"FREQ? {str(input_channel)}"))
        return self.InputFrequency(key)

    def set_excitation_frequency(self, input_channel, frequency):
        """Sets the excitation frequency (in Hz) for either the measurement or control inputs.

            Args:
                input_channel (int or str):
                    Specifies which input to get frequency from. Options are:
                    0 : measurement inputs, or
                    "A" : control input.

                frequency (Enum):
                    The excitation frequency in Hz (if float), represented as an object of type self.InputFrequency.

        """
        self.command(f"FREQ {input_channel},{frequency}")

    def set_digital_output(self, bit_weight):
        """Sets the status of the 5 digital output lines to high or low.

            Args:
                bit_weight (DigitalOutputRegister):
                    Determines which bits to set or reset.

        """
        bit_weight_integer = bit_weight.to_integer()
        self.command(f"DOUT {str(bit_weight_integer)}")

    def get_digital_output(self):
        """Returns which digital output bits are set or reset by representing them in a binary number.

            Returns:
                bit_weight (DigitalOutputRegister):
                    Determines which bits to set or reset.

        """
        bit_weight_integer = int(self.query("DOUT?"))
        return Model372DigitalOutputRegister.from_integer(bit_weight_integer)

    def set_interface(self, interface):
        """Sets the interface for the instrument to communicate over.

            Args:
                interface (self.Interface):
                    Selects the interface based on the values as defined in the self.Interface enum class.

        """
        self.command(f"INTSEL {interface}")

    def get_interface(self):
        """Returns the interface connected to the instrument.

            Returns:
                interface (self.Interface):
                    Returns the interface as an object of the self.Interface enum class.

        """
        value = int(self.query("INTSEL?"))
        return self.Interface(value)

    def set_alarm_parameters(self, input_channel, alarm_enable, alarm_settings=None):
        """Sets an alarm on the specified channel as defined by parameters.

            Args:
                input_channel (int or str):
                    Defines which channel to configure an alarm on. Options are:
                    0 for all measurement inputs,
                    1 - 16, or
                    "A" for control input.
                alarm_enable (bool)
                    Defines whether to turn alarm on or off.
                alarm_settings (Model372AlarmParameters)
                    Model372AlarmParameters object containing desired alarm settings.
                    Optional if alarm is disabled.

        """
        if alarm_settings is not None:
            if alarm_settings.visible is None:
                visible = ""
            else:
                visible = int(alarm_settings.visible)

            if alarm_settings.audible is None:
                audible = ""
            else:
                audible = int(alarm_settings.audible)

            # extra 0 added for unused data source parameter
            command_string = (f"ALARM {input_channel},{int(alarm_enable)},0,{alarm_settings.high_value}," +
                                f"{alarm_settings.low_value},{alarm_settings.deadband}," +
                                f"{int(alarm_settings.latch_enable)},{visible},{audible}")
            self.command(command_string)
        else:
            self.command(f"ALARM {input_channel},0,0,0,0,0,0,0")

    def get_alarm_parameters(self, input_channel):
        """Returns the parameters for the alarm set for the input at the specified channel.

            Args:
                input_channel (int or str):
                    Defines which channel to configure an alarm on. Options are: 1 - 16, or "A" for control input.

            Returns:
                (dict):
                    {"alarm_enable": bool, "alarm_settings": Model372AlarmParameters}

        """
        settings_string = self.query(f"ALARM? {str(input_channel)}")
        separated_settings = settings_string.split(",")
        alarm_settings = Model372AlarmParameters(int(separated_settings[2]),
                                                 int(separated_settings[3]), int(separated_settings[4]),
                                                 bool(int(separated_settings[5])), bool(int(separated_settings[6])),
                                                 bool(int(separated_settings[7])))

        return {'alarm_enable': bool(int(separated_settings[0])),
                'alarm_settings': alarm_settings}

    def set_relay_for_sample_heater_control_zone(self, relay_number):
        """Configures a relay to follow the sample heater output as part of a control zone.

            Settings can be further configured in set_control_loop_zone_parameters method.

            Args:
                relay_number (int):
                    The relay to configure. Options are: 1 or 2.

        """
        self.command(f"RELAY {relay_number},3,0,0")

    def set_relay_for_warmup_heater_control_zone(self, relay_number):
        """Configures a relay to follow the warm-up heater output as part of a control zone.

            Settings can be further configured in set_control_loop_zone_parameters method.

                Args:
                    relay_number (int):
                        The relay to configure. Options are: 1 or 2.

            """
        self.command(f"RELAY {relay_number},4,0,0")

    def get_ieee_interface_mode(self):
        """Returns the IEEE interface mode of the instrument.

            Returns:
                mode (self.InterfaceMode):
                    Returns the mode as an enum type of class self.InterfaceMode.

        """
        value = int(self.query("MODE?"))
        return self.InterfaceMode(value)

    def set_ieee_interface_mode(self, mode):
        """Sets the IEEE interface mode of the instrument.

            Args:
                mode (self.InterfaceMode):
                    Defines the mode of the instrument as an object of the enum type Model372IEEEInterfaceMode.

        """
        value = format(mode)
        self.command(f"MODE {str(value)}")

    def set_monitor_output_source(self, source):
        """Sets the source of the monitor output. Also affects the reference output.

            Args:
                source (self.MonitorOutputSource):
                    Defines the source to run the monitor output off of.

        """
        value = format(source)
        self.command(f"MONITOR {str(value)}")

    def get_monitor_output_source(self):
        """Returns the source for the monitor output.

            Returns:
                source (MonitorOutputSource):
                    Returns the source as an object of the MonitorOutputSource class.

        """
        value = int(self.query("MONITOR?"))
        return self.MonitorOutputSource(value)

    def get_warmup_heater_setup(self):
        """Returns the settings regarding the resistance, current and units of the warmup heater (output channel 1).

            Returns:
                (dict):
                    {"resistance": float, "max_current": float, "units": self.HeaterOutputUnits}
        """
        settings_string = self.query("HTRSET? 1")
        separated_settings = settings_string.split(",")
        # Check to see if current is enumerated or custom
        if int(separated_settings[1]) == 1:
            max_current = 0.45
        elif int(separated_settings[1]) == 2:
            max_current = 0.63
        else:
            max_current = float(separated_settings[2])

        return {'resistance': self.HeaterResistance(int(separated_settings[0])),
                'max_current': max_current,
                'units': self.HeaterOutputUnits(int(separated_settings[3]))}

    def get_sample_heater_setup(self):
        """Returns the setup of the sample heater (channel 0).

            Returns:
                (dict):
                    {"resistance": float, "units": self.HeaterOutputUnits}
        """
        settings_string = self.query("HTRSET? 0")
        separated_settings = settings_string.split(",")
        return {'resistance': float(separated_settings[0]),
                'units': self.HeaterOutputUnits(int(separated_settings[3]))}

    def setup_warmup_heater(self, resistance, max_current, units):
        """Configures the current and power of the warmup heater (output channel 1).

            The max current must not cause the heater to exceed it's max power (calculated by I = sqrt(P/R)) or it's
            max voltage (calculated by I = V/R). Check your heater's specifications before setting the max current, and
            use the lower current produced from the two calculations.

            Args:
                resistance (self.HeaterResistance):
                    Heater load in ohms, as an object of the enum type self.HeaterResistance.
                max_current (float):
                    User specified max current in A.
                units (self.HeaterOutputUnits):
                    Defines which units the output is displayed in (Current (A) or Power (W)).

        """
        command_string = f"HTRSET 1,{resistance},0,{max_current},{units}"
        self.command(command_string)

    def setup_sample_heater(self, resistance, units):
        """Configures the current and power of the sample heater (output channel 0.)

            Args:
                resistance (float):
                    Heater load in ohms. Options are: 1 - 2000.

                units (self.HeaterOutputUnits):
                    Defines which units the output is displayed in (Current (A) or Power (W)).

        """
        command_string = f"HTRSET 0,{resistance},0,0,{units}"
        self.command(command_string)

    def configure_analog_monitor_output_heater(self, source, high_value, low_value, settings=None):
        """Configures the still heater's analog settings for Monitor Out mode.

            Can fully configure the heater by including the settings parameter, but it is recommended to configure
            non-analog properties of the heater through the configure_heater method.

            Args:
                source (self.InputSensorUnits):
                    The units to use for channel data.
                high_value (float):
                    The data at which the output reaches +100% output.
                low_value (float):
                    The data at which the outputs reach 0% output for unipolar output, or -100% for bipolar.
                    output.
                settings (Model372HeaterOutputSettings):
                    Optional if heater is already configured using configure_heater. Gives non-analog configurations
                    for heater.

        """
        if settings is None:
            # Use the settings already configured to avoid changing any settings
            settings = self.get_heater_output_settings(2)
        # Retrieve value from input_channel enum
        if isinstance(settings.input_channel, self.InputChannel):
            input_channel = settings.input_channel.value
        else:
            input_channel = settings.input_channel
        command_string = f"ANALOG 2,{settings.polarity},1,{input_channel},{source},{high_value},{low_value},0"
        self.command(command_string)

    def get_analog_monitor_output_settings(self):
        """Retrieves the analog monitor settings of output 2 configured in monitor output mode.

            Returns:
                (dict):
                    {"source": self.InputSensorUnits, "high_value": float, "low_value": float}

        """
        settings_string = self.query("ANALOG? 2")
        separated_settings = settings_string.split(",")
        return {'source': self.InputSensorUnits(int(separated_settings[3])),
                'high_value': float(separated_settings[4]),
                'low_value': float(separated_settings[5])}

    def configure_analog_heater(self, output_channel, manual_value, settings=None):
        """Configures the analog settings of a heater for modes other than Monitor Out.

            (Use configure_analog_monitor_out_heater for Monitor Out mode). Can fully configure the heater by including
            the settings parameter, but it is recommended to first configure the heater using the configure_heater
            method before using this method.

            Args:
                output_channel (Model372HeaterOutput):
                    The output to configure.
                manual_value (float):
                    The value of the analog output as it applies to the set analog mode.
                settings (Model372HeaterOutputSettings):
                    Optional if heater is already configured using configure_heater. Gives non-analog configurations
                    for heater.

        """
        if settings is None:
            settings = self.get_heater_output_settings(output_channel)
        if isinstance(settings.input_channel, self.InputChannel):
            input_channel = settings.input_channel.value
        else:
            input_channel = settings.input_channel
        command_string = f"ANALOG {output_channel},{settings.output_mode},{settings.polarity},{input_channel},0,0,0,{manual_value}"
        self.command(command_string)

    def get_analog_manual_value(self, output_channel):
        """Returns the manual value of an analog heater.

            The manual value is the analog value used for Open Loop, Closed Loop, Warm Up, or Still mode.

            Args:
                output_channel (int):
                    The analog output to query. Options are: 1 (Warm up heater), or 2 (Still heater).

            Returns:
                (float):
                    The manual analog value for the heater.
        """
        settings_string = self.query(f"ANALOG? {str(output_channel)}")
        separated_settings = settings_string.split(",")
        return float(separated_settings[6])

    def set_website_login(self, username, password):
        """Sets the username and password to connect instrument to website.

            Args:
                username (str):
                    Username to set for login. Must be less than or equal to 15 characters. Method
                    automatically puts quotation marks around string, so they are not needed in the
                    string literal passed into the method.
                password (str):
                    Password to set for login. Must be less than or equal to 15 characters. Method
                    automatically puts quotation marks around string, so they are not needed in the
                    string literal passed into the method.

        """
        self.command(f"WEBLOG \"{username}\",\"{password}\"")

    def get_website_login(self):
        """Returns the set username and password for web login for the instrument.

            Returns:
                username (str):
                    The current set username for the web login
                password (str):
                    The current set password for the web login

        """
        username_password = self.query("WEBLOG?")
        separated_string = username_password.split(",")
        # Remove padded whitespace in the returned username and password
        username_split = separated_string[0].split(" ")
        username = username_split[0]
        password_split = separated_string[1].split(" ")
        password = password_split[0]
        return {"username": username,
                "password": password}

    def get_control_loop_zone_parameters(self, output_channel, zone):
        """Returns the settings parameters of the control loop on the specified output channel and zone.

            Args:
                output_channel (int):
                    Channel of the heater being queried. Options are: 0 for sample heater, or 1 for warm-up heater.
                zone (int):
                    Control loop zone to configure. Options are: 1 - 10.

            Returns:
                settings (Model372ControlLoopZoneSettings):
                    An object of the Model372ControlLoopZoneSettings class containing information of the
                    settings in the values of its variables.

        """
        settings_string = self.query(f"ZONE? {str(output_channel)},{str(zone)}")
        separated_settings = settings_string.split(",")
        # Use if statement to use correct dictionary to convert range to bool or float
        if output_channel == 0:
            heater_range = self.SampleHeaterOutputRange(int(separated_settings[5]))
        else:
            heater_range = bool(int(separated_settings[5]))
        settings = Model372ControlLoopZoneSettings(float(separated_settings[0]), float(separated_settings[1]),
                                                   float(separated_settings[2]), float(separated_settings[3]),
                                                   float(separated_settings[4]), heater_range,
                                                   float(separated_settings[6]), bool(int(separated_settings[7])),
                                                   bool(int(separated_settings[8])))
        return settings

    def set_control_loop_parameters(self, output_channel, zone, settings):
        """Returns the parameters of the control loop set in the specified zone for the specified heater output.

            Args:
                output_channel (int):
                    Channel of the heater being queried. Options are: 0 for sample heater, or 1 for warm-up heater.
                zone (int):
                    Control loop zone to configure. Options are: 1 - 10.
                settings (Model372ControlLoopZoneSettings):
                    An object of the Model372ControlLoopZoneSettings with the variable set to
                    configure the desired settings.

        """
        # Use if statement to correctly interpret range variable
        if output_channel == 0:
            heater_range = format(settings.heater_range)
        else:
            heater_range = int(settings.heater_range)
        command_string = (f"ZONE {str(output_channel)},{str(zone)},{str(settings.upper_bound)}," +
                         f"{str(settings.p_value)},{str(settings.i_value)},{str(settings.d_value)}," +
                         f"{str(settings.manual_output)},{str(heater_range)},{str(settings.ramp_rate)}," +
                         f"{str(int(settings.relay_1))},{str(int(settings.relay_2))}")
        self.command(command_string)

    def get_reading_status(self, input_channel):
        """Returns any flags raised during a measurement reading.

            Args:
                input_channel (str or int):
                    The input whose reading status is being queried. Options are:
                    1 - 16, or "A" (control input).

            Returns:
                bit_states (dict):
                    Dictionary containing the names of the flag and a boolean value corresponding to
                    if the flag is raised or not.

        """
        integer_representation = int(self.query(f"RDGST? {str(input_channel)}"))
        bit_states = Model372ReadingStatusRegister.from_integer(integer_representation)
        return bit_states


__all__ = ['Model372', 'Model372AlarmParameters', 'Model372ControlLoopZoneSettings', 'Model372CurveHeader',
           'Model372HeaterOutputSettings', 'Model372InputChannelSettings', 'Model372InputSetupSettings',
           'Model372ReadingStatusRegister', 'Model372ServiceRequestEnable', 'Model372ServiceRequestEnable',
           'Model372StandardEventRegister', 'Model372StatusByteRegister', 'Model372OperationEventRegister',
           'Model372DigitalOutputRegister']
