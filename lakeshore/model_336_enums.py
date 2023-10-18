"""Implements a class containing the enums relevant to the Model 336."""
from enum import IntEnum


class Model336Enums:
    """Class containing the enums relevant to the Model 336."""
    class InputChannel(IntEnum):
        """Enumeration where "NONE" is an option for sensor input."""
        NONE = 0
        CHANNEL_A = 1
        CHANNEL_B = 2
        CHANNEL_C = 3
        CHANNEL_D = 4
        CHANNEL_D2 = 5
        CHANNEL_D3 = 6
        CHANNEL_D4 = 7
        CHANNEL_D5 = 8

    class DisplaySetupMode(IntEnum):
        """Front panel display setup enum."""
        INPUT_A = 0
        INPUT_B = 1
        INPUT_C = 2
        INPUT_D = 3
        CUSTOM = 4
        FOUR_LOOP = 5
        ALL_INPUTS = 6
        INPUT_D2 = 7
        INPUT_D3 = 8
        INPUT_D4 = 9
        INPUT_D5 = 10

    class InputSensorType(IntEnum):
        """Sensor type enumeration.

            THERMOCOUPLE is only valid with the 3060 option, CAPACITANCE is only valid with the 3061 option.
        """
        DISABLED = 0
        DIODE = 1
        PLATINUM_RTD = 2
        NTC_RTD = 3
        THERMOCOUPLE = 4
        CAPACITANCE = 5

    class DiodeRange(IntEnum):
        """Diode voltage range enumeration"""
        TWO_POINT_FIVE_VOLTS = 0
        TEN_VOLTS = 1

    class RTDRange(IntEnum):
        """RTD resistance range enumeration.

            THIRTY_THOUSAND_OHM and ONE_HUNDRED_THOUSAND_OHM are only valid for NTC RTDs.
        """
        TEN_OHM = 0
        THIRTY_OHM = 1
        HUNDRED_OHM = 2
        THREE_HUNDRED_OHM = 3
        ONE_THOUSAND_OHM = 4
        THREE_THOUSAND_OHM = 5
        TEN_THOUSAND_OHM = 6
        THIRTY_THOUSAND_OHM = 7
        ONE_HUNDRED_THOUSAND_OHM = 8

    class ThermocoupleRange(IntEnum):
        """Thermocouple range enumeration."""
        FIFTY_MILLIVOLT = 0

    class HeaterOutputMode(IntEnum):
        """Control loop enumeration."""
        OFF = 0
        CLOSED_LOOP = 1
        ZONE = 2
        OPEN_LOOP = 3
        MONITOR_OUT = 4
        WARMUP_SUPPLY = 5

    class HeaterRange(IntEnum):
        """Current mode heater enumerations."""
        OFF = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3

    class HeaterVoltageRange(IntEnum):
        """Voltage mode heater enumerations."""
        VOLTAGE_OFF = 0
        VOLTAGE_ON = 1

    class DisplayFieldUnits(IntEnum):
        """Panel display units enumeration."""
        KELVIN = 1
        CELSIUS = 2
        SENSOR_UNITS = 3
        MINIMUM_DATA = 4
        MAXIMUM_DATA = 5
        SENSOR_NAME = 6
