"""Implements functionality unique to the Lake Shore Model 346."""

from enum import IntEnum  # pylint: disable=unused-import
from lakeshore.temperature_controllers import TemperatureController, CurveHeader, OperationEvent
from lakeshore.xip_instrument import XIPInstrument, StandardEventRegister, StatusByteRegister, RegisterBase
from lakeshore.model_346_enums import Model346Enums

Model346CurveHeader = CurveHeader
Model346StandardEventRegister = StandardEventRegister
Model346StatusByteRegister = StatusByteRegister
Model346OperationEvent = OperationEvent


class Model346OperationRegister(RegisterBase):
    """Class object representing the operation status register.

        (Not yet implemented)
    """


class Model346QuestionableRegister(RegisterBase):
    """Class object representing the questionable status register.

        (Not yet implemented)
    """


class Model346InputSensorSettings:
    """Class object used in the get/set_input_sensor methods."""

    def __init__(self, sensor_type, autorange_enable, compensation, units, input_range=None):
        """Constructor for the InputSensor class.

            Args:
                sensor_type (Model346Enums.InputSensorType):
                    Specifies input sensor type.
                autorange_enable (bool):
                    Specifies autoranging (False = off, True = on).
                compensation (bool):
                    Specifies input compensation. (False = off, True = on).
                units (Model346Enums.InputSensorUnits):
                    Specifies the preferred units parameter for sensor readings and for the control set-point.
                input_range (IntEnum):
                    Specifies input range if autorange_enable is False.
                    See IntEnum classes: Model346Enums.DiodeRange, Model346Enums.PTCRTDRange,
                    and Model346Enums.NTCRTDRange.

        """

        self.sensor_type = sensor_type
        self.autorange_enable = autorange_enable
        self.compensation = compensation
        self.units = units
        self.input_range = input_range


class Model346AlarmSettings:
    """Class used to configure an alarm in conjunction with the set/get_alarm_settings() method for the Model346."""

    def __init__(self, enabled, high_limit, low_limit, deadband, latch, audible, visible):
        """Constructor for AlarmSettings class.

            Args:
                enabled (bool):
                    Enables or Disables the alarm.
                high_limit (float):
                    Specifies the high limit for the alarm in Kelvin.
                low_limit (float):
                    Specifies the low limit for the alarm in Kelvin.
                deadband (float):
                    Specifies the deadband for the alarm in Kelvin.
                latch (bool):
                    Specifies whether the alarm latches when triggered.
                audible (bool):
                    Specifies whether the alarm is audible when triggered.
                visible (bool):
                    Specifies whether the alarm is visible when triggered.

        """
        self.enabled = enabled
        self.high_value = high_limit
        self.low_value = low_limit
        self.deadband = deadband
        self.latch = latch
        self.audible = audible
        self.visible = visible


class Model346StabilitySettings:
    """Class used to configure an alarm in conjunction with the set/get_alarm_settings() method for the Model346."""

    def __init__(self, enabled, acceptable_error, max_reading_to_reading_delta, settle_time, latch, audible, visible):
        """Constructor for AlarmSettings class.

            Args:
                enabled (bool):
                    Enables or Disables the alarm.
                acceptable_error (float):
                    Specifies max acceptable error between setpoint and reading.
                max_reading_to_reading_delta (float):
                    Specifies max difference between two readings.
                settle_time (float):
                    Specifies the amount of time both conditions must be true.
                latch (bool):
                    Specifies whether the stability latches when triggered.
                audible (bool):
                    Specifies whether the stability is audible when triggered.
                visible (bool):
                    Specifies whether the stability is visible when triggered.

        """
        self.enabled = enabled
        self.acceptable_error = acceptable_error
        self.max_reading_to_reading_delta = max_reading_to_reading_delta
        self.settle_time = settle_time
        self.latch = latch
        self.audible = audible
        self.visible = visible


