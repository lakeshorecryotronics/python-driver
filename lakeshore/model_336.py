"""Implements functionality unique to the Lake Shore Model 336 cryogenic temperature controller."""
from enum import IntEnum

from .generic_instrument import RegisterBase
from .temperature_controllers import TemperatureController, InstrumentException, StandardEventRegister, OperationEvent, \
    CurveHeader, AlarmSettings

Model336RelayControlMode = TemperatureController.RelayControlMode
Model336RelayControlAlarm = TemperatureController.RelayControlAlarm
Model336InterfaceMode = TemperatureController.InterfaceMode
Model336HeaterError = TemperatureController.HeaterError
Model336CurveFormat = TemperatureController.CurveFormat
Model336CurveTemperatureCoefficients = TemperatureController.CurveTemperatureCoefficient
Model336AutoTuneMode = TemperatureController.AutotuneMode
Model336HeaterResistance = TemperatureController.HeaterResistance
Model336Polarity = TemperatureController.Polarity
Model336DiodeCurrent = TemperatureController.DiodeCurrent
Model336HeaterOutputUnits = TemperatureController.HeaterOutputUnits
Model336InputSensorUnits = TemperatureController.InputSensorUnits
Model336ControlTypes = TemperatureController.ControlTypes
Model336LanStatus = TemperatureController.LanStatus
Model336Interface = TemperatureController.Interface
Model336CurveHeader = CurveHeader
Model336AlarmSettings = AlarmSettings
Model336DisplayFields = TemperatureController.DisplayFields
Model336DisplayFieldsSize = TemperatureController.DisplayFieldsSize
Model336StandardEventRegister = StandardEventRegister
Model336OperationEvent = OperationEvent


class Model336InputChannel(IntEnum):
    """Enumeration where "NONE" is an option for sensor input."""
    NONE = 0
    CHANNEL_A = 1
    CHANNEL_B = 2
    CHANNEL_C = 3
    CHANNEL_D = 4
    CHANNEL_D2 = 5
    CHANNEL_D3 = 6
    CHANNEL_D4 = 7
    CHANNEL_D5 = 8


class Model336DisplaySetupMode(IntEnum):
    """Front panel display setup enum."""
    INPUT_A = 0
    INPUT_B = 1
    INPUT_C = 2
    INPUT_D = 3
    CUSTOM = 4
    FOUR_LOOP = 5
    ALL_INPUTS = 6
    INPUT_D2 = 7
    INPUT_D3 = 8
    INPUT_D4 = 9
    INPUT_D5 = 10


class Model336InputSensorType(IntEnum):
    """Sensor type enumeration.

        THERMOCOUPLE is only valid with the 3060 option, CAPACITANCE is only valid with the 3061 option.
    """
    DISABLED = 0
    DIODE = 1
    PLATINUM_RTD = 2
    NTC_RTD = 3
    THERMOCOUPLE = 4
    CAPACITANCE = 5


class Model336DiodeRange(IntEnum):
    """Diode voltage range enumeration"""
    TWO_POINT_FIVE_VOLTS = 0
    TEN_VOLTS = 1


class Model336RTDRange(IntEnum):
    """RTD resistance range enumeration.

        THIRTY_THOUSAND_OHM and ONE_HUNDRED_THOUSAND_OHM are only valid for NTC RTDs.
    """
    TEN_OHM = 0
    THIRTY_OHM = 1
    HUNDRED_OHM = 2
    THREE_HUNDRED_OHM = 3
    ONE_THOUSAND_OHM = 4
    THREE_THOUSAND_OHM = 5
    TEN_THOUSAND_OHM = 6
    THIRTY_THOUSAND_OHM = 7
    ONE_HUNDRED_THOUSAND_OHM = 8


class Model336ThermocoupleRange(IntEnum):
    """Thermocouple range enumeration."""
    FIFTY_MILLIVOLT = 0


