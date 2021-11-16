"""Implements functionality unique to the Lake Shore Model 335 cryogenic temperature controller"""
from enum import IntEnum

from .temperature_controllers import TemperatureController, InstrumentException
from .temperature_controllers import RelayControlMode, RelayControlAlarm, InterfaceMode, HeaterError, \
    CurveFormat, CurveTemperatureCoefficient, BrightnessLevel, AutotuneMode, HeaterResistance, Polarity, \
    DiodeCurrent, HeaterOutputUnits, InputSensorUnits, ControlTypes, StandardEventRegister, OperationEvent, RegisterBase

Model335RelayControlMode = RelayControlMode
Model335RelayControlAlarm = RelayControlAlarm
Model335InterfaceMode = InterfaceMode
Model335HeaterError = HeaterError
Model335CurveFormat = CurveFormat
Model335CurveTemperatureCoefficient = CurveTemperatureCoefficient
Model335BrightnessLevel = BrightnessLevel
Model335AutoTuneMode = AutotuneMode
Model335HeaterResistance = HeaterResistance
Model335Polarity = Polarity
Model335DiodeCurrent = DiodeCurrent
Model335HeaterOutputUnits = HeaterOutputUnits
Model335InputSensorUnits = InputSensorUnits
Model335ControlTypes = ControlTypes

Model335StandardEventRegister = StandardEventRegister
Model335OperationEvent = OperationEvent


class Model335InputSensor(IntEnum):
    """Enumeration when "NONE" is an option for sensor input"""
    NONE = 0
    CHANNEL_A = 1
    CHANNEL_B = 2


class Model335MonitorOutUnits(IntEnum):
    """Units associated with a sensor channel"""
    KELVIN = 1
    CELSIUS = 2
    SENSOR = 3


class Model335InputSensorType(IntEnum):
    """Sensor type enumeration"""
    DISABLED = 0
    DIODE = 1
    PLATINUM_RTD = 2
    NTC_RTD = 3
    THERMOCOUPLE = 4


class Model335DiodeRange(IntEnum):
    """Diode voltage range enumeration"""
    TWO_POINT_FIVE_VOLTS = 0
    TEN_VOLTS = 1


class Model335RTDRange(IntEnum):
    """RTD resistance range enumeration"""
    TEN_OHM = 0
    THIRTY_OHM = 1
    HUNDRED_OHM = 2
    THREE_HUNDRED_OHM = 3
    ONE_THOUSAND_OHM = 4
    THREE_THOUSAND_OHM = 5
    TEN_THOUSAND_OHM = 6
    THIRTY_THOUSAND_OHM = 7
    ONE_HUNDRED_THOUSAND_OHM = 8


class Model335ThermocoupleRange(IntEnum):
    """Thermocouple range enumeration"""
    FIFTY_MILLIVOLT = 0


class Model335InputSensorSettings:
    """Class object used in the get/set_input_sensor methods"""

    def __init__(self, sensor_type, autorange_enable, compensation, units, input_range=None):
        """Constructor for the InputSensor class

            Args:
                sensor_type (Model335InputSensorType):
                    * Specifies input sensor type

                autorange_enable (bool):
                    * Specifies autoranging
                    * False = off and True = on

                compensation (bool):
                    * Specifies input compensation
                    * False = off and True = on

                units (Model335InputSensorUnits):
                    * Specifies the preferred units parameter for sensor readings and for the control setpoint

                input_range (IntEnum)
                    * Specifies input range if autorange_enable is false
                    * See IntEnum classes:
                        * Model335DiodeRange
                        * Model335RTDRange
                        * Model335ThermocoupleRange

        """

        self.sensor_type = sensor_type
        self.autorange_enable = autorange_enable
        self.compensation = compensation
        self.units = units
        self.input_range = input_range


class Model335HeaterOutType(IntEnum):
    """Heater output 2 enumeration"""
    CURRENT = 0
    VOLTAGE = 1


class Model335HeaterOutputDisplay(IntEnum):
    """Heater output display units enumeration"""
    CURRENT = 1
    POWER = 2


class Model335HeaterOutputMode(IntEnum):
    """Control loop enumeration"""
    OFF = 0
    CLOSED_LOOP = 1
    ZONE = 2
    OPEN_LOOP = 3
    MONITOR_OUT = 4
    WARMUP_SUPPLY = 5


