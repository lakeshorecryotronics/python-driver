"""Implements a class containing the enums relevant to temperature controllers."""
from enum import IntEnum


class TemperatureControllerEnums:
    """Class containing the enums relevant to temperature controllers."""

    class InputChannel(IntEnum):
        """Placeholder Enumeration of the display field input source."""

    class DisplayFieldUnits(IntEnum):
        """Placeholder Enumeration of the display field units."""

    class RelayControlMode(IntEnum):
        """Relay operating mode enumeration."""
        RELAY_OFF = 0
        RELAY_ON = 1
        ALARMS = 2

    class RelayControlAlarm(IntEnum):
        """Enumeration of the setting determining which alarm(s) cause a relay to close in alarm mode."""
        LOW_ALARM = 0
        HIGH_ALARM = 1
        BOTH_ALARMS = 2

    class InterfaceMode(IntEnum):
        """Enumeration for the mode of the remote interface."""
        LOCAL = 0
        REMOTE = 1
        REMOTE_LOCAL_LOCK = 2

    class HeaterError(IntEnum):
        """Enumeration for possible errors flagged by the heater."""
        NO_ERROR = 0
        HEATER_OPEN_LOAD = 1
        HEATER_SHORT = 2

    class CurveFormat(IntEnum):
        """Enumerations specify formats for temperature sensor curves."""
        MILLIVOLT_PER_KELVIN = 1
        VOLTS_PER_KELVIN = 2
        OHMS_PER_KELVIN = 3
        LOG_OHMS_PER_KELVIN = 4

    class CurveTemperatureCoefficient(IntEnum):
        """Enumerations specify positive/negative temperature sensor curve coefficients."""
        NEGATIVE = 1
        POSITIVE = 2

    class BrightnessLevel(IntEnum):
        """Enumerator to specify the brightness level of an instrument display."""
        QUARTER = 0
        HALF = 1
        THREE_QUARTERS = 2
        FULL = 3

    class AutotuneMode(IntEnum):
        """Enumerator used to represent the different autotune control modes."""
        P_ONLY = 0
        P_I = 1
        P_I_D = 2

    class HeaterResistance(IntEnum):
        """Enumerator used to represent the different heater resistances."""
        HEATER_25_OHM = 1
        HEATER_50_OHM = 2

    class Polarity(IntEnum):
        """Enumerator for unipolar or bipolar output operation."""
        UNIPOLAR = 0
        BIPOLAR = 1

    class DiodeCurrent(IntEnum):
        """Enumerator used to represent diode current ranges."""
        TEN_MICROAMPS = 0
        ONE_MILLIAMP = 1

    class HeaterOutputUnits(IntEnum):
        """Enumerator used to represent heater output unit settings."""
        CURRENT = 1
        POWER = 2

    class Interface(IntEnum):
        """Enumerator used to represent remote interface communication methods."""
        USB = 0
        ETHERNET = 1
        IEEE488 = 2

    class InputSensorUnits(IntEnum):
        """Enumerator used to represent temperature sensor unit options."""
        KELVIN = 1
        CELSIUS = 2
        SENSOR = 3

    class ControlTypes(IntEnum):
        """Enumerator used to represent the control type settings."""
        AUTO_OFF = 0
        CONTINUOUS = 1

    class LanStatus(IntEnum):
        """Represents the different status states for the lan connection."""
        STATIC_IP = 0
        DHCP = 1
        AUT0_IP = 2
        ADDRESS_NOT_ACQUIRED_ERROR = 3
        DUPLICATE_INITIAL_IP_ERROR = 4
        DUPLICATE_ONGOING_IP_ERROR = 5
        CABLE_UNPLUGGED = 6
        MODULE_ERROR = 7
        ACQUIRING_ADDRESS = 8
        ETHERNET_DISABLED = 9

    class DisplayFields(IntEnum):
        """Enumeration of the possible number of fields to include in a custom display mode."""
        LARGE_2 = 0
        LARGE_4 = 1
        SMALL_8 = 2

    class DisplayFieldsSize(IntEnum):
        """Enumeration of the display fields when mode is set to all inputs."""
        SMALL = 0
        LARGE = 1