class Model346ControlLoopZoneSettings:
    """Control loop configuration for a particular heater output and zone."""

    def __init__(self, upper_bound, proportional, integral, derivative, manual_out_value, heater_range, channel, rate,
                 output_limit=100.0):
        """Constructor.

            Args:
                upper_bound (float):
                    Specifies the upper set-point boundary of this zone in temperature units.
                proportional (float):
                    Specifies the proportional gain for this zone (0.1 to 100,000).
                integral (float):
                    Specifies the integral gain for this zone (0.1 to 100,000).
                derivative (float):
                    Specifies the derivative gain for this zone (0 to 20000).
                manual_out_value (float):
                    Specifies the manual output for this zone (0 to 100 %).
                heater_range (self.HeaterRange):
                    Specifies the heater range for this zone.
                    See self.HeaterRange IntEnum class.
                channel (alphanumeric):
                    Passing the NONE member will use the previously assigned sensor.
                rate (float):
                    Specifies the ramp rate for this zone (0.1 - 100 K/min). 0 disables ramping.

        """

        self.upper_bound = upper_bound
        self.proportional = proportional
        self.integral = integral
        self.derivative = derivative
        self.manual_out_value = manual_out_value
        self.output_limit = output_limit
        self.heater_range = heater_range
        self.channel = channel
        self.rate = rate


class Model346InputReadingStatus(RegisterBase):
    """Class object representing the input status flag bits."""

    bit_names = [
        "hardware_settling",
        "",
        "",
        "current_source_in_compliance",
        "temperature_underrange",
        "temperature_overrange",
        "sensor_units_readings_under_range",
        "sensor_units_readings_over_range"
    ]

    def __init__(self, hardware_settling, current_source_in_compliance, temperature_underrange, temperature_overrange,
                 sensor_units_readings_under_range, sensor_units_readings_over_range):
        self.hardware_settling = hardware_settling
        self.current_source_in_compliance = current_source_in_compliance
        self.temperature_underrange = temperature_underrange
        self.temperature_overrange = temperature_overrange
        self.sensor_units_readings_under_range = sensor_units_readings_under_range
        self.sensor_units_readings_over_range = sensor_units_readings_over_range


class Model346InputReadingOperationStatus(RegisterBase):
    """Class object representing the input reading operation status flag bits."""

    bit_names = [
        "curve_applied",
        "reading_in_celsius",
        "",
        "",
        "",
        "",
        "low_alarm_active",
        "high_alarm_active"
    ]

    def __init__(self, curve_applied, reading_in_celsius, low_alarm_active, high_alarm_active):
        self.curve_applied = curve_applied
        self.reading_in_celsius = reading_in_celsius
        self.low_alarm_active = low_alarm_active
        self.high_alarm_active = high_alarm_active


class Model346OutputOperationStatus(RegisterBase):
    """Class object representing the output operation status flag bits."""

    bit_names = [
        "",
        "ramp_active",
        "",
        "",
        "stabilizing",
        "stable",
        "warmup_mode",
        "warm"
    ]

    def __init__(self, ramp_active, stabilizing, stable, warmup_mode, warm):
        self.ramp_active = ramp_active
        self.stabilizing = stabilizing
        self.stable = stable
        self.warmup_mode = warmup_mode
        self.warm = warm


class OptionCard:
    """Represents an option card with additional information."""

    def __init__(self, card_type, max_channels, channels):
        self.card_type = card_type
        self.max_channels = max_channels
        self.channels = channels

    def __repr__(self):
        return f"OptionCard(type={self.card_type.name}, max_channels={self.max_channels}, channels={self.channels})"


