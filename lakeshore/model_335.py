"""Implements functionality unique to the Lake Shore Model 335 cryogenic temperature controller."""
from .model_335_enums import Model335Enums
from .temperature_controllers import TemperatureController, InstrumentException, StandardEventRegister, \
    OperationEvent, RegisterBase

Model335StandardEventRegister = StandardEventRegister
Model335OperationEvent = OperationEvent


class Model335InputSensorSettings:
    """Class object used in the get/set_input_sensor methods."""

    def __init__(self, sensor_type, autorange_enable, compensation, units, input_range=None):
        """Constructor for the InputSensor class.

            Args:
                sensor_type (Model335InputSensorType):
                    Specifies input sensor type.
                autorange_enable (bool):
                    Specifies autoranging (False = off, True = on).
                compensation (bool):
                    Specifies input compensation. (False = off, True = on).
                units (Model335InputSensorUnits):
                    Specifies the preferred units parameter for sensor readings and for the control set-point.
                input_range (IntEnum)
                    Specifies input range if autorange_enable is false.
                    See IntEnum classes: Model335DiodeRange, Model335RTDRange, and Model335ThermocoupleRange.

        """

        self.sensor_type = sensor_type
        self.autorange_enable = autorange_enable
        self.compensation = compensation
        self.units = units
        self.input_range = input_range


class Model335ControlLoopZoneSettings:
    """Control loop configuration for a particular heater output and zone."""

    def __init__(self, upper_bound, proportional, integral, derivative, manual_output_value,
                 heater_range, channel, ramp_rate):
        """Constructor.

            Args:
                upper_bound (float):
                    Specifies the upper set-point boundary of this zone in kelvin.
                proportional (float):
                    Specifies the proportional gain for this zone (0.1 to 1000).
                integral (float):
                    Specifies the integral gain for this zone (0.1 to 1000).
                derivative (float):
                    Specifies the derivative gain for this zone (0 to 200 %).
                manual_output_value (float):
                    Specifies the manual output for this zone (0 to 100 %).
                heater_range (Model335HeaterRange):
                    Specifies the heater range for this zone.
                    See Model335HeaterRange IntEnum class.
                channel (Model335InputSensor):
                    See Model335InputSensor IntEnum class.
                ramp_rate (float):
                    Specifies the ramp rate for this zone (0 - 100 K/min).

        """

        self.upper_bound = upper_bound
        self.proportional = proportional
        self.integral = integral
        self.derivative = derivative
        self.manual_output_value = manual_output_value
        self.heater_range = heater_range
        self.channel = channel
        self.ramp_rate = ramp_rate


class Model335StatusByteRegister(RegisterBase):
    """Class object representing the status byte register LSB to MSB."""

    bit_names = [
        "",
        "",
        "",
        "",
        "message_available_summary_bit",
        "event_status_summary_bit",
        "service_request",
        "operation_summary_bit"
    ]

    def __init__(self,
                 message_available_summary_bit,
                 event_status_summary_bit,
                 service_request,
                 operation_summary_bit):
        self.message_available_summary_bit = message_available_summary_bit
        self.event_status_summary_bit = event_status_summary_bit
        self.service_request = service_request
        self.operation_summary_bit = operation_summary_bit


class Model335ServiceRequestEnable(RegisterBase):
    """Class object representing the service request enable register LSB to MSB."""

    bit_names = [
        "",
        "",
        "",
        "",
        "message_available_summary_bit",
        "event_status_summary_bit",
        "",
        "operation_summary_bit"
    ]

    def __init__(self,
                 message_available_summary_bit,
                 event_status_summary_bit,
                 operation_summary_bit):
        self.message_available_summary_bit = message_available_summary_bit
        self.event_status_summary_bit = event_status_summary_bit
        self.operation_summary_bit = operation_summary_bit


class Model335InputReadingStatus(RegisterBase):
    """Class object representing the input status flag bits."""

    bit_names = [
        "invalid_reading",
        "",
        "",
        "",
        "temp_underrange",
        "temp_overrange",
        "sensor_units_zero",
        "sensor_units_overrange"
    ]

    def __init__(self, invalid_reading, temp_underrange, temp_overrange, sensor_units_zero, sensor_units_overrange):
        self.invalid_reading = invalid_reading
        self.temp_underrange = temp_underrange
        self.temp_overrange = temp_overrange
        self.sensor_units_zero = sensor_units_zero
        self.sensor_units_overrange = sensor_units_overrange


