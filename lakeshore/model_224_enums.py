"""Implements a class containing the enums relevant to the Model 224."""
from enum import IntEnum


class Model224Enums:
    """Class containing the enums relevant to the Model 224."""
    class InputSensorType(IntEnum):
        """Enumeration for the type of sensor being used for a given input."""
        INPUT_DISABLED = 0
        DIODE = 1
        PLATINUM_RTD = 2
        NTC_RTD = 3

    class InputSensorUnits(IntEnum):
        """Enumeration for the preferred units of an input sensor."""
        KELVIN = 1
        CELSIUS = 2
        SENSOR = 3

    class DiodeSensorRange(IntEnum):
        """Enumeration for the voltage range of a diode sensor."""
        RANGE_2_POINT_5_VOLTS = 0
        RANGE_10_VOLTS = 1

    class PlatinumRTDSensorResistanceRange(IntEnum):
        """Enumeration of the resistance range of a platinum RTD input sensor."""
        TEN_OHMS = 0
        THIRTY_OHMS = 1
        ONE_HUNDRED_OHMS = 2
        THREE_HUNDRED_OHMS = 3
        ONE_KILOHM = 4
        THREE_KILOHMS = 5
        TEN_KILOHMS = 6

    class NTCRTDSensorResistanceRange(IntEnum):
        """Enumeration of the resistance range of a NTC RTD input sensor."""
        TEN_OHMS = 0
        THIRTY_OHMS = 1
        ONE_HUNDRED_OHMS = 2
        THREE_HUNDRED_OHMS = 3
        ONE_KILOHM = 4
        THREE_KILOHMS = 5
        TEN_KILOHMS = 6
        THIRTY_KILOHMS = 7
        ONE_HUNDRED_KILOHMS = 8

    class InterfaceMode(IntEnum):
        """Enumeration for the mode of the remote interface."""
        LOCAL = 0
        REMOTE = 1
        REMOTE_LOCAL_LOCK = 2

    class RemoteInterface(IntEnum):
        """Enumeration for the remote interface being used to communicate with the instrument."""
        USB = 0
        ETHERNET = 1
        IEEE_488 = 2

    class DisplayFieldUnits(IntEnum):
        """Enumerated type defining how units are enumerated for settings and using Display Fields."""
        KELVIN = 1
        CELSIUS = 2
        SENSOR = 3
        MINIMUM_DATA = 4
        MAXIMUM_DATA = 5

    class InputChannel(IntEnum):
        """Enumerated type defining which input channels correspond to ints for setting and using Display Fields."""
        NO_INPUT = 0
        INPUT_A = 1
        INPUT_B = 2
        INPUT_C = 3
        INPUT_D1 = 4
        INPUT_D2 = 5
        INPUT_D3 = 6
        INPUT_D4 = 7
        INPUT_D5 = 8
        INPUT_C2 = 9
        INPUT_C3 = 10
        INPUT_C4 = 11
        INPUT_C5 = 12

    class DisplayMode(IntEnum):
        """Enumeration defining what input or information is shown on the front panel display."""
        INPUT_A = 0
        INPUT_B = 1
        INPUT_C = 2
        INPUT_D1 = 3
        CUSTOM = 4
        ALL_INPUTS = 5
        INPUT_D2 = 6
        INPUT_D3 = 7
        INPUT_D4 = 8
        INPUT_D5 = 9
        INPUT_C2 = 10
        INPUT_C3 = 11
        INPUT_C4 = 12
        INPUT_C5 = 13

    class NumberOfFields(IntEnum):
        """Enumerated type specifying the number of display fields to configure in the Custom display mode."""
        LARGE_4 = 0
        LARGE_8 = 1
        LARGE_4_SMALL_8 = 2
        SMALL_16 = 3

    class RelayControlAlarm(IntEnum):
        """Enumeration of the setting determining which alarm(s) cause a relay to activate in alarm mode."""
        LOW_ALARM = 0
        HIGH_ALARM = 1
        BOTH_ALARMS = 2

    class RelayControlMode(IntEnum):
        """Enumeration of the configured mode of a relay."""
        RELAY_OFF = 0
        RELAY_ON = 1
        ALARMS = 2

    class CurveFormat(IntEnum):
        """Enumerations specify formats for temperature sensor curves."""
        MILLIVOLT_PER_KELVIN = 1
        VOLTS_PER_KELVIN = 2
        OHMS_PER_KELVIN = 3
        LOG_OHMS_PER_KELVIN = 4

    class CurveTemperatureCoefficients(IntEnum):
        """Enumerations specify positive/negative temperature sensor curve coefficients."""
        NEGATIVE = 1
        POSITIVE = 2

    class DiodeExcitationCurrent(IntEnum):
        """Enum type representing the different excitation currents available for a diode sensor."""
        TEN_MICRO_AMPS = 0
        ONE_MILLI_AMP = 1

    class SoftCalSensorTypes(IntEnum):
        """Enum type representing the standard curves used to generate a SoftCal curve.

            The 3 standard curves each represent a different type of sensor that can be calibrated with a SoftCal curve.
        """
        DT_400 = 1
        PT_100 = 6
        PT_1000 = 7
