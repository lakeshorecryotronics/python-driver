"""Implements a class containing the enums relevant to the Model 346."""
from enum import IntEnum


class Model346Enums:
    """Class containing the enums relevant to the Model 346."""

    class InputSensorType(IntEnum):
        """Sensor type enumeration."""
        DISABLED = 0
        DIODE = 1
        PLATINUM_RTD = 2
        NTC_RTD = 3
        THERMOCOUPLE = 4

    class InputSensorUnits(IntEnum):
        """Enumerator used to represent temperature sensor unit options."""
        KELVIN = 0
        CELSIUS = 1

    class DiodeRange(IntEnum):
        """Diode voltage range enumeration"""
        TWO_POINT_FIVE_VOLTS = 0

    class PTCRTDRange(IntEnum):
        """PTC RTD resistance range enumeration."""
        TEN_OHM = 0
        ONE_HUNDRED_OHM = 1
        ONE_THOUSAND_OHM = 2

    class NTCRTDRange(IntEnum):
        """NTC RTD resistance range enumeration."""
        ONE_HUNDRED_OHM = 0
        THREE_HUNDRED_OHM = 1
        ONE_THOUSAND_OHM = 2
        THREE_THOUSAND_OHM = 3
        TEN_THOUSAND_OHM = 4
        THIRTY_THOUSAND_OHM = 5
        HUNDRED_THOUSAND_OHM = 6

    class ThermocoupleRange(IntEnum):
        """Thermocouple voltage range enumeration."""
        FIFTY_MILLIVOLTS = 0

    class HeaterRange(IntEnum):
        """Heater range enumerations."""
        OFF = 0
        LOW = 1
        HIGH = 2

    class HeaterOutputUnits(IntEnum):
        """Enumerator used to represent heater output unit settings."""
        POWER = 0
        CURRENT = 1

    class AlarmType(IntEnum):
        """Enumeration for possible alarm output types"""
        NONE = 0
        RELAY = 1
        FRONT_DISPLAY = 2
        FRONT_AUDIO = 3

    class OutputMode(IntEnum):
        """Output control enumeration."""
        OFF = 0
        PID = 1
        ZONE = 2
        OPEN_LOOP = 3
        MONITOR_OUT = 4

    class StandardCurveType(IntEnum):
        """Enumeration for standard curve types."""
        DIODE_DT670 = 2
        PTC_PT100 = 6
        NTC_RX102A_AA = 8
        NTC_RX202A_AA = 9
        NTC_RX103A_AA = 10
        THERMOCOUPLE_TYPE_K = 12
        THERMOCOUPLE_TYPE_E = 13

    class RelayControlAlarm(IntEnum):
        """Enumeration of the setting determining which alarm(s) cause a relay to close in alarm mode."""
        LOW_ALARM = 0
        HIGH_ALARM = 1
        LOW_OR_HIGH_ALARM = 2
        LOW_AND_HIGH_ALARM = 3

    class OptionCardType(IntEnum):
        """Enumeration for option card types."""
        NONE = 0
        SCANNER = 1
        LEVEL_SENSE = 2
        MOTOR_CONTROL = 3
        THERMOCOUPLE = 4