class Model335(Model335Enums, TemperatureController):
    """A class object representing the Lake Shore Model 335 cryogenic temperature controller."""

    # Initiate instrument specific registers
    _status_byte_register = Model335StatusByteRegister
    _service_request_enable = Model335ServiceRequestEnable

    vid_pid = [(0x1FB9, 0x0300)]

    def __init__(self,
                 baud_rate,
                 serial_number=None,
                 com_port=None,
                 timeout=2.0,
                 ip_address=None,
                 tcp_port=None,
                 **kwargs):
        # Call the parent init, then fill in values specific to the 335
        TemperatureController.__init__(self, serial_number, com_port, baud_rate, timeout, ip_address,
                                       tcp_port, **kwargs)

        # Disable emulation mode
        self._disable_emulation()

    # Alias specific temperature controller methods
    get_analog_output_percentage = TemperatureController._get_analog_output_percentage
    set_autotune = TemperatureController._set_autotune
    set_brightness = TemperatureController._set_brightness
    get_brightness = TemperatureController._get_brightness
    get_operation_condition = TemperatureController._get_operation_condition
    get_operation_event_enable = TemperatureController._get_operation_event_enable
    set_operation_event_enable = TemperatureController._set_operation_event_enable
    get_operation_event = TemperatureController._get_operation_event
    get_thermocouple_junction_temp = TemperatureController._get_thermocouple_junction_temp
    set_soft_cal_curve_dt_470 = TemperatureController._set_soft_cal_curve_dt_470
    set_soft_cal_curve_pt_100 = TemperatureController._set_soft_cal_curve_pt_100
    set_soft_cal_curve_pt_1000 = TemperatureController._set_soft_cal_curve_pt_1000
    set_diode_excitation_current = TemperatureController._set_diode_excitation_current
    get_diode_excitation_current = TemperatureController._get_diode_excitation_current
    get_tuning_control_status = TemperatureController._get_tuning_control_status
    set_filter = TemperatureController._set_filter
    get_filter = TemperatureController._get_filter

    def set_monitor_output_heater(self, channel, high_value, low_value, units=Model335Enums.MonitorOutUnits.KELVIN,
                                  polarity=TemperatureController.Polarity.UNIPOLAR):
        """Configures output 2. Use the set_heater_output_mode command to set the output mode to Monitor Out.

            Args:
                channel (Model335InputSensor):
                    Specifies which sensor input to monitor.
                high_value (float):
                    Represents the data at which the Monitor Out reaches +100% output.
                    Entered in the units designated by the <units> argument.
                low_value (float):
                    Represents the data at which the analog output reaches -100% output if bipolar,
                    or 0% output if unipolar. Entered in the units designated by the <units> argument.
                units (Model335MonitorOutUnits):
                    Specifies the units on which to base the output voltage.
                polarity (Model335Polarity):
                    Specifies output voltage is unipolar or bipolar.

        """
        self.command(f"ANALOG 2,{channel},{units},{high_value},{low_value},{polarity}")

    def get_monitor_output_heater(self):
        """Used to obtain all monitor out parameters for output 2.

            Returns:
                (dict):
                    {"channel": Model335InputSensor,
                    "units": Model335MonitorOutUnits,
                    "high_value": float,
                    "low_value": float,
                    "polarity": Model335Polarity}

                    See set_monitor_output_heater method arguments

        """
        parameters = self.query("ANALOG? 2").split(",")
        return {"channel": self.InputSensor(int(parameters[0])),
                "units": self.MonitorOutUnits(int(parameters[1])),
                "high_value": float(parameters[2]),
                "low_value": float(parameters[3]),
                "polarity": self.Polarity(int(parameters[4]))}

    def get_celsius_reading(self, channel):
        """Returns the temperature value in Celsius of either channel.

            Args:
                channel (str):
                    Selects the sensor input to query ("A" or "B"),

        """
        return float(self.query(f"CRDG? {channel}"))

    def set_display_setup(self, mode):
        """Sets the display mode.

            Args:
                mode (Model335DisplaySetup):
                    Specifies the front panel display mode.
                    See Model335DisplaySetup IntEnum class.

        """
        self.command(f"DISPLAY {mode}")

    def get_display_setup(self):
        """Returns the display mode.

            Return:
                (Model335DisplaySetup):
                    Specifies the front panel display mode.
                    See Model335DisplaySetup IntEnum class.

        """
        return self.DisplaySetup(int(self.query("DISPLAY?")))

    def set_heater_setup_one(self, heater_resistance, max_current, output_display_mode):
        """Method to configure heater output one.

            Args:
                heater_resistance (Model335HeaterResistance):
                    See Model335HeaterResistance IntEnum class.
                max_current (float):
                    Specifies the maximum current for the heater.
                output_display_mode (Model335HeaterOutputDisplay):
                    Specifies how the heater output is displayed.
                    See Model335HeaterOutType IntEnum class.

        """
        self.command(f"HTRSET 1,0,{heater_resistance},0,{max_current},{output_display_mode}")

    def set_heater_setup_two(self, output_type, heater_resistance, max_current, display_mode):
        """Method to configure the heater output 2.

            Args:
                output_type (Model335HeaterOutType):
                    Specifies whether the heater output is in constant current or voltage mode.
                    See Model335HeaterOutType IntEnum class.
                heater_resistance (Model335HeaterResistance):
                    See Model335HeaterResistance IntEnum class.
                max_current (float):
                    Specifies the maximum current for the heater.
                display_mode (Model335HeaterOutType):
                    Specifies how the heater output is displayed.
                    Required only if output_type is set to CURRENT.
                    See Model335HeaterOutType IntEnum class.

        """
        self.command(f"HTRSET 2,{output_type},{heater_resistance},0,{max_current},{display_mode}")

    def get_heater_setup(self, heater_output):
        """Returns the heater configuration status.

            Args:
                heater_output (int):
                    Selects which heater output to query:

            Return:
                (dict):
                    See set_heater_setup_one/set_heater_setup_two method arguments.
                    {"output_type": Model335HeaterOutType, "heater_resistance": Model335HeaterResistance,
                    "max_current": float, "output_display_mode": Model335HeaterOutputDisplay}

        """
        heater_setup = self.query(f"HTRSET? {heater_output}").split(",")
        if int(heater_setup[2]) == 0:
            max_current = float(heater_setup[3])
        else:
            preset_currents = ["USER", 0.707, 1.0, 1.141, 1.732]
            current_index = int(heater_setup[2])
            max_current = preset_currents[current_index]

        return {"output_type": self.HeaterOutType(int(heater_setup[0])),
                "heater_resistnace": self.HeaterResistance(int(heater_setup[1])),
                "max_current": max_current,
                "output_display_mode": self.HeaterOutputDisplay(int(heater_setup[4]))}

    def set_input_sensor(self, channel, sensor_parameters):
        """Sets the sensor type and associated parameters.

            Args:
                channel (str):
                    Specifies input to configure ("A" or "B").
                sensor_parameters (Model335InputSensorSettings):
                    See Model335InputSensorSettings class.

        """
        autorange_enable = bool(int(sensor_parameters.autorange_enable))
        if autorange_enable:
            input_range = 0
        else:
            input_range = sensor_parameters.input_range

        command_string = (f"INTYPE {channel},{sensor_parameters.sensor_type},{int(sensor_parameters.autorange_enable)}," +
                            f"{input_range},{int(sensor_parameters.compensation)},{sensor_parameters.units}")

        self.command(command_string)

    def get_input_sensor(self, channel):
        """Returns the sensor type and associated parameters.

            Args:
                channel (str):
                    Specifies sensor input to configure ("A" or "B").

            Return:
                (Model335InputSensorSettings):
                    See Model335InputSensor IntEnum class.

        """
        sensor_configuration = self.query(f"INTYPE? {channel}").split(",")
        input_sensor_type = self.InputSensorType(int(sensor_configuration[0]))

        sensor_range = None
        if bool(int(sensor_configuration[1])):
            sensor_range = 0
        elif input_sensor_type == self.InputSensorType.DISABLED:
            sensor_range = 0
        elif input_sensor_type == self.InputSensorType.DIODE:
            sensor_range = self.DiodeRange(int(sensor_configuration[2]))
        elif input_sensor_type in (self.InputSensorType.PLATINUM_RTD or self.InputSensorType.NTC_RTD):
            sensor_range = self.RTDRange(int(sensor_configuration[2]))
        elif input_sensor_type == self.InputSensorType.THERMOCOUPLE:
            sensor_range = self.ThermocoupleRange(int(sensor_configuration[2]))

        return Model335InputSensorSettings(input_sensor_type, bool(int(sensor_configuration[1])),
                                           bool(int(sensor_configuration[3])),
                                           self.InputSensorUnits(int(sensor_configuration[4])),
                                           sensor_range)

    def get_all_kelvin_reading(self):
        """Returns the temperature value in kelvin of all channels.

            Return:
                (list: float)
                    * [channel_A, channel_B]

        """
        return [float(self.query("KRDG? A")), float(self.query("KRDG? B"))]

    def set_heater_output_mode(self, output, mode, channel, powerup_enable=False):
        """Configures the heater output mode.

            Args:
                output (int):
                    Specifies which output to configure (1 or 2).
                mode (Model335HeaterOutputMode):
                    Member of Model335HeaterOutputMode IntEnum class.
                    Specifies the control mode.
                channel (Model335InputSensor):
                    Specifies which input to use for control.
                powerup_enable (bool):
                    Specifies whether the output remains on (True)
                    or shuts off after power cycle (False).

        """
        command_string = f"OUTMODE {output},{mode},{channel},{int(powerup_enable)}"
        self.command(command_string)

    def get_heater_output_mode(self, output):
        """Returns the heater output mode for a given output and whether powerup is enabled.

            Args:
                output (int):
                    Specifies which output to query (1 or 2).

            Return:
                (dict):
                {"mode": Model335HeaterOutputMode, "channel": Model335InputSensor, "powerup_enable": bool}

        """
        outmode = self.query(f"OUTMODE? {output}").split(",")

        return {"mode": self.HeaterOutputMode(int(outmode[0])),
                "channel": self.InputSensor(int(outmode[1])),
                "powerup_enable": bool(int(outmode[2]))}

    def set_output_two_polarity(self, output_polarity):
        """Sets polarity of output 2 to either unipolar or bipolar.

            Only applicable when output 2 is in voltage mode.

            Args:
                output_polarity (Model335Polarity):
                    Specifies whether output voltage is UNIPOLAR or BIPOLAR.

        """
        self.command(f"POLARITY 2,{output_polarity}")

    def get_output_2_polarity(self):
        """Returns the polarity of output 2.

            Return:
                (Model335Polarity):
                    Specifies whether output is UNIPOLAR or BIPOLAR.

        """
        return self.Polarity(int(self.query("POLARITY?")))

    def set_heater_range(self, output, heater_range):
        """Sets the heater range for a particular output.

            The range setting has no effect if an output is in the off mode, and does not apply to an output in Monitor
            Out mode. An output in Monitor Out mode is always on.

            Args:
                output (int):
                    Specifies which output to configure (1 or 2).
                heater_range (IntEnum):
                    For Outputs 1 and 2 in Current mode: Model335HeaterRange IntEnum member.
                    For Output 2 in Voltage mode: Model335HeaterVoltageRange IntEnum member.

        """
        self.command(f"RANGE {output},{heater_range}")

    def get_heater_range(self, output):
        """Returns the heater range for a particular output.

            Args:
                output (int):
                    Specifies which output to configure (1 or 2).

            Return:
                heater_range (IntEnum):
                    For Outputs 1 and 2 in Current mode: Model335HeaterRange IntEnum member.
                    For Output 2 in Voltage mode: Model335HeaterVoltageRange IntEnum member.

        """
        heater_range = int(self.query(f"RANGE? {output}"))
        if output == 2:
            # Check if output 2 is in voltage mode
            output_2_heater_setup = self.query("HTRSET? 2").split(",")
            output_2_voltage_enable = bool(int(output_2_heater_setup[0]))
            if output_2_voltage_enable:
                heater_range = self.HeaterVoltageRange(heater_range)
            else:
                heater_range = self.HeaterRange(heater_range)
        else:
            heater_range = self.HeaterRange(heater_range)
        return heater_range

    def all_heaters_off(self):
        """Recreates the front panel safety feature of shutting off all heaters."""

        self.command("RANGE 1,0")
        self.command("RANGE 2,0")

    def get_input_reading_status(self, channel):
        """Returns the state of the input status flag bits.

            Args:
                channel (str):
                    Specifies which channel to query ("A" or "B").

            Return:
                (InputReadingStatus):
                    Boolean representation of each bit of the input status flag register.
        """
        response = int(self.query(f"RDGST? {channel}"))
        return Model335InputReadingStatus.from_integer(response)

    def set_warmup_supply(self, control, percentage):
        """Warmup mode applies only to Output 2 in Voltage mode.

            The Output Type parameter must be configured using the set_heater_setup() method, and the Output mode and
            Control Input parameters must be configured using the set_monitor_out_parameters() method.

            Args:
                control (Model335WarmupControl):
                    Specifies the type of control used.
                percentage (float):
                    Specifies the percentage of full scale (10 V) Monitor Out voltage to apply.

        """
        # Check if output 2 is in voltage mode
        output_2_heater_setup = self.query("HTRSET? 2").split(",")
        output_2_voltage_enable = bool(int(output_2_heater_setup[0]))
        if not output_2_voltage_enable:
            raise InstrumentException("Output 2 is not configured in voltage mode")

        command_string = f"WARMUP 2,{control},{percentage}"
        self.command(command_string)

    def get_warmup_supply(self):
        """Returns the output 2 warmup supply configuration.

            Return:
                (dict):
                    {"control": Model335WarmupControl, "percentage": float}

        """
        warmup_supply = self.query("WARMUP? 2").split(",")
        return {"control": self.WarmupControl(int(warmup_supply[0])),
                "percentage": float(warmup_supply[1])}

    def set_control_loop_zone_table(self, output, zone, control_loop_zone):
        """Configures the output zone parameters.

            Args:
                output (int):
                    Specifies which heater output to configure (1 or 2).
                zone (int):
                    Specifies which zone in the table to configure (1 to 10).
                control_loop_zone (ControlLoopZone):
                    See ControlLoopZone class.

        """
        command_string = (f"ZONE {output},{zone},{control_loop_zone.upper_bound},{control_loop_zone.proportional}," +
                            f"{control_loop_zone.integral},{control_loop_zone.derivative},{control_loop_zone.manual_output_value}," +
                            f"{control_loop_zone.heater_range},{control_loop_zone.channel},{control_loop_zone.ramp_rate}")
        self.command(command_string)

    def get_control_loop_zone_table(self, output, zone):
        """Returns a list of zone control parameters for a selected output and zone.

            Args:
                output (int):
                    Specifies which heater output to query (1 or 2).
                zone (int):
                    Specifies which zone in the table to query (1 to 10).

            Return:
                (Model335ControlLoopZone):
                    See Model335ControlLoopZone class.

        """
        zone_parameters = self.query(f"ZONE? {output},{zone}").split(",")
        control_loop_zone_parameters = Model335ControlLoopZoneSettings(float(zone_parameters[0]),
                                                                       float(zone_parameters[1]),
                                                                       float(zone_parameters[2]),
                                                                       float(zone_parameters[3]),
                                                                       float(zone_parameters[4]),
                                                                       self.HeaterRange(int(zone_parameters[5])),
                                                                       self.InputSensor(int(zone_parameters[6])),
                                                                       float(zone_parameters[7]))
        return control_loop_zone_parameters

    def _disable_emulation(self):
        """Disables emulation mode so that instrument is compatible with Python Driver."""
        self.command("EMUL 0", check_errors=False)


__all__ = ['Model335', 'Model335ControlLoopZoneSettings', 'Model335InputReadingStatus', 'Model335InputSensorSettings',
           'Model335OperationEvent',  'Model335ServiceRequestEnable', 'Model335StandardEventRegister',
           'Model335StatusByteRegister']
