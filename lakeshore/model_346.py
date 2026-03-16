"""Implements functionality unique to the Lake Shore Model 346."""

import warnings

from lakeshore.temperature_controllers import TemperatureController, CurveHeader, OperationEvent
from lakeshore.xip_instrument import XIPInstrument, StandardEventRegister, StatusByteRegister, RegisterBase
from lakeshore.model_346_enums import Model346Enums

Model346CurveHeader = CurveHeader
Model346StandardEventRegister = StandardEventRegister
Model346StatusByteRegister = StatusByteRegister
Model346OperationEvent = OperationEvent


class Model346OperationRegister(RegisterBase):
    """Class object representing the operation status register.

        Represents the top-level STATus:OPERation:CONDition? register.

            Bit 0 (weight 1):     CORE Summary Bit (A, B, C1-4, D1-4)
            Bit 1 (weight 2):     OPTion Summary Bit (E, F, G, H)
            Bit 2 (weight 4):     OUTput Summary Bit (1-10)
            Bit 4 (weight 16):    ALL WARM bit
            Bit 15 (weight 32768): External 24V not present

        All other bits (3, 5-14) are not used per the manual.

    """

    bit_names = [
        "core_summary",          # Bit 0: CORE Summary Bit
        "option_summary",        # Bit 1: OPTion Summary Bit
        "output_summary",        # Bit 2: OUTput Summary Bit
        "",                      # Bit 3: not used
        "all_warm",              # Bit 4: ALL WARM bit
        "", "", "", "",          # Bits 5-8: not used
        "", "", "", "",          # Bits 9-12: not used
        "", "",                  # Bits 13-14: not used
        "external_24v_missing"   # Bit 15: External 24V not present
    ]

    def __init__(self,
                 core_summary,
                 option_summary,
                 output_summary,
                 all_warm,
                 external_24v_missing):
        self.core_summary = core_summary
        self.option_summary = option_summary
        self.output_summary = output_summary
        self.all_warm = all_warm
        self.external_24v_missing = external_24v_missing


class Model346QuestionableRegister(RegisterBase):
    """Class object representing the questionable status register.

        Represents the top-level STATus:QUEStionable:CONDition? register.

        The Model 346 status system organizes questionable status into::
        
            - CORE: Inputs A, B, C1-C4, D1-D4 (RDGST? status)
            - OPTion: Option cards E, F, G, H (channels 1-4 each)
            - OUTput: Outputs 1-10 (OUTST? status)
            - FUNCtion: Functions 1-16

    """

    bit_names = [
        "core_summary",     # Bit 0: CORE questionable summary
        "option_summary",   # Bit 1: OPTion questionable summary
        "output_summary",   # Bit 2: OUTput questionable summary
        "function_summary"  # Bit 3: FUNCtion questionable summary
    ]

    def __init__(self,
                 core_summary,
                 option_summary,
                 output_summary,
                 function_summary):
        self.core_summary = core_summary
        self.option_summary = option_summary
        self.output_summary = output_summary
        self.function_summary = function_summary


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
                    Specifies the high limit for the alarm. Units depend on
                    whether a curve is assigned to the input (sensor units if
                    no curve, K or C per INTYPE if a curve is assigned).
                low_limit (float):
                    Specifies the low limit for the alarm.
                deadband (float):
                    Specifies the deadband for the alarm.
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
    """Class used to configure stability settings in conjunction with the set/get_stability_settings() method for the Model346."""

    def __init__(self, enabled, setpoint_error, settle_time, audible, visible):
        """Constructor for StabilitySettings class.

            Args:
                enabled (bool):
                    Enables or Disables the stability.
                setpoint_error (float):
                    Specifies max acceptable error between setpoint and reading.
                settle_time (float):
                    Specifies the amount of time both conditions must be true.
                audible (bool):
                    Specifies whether the stability is audible when triggered.
                visible (bool):
                    Specifies whether the stability is visible when triggered.

        """
        self.enabled = enabled
        self.setpoint_error = setpoint_error
        self.settle_time = settle_time
        self.audible = audible
        self.visible = visible


