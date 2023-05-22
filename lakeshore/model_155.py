"""Implements functionality unique to the Lake Shore 155 Precision Source."""

from time import sleep
import itertools

from .xip_instrument import XIPInstrument, RegisterBase, StatusByteRegister, StandardEventRegister


class PrecisionSourceOperationRegister(RegisterBase):
    """Class object representing the operation status register."""

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
    """Class object representing the questionable status register."""

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
    """A class object representing a Lake Shore 155 precision I/V source."""

    vid_pid = [(0x1FB9, 0x0103)]

    def __init__(self,
                 serial_number=None,
                 com_port=None,
                 baud_rate=115200,
                 flow_control=False,
                 timeout=2.0,
                 ip_address=None,
                 tcp_port=7777,
                 **kwargs):

        # Call the parent init, then fill in values specific to the 155
        XIPInstrument.__init__(self, serial_number, com_port, baud_rate, flow_control, timeout, ip_address, tcp_port, **kwargs)
        self.status_byte_register = StatusByteRegister
        self.standard_event_register = StandardEventRegister
        self.operation_register = PrecisionSourceOperationRegister
        self.questionable_register = PrecisionSourceQuestionableRegister

    def sweep_voltage(self,
                      dwell_time,
                      offset_values=None,
                      amplitude_values=None,
                      frequency_values=None):
        """Sweep source output voltage parameters based on list arguments.

            Args:
                dwell_time (float):
                    The length of time in seconds to wait at each parameter combination.
                    Note that the update rate will be limited by the SCPI communication response time.
                    The response time is usually on the order of 10-30 milliseconds.
                offset_values (list):
                    DC offset values in volts to sweep over.
                amplitude_values (list):
                    Peak to peak values in volts to sweep over.
                frequency_values (list):
                    Frequency values in Hertz to sweep over.

        """

        # Change the output mode to source voltage instead of current.
        self.command("SOURCE:FUNCTION:MODE VOLTAGE")

        # Configure the instrument to output a sine wave
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
        """Sweep the source output current parameters based on list arguments

            Args:
                dwell_time (float):
                    The length of time in seconds to wait at each parameter combination.
                    Note that the update rate will be limited by the SCPI communication response time.
                    The response time is usually on the order of 10-30 milliseconds.
                offset_values (list):
                    DC offset values in volts to sweep over.
                amplitude_values (list):
                    Peak to peak values in volts to sweep over.
                frequency_values (list):
                    Frequency values in Hertz to sweep over.

        """

        # Change the output mode to source current instead of voltage
        self.command("SOURCE:FUNCTION:MODE CURRENT")

        # Configure the instrument to output a sine wave
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

    def enable_output(self):
        """Turns on the source output."""
        self.command("OUTPUT ON")

    def disable_output(self):
        """Turns off the source output."""
        self.command("OUTPUT OFF")

    def set_output(self, output_on):
        """Configure the source output on or off.

            Args:
                output_on (bool):
                    Turns the source output on when True, off when False.

        """
        if output_on:
            self.enable_output()
        else:
            self.disable_output()

    def route_terminals(self, output_connections_location="REAR"):
        """Configures whether the source output is routed through the front or rear connections.

            Args:
                output_connections_location (str):
                    Valid options are: "REAR" (Output is routed out the rear connections), and
                    "FRONT" (Output is routed out the front connections).

        """
        self.command("ROUTE:TERMINALS " + output_connections_location)

    def output_sine_current(self, amplitude, frequency, offset=0.0, phase=0.0):
        """Configures and enables the source output to be a sine wave current source.

            Args:
                amplitude (float):
                    The peak current amplitude value in amps.
                frequency (float):
                    The source frequency value in hertz.
                offset (float):
                    The DC offset current in amps.
                phase (float):
                    Shifts the phase of the output relative to the reference out. Must be between -180 and 180 degrees.

        """

        # Change the output mode to source current instead of voltage
        self.command("SOURCE:FUNCTION:MODE CURRENT")

        # Configure the instrument to output a sine wave
        self.command("SOURCE:FUNCTION:SHAPE SIN")

        # Configure the output amplitude
        self.command("SOURCE:CURRENT:AMPLITUDE " + str(amplitude))

        # Configure the output frequency
        self.command("SOURCE:FREQUENCY " + str(frequency))

        # Configure the output DC offset
        self.command("SOURCE:CURRENT:OFFSET " + str(offset))

        # Configure the phase of the output
        self.command("SOURCE:PHASE " + str(phase))

        # Turn on the output current
        self.command("OUTPUT ON")

    def output_sine_voltage(self, amplitude, frequency, offset=0.0, phase=0.0):
        """Configures and enables the source output to be a sine wave voltage source.

            Args:
                amplitude (float):
                    The peak voltage amplitude value in volts.
                frequency (float):
                    The source frequency value in hertz.
                offset (float):
                    The DC offset voltage in volts.
                phase (float):
                    Shifts the phase of the output relative to the reference out. Must be between -180 and 180 degrees.

        """

        # Change the output mode to source voltage instead of current
        self.command("SOURCE:FUNCTION:MODE VOLTAGE")

        # Configure the instrument to output a sine wave
        self.command("SOURCE:FUNCTION:SHAPE SIN")

        # Configure the output amplitude
        self.command("SOURCE:VOLTAGE:AMPLITUDE " + str(amplitude))

        # Configure the output frequency
        self.command("SOURCE:FREQUENCY " + str(frequency))

        # Configure the output DC offset
        self.command("SOURCE:VOLTAGE:OFFSET " + str(offset))

        # Configure the phase of the output
        self.command("SOURCE:PHASE " + str(phase))

        # Turn on the output voltage
        self.command("OUTPUT ON")

    def output_dc_current(self, current_level):
        """Configures the source output to be a DC current source.

            Args:
                current_level (float):
                    The output current level in amps.

        """

        # Change the output mode to source current instead of voltage
        self.command("SOURCE:FUNCTION:MODE CURRENT")

        # Configure the instrument to output a sine wave
        self.command("SOURCE:FUNCTION:SHAPE DC")

        # Configure DC current level
        self.command("SOURCE:CURRENT:AMPLITUDE " + str(current_level))

        # Turn on the output current
        self.command("OUTPUT ON")

    def output_dc_voltage(self, voltage_level):
        """Configures the source output to be a DC current source.

            Args:
                voltage_level (float):
                    The output voltage level in volts.

        """

        # Change the output mode to source voltage instead of current
        self.command("SOURCE:FUNCTION:MODE VOLTAGE")

        # Configure the instrument to output a sine wave
        self.command("SOURCE:FUNCTION:SHAPE DC")

        # Configure DC current level
        self.command("SOURCE:VOLTAGE:AMPLITUDE " + str(voltage_level))

        # Turn on the output voltage
        self.command("OUTPUT ON")

    def get_output_settings(self):
        """Returns a dictionary of the output settings."""

        mode = self.query("SOURCE:FUNCTION:MODE?")

        output_settings = {"mode": mode,
                           "output_shape": self.query("SOURCE:FUNCTION:SHAPE?"),
                           "amplitude": float(self.query("SOURCE:" + mode + ":AMPLITUDE?")),
                           "frequency": float(self.query("SOURCE:FREQUENCY?")),
                           "offset": float(self.query("SOURCE:" + mode + ":OFFSET?")),
                           "phase": float(self.query("SOURCE:PHASE?")),
                           "autorange": bool(self.query("SOURCE:" + mode + ":RANGE:AUTO?")),
                           "range": self.query("SOURCE:" + mode + ":RANGE?"),
                           "limit": float(self.query("SOURCE:" + mode + ":LIMIT?")),
                           "protection": float(self.query("SOURCE:" + mode + ":PROTECTION?"))}

        return output_settings

    def enable_autorange(self):
        """Enables the instrument to automatically select the best range for the given output parameters."""
        self.command("SOURCE:VOLTAGE:RANGE:AUTO ON")
        self.command("SOURCE:CURRENT:RANGE:AUTO ON")

    def disable_autorange(self):
        """Enables the instrument to automatically select the best range for the given output parameters."""
        self.command("SOURCE:VOLTAGE:RANGE:AUTO OFF")
        self.command("SOURCE:CURRENT:RANGE:AUTO OFF")

    def set_current_range(self, current_range="100E-3"):
        """Manually sets the current range when autorange is disabled.

            Args:
                current_range (str):
                    The range in amps. Valid ranges are: "100E-3", "10E-3", "1E-3", "100E-6", "10E-6", and "1E-6".

        """
        self.command("SOURCE:CURRENT:RANGE " + current_range)

    def set_voltage_range(self, voltage_range="10"):
        """Manually sets the voltage range when autorange is disabled.

            Args:
                voltage_range (str):
                    The range in volts. Valid ranges are: "100", "10", "1", "0.1", and "0.01".

        """
        self.command("SOURCE:VOLTAGE:RANGE " + voltage_range)

    def set_current_limit(self, current_limit):
        """Sets the highest settable current output value when in current mode.

            Args:
                current_limit (float):
                    The maximum settable current in amps. Must be between 0 and 100 milli-amps.

        """
        self.command("SOURCE:CURRENT:LIMIT " + str(current_limit))

    def set_voltage_limit(self, voltage_limit):
        """Sets the highest settable voltage output value when in voltage mode.

            Args:
                voltage_limit (float):
                    The maximum settable voltage in amps. Must be between 0 and 100 volts.

        """
        self.command("SOURCE:VOLTAGE:LIMIT " + str(voltage_limit))

    def set_current_mode_voltage_protection(self, max_voltage):
        """Sets the maximum voltage level permitted by the instrument when sourcing current.

            Args:
                max_voltage (float):
                    The maximum permissible voltage. Must be between 1 and 100 volts.

        """
        self.command("SOURCE:CURRENT:PROTECTION " + str(max_voltage))

    def set_voltage_mode_current_protection(self, max_current):
        """Sets the maximum current level permitted by the instrument when sourcing voltage.

            Args:
                max_current (float):
                    The maximum permissible voltage. Must be between 1 and 100 volts.

        """
        self.command("SOURCE:VOLTAGE:PROTECTION " + str(max_current))

    def enable_ac_high_voltage_compliance(self):
        """Configures the current mode compliance voltage to be 100V in AC output modes."""
        self.command("SOURCE:CURRENT:AC:VRANGE 100")

    def disable_ac_high_voltage_compliance(self):
        """Configures the current mode compliance voltage to be 10V in AC output modes."""
        self.command("SOURCE:CURRENT:AC:VRANGE 10")


# Create an alias using the product name
Model155 = PrecisionSource
