"""Implements functionality unique to the Model 643 and 648 electromagnet power supplies."""

import serial
from .generic_instrument import GenericInstrument


class ElectromagnetPowerSupply(GenericInstrument):
    """ class object representing a Lake Shore Model 643 or 648 electromagnet power supply."""
    vid_pid = [(0x1FB9, 0x0601), (0x1FB9, 0x0602)]  # 643, 648

    def __init__(self,
                 serial_number=None,
                 com_port=None,
                 baud_rate=57600,
                 data_bits=7,
                 stop_bits=1,
                 parity=serial.PARITY_ODD,
                 flow_control=False,
                 handshaking=False,
                 timeout=2.0,
                 ip_address=None,
                 tcp_port=7777,
                 **kwargs):

        # Call the parent init, then fill in values specific to the instrument
        GenericInstrument.__init__(self, serial_number, com_port, baud_rate, data_bits, stop_bits, parity, flow_control,
                                   handshaking, timeout, ip_address, tcp_port, **kwargs)

    def set_limits(self, max_current: float, max_ramp_rate: float) -> None:
        """Sets the upper setting limits for output current, and output current ramp rate.

            This is a software limit that will limit the setting of the values. Only limits internal
            setting of the current.

        Args:
            max_current (float): The maximum output current setting allowed. The Model
                643 bounds are 0.0000 - 70.1000 A. The Model 648 bounds are 0.0000 - 135.1000 A.
            max_ramp_rate (float): The maximum output current ramp rate setting allowed (0.0001 - 50.000 A/s).
        """
        self.command(f"LIMIT {max_current}, {max_ramp_rate}")

    def get_limits(self) -> list[float]:
        """Returns the upper setting limits for output current, and output current ramp rate.

            This is a software limit that limits the setting of the values. Only limits the internal
            setting of the current.

        Returns:
            list[float]: List of [output_current, output_current_ramp_rate].
        """
        return [float(element) for element in self.query("LIMIT?").split(',')]

    def set_ramp_rate(self, ramp_rate: float) -> None:
        """Sets the output current ramp rate.

            This value will be used in both the positive and negative directions. Setting value is limited by set_limit.

        Args:
            ramp_rate (float):  The rate at which the current will ramp when a new output current setting is entered
                (0.0001 - 50.000 A/s).
        """
        self.command(f"RATE {ramp_rate}")

    def get_ramp_rate(self) -> float:
        """Returns the output current ramp rate.

            This value is used in both the positive and negative directions.

        Returns:
            float: The rate at which the current will ramp when a new output current setting is entered.
        """
        return float(self.query("RATE?"))

    def set_ramp_segment(self, segment: int, current: float, ramp_rate: float) -> None:
        """Sets the current and ramp rate of one of the ramp segments.

        Args:
            segment (int): Specifies the ramp segment to be modified (1 - 5).
            current (float): Specifies the upper output current setting that will use this segment. The Model
                643 bounds are 0.0000 - 70.1000 A. The Model 648 bounds are 0.0000 - 135.1000 A.
            ramp_rate (float): Specifies the rate at which the current will ramp at when the output current is in this
                segment. (0.0001 - 50.000 A/s)
        """
        self.command(f"RSEGS {segment}, {current}, {ramp_rate}")

    def get_ramp_segment(self, segment: int) -> list[float]:
        """Returns the current and ramp rate of a specific ramp segment.

        Args:
            segment (int): Specifies the ramp segment to be modified (1 - 5).

        Returns:
            list[float]: List of current and ramp_rate settings. [current, ramp_rate].
        """
        return [float(x) for x in self.query(f"RSEGS? {segment}").split(',')]

    def set_ramp_segments_enable(self, state: bool) -> None:
        """Specifies if ramp segments are to be used.

            Ramp segments are used to change the output current ramp rate based on the output current.

        Args:
            state (bool): The state of the ramp segments enable. 0=Disabled and 1=Enabled.
        """
        self.command(f"RSEG {int(state)}")

    def get_ramp_segments_enable(self) -> bool:
        """Returns if ramp segments are to be used.

            Ramp segments are used to change the output current ramp rate based on the output current.

        Returns:
            bool: Whether ramp segments are enabled. 0=Disabled and 1=Enabled.
        """
        return bool(int(self.query("RSEG?")))

    def set_current(self, current: float) -> None:
        """Sets the output current setting.

            The setting value is limited by set_limit.

        Args:
            current (float): The output current value that the output will ramp to at the present ramp rate. The Model
                643 bounds are 0.0000 - +/-70.1000 A. The Model 648 bounds are 0.0000 - +/-135.1000 A.
        """
        self.command(f"SETI {current}")

    def get_current(self) -> float:
        """Returns the output current setting.

        Returns:
            float: The output current value that the output will ramp to at the present ramp rate.
        """
        return float(self.query("SETI?"))

    def get_measured_current(self) -> float:
        """Returns actual measured output current.

        Returns:
            float: Measured output current.
        """
        return float(self.query("RDGI?"))

    def get_measured_voltage(self) -> float:
        """Returns actual output voltage measured at the power supply terminals.

        Returns:
            float: Measured output voltage.
        """
        return float(self.query("RDGV?"))

    def stop_output_current_ramp(self) -> None:
        """Stops the output current ramp.

            Stops within 2 s of sending command. TO restart the ramp, use the set_current method to set a new output
            current set-point.
        """
        self.command("STOP")


# Create an aliases using the product names
Model643 = ElectromagnetPowerSupply
Model648 = ElectromagnetPowerSupply