class Model346ControlLoopZoneSettings:
    """Control loop configuration for a particular heater output and zone."""

    def __init__(self, upper_bound, proportional, integral, derivative, manual_out_value, output_limit, heater_range,
                 channel, rate):
        """Constructor.

            Args:
                upper_bound (float):
                    Specifies the upper boundary of the zone in temperature units.
                proportional (float):
                    Specifies the proportional gain value (0.1 to 100,000).
                integral (float):
                    Specifies the integral gain value (0.1 to 100,000).
                derivative (float):
                    Specifies the derivative gain value (0 to 20,000).
                manual_out_value (float):
                    Specifies the manual output percentage (0 to 100).
                output_limit (float):
                    Specifies the output limit percentage (0 to 100).
                heater_range (Model346Enums.HeaterRange):
                    Specifies the heater range for this zone (0 = Off, 1 = Low, 2 = High).
                channel (str):
                    Specifies input to use for control (A, B, C1-C4, D1-D4, E1-E4, F1-F4, G1-G4, H1-H4).
                rate (float):
                    Specifies the ramp rate in K/min (0.1 to 100, 0 disables ramping).

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


class Model346OutputModeSettings:
    """Class used to configure output mode settings in conjunction with the set/get_output_mode() methods."""

    def __init__(self, mode, input_channel, powerup_enable, warmup):
        """Constructor for OutputModeSettings class.

            Args:
                mode (Model346Enums.OutputMode):
                    Specifies the control mode (Off, Closed Loop PID, Zone, Open Loop, Monitor Out).
                input_channel (str):
                    Specifies input to use for control (A, B, C1-C4, D1-D4, E1-E4, F1-F4, G1-G4, H1-H4, NONE).
                    Unused if not in PID mode.
                powerup_enable (bool):
                    Specifies whether the output restarts (True) or remains off (False) after power cycle.
                warmup (bool):
                    Specifies if the output will be used for warmup (True) or not (False).

        """
        self.mode = mode
        self.input_channel = input_channel
        self.powerup_enable = powerup_enable
        self.warmup = warmup


class Model346RelayControlSettings:
    """Class used to configure relay control settings."""

    def __init__(self, mode, instance, condition):
        """Constructor for RelayControlSettings class.

            Args:
                mode (Model346Enums.RelayControlMode):
                    Specifies the relay control feature/mode.
                instance (str | int):
                    Input instance for the specified mode. Type depends on mode:
                    - For THERMOMETRY_INPUT: input channel (A, B, C1-C4, D1-D4, E1-E4, F1-F4, G1-G4, H1-H4, NONE)
                    - For OUTPUT_STATUS: numeric output (1-10)
                    - For FUNCTION_OUTPUT: function ID (1-16)
                    - For DIGITAL_INPUT: digital input number (1-2)
                    - For SYSTEM_STATUS: 0 (warmup all)
                    - For OFF and ON: ignored (use 0)
                condition (int | IntEnum):
                    Condition to evaluate. Type depends on mode:
                    - For THERMOMETRY_INPUT: RelayThermometryCondition enum
                    - For OUTPUT_STATUS: RelayOutputStatusCondition enum
                    - For DIGITAL_INPUT: RelayDigitalInputCondition enum
                    - For FUNCTION_OUTPUT: RelayFunctionOutputCondition enum
                    - For OFF, ON, and SYSTEM_STATUS: ignored (use 0)

        """
        self.mode = mode
        self.instance = instance
        self.condition = condition


class Model346InputReadingStatus(RegisterBase):
    """Class object representing the input status flag bits.
    
        Represents the RDGST? input reading status query result.
        
        Per status_reference.rst, bit mapping is::
        
            Bit 0 (weight 1):   Hardware settling
            Bit 1:              (not used)
            Bit 2 (weight 4):   Temperature extrapolated
            Bit 3 (weight 8):   Current source in compliance
            Bit 4 (weight 16):  Temperature underrange
            Bit 5 (weight 32):  Temperature overrange
            Bit 6 (weight 64):  Sensor units reading under range
            Bit 7 (weight 128): Sensor units reading over range

    """

    bit_names = [
        "hardware_settling",                  # Bit 0
        "",                                   # Bit 1 (not used per manual)
        "temperature_extrapolated",           # Bit 2
        "current_source_in_compliance",       # Bit 3
        "temperature_underrange",             # Bit 4
        "temperature_overrange",              # Bit 5
        "sensor_units_readings_under_range",  # Bit 6
        "sensor_units_readings_over_range"    # Bit 7
    ]

    def __init__(self, hardware_settling, temperature_extrapolated, current_source_in_compliance,
                 temperature_underrange, temperature_overrange,
                 sensor_units_readings_under_range, sensor_units_readings_over_range):
        self.hardware_settling = hardware_settling
        self.temperature_extrapolated = temperature_extrapolated
        self.current_source_in_compliance = current_source_in_compliance
        self.temperature_underrange = temperature_underrange
        self.temperature_overrange = temperature_overrange
        self.sensor_units_readings_under_range = sensor_units_readings_under_range
        self.sensor_units_readings_over_range = sensor_units_readings_over_range


class Model346InputReadingOperationStatus(RegisterBase):
    """Class object representing the input reading operation status flag bits.
    
        Represents the RDGOPR? input reading operation status query result.
        
            Bit 0 (weight 1):    Curve applied to input
            Bit 1 (weight 2):    Input reading and settings in Celsius
            Bits 2-5:            (not used)
            Bit 6 (weight 64):   Input low alarm active
            Bit 7 (weight 128):  Input high alarm active
            Bit 8 (weight 256):  Threshold 1 active
            Bit 9 (weight 512):  Threshold 2 active
            Bit 10 (weight 1024): Threshold 3 active
            Bit 11 (weight 2048): Threshold 4 active

    """

    bit_names = [
        "curve_applied",
        "reading_in_celsius",
        "",
        "",
        "",
        "",
        "low_alarm_active",
        "high_alarm_active",
        "threshold_1_active",
        "threshold_2_active",
        "threshold_3_active",
        "threshold_4_active"
    ]

    def __init__(self, curve_applied, reading_in_celsius, low_alarm_active, high_alarm_active,
                 threshold_1_active=False, threshold_2_active=False,
                 threshold_3_active=False, threshold_4_active=False):
        self.curve_applied = curve_applied
        self.reading_in_celsius = reading_in_celsius
        self.low_alarm_active = low_alarm_active
        self.high_alarm_active = high_alarm_active
        self.threshold_1_active = threshold_1_active
        self.threshold_2_active = threshold_2_active
        self.threshold_3_active = threshold_3_active
        self.threshold_4_active = threshold_4_active


class Model346OutputOperationStatus(RegisterBase):
    """Class object representing the output operation status flag bits.
    
        Represents the OUTOPR? output operation query result.
        
        Per status_reference.rst, bit mapping is::
        
            Bit 0:              (not used)
            Bit 1 (weight 2):   RAMPST? is non-zero (ramp active)
            Bits 2-3:           (not used)
            Bit 4 (weight 16):  Output is stabilizing
            Bit 5 (weight 32):  Output is stable
            Bit 6 (weight 64):  Output is in warmup mode (heaters only)
            Bit 7 (weight 128): Output is warm (heaters only)

    """

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

class Model346OutputStatus(RegisterBase):
    """Class object representing the output status flag bits.
    
        Represents the OUTST? output status query result.
        
        Per status_reference.rst, bit mapping is::
        
            Bit 0 (weight 1): HTRST? is non-zero (heater error)
            Bit 1 (weight 2): Output is percentage limited
            Bit 2 (weight 4): Output current source is zeroed to prevent
                              transience while changing ranges

    """

    bit_names = [
        "heater_error",
        "percentage_limited",
        "current_source_zeroed"
    ]

    def __init__(self, heater_error, percentage_limited, current_source_zeroed):
        self.heater_error = heater_error
        self.percentage_limited = percentage_limited
        self.current_source_zeroed = current_source_zeroed

class Model346FilterSettings:
    """Class used to configure input filter settings in conjunction with the set/get_filter() methods."""

    def __init__(self, filter_enable, data_points, reset_threshold):
        """Constructor for Model346FilterSettings class.

            Args:
                filter_enable (bool):
                    Enables or disables the filter.
                    False = Disabled, True = Enabled
                data_points (int):
                    Specifies the number of points (2 to 64) used in the filter.
                    The filter is a running average that smooths input readings exponentially.
                reset_threshold (int):
                    Specifies what percent of full scale reading (1 to 10%) limits the filtering function.
                    Reading changes greater than this percentage reset the filter.

        """
        self.filter_enable = filter_enable
        self.data_points = data_points
        self.reset_threshold = reset_threshold


class Model346ThresholdSettings:
    """Class used to configure input threshold settings in conjunction with the set/get_threshold() methods."""

    def __init__(self, value, comparison):
        """Constructor for Model346ThresholdSettings.

            Args:
                value (float):
                    Threshold value.
                comparison (Model346Enums.ThresholdComparison):
                    Comparison operator.
        """

        self.value = value
        self.comparison = comparison


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

        # Configure status register classes for the Model 346
        self.status_byte_register = StatusByteRegister
        self.standard_event_register = StandardEventRegister
        self.operation_register = Model346OperationRegister
        self.questionable_register = Model346QuestionableRegister

    def set_filter(self, input_channel, filter_settings):
        """Configures the input filter for the specified channel.

            The reading filter applies exponential smoothing to the sensor input readings.
            If the filter is turned on for a sensor input, all reading values for that input
            are filtered. The filter is a running average, so it does not change the update rate
            of an input. The filtered reading is used for everything except closed loop control
            loop calculations, which use the unfiltered reading.

            Args:
                input_channel (str):
                    Specifies input to configure: A, B, C1, C2, C3, C4, D1, D2, D3, D4,
                    E1, E2, E3, E4, F1, F2, F3, F4, G1, G2, G3, G4, H1, H2, H3, H4
                filter_settings (Model346FilterSettings):
                    The filter configuration to apply to the input.

        """
        self.command(f"FILTER {input_channel},{int(filter_settings.filter_enable)},"
                     f"{filter_settings.data_points},{filter_settings.reset_threshold}")

    def get_filter(self, input_channel):
        """Returns the input filter configuration for the specified channel.

            Args:
                input_channel (str):
                    Specifies input to query: A, B, C1, C2, C3, C4, D1, D2, D3, D4,
                    E1, E2, E3, E4, F1, F2, F3, F4, G1, G2, G3, G4, H1, H2, H3, H4

            Returns:
                Model346FilterSettings:
                    An Model346FilterSettings object populated with the filter parameters.

        """
        filter_response = self.query(f"FILTER? {input_channel}").split(",")
        return Model346FilterSettings(
            filter_enable=bool(int(filter_response[0])),
            data_points=int(filter_response[1]),
            reset_threshold=int(filter_response[2])
        )

    def get_option_card_slot(self):
        """
        Returns the available option card slots.
        """
        return self.option_card_slots

    def get_digital_input_status(self):
        """Returns the status of the digital inputs.

            Returns:
                dict[str, int]:
                    {"input_one": int, "input_two": int}

        """
        input_status = self.query("DIGIN?").split(",")
        return {"input_one": int(input_status[0]), "input_two": int(input_status[1])}

    def set_threshold(self, input_channel, threshold_id, threshold_settings):
        """Configures a reading threshold for the specified input.

            The threshold feature allows monitoring of up to four independent thresholds per input.

            Args:
                input_channel (str):
                    Specifies input to configure: A, B, C1-C4, D1-D4, E1-E4, F1-F4, G1-G4, H1-H4.
                threshold_id (int):
                    Threshold identifier (1 to 4).
                threshold_settings (Model346ThresholdSettings):
                    Threshold configuration to apply.

        """
        self.command(
            f"THRESHOLD {input_channel},{threshold_id},{float(threshold_settings.value)},"
            f"{int(threshold_settings.comparison)}"
        )

    def get_threshold(self, input_channel, threshold_id):
        """Returns the reading threshold configuration for the specified input and threshold ID.

            Args:
                input_channel (str):
                    Specifies input to query: A, B, C1-C4, D1-D4, E1-E4, F1-F4, G1-G4, H1-H4.
                threshold_id (int):
                    Threshold identifier (1 to 4).

            Returns:
                Model346ThresholdSettings:
                    An object populated with the threshold value and comparison operator.
        """
        response = self.query(f"THRESHOLD? {input_channel},{threshold_id}").split(",")
        return Model346ThresholdSettings(
            value=float(response[0]),
            comparison=self.ThresholdComparison(int(response[1]))
        )

    def set_alarm_settings(self, input_channel, alarm_settings):
        """Sets the configuration of a particular alarm.

            Args:
                input_channel (str):
                    Specifies the input channel to configure (e.g., A, B, C1, C2, etc.).
                alarm_settings (Model346AlarmSettings):
                    The configuration that should be applied to the alarm.

        """
        command_string = (
            f"ALARM {input_channel},{int(alarm_settings.enabled)},"
            f"{alarm_settings.high_value},{alarm_settings.low_value},"
            f"{alarm_settings.deadband},{int(alarm_settings.latch)},"
            f"{int(alarm_settings.audible)},{int(alarm_settings.visible)}"
        )
        self.command(command_string)

    def get_alarm_settings(self, input_channel):
        """Returns present configuration of a particular alarm.

            Args:
                input_channel (str):
                    Specifies the input channel to query (e.g., A, B, C1, C2, etc.).

            Returns:
                Model346AlarmSettings:
                    An Model346AlarmSettings object populated with the respective alarm parameters.

        """
        alarm_params = self.query(f"ALARM? {input_channel}").split(",")
        return Model346AlarmSettings(
            enabled=bool(int(alarm_params[0])),
            high_limit=float(alarm_params[1]),
            low_limit=float(alarm_params[2]),
            deadband=float(alarm_params[3]),
            latch=bool(int(alarm_params[4])),
            audible=bool(int(alarm_params[5])),
            visible=bool(int(alarm_params[6]))
        )

    def set_stability_settings(self, output_channel, stability_settings):
        """Sets the stability detection configuration for a particular output.

            Args:
                output_channel (int):
                    Specifies the output channel to configure (1 to 10).
                stability_settings (Model346StabilitySettings):
                    The configuration that should be applied to the output.

        """
        command_string = (
            f"OUTSTABLE {output_channel},{int(stability_settings.enabled)},"
            f"{stability_settings.setpoint_error},"
            f"{stability_settings.settle_time},"
            f"{int(stability_settings.audible)},{int(stability_settings.visible)}"
        )
        self.command(command_string)

    def get_stability_settings(self, output_channel):
        """Returns present configuration of a particular stability setting.

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
            setpoint_error=float(stability_params[1]),
            settle_time=float(stability_params[2]),
            audible=bool(int(stability_params[3])),
            visible=bool(int(stability_params[4]))
        )

    def turn_relay_on(self, relay_number):
        """Turns the specified relay on.

            Args:
                relay_number (int):
                    The relay to turn on.
                    Options are:
                    1 or 2.

        """
        self.command(f"RELAY {relay_number},1,0,0")

    def turn_relay_off(self, relay_number):
        """Turns the specified relay off.

            Args:
                relay_number (int):
                    The relay to turn off.
                    Options are:
                    1 or 2.

        """
        self.command(f"RELAY {relay_number},0,0,0")

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
        """Returns the sensor type and associated parameters.

            Args:
                input_channel (str):
                    Specifies input to query (A - H4).

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
                    Specifies which output to configure (1 to 4, 9, or 10).
                heater_range (Model346Enums.HeaterRange):
                    The heater range to apply to a particular output.

        """
        self.command(f"RANGE {output},{heater_range}")

    def get_heater_range(self, output):
        """Returns the heater range for a particular output.

            Args:
                output (int):
                    Specifies which output to query (1 to 4, 9, or 10).

            Returns:
                (Model346Enums.HeaterRange):
                    The heater range being applied to a particular output.

        """
        heater_range = int(self.query(f"RANGE? {output}"))
        return Model346Enums.HeaterRange(heater_range)

    def set_heater_autorange(self, output, enabled):
        """Sets the heater autorange setting for a particular output.

            Args:
                output (int):
                    Specifies which output to configure (1 - 4).
                enabled (int):
                    Whether autorange should be enabled or disabled.

        """
        self.command(f"HTRAUTO {output},{enabled}")

    def get_heater_autorange(self, output):
        """Returns the heater autorange setting for a particular output.

            Args:
                output (int):
                    Specifies which output to query (1 - 4).

            Returns:
                (Model346Enums.HeaterAutorange):
                    Whether autorange is enabled or disabled.

        """
        heater_range = int(self.query(f"HTRAUTO? {output}"))
        return Model346Enums.HeaterAutorange(heater_range)

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
        return Model346.HeaterRangeAnalogOutput(analog_out_range)

    def set_output_percent_limit(self, output, percent_limit):
        """Sets the output percent limit for a particular output.

            Args:
                output (int):
                    Specifies which output to configure (1 - 10).
                percent_limit (float):
                    Sets a percentage limit for a particular output (0 to 100).

        """
        self.command(f"OUTLIMIT {output},{percent_limit}")

    def get_output_percent_limit(self, output):
        """Returns the output percent limit for a particular output.

            Args:
                output (int):
                    Specifies which output to query (1 - 10).

            Returns:
                float:
                    The set percentage limit for a particular output.

        """
        output_limit = float(self.query(f"OUTLIMIT? {output}"))
        return output_limit

    def all_heaters_off(self):
        """Recreates the front panel safety feature of shutting off all heaters."""
        self.command(
            "RANGE 1,0;RANGE 2,0;RANGE 3,0;RANGE 4,0;RANGE 5,0;RANGE 6,0;RANGE 7,0;RANGE 8,0;RANGE 9,0;RANGE 10,0;")

    def set_heater_setup(self, output, heater_resistance, max_output, output_units):
        """Method to configure the heaters.

            Args:
                output (int):
                    Specifies which heater output to configure (1 to 4, 9 or 10)
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
                    Specifies which heater output to query (1 to 4, 9 or 10).

            Returns:
                dict[str, float | Model346Enums.HeaterOutputUnits]:
                    {"heater_resistance": float, "max_output": float, "output_units": HeaterOutputUnits}

        """
        heater_setup = self.query(f"HTRSET? {output}").split(",")
        return {
            "heater_resistance": (int(heater_setup[0])),
            "max_output": float(heater_setup[1]),
            "output_units": self.HeaterOutputUnits(int(heater_setup[2]))
        }

    def get_heater_output_measurements(self, output):
        """Returns the heater output measurements.

            Args:
                output (int):
                    Specifies which heater output to query (1 - 8).

            Returns:
                dict[str, float]:
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
                    For outputs 5-8: output_value is voltage in Volts, output_power is not calculated and will return as 0
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
                    Specifies which output to configure (1 - 10).
                mode (Model346Enums.OutputMode):
                    Specifies the control mode.
                input_channel (str):
                    Specifies which input to use for control (A - H4, NONE). 
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
                    Specifies which output to retrieve (1 - 10).

            Returns:
                Model346OutputModeSettings:
                    A Model346OutputModeSettings object populated with the output mode parameters.

        """
        response = self.query(f"OUTMODE? {output}").split(",")
        return Model346OutputModeSettings(
            mode=self.OutputMode(int(response[0])),
            input_channel=response[1],
            powerup_enable=bool(int(response[2])),
            warmup=bool(int(response[3]))
        )

    def set_output_group(self, output, group):
        """Assigns a heater output to a virtual heater group for coordinated control.

            Args:
                output (int):
                    Specifies which heater output to configure (1 - 4).
                group (int):
                    The virtual heater group to assign the output to: 9 or 10.
                    Set to 0 to remove the output from a group.

        """
        self.command(f"OUTGROUP {output},{group}")

    def get_output_group(self, output):
        """Returns the virtual heater group assignment for a particular output.

            Args:
                output (int):
                    Specifies which heater output to query (1 - 4).

            Returns:
                int:
                    The virtual heater group (9 or 10), or 0 if not assigned to a group.

        """
        return int(self.query(f"OUTGROUP? {output}"))

    def start_warmup(self, room_temperature=293.15, percent_out=10):
        """Starts the warmup process for all heaters configured with
        warmup set to True in OUTMODE.

        Args:
            room_temperature (float):
                Target temperature in Kelvin (275 to 325). Defaults to 293.15 K.
            percent_out (float):
                The acceptable output percentage for the system to be considered
                WARM (0 to 100). Defaults to 10.
        """
        self.command(f"WARM {room_temperature}, {percent_out}")

    def set_analog_output_settings(self, output, high_value, low_value):
        """Configures a voltage-controlled output.

            Use the set_output_mode command to set the output mode to Monitor Out.

            Args:
                output (int):
                    Analog output channel to configure (5 - 8).
                high_value (float):
                    Represents the input reading at which the Monitor Out reaches
                    +100% output (+10 V).
                low_value (float):
                    Represents the input reading at which the analog output reaches
                    0% output (0 V).

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

    def reset_alarm_status(self):
        """Resets all alarm statuses including latched alarms."""
        self.command("ALMRST")

    def set_keypad_lock(self, state):
        """Sets the state of the front panel settings lock.

            Args:
                state (bool): The desired state of the settings lock (True for locked, False for unlocked).

        """
        command_string = f"SYSTem:KLOCk {int(state)}"
        self.command(command_string)

    def get_keypad_lock(self):
        """Returns the current state of the front panel settings lock.

            Returns:
                bool: True if settings are locked, False if unlocked.

        """
        response = self.query("SYSTem:KLOCk?")
        return bool(int(response.strip()))

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
                (Model346InputReadingStatus):
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

    def get_output_status(self, output):
        """Returns the status of the specified output.

            Args:
                output (int):
                    Specifies the output to query (1 - 10).

            Returns:
                (Model346OutputStatus):
                    Boolean representation of each bit of the output status flag register.
                    Includes:
                    - heater_error: HTRST? is non-zero
                    - percentage_limited: Output is percentage limited
                    - current_source_zeroed: Output current source is zeroed to prevent transience while changing ranges

        """
        response = int(self.query(f"OUTST? {output}"))
        return Model346OutputStatus.from_integer(response)

    def get_thermocouple_junction_temp(self, input_channel):
        """Returns the thermocouple junction temperature for the specified input channel.

            Args:
                input_channel (str):
                    Specifies the thermocouple input to query (E1, E2, F1, F2, G1, G2, H1, H2).

            Returns:
                float:
                    The thermocouple junction temperature in Kelvin.

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
                    Specifies which output to reset (1 - 10).

        """
        self.command(f"SETPRST {output}")

    def get_ramp_setpoint(self, output):
        """Returns the current setpoint for a particular output.

            Args:
                output (int):
                    Specifies which output to query (1 - 10).

            Returns:
                float:
                    The current control setpoint for the specified output.

        """
        return float(self.query(f"RAMPSETP? {output}"))

    def set_control_loop_zone_table(self, output, zone_number, zone_settings):
        """Sets the control loop zone table for a particular output.

            Args:
                output (int):
                    Specifies which output to configure (1 to 4, 9, or 10).
                zone_number (int):
                    Specifies which zone to configure (1 - 10).
                zone_settings (Model346ControlLoopZoneSettings):
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
                    Specifies which output to query (1 to 4, 9, or 10).
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

    def set_relay_alarms(self, relay_number, mode, input_channel, condition):
        """Sets a relay to turn on and off automatically based on the state of the alarm of the specified input channel.

            Args:
                relay_number (int):
                    The relay to configure (1 or 2).
                mode (Model346Enums.RelayControlMode):
                    Specifies the relay control feature/mode.
                input_channel (str | int):
                    Input instance for the specified mode. Type depends on mode:
                    - For THERMOMETRY_INPUT: input channel (A, B, C1-C4, D1-D4, E1-E4, F1-F4, G1-G4, H1-H4, NONE)
                    - For OUTPUT_STATUS: numeric output (1-10)
                    - For FUNCTION_OUTPUT: function ID (1-16)
                    - For DIGITAL_INPUT: digital input number (1-2)
                    - For SYSTEM_STATUS: 0 (warmup all)
                    - For OFF and ON: ignored (use 0)
                condition (int | IntEnum):
                    Condition to evaluate. Type depends on mode:
                    - For THERMOMETRY_INPUT: RelayThermometryCondition enum or int (0-10)
                    - For OUTPUT_STATUS: RelayOutputStatusCondition enum or int (0-4)
                    - For DIGITAL_INPUT: RelayDigitalInputCondition enum or int (0-1)
                    - For FUNCTION_OUTPUT: RelayFunctionOutputCondition enum or int (0-1)
                    - For OFF, ON, and SYSTEM_STATUS: ignored (use 0)

        """
        self.command(f"RELAY {relay_number},{mode},{input_channel},{condition}")

    def get_relay_alarm_control_parameters(self, relay_number):
        """Returns the relay control parameters for a specified relay.

            Args:
                relay_number (int):
                    The relay to query (1 or 2).

            Returns:
                Model346RelayControlSettings:
                    A Model346RelayControlSettings object populated with relay control parameters.

        """
        response = self.query(f"RELAY? {relay_number}").split(",")
        mode = self.RelayControlMode(int(response[0]))

        # Parse condition based on mode
        condition_value = int(response[2])
        if mode == self.RelayControlMode.THERMOMETRY_INPUT:
            condition = self.RelayThermometryCondition(condition_value)
        elif mode == self.RelayControlMode.OUTPUT_STATUS:
            condition = self.RelayOutputStatusCondition(condition_value)
        elif mode == self.RelayControlMode.DIGITAL_INPUT:
            condition = self.RelayDigitalInputCondition(condition_value)
        elif mode == self.RelayControlMode.FUNCTION_OUTPUT:
            condition = self.RelayFunctionOutputCondition(condition_value)
        else:
            condition = condition_value  # For OFF, ON, and SYSTEM_STATUS modes

        return Model346RelayControlSettings(
            mode=mode,
            instance=response[1],
            condition=condition
        )

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
            Model346Enums.OptionCardType: The type of option card connected to the slot.

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
        """Returns the list of channels available on the specified option card slot.

        Args:
            slot (str): Specifies the slot to query (E, F, G, H).

        Returns:
            list[str]: The list of channels available on the option card in the specified slot.

        Raises:
            ValueError: If the option card type is unsupported.
        """

        if slot not in self.option_card_slots:
            warnings.warn(
                f"Invalid slot: {slot}. Valid slots are {', '.join(self.option_card_slots)}.",
                UserWarning,
                stacklevel=2,
            )
            return []

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
           'Model346OutputOperationStatus', 'Model346OutputStatus', 'Model346ControlLoopZoneSettings',
           'Model346OutputModeSettings', 'Model346StabilitySettings', 'Model346FilterSettings',
           'Model346ThresholdSettings']
