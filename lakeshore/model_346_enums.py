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
        """Heater range enumerations for heater outputs(1-4) amd heater groups 9 and 10."""
        OFF = 0
        LOW = 1
        HIGH = 2

    class HeaterAutorange(IntEnum):
        """Heater autorange enumeration for heater outputs 1-4."""
        DISABLED = 0
        ENABLED = 1

    class HeaterRangeAnalogOutput(IntEnum):
        """Heater range enumeration for analog outputs 5 and 8."""
        OFF = 0
        ON = 1

    class HeaterOutputUnits(IntEnum):
        """Enumerator used to represent heater output unit settings."""
        POWER = 0
        CURRENT = 1

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

    class RelayControlMode(IntEnum):
        """Enumeration for relay control feature/mode."""
        OFF = 0
        ON = 1
        ALARMS = 2
        THERMOMETRY_INPUT = 2
        OUTPUT_STATUS = 3
        DIGITAL_INPUT = 4
        SYSTEM_STATUS = 5
        FUNCTION_OUTPUT = 6

    class RelayThermometryCondition(IntEnum):
        """Enumeration for relay thermometry input conditions."""
        LOW_ALARM_ACTIVE = 0
        HIGH_ALARM_ACTIVE = 1
        EITHER_ALARM_ACTIVE = 2
        BOTH_ALARMS_ACTIVE = 3
        THRESHOLD_1 = 4
        THRESHOLD_2 = 5
        THRESHOLD_3 = 6
        THRESHOLD_4 = 7
        SENSOR_FAULT = 8
        TEMPERATURE_FAULT = 9
        TEMPERATURE_EXTRAPOLATED = 10

    class RelayOutputStatusCondition(IntEnum):
        """Enumeration for relay output status conditions."""
        OUTPUT_LOAD_FAULT = 0
        OUTPUT_STABILIZING = 1
        OUTPUT_STABLE = 2
        OUTPUT_WARM = 3
        OUTPUT_SETPOINT_RAMPING_COMPLETE = 4

    class RelayDigitalInputCondition(IntEnum):
        """Enumeration for relay digital input conditions."""
        LOW = 0
        HIGH = 1

    class RelayFunctionOutputCondition(IntEnum):
        """Enumeration for relay function output conditions."""
        FALSE = 0
        TRUE = 1

    class ThresholdComparison(IntEnum):
        """Enumeration for threshold comparison operator."""
        LESS_THAN = 0
        GREATER_THAN = 1

    class OptionCardType(IntEnum):
        """Enumeration for option card types."""
        NONE = 0
        SCANNER = 1
        LEVEL_SENSE = 2
        MOTOR_CONTROL = 3
        THERMOCOUPLE = 4