class Model335WarmupControl(IntEnum):
    """Heater output 2 voltage mode warmup enumerations"""
    AUTO_OFF = 0
    CONTINUOUS = 1


class Model335HeaterRange(IntEnum):
    """Control loop heater range enumeration"""
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Model335ControlLoopZoneSettings:
    """Control loop configuration for a particular heater output and zone"""

    def __init__(self, upper_bound, proportional, integral, derivative, manual_output_value,
                 heater_range, channel, ramp_rate):
        """Constructor

            Args:
                upper_bound (float):
                    * Specifies the upper Setpoint boundary of this zone in kelvin

                proportional (float):
                    * Specifies the proportional gain for this zone
                    * 0.1 to 1000

                integral (float):
                    * Specifies the integral gain for this zone
                    * 0.1 to 1000

                derivative (float):
                    * Specifies the derivative gain for this zone
                    * 0 to 200 %

                manual_output_value (float):
                    * Specifies the manual output for this zone
                    * 0 to 100 %

                heater_range (Model335HeaterRange):
                    * Specifies the heater range for this zone
                    * See Model335HeaterRange IntEnum class

                channel (Model335InputSensor):
                    * See Model335InputSensor IntEnum class

                ramp_rate (float):
                    * Specifies the ramp rate for this zone
                    * 0 - 100 K/min

        """

        self.upper_bound = upper_bound
        self.proportional = proportional
        self.integral = integral
        self.derivative = derivative
        self.manual_output_value = manual_output_value
        self.heater_range = heater_range
        self.channel = channel
        self.ramp_rate = ramp_rate


class Model335DisplaySetup(IntEnum):
    """Panel display setup enumeration"""
    INPUT_A = 0
    INPUT_A_MAX_MIN = 1
    TWO_INPUT_A = 2
    INPUT_B = 3
    INPUT_B_MAX_MIN = 4
    TWO_INPUT_B = 5
    CUSTOM = 6
    TWO_LOOP = 7


class Model335HeaterVoltageRange(IntEnum):
    """Voltage mode heater enumerations"""
    VOLTAGE_OFF = 0
    VOLTAGE_ON = 1


class Model335DisplayInputChannel(IntEnum):
    """Panel display information enumeration"""
    NONE = 0
    INPUT_A = 1
    INPUT_B = 2
    SETPOINT_1 = 3
    SETPOINT_2 = 4
    OUTPUT_1 = 5
    OUTPUT_2 = 6


class Model335DisplayFieldUnits(IntEnum):
    """Panel display units enumeration"""
    KELVIN = 1
    CELSIUS = 2
    SENSOR_UNITS = 3
    MINIMUM_DATA = 4
    MAXIMUM_DATA = 5
    SENSOR_NAME = 6


class Model335StatusByteRegister(RegisterBase):
    """Class object representing the status byte register LSB to MSB"""

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
    """Class object representing the service request enable register LSB to MSB"""

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
    """Class object representing the input status flag bits"""

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


