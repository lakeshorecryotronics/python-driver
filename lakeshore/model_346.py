"""Implements functionality unique to the Lake Shore Model 346."""

from lakeshore.temperature_controllers import TemperatureController, CurveHeader
from lakeshore.xip_instrument import XIPInstrument, StandardEventRegister, StatusByteRegister, RegisterBase
from lakeshore.model_346_enums import Model346Enums
from enum import IntEnum

Model346CurveHeader = CurveHeader
Model346StandardEventRegister = StandardEventRegister
Model346StatusByteRegister = StatusByteRegister


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

    def __init__(self, sensor_type, autorange_enable, compensation, units, vi_swapped, input_range=None):
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
                vi_swapped (bool):
                    Specifies whether readings have swapped vi leads. (False = off, True = on).
                input_range (IntEnum):
                    Specifies input range if autorange_enable is False.
                    See IntEnum classes: Model346Enums.DiodeRange, Model346Enums.PTCRTDRange,
                    and Model346Enums.NTCRTDRange.

        """

        self.sensor_type = sensor_type
        self.autorange_enable = autorange_enable
        self.compensation = compensation
        self.units = units
        self.vi_swapped = vi_swapped
        self.input_range = input_range


class Model346AlarmSettings:
    """Class used to configure an alarm in conjunction with the set/get_alarm_settings() method for the Model346."""

    def __init__(self, alarm_type, output, input_channel, low_value, high_value):
        """Constructor for AlarmSettings class.

            Args:
                alarm_type (Model346Enums.AlarmType):
                    Specifies the type of alarm to activate when an alarm condition occurs.
                output (int):
                    Specifies which output to activate when an alarm condition occurs (dependent on alarm_type).
                input_channel (str):
                    Specifies the input to monitor (A - H4).
                low_value (float):
                    Sets the value the source is checked against to activate low alarm.
                high_value (float):
                    Sets the value the source is checked against to activate the high alarm.
        """
        self.alarm_type = alarm_type
        self.output = output
        self.input_channel = input_channel
        self.low_value = low_value
        self.high_value = high_value


class Model346(Model346Enums, XIPInstrument, TemperatureController):
    """
    Class for interaction with the Lake Shore Model 346 cryogenic temperature controller.
    """

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

    def get_digit_input_status(self):
        """Returns the status of the digital inputs.

            Returns:
                dict[str, int]:
                    {"input_one": int, "input_two": int}

        """
        input_status = self.query("DIGIN?").split(",")
        return {"input_one": int(input_status[0]), "input_two": int(input_status[1])}

    def set_alarm_settings(self, alarm_id, alarm_settings):
        """Sets the configuration of a particular alarm.

            Args:
                alarm_id (int):
                    Specifies the alarm of interest.
                alarm_settings (Model346AlarmSettings):
                    The configuration that should be applied to the alarm.

        """
        self.command(f"ALARM {alarm_id},{alarm_settings.input_channel},{alarm_settings.low_value}"
                     f",{alarm_settings.high_value},{alarm_settings.alarm_type},{alarm_settings.output}")

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
        return Model346AlarmSettings(self.AlarmType(int(alarm_params[3])),
                                     int(alarm_params[4]),
                                     alarm_params[0],
                                     float(alarm_params[1]),
                                     float(alarm_params[2]))

    def turn_alarm_off(self, alarm_id):
        """Sets the output type of a particular alarm to NONE (off).

                Args:
                    alarm_id (int):
                        Specifies the alarm of interest.

        """
        self.command(f"ALARM {alarm_id},,,,{self.AlarmType.NONE},")

    def turn_relay_on(self, relay_number):
        """Turns the specified relay on.

            Args:
                relay_number (int):
                    The relay to turn on.
                    Options are:
                    1 or 2.

        """
        self.command(f"RELAY {relay_number},1")

    def turn_relay_off(self, relay_number):
        """Turns the specified relay off.

            Args:
                relay_number (int):
                    The relay to turn off.
                    Options are:
                    1 or 2.

        """
        self.command(f"RELAY {relay_number},0")

    def get_relay_status(self, relay_channel):
        """Returns whether the relay at the specified channel is on or off.

            Args:
                relay_channel (int):
                    The relay channel to query.

            Returns:
                bool:
                    True if relay is on, False if relay is off.

        """
        return bool(int(self.query(f"RELAY? {relay_channel}")))

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
                     f"{input_range},{int(sensor_params.compensation)},{sensor_params.units},"
                     f"{int(sensor_params.vi_swapped)}")

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

        return Model346InputSensorSettings(sensor_type,
                                           bool(int(sensor_params[1])),
                                           bool(int(sensor_params[3])),
                                           self.InputSensorUnits(int(sensor_params[4])),
                                           bool(int(sensor_params[5])),
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

    def all_heaters_off(self):
        """Recreates the front panel safety feature of shutting off all heaters."""
        self.command("RANGE 1,0;RANGE 2,0;RANGE 3,0;RANGE 4,0")

    def set_heater_setup(self, output, heater_resistance, max_current, output_units):
        """Method to configure the heaters.

            Args:
                output (int):
                    Specifies which heater output to configure (1 - 4).
                heater_resistance (float):
                    10 to 100 ohms.
                max_current (float):
                    User defined maximum output current.
                    If HeaterRange.LOW (0.0 - 0.2).
                    If HeaterRange.HIGH (0.0 - 2.0).
                output_units (Model346Enums.HeaterOutputUnits):
                    Specifies whether the heater output displays in power or current.

        """
        self.command(f"HTRSET {output},{heater_resistance},{max_current},{output_units}")

    def get_heater_setup(self, output):
        """Returns the heater configuration status.

            Args:
                output (int):
                    Specifies which heater output to configure (1 - 4)

            Returns:
                dict[str, float | Model346Enums.HeaterOutputUnits]:
                    {"heater_resistance": float, "max_current": float, "output_units": HeaterOutputUnits}

        """
        heater_setup = self.query(f"HTRSET? {output}").split(",")
        return {
            "heater_resistance": float(heater_setup[0]), 
            "max_current": float(heater_setup[1]), 
            "output_units": self.HeaterOutputUnits(int(heater_setup[2]))
        }

    def set_output_mode(self, output, mode, input_channel, powerup_enable=False):
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

        """
        command_string = f"OUTMODE {output},{mode},{input_channel},{int(powerup_enable)}"
        self.command(command_string)

    def get_output_mode(self, output):
        """Returns the output mode for a particular output.

            Args:
                output (int):
                    Specifies which output to retrieve (1 - 8).

            Returns:
                dict[str, Model346Enums.OutputMode | str | bool]:
                    {"mode": OutputMode, "input_channel": str, "powerup_enable": bool}

        """
        outmode = self.query(f"OUTMODE? {output}").split(",")
        return {
            "mode": self.OutputMode(int(outmode[0])),
            "input_channel": outmode[1],
            "powerup_enable": bool(int(outmode[2]))
        }

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


__all__ = ['Model346AlarmSettings', 'Model346InputSensorSettings', 'Model346', 'Model346CurveHeader',
           'Model346OperationRegister', 'Model346QuestionableRegister', 'Model346StandardEventRegister',
           'Model346StatusByteRegister']