class Model336InputSensorSettings:
    """Class object used in the get/set_input_sensor methods."""

    def __init__(self, sensor_type, autorange_enable, compensation, units, input_range=None):
        """Constructor for the InputSensorSettings class.

            Args:
                sensor_type (Model336InputSensorType):
                    Specifies input sensor type
                autorange_enable (bool):
                    Specifies auto-ranging (False = off, True = on)
                compensation (bool):
                    Specifies input compensation (False = off, True = on)
                units (Model336InputSensorUnits):
                    Specifies the preferred units parameter for sensor readings and for the control set-point.
                input_range (IntEnum)
                    Specifies input range if autorange_enable is false.
                    See IntEnum classes: Model336DiodeRange, Model336RTDRange, andModel336ThermocoupleRange.

        """
        self.sensor_type = sensor_type
        self.autorange_enable = autorange_enable
        self.compensation = compensation
        self.units = units
        self.input_range = input_range


class Model336HeaterOutputMode(IntEnum):
    """Control loop enumeration."""
    OFF = 0
    CLOSED_LOOP = 1
    ZONE = 2
    OPEN_LOOP = 3
    MONITOR_OUT = 4
    WARMUP_SUPPLY = 5


class Model336HeaterRange(IntEnum):
    """Current mode heater enumerations."""
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Model336HeaterVoltageRange(IntEnum):
    """Voltage mode heater enumerations."""
    VOLTAGE_OFF = 0
    VOLTAGE_ON = 1


class Model336DisplayUnits(IntEnum):
    """Panel display units enumeration."""
    KELVIN = 1
    CELSIUS = 2
    SENSOR_UNITS = 3
    MINIMUM_DATA = 4
    MAXIMUM_DATA = 5
    SENSOR_NAME = 6


