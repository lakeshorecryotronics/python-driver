"""Implements functionality unique to the Lake Shore Model 346."""

from lakeshore.temperature_controllers import TemperatureController
from lakeshore.xip_instrument import XIPInstrument
from lakeshore.model_346_enums import Model346Enums


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