class Model335(TemperatureController):
    """A class object representing the Lake Shore Model 335 cryogenic temperature controller"""

    # Initiate enum types for temperature controllers
    _input_channel_enum = Model335DisplayInputChannel
    _display_units_enum = Model335DisplayFieldUnits

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

    def set_monitor_output_heater(self, channel, high_value, low_value, units=Model335MonitorOutUnits.KELVIN,
                                  polarity=Model335Polarity.UNIPOLAR):
        """Configures output 2. Use the set_heater_output_mode command to set the output mode to Monitor Out.

            Args:
                channel (Model335InputSensor):
                    * Specifies which sensor input to monitor

                high_value (float):
                    * Represents the data at which the Monitor Out reaches +100% output
                    * Entered in the units designated by the <units> argument

                low_value (float):
                    * Represents the data at which the analog output reaches -100% output if bipolar,
                    * or 0% outputif unipolar. Entered in the units designated by the <units> argument

                units (Model335MonitorOutUnits):
                    * Specifies the units on which to base the output voltage

                polarity (Model335Polarity):
                    * Specifies output voltage is unipolar or bipolar

        """
        self.command(f"ANALOG 2,{channel},{units},{high_value},{low_value},{polarity}")

    def get_monitor_output_heater(self):
        """Used to obtain all monitor out parameters for output 2.

            Return:
                (dict):
                    * See set_monitor_output_heater method arguments
                    * Keys:
                        * "channel": Model335InputSensor
                        * "units": Model335MonitorOutUnits
                        * "high_value": float
                        * "low_value": float
                        * "polarity": Model335Polarity

        """
        parameters = self.query("ANALOG? 2").split(",")
        return {"channel": Model335InputSensor(int(parameters[0])),
                "units": Model335MonitorOutUnits(int(parameters[1])),
                "high_value": float(parameters[2]),
                "low_value": float(parameters[3]),
                "polarity": Model335Polarity(int(parameters[4]))}

    def get_celsius_reading(self, channel):
        """Returns the temperature value in celsius of either channel.

            Args:
                channel (str):
                    * Selects the sensor input to query
                    * "A" or "B"

        """
        return float(self.query(f"CRDG? {channel}"))

    def set_display_setup(self, mode):
        """Sets the display mode

            Args:
                mode (Model335DisplaySetup):
                    * Specifies the front panel display mode
                    * See Model335DisplaySetup IntEnum class

        """
        self.command(f"DISPLAY {mode}")

    def get_display_setup(self):
        """Returns the display mode

            Return:
                (Model335DisplaySetup):
                    * Specifies the front panel display mode
                    * See Model335DisplaySetup IntEnum class

        """
        return Model335DisplaySetup(int(self.query("DISPLAY?")))

    def set_heater_setup_one(self, heater_resistance, max_current, output_display_mode):
        """Method to configure heater output one.

            Args:
                heater_resistance (Model335HeaterResistance):
                    * See Model335HeaterResistance IntEnum class

                max_current (float):
                    * Specifies the maximum current for the heater

                output_display_mode (Model335HeaterOutputDisplay):
                    * Specifies how the heater output is displayed
                    * See Model335HeaterOutType IntEnum class

        """
        self.command(f"HTRSET 1,0,{heater_resistance},0,{max_current},{output_display_mode}")

    def set_heater_setup_two(self, output_type, heater_resistance, max_current, display_mode):
        """Method to configure the heater output 2.

            Args:
                output_type (Model335HeaterOutType):
                    * Specifies wheter the heater output is in constant current or voltage mode
                    * See Model335HeaterOutType IntEnum class

                heater_resistance (Model335HeaterResistance):
                    * See Model335HeaterResistance IntEnum class

                max_current (float):
                    * Specifies the maximum current for the heater

                display_mode (Model335HeaterOutType):
                    * Specifies how the heater output is displayed
                    * Required only if output_type is set to CURRENT
                    * See Model335HeaterOutType IntEnum class

        """
        self.command(f"HTRSET 2,{output_type},{heater_resistance},0,{max_current},{display_mode}")

    def get_heater_setup(self, heater_output):
        """Returns the heater configuration status.

            Args:
                heater_output (int)
                    * Selects which heater output to query

            Return:
                (dict):
                    * See set_heater_setup_one/set_heater_setup_two method arguments
                    * Keys:
                        * "output_type": Model335HeaterOutType
                        * "heater_resistance": Model335HeaterResistance
                        * "max_current": float
                        * "output_display_mode": Model335HeaterOutputDisplay

        """
        heater_setup = self.query(f"HTRSET? {heater_output}").split(",")
        if int(heater_setup[2]) == 0:
            max_current = float(heater_setup[3])
        else:
            preset_currents = ["USER", 0.707, 1.0, 1.141, 1.732]
            current_index = int(heater_setup[2])
            max_current = preset_currents[current_index]

        return {"output_type": Model335HeaterOutType(int(heater_setup[0])),
                "heater_resistnace": Model335HeaterResistance(int(heater_setup[1])),
                "max_current": max_current,
                "output_display_mode": Model335HeaterOutputDisplay(int(heater_setup[4]))}

    def set_input_sensor(self, channel, sensor_parameters):
        """Sets the sensor type and associated parameters.

            Args:
                channel (str):
                    * Specifies input to configure
                    * "A" or "B"

                sensor_parameters (Model335InputSensorSettings):
                    * See Model335InputSensorSettings class

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
                    * Specifies sensor input to configure
                    * "A" or "B"

            Return:
                (Model335InputSensorSettings):
                    * See Model335InputSensor IntEnum class

        """
        sensor_configuration = self.query(f"INTYPE? {channel}").split(",")
        input_sensor_type = Model335InputSensorType(int(sensor_configuration[0]))

        sensor_range = None
        if bool(int(sensor_configuration[1])):
            sensor_range = 0
        elif input_sensor_type == Model335InputSensorType.DISABLED:
            sensor_range = 0
        elif input_sensor_type == Model335InputSensorType.DIODE:
            sensor_range = Model335DiodeRange(int(sensor_configuration[2]))
        elif input_sensor_type in (Model335InputSensorType.PLATINUM_RTD or Model335InputSensorType.NTC_RTD):
            sensor_range = Model335RTDRange(int(sensor_configuration[2]))
        elif input_sensor_type == Model335InputSensorType.THERMOCOUPLE:
            sensor_range = Model335ThermocoupleRange(int(sensor_configuration[2]))

        return Model335InputSensorSettings(input_sensor_type, bool(int(sensor_configuration[1])),
                                           bool(int(sensor_configuration[3])),
                                           Model335InputSensorUnits(int(sensor_configuration[4])),
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
                    * Specifies which output to configure (1 or 2)

                mode (Model335HeaterOutputMode):
                    * Member of Model335HeaterOutputMode IntEnum class
                    * Specifies the control mode

                channel (Model335InputSensor)
                    * Specifies which input to use for control

                powerup_enable (bool)
                    * Specifies whether the output remains on (True)
                    * or shuts off after power cycle (False)

        """
        command_string = f"OUTMODE {output},{mode},{channel},{int(powerup_enable)}"
        self.command(command_string)

    def get_heater_output_mode(self, output):
        """Returns the heater output mode for a given output and whether powerup is enabled.

            Args:
                output (int):
                    * Specifies which output to query (1 or 2)

            Return:
                (dict):
                    * Keys:
                        * "mode": Model335HeaterOutputMode
                        * "channel": Model335InputSensor
                        * "powerup_enable": bool

        """
        outmode = self.query(f"OUTMODE? {output}").split(",")

        return {"mode": Model335HeaterOutputMode(int(outmode[0])),
                "channel": Model335InputSensor(int(outmode[1])),
                "powerup_enable": bool(int(outmode[2]))}

    def set_output_two_polarity(self, output_polarity):
        """Sets polarity of output 2 to either unipolar or bipolar, only applicable when
        output 2 is in voltage mode.

            Args:
                output_polarity (Model335Polarity)
                    * Specifies whether output voltage is UNIPOLAR or BIPOLAR

        """
        self.command(f"POLARITY 2,{output_polarity}")

    def get_output_2_polarity(self):
        """Returns the polarity of output 2

            Return:
                (Model335Polarity)
                    * Specifies whether output is UNIPOLAR or BIPOLAR

        """
        return Model335Polarity(int(self.query("POLARITY?")))

    def set_heater_range(self, output, heater_range):
        """Sets the heater range for a particular output. The range setting has no effect if an output is in
        the off mode, and does not apply to an output in Monitor Out mode. An output in Monitor Out mode is always on.

            Args:
                output (int):
                    * Specifies which output to configure (1 or 2)

                heater_range (IntEnum):
                    * For Outputs 1 and 2 in Current mode:
                        * Model335HeaterRange IntEnum member
                    * For Output 2 in Voltage mode:
                        * Model335HeaterVoltageRange IntEnum member

        """
        self.command(f"RANGE {output},{heater_range}")

    def get_heater_range(self, output):
        """Returns the heater range for a particular output.

            Args:
                output (int):
                    * Specifies which output to configure (1 or 2)

            Return:
                heater_range (IntEnum):
                    * For Outputs 1 and 2 in Current mode:
                        * Model335HeaterRange IntEnum member
                    * For Output 2 in Voltage mode:
                        * Model335HeaterVoltageRange IntEnum member

        """
        heater_range = int(self.query(f"RANGE? {output}"))
        if output == 2:
            # Check if output 2 is in voltage mode
            output_2_heater_setup = self.query("HTRSET? 2").split(",")
            output_2_voltage_enable = bool(int(output_2_heater_setup[0]))
            if output_2_voltage_enable:
                heater_range = Model335HeaterVoltageRange(heater_range)
            else:
                heater_range = Model335HeaterRange(heater_range)
        else:
            heater_range = Model335HeaterRange(heater_range)
        return heater_range

    def all_heaters_off(self):
        """Recreates the front panel safety feature of shutting off all heaters"""

        self.command("RANGE 1,0")
        self.command("RANGE 2,0")

    def get_input_reading_status(self, channel):
        """Returns the state of the input status flag bits.

            Args:
                channel (str):
                    * Specifies which channel to query
                    * "A" or "B"

            Return:
                (InputReadingStatus):
                    * Boolean representation of each bit of the input status flag register
        """
        response = int(self.query(f"RDGST? {channel}"))
        return Model335InputReadingStatus.from_integer(response)

    def set_warmup_supply(self, control, percentage):
        """Warmup mode applies only to Output 2 in Voltage mode. The Output Type parameter
        must be configured using the set_heater_setup() method, and the Output mode and Control
        Input parameters must be configured using the set_monitor_out_parameters() method.

            Args:
                control (Model335WarmupControl):
                    * Specifies the type of control used

                percentage (float):
                    * Specifies the percentage of full scale (10 V) Monitor Out voltage to apply

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
                    * Keys:
                        * "control": Model335WarmupControl
                        * "percentage": float

        """
        warmup_supply = self.query("WARMUP? 2").split(",")
        return {"control": Model335WarmupControl(int(warmup_supply[0])),
                "percentage": float(warmup_supply[1])}

    def set_control_loop_zone_table(self, output, zone, control_loop_zone):
        """Configures the output zone parameters.

            Args:
                output (int):
                    * Specifies which heater output to configure
                    * 1 or 2

                zone (int):
                    * Specifies which zone in the table to configure
                    * 1 to 10

                control_loop_zone (ControlLoopZone):
                    * See ControlLoopZone class

        """
        command_string = (f"ZONE {output},{zone},{control_loop_zone.upper_bound},{control_loop_zone.proportional}," +
                            f"{control_loop_zone.integral},{control_loop_zone.derivative},{control_loop_zone.manual_output_value}," +
                            f"{control_loop_zone.heater_range},{control_loop_zone.channel},{control_loop_zone.ramp_rate}")
        self.command(command_string)

    def get_control_loop_zone_table(self, output, zone):
        """Returns a list of zone control parameters for a selected output and zone.

            Args:
                output (int):
                    * Specifies which heater output to query
                    * 1 or 2

                zone (int):
                    * Specifies which zone in the table to query
                    * 1 to 10

            Return:
                (Model335ControlLoopZone):
                    * See Model335ControlLoopZone class

        """
        zone_parameters = self.query(f"ZONE? {output},{zone}").split(",")
        control_loop_zone_parameters = Model335ControlLoopZoneSettings(float(zone_parameters[0]),
                                                                       float(zone_parameters[1]),
                                                                       float(zone_parameters[2]),
                                                                       float(zone_parameters[3]),
                                                                       float(zone_parameters[4]),
                                                                       Model335HeaterRange(int(zone_parameters[5])),
                                                                       Model335InputSensor(int(zone_parameters[6])),
                                                                       float(zone_parameters[7]))
        return control_loop_zone_parameters

    def _disable_emulation(self):
        """Disables emulation mode so that instrument is compatible with Python Driver."""
        self.command("EMUL 0", check_errors=False)


__all__ = ['Model335', 'Model335AutoTuneMode', 'Model335BrightnessLevel', 'Model335ControlLoopZoneSettings',
           'Model335ControlTypes', 'Model335CurveFormat', 'Model335CurveFormat', 'Model335CurveTemperatureCoefficient',
           'Model335DiodeCurrent', 'Model335DiodeRange', 'Model335DisplayFieldUnits', 'Model335DisplayInputChannel',
           'Model335DisplaySetup', 'Model335HeaterError', 'Model335HeaterOutputDisplay', 'Model335HeaterOutputMode',
           'Model335HeaterOutputUnits', 'Model335HeaterOutType', 'Model335HeaterRange', 'Model335HeaterResistance',
           'Model335HeaterVoltageRange', 'Model335InputReadingStatus', 'Model335InputSensor',
           'Model335InputSensorSettings', 'Model335InputSensorType', 'Model335InputSensorUnits',
           'Model335InterfaceMode', 'Model335MonitorOutUnits', 'Model335OperationEvent', 'Model335Polarity',
           'Model335RelayControlAlarm', 'Model335RelayControlMode', 'Model335RTDRange', 'Model335ServiceRequestEnable',
           'Model335StandardEventRegister', 'Model335StatusByteRegister', 'Model335ThermocoupleRange',
           'Model335WarmupControl']