class Model346(Model346Enums, XIPInstrument, TemperatureController):
    """
    Class for interaction with the Lake Shore Model 346 cryogenic temperature controller.
    """

    option_card_slots = ["E", "F", "G", "H"]

    # Define the max number of channels for each option card. Only supported types are listed
    max_channels = {
        Model346Enums.OptionCardType.SCANNER: 4,
        Model346Enums.OptionCardType.THERMOCOUPLE: 2,
    }

    vid_pid = [(0x1FB9, 0x0307)]

    def __init__(self,
                 serial_number=None,
                 com_port=None,
                 baud_rate=921600,
                 flow_control=False,
                 timeout=5.0,
                 ip_address=None,
                 tcp_port=7777,
                 **kwargs):

        super().__init__(
            serial_number,
            com_port,
            baud_rate,
            flow_control,
            timeout,
            ip_address,
            tcp_port,
            **kwargs)

    def get_option_card_slot(self):
        """
        Returns the available option card slots.
        """
        return self.option_card_slots

    def get_digit_input_status(self):
        """Returns the status of the digital inputs.

            Returns:
                dict[str, int]:
                    {"input_one": int, "input_two": int}

        """
        input_status = self.query("DIGIN?").split(",")
        return {"input_one": int(input_status[0]), "input_two": int(input_status[1])}

    def set_alarm_settings(self, input_channel, alarm_settings):
        """Sets the configuration of a particular alarm.

            Args:
                input_channel (str):
                    Specifies the input channel to configure (e.g., A, B, C1, C2, etc.).
                alarm_settings (Model346AlarmSettings):
                    The configuration that should be applied to the alarm.

            Command Format:
                ALARM <input>, <enabled>, <high limit>, <low limit>, <deadband>,
                <latch>, <audible>, <visible>
        """
        command_string = (
            f"ALARM {input_channel},{int(alarm_settings.enabled)},"
            f"{alarm_settings.high_value},{alarm_settings.low_value},"
            f"{alarm_settings.deadband},{int(alarm_settings.latch)},"
            f"{int(alarm_settings.audible)},{int(alarm_settings.visible)}"
        )
        self.command(command_string)

    def get_alarm_settings(self, alarm_id):
        """Returns present configuration of a particular alarm.

            Args:
                alarm_id (int):
                    Specifies the alarm of interest.

            Returns:
                Model346AlarmSettings:
                    An Model346AlarmSettings object populated with the respective alarm parameters.

        """
        alarm_params = self.query(f"ALARM? {alarm_id}").split(",")
        return Model346AlarmSettings(
            enabled=bool(int(alarm_params[0])),
            high_limit=float(alarm_params[1]),
            low_limit=float(alarm_params[2]),
            deadband=float(alarm_params[3]),
            latch=bool(int(alarm_params[4])),
            audible=bool(int(alarm_params[5])),
            visible=bool(int(alarm_params[6]))
        )

    def turn_alarm_off(self, alarm_id):
        """Sets the output mode of a particular alarm to NONE (off).

                Args:
                    alarm_id (int):
                        Specifies the alarm of interest.

        """
        self.command(f"ALARM {alarm_id},,,,{self.AlarmType.NONE},")

    def set_stability_settings(self, output_channel, stability_settings):
        """Sets the configuration of a particular alarm.

            Args:
                output_channel (str):
                    Specifies the output channel to configure (e.g., 1, 2, 5, 6, 9 etc.).
                stability_settings (Model346StabilitySettings):
                    The configuration that should be applied to the output.

            Command Format:
                OUTSTABLE <output>, <enabled>, <high limit>, <low limit>, <deadband>,
                <latch>, <audible>, <visible>
        """
        command_string = (
            f"OUTSTABLE {output_channel},{int(alarm_settings.enabled)},"
            f"{stability_settings.acceptable_error},{stability_settings.max_reading_to_reading_delta},"
            f"{stability_settings.settle_time},{int(stability_settings.latch)},"
            f"{int(stability_settings.audible)},{int(stability_settings.visible)}"
        )
        self.command(command_string)

    def get_stability_settings(self, output_channel):
        """Returns present configuration of a particular alarm.

            Args:
                output_channel (int):
                    Specifies the output of interest.

            Returns:
                Model346StabilitySettings:
                    An Model346StabilitySettings object populated with the respective stability parameters.

        """
        stability_params = self.query(f"OUTSTABLE? {output_channel}").split(",")
        return Model346StabilitySettings(
            enabled=bool(int(stability_params[0])),
            acceptable_error=float(stability_params[1]),
            max_reading_to_reading_delta=float(stability_params[2]),
            settle_time=float(stability_params[3]),
            latch=bool(int(stability_params[4])),
            audible=bool(int(stability_params[5])),
            visible=bool(int(stability_params[6]))
        )

    def turn_relay_on(self, relay_number):
        """Turns the specified relay on.

            Args:
                relay_number (int):
                    The relay to turn on.
                    Options are:
                    1 or 2.

        """
        input_channel = None
        condition = 0
        self.command(f"RELAY {relay_number},1,{input_channel},{condition}")

    def turn_relay_off(self, relay_number):
        """Turns the specified relay off.

            Args:
                relay_number (int):
                    The relay to turn off.
                    Options are:
                    1 or 2.

        """
        input_channel = None
        condition = 0
        self.command(f"RELAY {relay_number},0,{input_channel},{condition}")

    def set_input_sensor(self, input_channel, sensor_params):
        """Sets the sensor type and associated parameters.

            Args:
                input_channel (str):
                    Specifies input to configure (A - H4).
                sensor_params (Model346InputSensorSettings):
                    See Model346InputSensorSettings class.

        """
        autorange_enable = sensor_params.autorange_enable
        if autorange_enable:
            input_range = 0
        else:
            input_range = sensor_params.input_range

        self.command(f"INTYPE {input_channel},{sensor_params.sensor_type},{int(autorange_enable)},"
                     f"{input_range},{int(sensor_params.compensation)},{sensor_params.units}")

    def get_input_sensor(self, input_channel):
        """Sets the sensor type and associated parameters.

            Args:
                input_channel (str):
                    Specifies input to configure (A - H4).

            Returns:
                Model346InputSensorSettings:
                    The configured sensor settings for a particular input sensor.

        """
        sensor_params = self.query(f"INTYPE? {input_channel}").split(",")
        sensor_type = Model346Enums.InputSensorType(int(sensor_params[0]))

        input_range = -1
        if sensor_type == Model346Enums.InputSensorType.DIODE:
            input_range = Model346Enums.DiodeRange(int(sensor_params[2]))
        elif sensor_type == Model346Enums.InputSensorType.NTC_RTD:
            input_range = Model346Enums.NTCRTDRange(int(sensor_params[2]))
        elif sensor_type == Model346Enums.InputSensorType.PLATINUM_RTD:
            input_range = Model346Enums.PTCRTDRange(int(sensor_params[2]))
        elif sensor_type == Model346Enums.InputSensorType.THERMOCOUPLE:
            input_range = Model346Enums.ThermocoupleRange(int(sensor_params[2]))

        return Model346InputSensorSettings(sensor_type,
                                           bool(int(sensor_params[1])),
                                           bool(int(sensor_params[3])),
                                           self.InputSensorUnits(int(sensor_params[4])),
                                           input_range)

    def set_heater_range(self, output, heater_range):
        """Sets the heater range for a particular output.

            The range setting has no effect if an output is in
            the Off mode, and does not apply to an output in Monitor
            Out mode. An output in Monitor Out mode is always on.

            Args:
                output (int):
                    Specifies which output to configure (1 - 4).
                heater_range (Model346Enums.HeaterRange):
                    The heater range to apply to a particular output.

        """
        self.command(f"RANGE {output},{heater_range}")

    def get_heater_range(self, output):
        """Returns the heater range for a particular output.

            Args:
                output (int):
                    Specifies which output to query (1 - 4).

            Returns:
                (Model346Enums.HeaterRange):
                    The heater range being applied to a particular output.

        """
        heater_range = int(self.query(f"RANGE? {output}"))
        return Model346Enums.HeaterRange(heater_range)

    def set_heater_autorange(self, output, enabled):
        """Sets the heater autorange  setting for a particular output.

            Args:
                output (int):
                    Specifies which output to configure (1 - 4).
                enabled (bool):
                    Whether autorange should be enabled or disabled.

        """
        self.command(f"HTRAUTO {output},{enabled}")

    def get_heater_autorange(self, output):
        """Returns the heater autorange setting for a particular output.

            Args:
                output (int):
                    Specifies which output to query (1 - 4).

            Returns:
                (bool):
                    Whether autorange should be enabled or disabled.

        """
        heater_range = int(self.query(f"HTRAUTO? {output}"))
        return Model346Enums.HeaterRange(heater_range)

    def set_analog_out_state(self, output, analog_out_state):
        """Sets the analog out state to enable or disable

            Args:
                output (int):
                    Specifies which output to configure (5 - 8).
                analog_out_state (int):
                    OFF = 0 , ON = 1.
        """

        self.command(f"RANGE {output},{analog_out_state}")

    def get_analog_out_state(self, output):
        """Returns the analog state for a particular output.

            Args:
                output (int):
                    Specifies which output to query (5 - 8).

            Returns:
                (int):
                    The analog output state being applied to a particular output.
                    OFF = 0, ON = 1.

        """
        analog_out_range = int(self.query(f"RANGE? {output}"))
        return analog_out_range

    def set_output_percent_limit(self, output, percent_limit):
        """Sets the output percent limit for a particular output.
        Args:
            output (int):
                Specifies which output to configure (1 - 10).
            percent_limit (int):
                Sets a percentage limit for a particular output.
            """
        self.command(f"OUTLIMIT {output},{percent_limit}")

    def get_output_percent_limit(self, output):
        """Sets the output percent limit for a particular output.
        Args:
            output (int):
                Specifies which output to configure (1 - 10).
        Returns:
             (int):
              The set percentage limit for a particular output.
            """
        output_limit = int(self.query(f"OUTLIMIT? {output}"))
        return output_limit

    def all_heaters_off(self):
        """Recreates the front panel safety feature of shutting off all heaters."""
        self.command(
            "RANGE 1,0;RANGE 2,0;RANGE 3,0;RANGE 4,0;RANGE 5,0;RANGE 6,0;RANGE 7,0;RANGE 8,0;RANGE 9,0;RANGE 10,0;")

    def set_heater_setup(self, output, heater_resistance, max_output, output_units):
        """Method to configure the heaters.

            Args:
                output (int):
                    Specifies which heater output to configure (1 - 4).
                heater_resistance (float):
                    10 to 100 ohms.
                max_output (float):
                    User defined maximum output.
                    Represents 100% output as either power (watts) or current (amps)
                    depending on the output_units parameter.
                output_units (Model346Enums.HeaterOutputUnits):
                    Specifies whether the heater output displays in power or current.

        """
        self.command(f"HTRSET {output},{heater_resistance},{max_output},{output_units}")

    def get_heater_setup(self, output):
        """Returns the heater configuration status.

            Args:
                output (int):
                    Specifies which heater output to configure (1 - 4)

            Returns:
                dict[str, float | Model346Enums.HeaterOutputUnits]:
                    {"heater_resistance": float, "max_output": float, "output_units": HeaterOutputUnits}

        """
        heater_setup = self.query(f"HTRSET? {output}").split(",")
        return {
            "heater_resistance": (int(heater_setup[0])),
            "max_output": float(heater_setup[1]),  # Keep as float
            "output_units": self.HeaterOutputUnits(int(heater_setup[2]))  # Rename key to match expected format
        }

    def get_heater_output_measurements(self, output):
        """Returns the heater output measurements.

            Args:
                output (int):
                    Specifies which heater output to query (1 - 4)

            Returns:
                dict[str, float ]:
                    {"heater_voltage": float, "heater_current": float, "heater_resistance": float, "heater_power": float}

        """
        heater_measurements = self.query(f"HTRDIAG? {output}").split(",")
        return {
            "heater_voltage": float(heater_measurements[0]),
            "heater_current": float(heater_measurements[1]),
            "heater_resistance": float(heater_measurements[2]),
            "heater_power": float(heater_measurements[3])
        }

    def get_calculated_heater_output(self, output):
        """Returns the calculated output value and power for the specified output.

            Args:
                output (int):
                    Specifies which output to query (1 - 10).

            Returns:
                dict[str, float]:
                    {"output_value": float, "output_power": float}
                    
                    For outputs 1-4: output_value is current in Amperes
                    For outputs 5-8: output_value is voltage in Volts, output_power is 0.0
                    For outputs 9-10: output_value is sum of currents, output_power is sum of powers

        """
        heater_output = self.query(f"HTROUT? {output}").split(",")
        return {
            "output_value": float(heater_output[0]),
            "output_power": float(heater_output[1])
        }

    def set_output_mode(self, output, mode, input_channel, powerup_enable=False, warmup=False):
        """Configures the output mode of a particular output.

            Args:
                output (int):
                    Specifies which output to configure (1 - 8)
                mode (Model346Enums.OutputMode):
                    Specifies the control mode.
                input_channel (str):
                    Specifies which input to use for control (A - H4). 
                    Unused if not in PID mode.
                powerup_enable (bool):
                    Specifies whether the output remains on (True)
                    or shuts off after power cycle (False).
                warmup (bool):
                    Specifies whether the output is enabled and set when a WARM is issued (True)
                    or not (False).

        """
        command_string = f"OUTMODE {output},{mode},{input_channel},{int(powerup_enable)},{int(warmup)}"
        self.command(command_string)

    def get_output_mode(self, output):
        """Returns the output mode for a particular output.

            Args:
                output (int):
                    Specifies which output to retrieve (1 - 8).

            Returns:
                dict[str, Model346Enums.OutputMode | str | bool]:
                    {"mode": OutputMode, "input_channel": str, "powerup_enable": bool, "warmup": bool}

        """
        response = self.query(f"OUTMODE? {output}").split(",")
        return {
            "mode": self.OutputMode(int(response[0])),
            "input_channel": response[1],
            "powerup_enable": bool(int(response[2])),
            "warmup": bool(int(response[3]))
        }

    def start_warmup(self, room_temperature=293.15, percent_out=10):
        """Starts the warmup process for all heaters configured with
        warmup set to True in OUTMODE

        Args:
            room_temperature (float):
                Specifies the room temperature in degrees Kelvin, defaulting to 293.15 K or about 68 F.
        """
        self.command(f"WARM {room_temperature}, {percent_out}")

    def set_analog_output_settings(self, output, high_value, low_value):
        """Configures a voltage-controlled output.

            Use the set_output_mode command to set the output mode to Monitor Out.

            Args:
                output (int):
                    Analog output channel to configure (5 - 8)
                high_value (float):
                    Represents the data at which the Monitor Out reaches +100% output.
                low_value (float):
                    Represents the data at which the analog output reaches 0% output.

        """
        command_string = f"ANALOG {output},{high_value},{low_value}"
        self.command(command_string)

    def get_analog_output_settings(self, output):
        """Used to obtain the monitor out parameters for a specific output.

            Args:
                output (int):
                    Analog output of interest (5 - 8).

            Returns:
                dict[str, float]:
                    {"high_value": float, "low_value": float}

        """
        response = self.query(f"ANALOG? {output}").split(",")
        return {"high_value": float(response[0]), "low_value": float(response[1])}

    def get_alarm_status(self, channel):
        """Implementation does not exist yet (ALARMST?). Overrides from base."""
        raise NotImplementedError("Implementation does not exist yet")

    def reset_alarm_status(self):
        """Implementation does not exist yet (ALRMST?). Overrides from base."""
        raise NotImplementedError("Implementation does not exist yet")

    def set_ieee_488(self, address):
        """Implementation does not exist yet (IEEE). Overrides from base."""
        raise NotImplementedError("Implementation does not exist yet")

    def get_ieee_488(self):
        """Implementation does not exist yet (IEEE?). Overrides from base."""
        raise NotImplementedError("Implementation does not exist yet")

    def set_keypad_lock(self, state):
        """Sets the state of the front panel keypad lock.

            Args:
                state (bool): The desired state of the keypad lock (True for locked, False for unlocked).

        """
        command_string = f"SYSTem:KLOCk {int(state)}"
        self.command(command_string)

    def get_keypad_lock(self):
        """Returns the current state of the front panel keypad lock.

            Returns:
                bool: True if the keypad is locked, False if it is unlocked.

        """
        response = self.query("SYSTem:KLOCk?")
        return bool(int(response.strip()))

    def set_remote_interface_mode(self, mode):
        """Implementation does not exist yet (MODE). Overrides from base."""
        raise NotImplementedError("Implementation does not exist yet")

    def get_remote_interface_mode(self):
        """Implementation does not exist yet (MODE?). Overrides from base."""
        raise NotImplementedError("Implementation does not exist yet")

    def reset_min_max_data(self, channel):
        """Resets the minimum and maximum reading data for the give input, or all inputs if ALL is specified.

            Args:
                channel (str):
                    Specifies the input channel to reset (A - H4) or ALL to reset all inputs.

        """
        command_string = f"MNMXRST {channel}"
        self.command(command_string)

    def get_input_reading_status(self, input_channel):
        """Returns the status of the specified input channel.

            Args:
                input_channel (str):
                    Specifies the input channel to query (A - H4).

            Returns:
                (InputReadingStatus):
                    Boolean representation of each bit of the input status flag register.

        """
        response = int(self.query(f"RDGST? {input_channel}"))
        return Model346InputReadingStatus.from_integer(response)

    def get_input_reading_operation_status(self, input_channel):
        """Returns the operation status of the specified input channel.

            Args:
                input_channel (str):
                    Specifies the input channel to query (A - H4).

            Returns:
                (Model346InputReadingOperationStatus):
                    Boolean representation of each bit of the input operation status flag register.
                    Includes: curve_applied, reading_in_celsius, low_alarm_active, high_alarm_active.

        """
        response = int(self.query(f"RDGOPR? {input_channel}"))
        return Model346InputReadingOperationStatus.from_integer(response)

    def get_output_operation_status(self, output):
        """Returns the operation status of the specified output.

            Args:
                output (int):
                    Specifies the output to query (1 - 10).

            Returns:
                (Model346OutputOperationStatus):
                    Boolean representation of each bit of the output operation status flag register.
                    Includes: ramp_active, stabilizing, stable, warmup_mode, warm.

        """
        response = int(self.query(f"OUTOPR? {output}"))
        return Model346OutputOperationStatus.from_integer(response)

    def _get_thermocouple_junction_temp(self, input_channel):
        """Returns the thermocouple junction temperature for the specified input channel.

            Args:
                input_channel (str):
                    Specifies the input channel to query (A - H4).

            Returns:
                float:
                    The thermocouple junction temperature in degrees Kelvin.

        """
        response = float(self.query(f"TEMP? {input_channel}"))
        return response

    def set_heater_limit(self, output, enabled, short_circuit_resistance, open_circuit_resistance):
        """Enables or disables the heater limit for a particular output and sets the bounds.

            Args:
                output (int):
                    Specifies which output to configure (1 - 4).
                enabled (int):
                    Specifies whether the heater limit is enabled.
                short_circuit_resistance (float):
                    Specifies the short circuit limit in ohms.
                open_circuit_resistance (float):
                    Specifies the open circuit limit in ohms.

        """
        self.command(f"HTRLIM {output},{int(enabled)},{short_circuit_resistance},{open_circuit_resistance}")

    def get_heater_limit(self, output):
        """Returns the heater limit settings for a particular output.

            Args:
                output (int):
                    Specifies which output to query (1 - 4).

            Returns:
                dict[str, float | bool]:
                    {"enabled": bool, "short_circuit_resistance": float, "open_circuit_resistance": float}

        """
        response = self.query(f"HTRLIM? {output}").split(",")
        return {
            "enabled": bool(int(response[0])),
            "short_circuit_resistance": float(response[1]),
            "open_circuit_resistance": float(response[2])
        }

    def reset_control_setpoint(self, output):
        """Resets the control setpoint for a particular output.

            Args:
                output (int):
                    Specifies which output to reset (1 - 8).

        """
        self.command(f"SETPRST {output}")

    def get_ramp_setpoint(self, output):
        """Returns the current setpoint for a particular output.

            Args:
                output (int):
                    Specifies which output to query (1 - 8).

            Returns:
                float:
                    The current control setpoint for the specified output.

        """
        return float(self.query(f"RAMPSETP? {output}"))

    def set_control_loop_zone_table(self, output, zone_number, zone_settings):
        """Sets the control loop zone table for a particular output.

            Args:
                output (int):
                    Specifies which output to configure (1 - 8).
                zone_number (int):
                    Specifies which zone to configure (1 - 10).
                zone_settings (Model346ControlLoopZeroSettings):
                    The settings to apply to the specified zone.

        """
        command_string = (f"ZONE {output},{zone_number},{zone_settings.upper_bound},{zone_settings.proportional}," +
                          f"{zone_settings.integral},{zone_settings.derivative},{zone_settings.manual_out_value}," +
                          f"{zone_settings.output_limit},{zone_settings.heater_range},{zone_settings.channel}," +
                          f"{zone_settings.rate}")
        self.command(command_string)

    def get_control_loop_zone_table(self, output, zone_number):
        """Returns the control loop zone table for a particular output and zone.

            Args:
                output (int):
                    Specifies which output to query (1 - 8).
                zone_number (int):
                    Specifies which zone to query (1 - 10).

            Returns:
                Model346ControlLoopZoneSettings:
                    The settings for the specified control loop zone.

        """
        response = self.query(f"ZONE? {output},{zone_number}").split(",")
        return Model346ControlLoopZoneSettings(
            upper_bound=float(response[0]),
            proportional=float(response[1]),
            integral=float(response[2]),
            derivative=float(response[3]),
            manual_out_value=float(response[4]),
            output_limit=float(response[5]),
            heater_range=self.HeaterRange(int(response[6])),
            channel=response[7],
            rate=float(response[8])
        )

    def get_curve_number_of_points(self, curve_number):
        """Returns the number of data points in a curve.

            Args:
                curve_number (int):
                    Specifies which curve to query (1 - 60).

            Returns:
                int:
                    The number of points in the specified curve.
                    Returns 0 if the curve is deleted/empty

        """
        return int(self.query(f"CRVNUMPTS? {curve_number}"))

    def get_digital_input_state(self, input_number):
        """Embedded needs to be updated to support this method."""

        raise NotImplementedError("Embedded needs to be updated to support this method")

    def set_relay_alarms(self, relay_number, mode, input_channel, condition):
        """Sets a relay to turn on and off automatically based on the state of the alarm of the specified input channel.

            Args:
                relay_number (int):
                    The relay to configure.
                    Options are:
                    1 or 2.
                mode (Model346Enums.RelayControlMode):
                input_channel (str or int):
                    Specifies which input alarm activates the relay.
                condition (int):
                    Specifies the condition that triggers the relay.

        """
        self.command(f"RELAY {relay_number},{mode},{input_channel},{condition}")

    def get_relay_alarm_control_parameters(self, relay_number):
        """Returns the relay control parameters for a specified relay.

            Args:
                relay_number (int):
                    The relay to query.
                    Options are:
                    1 or 2.

            Returns:
                dict[str, Model346Enums.RelayControlMode | str | int]:
                    {"mode": RelayControlMode, "input_channel": str, "condition": int}

        """
        response = self.query(f"RELAY? {relay_number}").split(",")
        return {
            "mode": self.RelayControlMode(int(response[0])),
            "input_channel": response[1],
            "condition": self.RelayControlAlarm(int(response[2]))
        }

    def set_thermocouple_compensation_offset(self, input_channel, offset):
        """Sets the thermal block compensation offset for a thermocouple input.
        
            Args:
                input_channel (str):
                    Specifies the thermocouple input to configure.
                    Valid channels: E1, E2, F1, F2, G1, G2, H1, H2
                offset (float):
                    Offset value in Kelvin to apply to the thermal block temperature reading
        """
        self.command(f"TCCOMPOFFSET {input_channel},{offset}")

    def get_thermocouple_compensation_offset(self, input_channel):
        """Returns the thermal block compensation offset for a thermocouple input.
        
            Args:
                input_channel (str):
                    Specifies the thermocouple input to query.
                    Valid channels: E1, E2, F1, F2, G1, G2, H1, H2
            
            Returns:
                float:
                    Offset value in Kelvin currently applied to the thermal block reading.
                    Returns 0.0 if no offset has been configured.
        """
        return float(self.query(f"TCCOMPOFFSET? {input_channel}"))

    def get_installed_option_cards(self):
        """Queries the installed option cards and returns detailed information.

        Returns:
            dict[str, OptionCard]: A dictionary mapping slots (E, F, G, H) to OptionCard objects.
        """
        # Query the CARDS? command to get the option card types
        response = self.query("CARDS?").split(",")

        # Map the response to OptionCard objects
        return {
            slot: OptionCard(
                card_type=Model346Enums.OptionCardType(int(response[i])),
                max_channels=self.max_channels.get(Model346Enums.OptionCardType(int(response[i])), 0),
                channels=self.get_option_card_channels(slot) if Model346Enums.OptionCardType(
                    int(response[i])) in self.max_channels else []
            )
            for i, slot in enumerate(self.option_card_slots)
        }

    def get_option_card_type(self, slot):
        """Returns the type of option card connected to the specified slot.

        Args:
            slot (str): Specifies the slot to query (E, F, G, H).

        Returns:
            str: The type of option card connected to the slot:
                - "Nothing"
                - "Scanner"
                - "Motor" # Currently not supported by python driver
                - "Level Sense" # Currently not supported by python driver
                - "Thermocouple"

        Raises:
            ValueError: If the slot is invalid.
        """
        if slot not in self.option_card_slots:
            raise ValueError(f"Invalid slot: {slot}. Valid slots are {', '.join(self.option_card_slots)}.")

        # Query the CARDS? command
        response = self.query("CARDS?").split(",")

        slot_index = self.option_card_slots.index(slot)

        # Return the type of the option card connected to the slot
        return Model346Enums.OptionCardType(int(response[slot_index]))

    def get_option_card_channels(self, slot):
        """Returns the number of channels available on the specified option card slot.

        Args:
            slot (str): Specifies the slot to query (E, F, G, H).

        Returns:
            int: The number of channels available on the option card in the specified slot.

        Raises:
            ValueError: If the slot is invalid.
        """
        if slot not in self.option_card_slots:
            raise ValueError(f"Invalid slot: {slot}. Valid slots are {', '.join(self.option_card_slots)}.")

        # Get the type of the option card in the specified slot
        option_card_type = self.get_option_card_type(slot)

        # If option card is not a scanner or thermocouple, raise value error
        if option_card_type not in [self.OptionCardType.SCANNER, self.OptionCardType.THERMOCOUPLE]:
            raise ValueError(f"Unsupported option card type: {option_card_type.name}.")
        # Get the max channel count for the option card type
        max_channel_count = self.max_channels.get(option_card_type, 0)

        # Generate the list of channels based on the max channel count
        return [f"{slot}{i}" for i in range(1, max_channel_count + 1)]


__all__ = ['Model346AlarmSettings', 'Model346InputSensorSettings', 'Model346', 'Model346CurveHeader',
           'Model346OperationEvent',
           'Model346OperationRegister', 'Model346QuestionableRegister', 'Model346StandardEventRegister',
           'Model346StatusByteRegister', 'Model346InputReadingStatus', 'Model346InputReadingOperationStatus',
           'Model346OutputOperationStatus', 'Model346ControlLoopZoneSettings']
