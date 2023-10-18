"""Implements a class containing the enums relevant to the Model 335."""
from enum import IntEnum


class Model335Enums:
    """Class containing the enums relevant to the Model 335."""
    class InputSensor(IntEnum):
        """Enumeration when "NONE" is an option for sensor input."""
        NONE = 0
        CHANNEL_A = 1
        CHANNEL_B = 2

    class MonitorOutUnits(IntEnum):
        """Units associated with a sensor channel."""
        KELVIN = 1
        CELSIUS = 2
        SENSOR = 3

    class InputSensorType(IntEnum):
        """Sensor type enumeration."""
        DISABLED = 0
        DIODE = 1
        PLATINUM_RTD = 2
        NTC_RTD = 3
        THERMOCOUPLE = 4

    class DiodeRange(IntEnum):
        """Diode voltage range enumeration."""
        TWO_POINT_FIVE_VOLTS = 0
        TEN_VOLTS = 1

    class RTDRange(IntEnum):
        """RTD resistance range enumeration."""
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

    class HeaterOutType(IntEnum):
        """Heater output 2 enumeration."""
        CURRENT = 0
        VOLTAGE = 1

    class HeaterOutputDisplay(IntEnum):
        """Heater output display units enumeration."""
        CURRENT = 1
        POWER = 2

    class HeaterOutputMode(IntEnum):
        """Control loop enumeration."""
        OFF = 0
        CLOSED_LOOP = 1
        ZONE = 2
        OPEN_LOOP = 3
        MONITOR_OUT = 4
        WARMUP_SUPPLY = 5

    class WarmupControl(IntEnum):
        """Heater output 2 voltage mode warmup enumerations."""
        AUTO_OFF = 0
        CONTINUOUS = 1

    class HeaterRange(IntEnum):
        """Control loop heater range enumeration."""
        OFF = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3

    class DisplaySetup(IntEnum):
        """Panel display setup enumeration."""
        INPUT_A = 0
        INPUT_A_MAX_MIN = 1
        TWO_INPUT_A = 2
        INPUT_B = 3
        INPUT_B_MAX_MIN = 4
        TWO_INPUT_B = 5
        CUSTOM = 6
        TWO_LOOP = 7

    class HeaterVoltageRange(IntEnum):
        """Voltage mode heater enumerations."""
        VOLTAGE_OFF = 0
        VOLTAGE_ON = 1

    class InputChannel(IntEnum):
        """Panel display information enumeration."""
        NONE = 0
        INPUT_A = 1
        INPUT_B = 2
        SETPOINT_1 = 3
        SETPOINT_2 = 4
        OUTPUT_1 = 5
        OUTPUT_2 = 6

    class DisplayFieldUnits(IntEnum):
        """Panel display units enumeration."""
        KELVIN = 1
        CELSIUS = 2
        SENSOR_UNITS = 3
        MINIMUM_DATA = 4
        MAXIMUM_DATA = 5
        SENSOR_NAME = 6
