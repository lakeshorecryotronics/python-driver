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

    class InputSensorUnits(IntEnum):
        """Enumerator used to represent temperature sensor unit options."""
        KELVIN = 1
        CELSIUS = 2
        FAHRENHEIT = 3
        DUMMY = 255

    class DiodeRange(IntEnum):
        """Diode voltage range enumeration"""
        TWO_POINT_FIVE_VOLTS = 0
        # TEN_VOLTS = 1

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
        WARMUP_SUPPLY = 5
        MIRRORING = 6