class Model336ControlLoopZoneSettings:
    """Control loop configuration for a particular heater output and zone."""

    def __init__(self, upper_bound, proportional, integral, derivative, manual_out_value, heater_range, channel, rate):
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
                manual_out_value (float):
                    Specifies the manual output for this zone (0 to 100 %).
                heater_range (Model336HeaterRange):
                    Specifies the heater range for this zone.
                    See Model336HeaterRange IntEnum class.
                channel (Model336InputChannel):
                    See Model336InputChannel IntEnum class.
                    Passing the NONE member will use the previously assigned sensor.
                rate (float):
                    Specifies the ramp rate for this zone ( 0 - 100 K/min).

        """

        self.upper_bound = upper_bound
        self.proportional = proportional
        self.integral = integral
        self.derivative = derivative
        self.manual_out_value = manual_out_value
        self.heater_range = heater_range
        self.channel = channel
        self.rate = rate


class Model336StatusByteRegister(RegisterBase):
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


class Model336ServiceRequestEnable(RegisterBase):
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


class Model336InputReadingStatus(RegisterBase):
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


class Model336(TemperatureController):
    """A class object representing the Lake Shore Model 336 cryogenic temperature controller."""

    vid_pid = [(0x1FB9, 0x0301)]

    # Initiate instrument specific registers
    status_byte_register = Model336StatusByteRegister
    service_request_enable = Model336ServiceRequestEnable

    def __init__(self,
                 serial_number=None,
                 com_port=None,
                 timeout=2.0,
                 ip_address=None,
                 tcp_port=7777,
                 **kwargs):

        # Call the parent init, then fill in values specific to the 336
        TemperatureController.__init__(self, serial_number, com_port, 57600, timeout, ip_address,
                                       tcp_port, **kwargs)

        # Initiate enum types for temperature controllers class
        self.InputChannel = Model336InputChannel
        self.DisplayFieldUnits = Model336DisplayUnits

    # Alias specific temperature controller methods
    get_analog_output_percentage = TemperatureController._get_analog_output_percentage
    set_autotune = TemperatureController._set_autotune
    set_contrast_level = TemperatureController._set_contrast_level
    get_contrast_level = TemperatureController._get_contrast_level
    get_operation_condition = TemperatureController._get_operation_condition
    get_operation_event_enable = TemperatureController._get_operation_event_enable
    set_operation_event_enable = TemperatureController._set_operation_event_enable
    get_operation_event = TemperatureController._get_operation_event
    get_thermocouple_junction_temp = TemperatureController._get_thermocouple_junction_temp
    set_soft_cal_curve_dt_470 = TemperatureController._set_soft_cal_curve_dt_470
    set_soft_cal_curve_pt_100 = TemperatureController._set_soft_cal_curve_pt_100
    set_soft_cal_curve_pt_1000 = TemperatureController._set_soft_cal_curve_pt_1000
    set_filter = TemperatureController._set_filter
    get_filter = TemperatureController._get_filter
    set_network_settings = TemperatureController._set_network_settings
    get_network_settings = TemperatureController._get_network_settings
    get_network_configuration = TemperatureController._get_network_configuration
    set_website_login = TemperatureController._set_website_login
    get_website_login = TemperatureController._get_website_login
    get_celsius_reading = TemperatureController._get_celsius_reading
    set_interface = TemperatureController._set_interface
    get_interface = TemperatureController._get_interface
    get_tuning_control_status = TemperatureController._get_tuning_control_status
    set_diode_excitation_current = TemperatureController._set_diode_excitation_current
    get_diode_excitation_current = TemperatureController._get_diode_excitation_current

    def set_monitor_output_heater(self, output, channel, units, high_value, low_value, polarity):
        """Configures a voltage-controlled output.

            Use the set_heater_output_mode command to set the output mode to Monitor Out.

            Args:
                output (int):
                    Voltage-controlled output to configure (3 or 4)
                channel (Model336InputChannel):
                    Specifies which sensor input to monitor.
                    A member of the Model336InputChannel IntEnum class.
                units (Model336InputSensorUnits):
                    Specifies the units on which to base the output voltage.
                    A member of the Model336InputSensorUnits IntEnum class.
                high_value (float):
                    Represents the data at which the Monitor Out reaches +100% output.
                    Entered in the units designated by the <units> argument.
                low_value (float):
                    Represents the data at which the analog output reaches -100% output if bipolar,
                    or 0% output if unipolar. Entered in the units designated by the <units> argument.
                polarity (Model336Polarity):
                    Specifies whether the output voltage is unipolar or bipolar.
                    Member of the Model336Polarity IntEnum class.

        """
        command_string = f"ANALOG {output},{channel},{units},{high_value},{low_value},{polarity}"
        self.command(command_string)

    def get_monitor_output_heater(self, output):
        """Used to obtain all monitor out parameters for a specific output.

            Args:
                output (int):
                    Voltage-controlled output to configure (3 or 4).

            Returns:
                (dict):
                    See set_monitor_output_heater arguments

        """
        response = self.query(f"ANALOG? {output}").split(",")
        return {"channel": Model336InputChannel(int(response[0])),
                "units": Model336InputSensorUnits(int(response[1])),
                "high_value": float(response[2]),
                "low_value": float(response[3]),
                "polarity": Model336Polarity(int(response[4]))}

    def set_display_setup(self, mode, num_fields="", displayed_output=""):
        """Sets the display mode.

            Args:
                mode (Model336DisplaySetupMode):
                    Member of Model336DisplaySetupMode IntEnum class
                    Specifies display mode for default and 3062 options
                num_fields (IntEnum)
                    When mode is set to custom, specifies the number of fields (Member of Model336DisplayFields).
                    When mode is set to all inputs, specifies size of readings (Member of Model336DisplayFieldsSize).
                displayed_output (int):
                    Configures the bottom half of the custom display screen.
                    Only required if mode is set to CUSTOM.
                    Output: (1 - 4)

        """
        if mode == Model336DisplaySetupMode.CUSTOM:
            if not isinstance(num_fields, Model336DisplayFields):
                raise InstrumentException("num_fields argument must be of type \"Model336DisplaySetupCustom\"")
        elif mode == Model336DisplaySetupMode.ALL_INPUTS:
            if not isinstance(num_fields, Model336DisplayFieldsSize):
                raise InstrumentException("num_fields argument must be of type \"Model336DisplaySetupAllInputs\"")

        command_string = f"DISPLAY {mode},{num_fields},{displayed_output}"
        self.command(command_string)

    def get_display_setup(self):
        """Returns the display mode.

            Returns:
                (dict):
                    See set_display_setup method arguments.
                    Keys: "mode", "num_fields", "displayed_output"

        """
        display_setup_response = self.query("DISPLAY?").split(",")
        mode = Model336DisplaySetupMode(int(display_setup_response[0]))
        if mode == Model336DisplaySetupMode.CUSTOM:
            num_fields = Model336DisplayFields(int(display_setup_response[1]))
            displayed_output = int(display_setup_response[2])
        elif mode == Model336DisplaySetupMode.ALL_INPUTS:
            num_fields = Model336DisplayFieldsSize(int(display_setup_response[1]))
            displayed_output = None
        else:
            num_fields = None
            displayed_output = None

        return {"mode": mode,
                "num_fields": num_fields,
                "displayed_output": displayed_output}

    def set_heater_setup(self, output, heater_resistance, max_current, heater_output):
        """Method to configure the heaters.

            Args:
                output (int):
                    Specifies which heater output to configure (1 or 2).
                heater_resistance (Model336HeaterResistance):
                    Member of Model336HeaterResistance IntEnum class.
                max_current (float):
                    User defined maximum output current (see table 4-11 for max current and resistance relationships).
                heater_output (Model336HeaterOutputUnits):
                    Specifies whether the heater output displays in current or power.
                    Member of Model336HeaterOutputUnits IntEnum class.

        """
        self.command(f"HTRSET {output},{heater_resistance},0,{max_current},{heater_output}")

    def get_heater_setup(self, heater_output):
        """Returns the heater configuration status.

            Args:
                heater_output (int):
                    Specifies which heater output to configure (1 or 2)

            Returns:
                (dict):
                    See set_heater_setup arguments
                    Keys: heater_resistance, max_current, output_display_mode.

        """
        heater_setup = self.query(f"HTRSET? {heater_output}").split(",")
        if int(heater_setup[1]) == 0:
            max_current = float(heater_setup[2])
        else:
            preset_currents = ["USER", 0.707, 1.0, 1.141, 2.0]
            current_index = int(heater_setup[1])
            max_current = preset_currents[current_index]

        return {"heater_resistance": Model336HeaterResistance(int(heater_setup[0])),
                "max_current": max_current,
                "output_display_mode": Model336HeaterOutputUnits(int(heater_setup[3]))}

    def set_input_sensor(self, channel, sensor_parameters):
        """Sets the sensor type and associated parameters.

            Args:
                channel (str):
                    Specifies input to configure ("A" - "D"):
                    3062 option ("D1" - "D5")
                sensor_parameters (Model336InputSensorSettings):
                    See Model336InputSensorSettings class.

        """
        autorange_enable = sensor_parameters.autorange_enable
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
                    Specifies sensor input to configure ("A" or "B")

            Returns:
                (Model336InputSensorSettings):
                    See Model336InputSensorSettings class.

        """
        sensor_config = self.query(f"INTYPE? {channel}").split(",")
        sensor_type = Model336InputSensorType(int(sensor_config[0]))
        autorange_enable = bool(int(sensor_config[1]))
        if autorange_enable:
            input_range = 0
        else:
            if sensor_type == Model336InputSensorType.DIODE:
                input_range = Model336DiodeRange(int(sensor_config[2]))
            elif sensor_type in (Model336InputSensorType.PLATINUM_RTD, Model336InputSensorType.NTC_RTD):
                input_range = Model336RTDRange(int(sensor_config[2]))
            elif sensor_type == Model336InputSensorType.THERMOCOUPLE:
                input_range = Model336ThermocoupleRange(int(sensor_config[2]))
            else:
                input_range = int(sensor_config[2])

        return Model336InputSensorSettings(sensor_type,
                                           bool(int(sensor_config[1])),
                                           bool(int(sensor_config[3])),
                                           Model336InputSensorUnits(int(sensor_config[4])),
                                           input_range)

    def get_all_kelvin_reading(self):
        """Returns the temperature value in kelvin of all channels.

            Returns:
                (list: float):
                    [channel_A, channel_B, channel_C, channel_D]

        """
        kelvin_reading = self.query("KRDG? 0").split(",")
        return [float(channel) for channel in kelvin_reading]

    def set_heater_output_mode(self, output, mode, channel, powerup_enable=False):
        """Configures the heater output mode.

            Args:
                output (int):
                    Specifies which output to configure (1 - 4)
                mode (Model336HeaterOutputMode):
                    Member of Model336HeaterOutputMode IntEnum class.
                    Specifies the control mode.
                channel (Model336InputChannel):
                    Model336InputChannel IntEnum class.
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
                    Specifies which output to retrieve (1 - 4).

            Returns:
                (dict):
                    See set_heater_output_mode method arguments.
                    Keys: mode, channel, powerup_enable.

        """
        outmode = self.query(f"OUTMODE? {output}").split(",")
        return {"mode": Model336HeaterOutputMode(int(outmode[0])),
                "channel": Model336InputChannel(int(outmode[1])),
                "powerup_enable": bool(int(outmode[2]))}

    def set_heater_range(self, output, heater_range):
        """Sets the heater range for a particular output.

            The range setting has no effect if an output is in
            the Off mode, and does not apply to an output in Monitor
            Out mode. An output in Monitor Out mode is always on.

            Args:
                output (int):
                    Specifies which output to configure (1 - 4).
                heater_range (IntEnum):
                    For Outputs 1 and 2: Member of Model336HeaterRange IntEnum class.
                    For Outputs 3 and 4: Model336HeaterVoltageRange IntEnum class.

        """
        self.command(f"RANGE {output},{heater_range}")

    def get_heater_range(self, output):
        """Returns the heater range for a particular output.

            Args:
                output (int):
                    Specifies which output to query (1 or 2).

            Returns:
                (IntEnum):
                    For Outputs 1 and 2: Member of Model336HeaterRange IntEnum class.
                    For Outputs 3 and 4: Member of Model336HeaterVoltageRange IntEnum class.

        """
        heater_range = int(self.query(f"RANGE? {output}"))

        if output in (3, 4):
            heater_range = Model336HeaterVoltageRange(heater_range)
        else:
            heater_range = Model336HeaterRange(heater_range)

        return heater_range

    def all_heaters_off(self):
        """Recreates the front panel safety feature of shutting off all heaters."""
        self.command("RANGE 1,0;RANGE 2,0;RANGE 3,0;RANGE 4,0")

    def get_input_reading_status(self, channel):
        """Reruns the state of the input status flag bits.

            Args:
                channel (str):
                    Specifies which channel to query ("A" - "D").
                    Use "D1" - "D5" for 3062 option.

            Returns:
                (Model336InputReadingStatus):
                    Boolean representation of each bit in the input status flag register.

        """
        response = int(self.query(f"RDGST? {channel}"))
        return Model336InputReadingStatus.from_integer(response)

    def get_all_sensor_reading(self):
        """Returns the sensor unit reading of all channels.

            Returns:
                (list: float):
                    [channel_A, channel_B, channel_C, channel_D]

        """
        sensor_reading = self.query("SRDG? 0").split(",")
        return [float(channel) for channel in sensor_reading]

    def set_warmup_supply_parameter(self, output, control, percentage):
        """Warmup mode applies only to voltage heater outputs 3 and 4.

            The Output mode and Control Input parameters must be configured using the set_monitor_out_parameters()
            method.

            Args:
                output (int):
                    Specifies which output to configure (3 or 4).
                control (Model336ControlTypes):
                    Member of the Model336ControlTypes IntEnum class.
                percentage (float):
                    Specifies the percentage of full scale (10 V) Monitor Out voltage to apply to turn on the external
                    power supply. (A value of 50.5 translates to a 50.5 percent output voltage).

        """
        command_string = f"WARMUP {output},{control},{percentage}"
        self.command(command_string)

    def get_warmup_supply_parameter(self, output):
        """Returns the warmup supply configuration for a particular output.

            Args:
                output (int):
                    Specifies which analog voltage heater output to retrieve (3 or 4).

            Returns:
                (dict):
                    See set_warmup_supply_parameter method arguments

        """
        warmup_supply = self.query(f"WARMUP? {output}").split(",")
        return {"control": Model336ControlTypes(int(warmup_supply[0])),
                "percentage": float(warmup_supply[1])}

    def set_control_loop_zone_table(self, output, zone, control_loop_zone):
        """Configures the output zone parameters.

            Args:
                output (int):
                    Specifies which analog voltage heater output to configure (1 or 2).
                zone (int):
                    Specifies which zone in the table to configure (1 to 10).
                control_loop_zone (Model336ControlLoopZoneSettings):
                    See Model336ControlLoopZoneSettings class.

        """
        command_string = (f"ZONE {output},{zone},{control_loop_zone.upper_bound},{control_loop_zone.proportional}," +
                            f"{control_loop_zone.integral},{control_loop_zone.derivative}," +
                            f"{control_loop_zone.manual_out_value},{control_loop_zone.heater_range}," +
                            f"{control_loop_zone.channel},{control_loop_zone.rate}")
        self.command(command_string)

    def get_control_loop_zone_table(self, output, zone):
        """Returns a list of zone control parameters for a selected output and zone.

            Args:
                output (int):
                    Specifies which heater output to query (1 or 2).
                zone (int):
                    Specifies which zone in the table to query (1 to 10).

            Returns:
                (Model336ControlLoopZoneSettings):
                    See Model336ControlLoopZoneSettings class.

        """
        zone_parameters = self.query(f"ZONE? {output},{zone}").split(",")
        return Model336ControlLoopZoneSettings(float(zone_parameters[0]),
                                               float(zone_parameters[1]),
                                               float(zone_parameters[2]),
                                               float(zone_parameters[3]),
                                               float(zone_parameters[4]),
                                               Model336HeaterRange(int(zone_parameters[5])),
                                               Model336InputChannel(int(zone_parameters[6])),
                                               float(zone_parameters[7]))

    def _autotune_error(self):
        """Method to raise an exception if autotune error has occurred."""

        tuning_status = self.query("TUNEST?").split(",")

        if bool(int(tuning_status[2])):
            raise InstrumentException("An autotune error is present")


