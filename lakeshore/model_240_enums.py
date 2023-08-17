"""Implements a class containing the enums relevant to the Model 240."""
from enum import IntEnum


class Model240Enums:
    """Class containing the enums relevant to the Model 240."""
    class Units(IntEnum):
        """Enumerations that specify temperature units."""
        KELVIN = 1
        CELSIUS = 2
        SENSOR = 3
        FAHRENHEIT = 4

    class CurveFormat(IntEnum):
        """Enumerations that specify temperature sensor curve format units."""
        VOLTS_PER_KELVIN = 2
        OHMS_PER_KELVIN = 3
        LOG_OHMS_PER_KELVIN = 4

    class Coefficients(IntEnum):
        """Enumerations that specify a positive or negative coefficient."""
        NEGATIVE = 1
        POSITIVE = 2

    class SensorTypes(IntEnum):
        """Enumerations specify types of temperature sensors."""
        DIODE = 1
        PLATINUM_RTD = 2
        NTC_RTD = 3

    class BrightnessLevel(IntEnum):
        """Enumerations for the screen brightness levels."""
        OFF = 0
        LOW = 25
        MED_LOW = 50
        MED_HIGH = 75
        HIGH = 100

    class TemperatureCoefficient(IntEnum):
        """Enumerations specify positive/negative temperature sensor curve coefficients."""
        NEGATIVE = 1
        POSITIVE = 2

    class InputRange(IntEnum):
        """Enumerations to specify the input range when auto-range is off."""
        RANGE_DIODE = 0
        RANGE_PTRTD_1_KIL_OHMS = 0
        RANGE_NTCRTD_10_OHMS = 0
        RANGE_NTCRTD_30_OHMS = 1
        RANGE_NTCRTD_100_OHMS = 2
        RANGE_NTCRTD_1_KIL_OHMS = 4
        RANGE_NTCRTD_3_KIL_OHMS = 5
        RANGE_NTCRTD_10_KIL_OHMS = 6
        RANGE_NTCRTD_30_KIL_OHMS = 7
        RANGE_NTCRTD_100_KIL_OHMS = 8
