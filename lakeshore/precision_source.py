"""Implements functionality unique to the Lake Shore 155 Precision Source"""

from time import sleep
import itertools

from .xip_instrument import XIPInstrument, RegisterBase, StatusByteRegister, StandardEventRegister


class PrecisionSourceOperationRegister(RegisterBase):
    """Class object representing the operation status register"""

    bit_names = [
        "",
        "",
        "",
        "",
        "",
        "waiting_for_trigger_event",
        "waiting_for_arm_event",
        "",
        "",
        "",
        "trigger_model_is_idle",
        "",
        "interlock_is_open"
    ]

    def __init__(self,
                 waiting_for_trigger_event,
                 waiting_for_arm_event,
                 trigger_model_is_idle,
                 interlock_is_open):
        self.waiting_for_trigger_event = waiting_for_trigger_event
        self.waiting_for_arm_event = waiting_for_arm_event
        self.trigger_model_is_idle = trigger_model_is_idle
        self.interlock_is_open = interlock_is_open


class PrecisionSourceQuestionableRegister(RegisterBase):
    """Class object representing the questionable status register"""

    bit_names = [
        "voltage_source_in_current_limit",
        "current_source_in_voltage_compliance",
        "",
        "",
        "",
        "",
        "",
        "",
        "calibration_error",
        "inter_processor_communication_error"
    ]

    def __init__(self,
                 voltage_source_in_current_limit,
                 current_source_in_voltage_compliance,
                 calibration_error,
                 inter_processor_communication_error):
        self.voltage_source_in_current_limit = voltage_source_in_current_limit
        self.current_source_in_voltage_compliance = current_source_in_voltage_compliance
        self.calibration_error = calibration_error
        self.inter_processor_communication_error = inter_processor_communication_error


class PrecisionSource(XIPInstrument):
    """A class object representing a Lake Shore 155 precision I/V source"""

    vid_pid = [(0x1FB9, 0x0103)]

    def __init__(self, serial_number=None,
                 com_port=None, baud_rate=115200, flow_control=False,
                 timeout=2.0,
                 ip_address=None):
        # Call the parent init, then fill in values specific to the 155
        XIPInstrument.__init__(self, serial_number, com_port, baud_rate, flow_control, timeout, ip_address)
        self.status_byte_register = StatusByteRegister
        self.standard_event_register = StandardEventRegister
        self.operation_register = PrecisionSourceOperationRegister
        self.questionable_register = PrecisionSourceQuestionableRegister

    def sweep_voltage(self,
                      dwell_time,
                      offset_values=None,
                      amplitude_values=None,
                      frequency_values=None):
        """Sweep source output voltage parameters based on list arguments"""

        # Change the output mode to source voltage instead of current.
        self.command("SOURCE:FUNCTION:MODE VOLTAGE")

        # Configure the instrument to automatically choose the best range for a given output setting
        self.command("SOURCE:FUNCTION:SHAPE SIN")

        # Turn on the output voltage
        self.command("OUTPUT ON")

        # Check to see if arguments were passed for each parameter.
        # If not, initialize them in a way they will be ignored.
        if offset_values is None:
            offset_values = [None]

        if amplitude_values is None:
            amplitude_values = [None]

        if frequency_values is None:
            frequency_values = [None]

        # Step through every combination of the three values.
        for offset, frequency, amplitude in itertools.product(offset_values, frequency_values, amplitude_values):

            parameter_commands = []

            if offset is not None:
                parameter_commands.append("SOURCE:VOLTAGE:OFFSET " + str(offset))
            if frequency is not None:
                parameter_commands.append("SOURCE:FREQUENCY " + str(frequency))
            if amplitude is not None:
                parameter_commands.append("SOURCE:VOLTAGE:AMPLITUDE " + str(amplitude))

            self.command(*parameter_commands)

            sleep(dwell_time)

    def sweep_current(self,
                      dwell_time,
                      offset_values=None,
                      amplitude_values=None,
                      frequency_values=None):
        """Sweep the source output current parameters based on list arguments"""

        # Change the output mode to source current instead of voltage
        self.command("SOURCE:FUNCTION:MODE CURRENT")

        # Configure the instrument to automatically choose the best range for a given output setting
        self.command("SOURCE:FUNCTION:SHAPE SIN")

        # Turn on the output voltage
        self.command("OUTPUT ON")

        # Check to see if arguments were passed for each parameter.
        # If not, initialize them in a way they will be ignored.
        if offset_values is None:
            offset_values = [None]

        if amplitude_values is None:
            amplitude_values = [None]

        if frequency_values is None:
            frequency_values = [None]

        # Step through every combination of the three values.
        for offset, frequency, amplitude in itertools.product(offset_values, frequency_values, amplitude_values):

            parameter_commands = []

            if offset is not None:
                parameter_commands.append("SOURCE:CURRENT:OFFSET " + str(offset))
            if frequency is not None:
                parameter_commands.append("SOURCE:FREQUENCY " + str(frequency))
            if amplitude is not None:
                parameter_commands.append("SOURCE:CURRENT:AMPLITUDE " + str(amplitude))

            self.command(*parameter_commands)

            sleep(dwell_time)