__all__ = ['Model336RelayControlMode', 'Model336RelayControlAlarm', 'Model336InterfaceMode', 'Model336HeaterError',
           'Model336CurveFormat', 'Model336CurveTemperatureCoefficients', 'Model336AutoTuneMode',
           'Model336HeaterResistance', 'Model336Polarity', 'Model336DiodeCurrent', 'Model336HeaterOutputUnits',
           'Model336InputSensorUnits', 'Model336ControlTypes', 'Model336LanStatus', 'Model336Interface',
           'Model336CurveHeader', 'Model336AlarmSettings', 'Model336StandardEventRegister', 'Model336OperationEvent',
           'Model336InputChannel', 'Model336DisplaySetupMode', 'Model336DisplayFields',
           'Model336DisplayFieldsSize', 'Model336InputSensorType', 'Model336DiodeRange', 'Model336RTDRange',
           'Model336ThermocoupleRange', 'Model336InputSensorSettings', 'Model336HeaterOutputMode',
           'Model336HeaterRange', 'Model336HeaterVoltageRange', 'Model336DisplayUnits',
           'Model336ControlLoopZoneSettings', 'Model336StatusByteRegister', 'Model336ServiceRequestEnable',
           'Model336InputReadingStatus', 'AlarmSettings', 'Model336']
