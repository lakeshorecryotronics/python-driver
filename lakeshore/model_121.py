"""Implements functionality unique to the Lake Shore Model 121 programmable DC current source."""
import serial

from .generic_instrument import GenericInstrument


class Model121(GenericInstrument):
    """A class object representing the Lake Shore Model 121 programmable DC current source."""

    vid_pid = [(0x1FB9, 0x0100)]

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

        # Call the parent init, then fill in values specific to the 121
        GenericInstrument.__init__(self, serial_number, com_port, baud_rate, data_bits, stop_bits, parity, flow_control,
                                   handshaking, timeout, ip_address, tcp_port, **kwargs)

    def command(self, command_string: str) -> None:
        """Sends a command to the instrument.

        Args:
            command_string (str): A serial command.

        """
        # Overload of parent command.
        # In order to avoid overlapping commands, a short query is appended to block the instruction.
        # The type of query that is used here is not important. It only matters that some query is sent which
        # will block.

        GenericInstrument.query(self, command_string + '; COMP?')

    def get_identity(self) -> list[str]:
        """Returns the Manufacturer ID, model number, serial number, and firmware version of instrument.

        Returns:
            list[str]: [manufacturer_id, model_number, serial_number, firmware_version]

        """
        return self.query('*IDN?').split(',')

    def reset_instrument(self) -> None:
        """Sets instrument parameters to power-up settings."""
        self.command("*RST")

    def set_display_brightness(self, brightness_level: int) -> None:
        """Sets the display contrast for the front panel seven-segment display.

            A higher number makes the display brighter. The default setting is 8. The display can be turned off by
            setting the brightness to 0.

        Args:
            brightness_level (int): The display brightness (0-15).

        """
        self.command(f"BRIGT {brightness_level}")

    def get_display_brightness(self) -> int:
        """Gets the display contrast for the front panel seven-segment display.

            A higher number makes the display brighter. The default setting is 8. Brightness level 0 means the display
            is turned off.

        Returns:
            int: The display brightness (0-15).

        """
        return int(self.query("BRIGT?"))

    def get_compliance_limit_status(self) -> bool:
        """Returns the voltage compliance status of the current source output.

        Returns:
            bool: False = normal operation. True = in compliance limit.

        """
        return bool(int(self.query("COMP?")))

    def set_factory_defaults(self) -> None:
        """Sets all configuration values to factory defaults and resets the instrument."""
        self.command("DFLT 99")

    def lock_front_panel(self) -> None:
        """Locks the front panel keypad."""
        self.command("LOCK 1")

    def unlock_front_panel(self) -> None:
        """Unlocks the front panel keypad."""
        self.command("LOCK 0")

    def get_front_panel_lock_status(self) -> bool:
        """Returns if the front panel keypad  is locked or not.

        Returns:
            bool: True = Locked, False = Unlocked.
        """
        return bool(int(self.query("LOCK?")))

    def set_power_up_enable(self, state: bool) -> None:
        """Specifies whether the output remains on or shuts off after power cycle.

        Args:
            state (bool): True = Enabled, False = Disabled.

        """
        self.command(f"PWUPENBL {int(state)}")

    def save_current_state(self) -> None:
        """Saves the present range, polarity, and user current value.

            This saved state will be loaded on future power ups.

        """
        self.command("SETSAVE")