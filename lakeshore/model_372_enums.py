"""Implements a class containing the enums relevant to the Model 372."""
from enum import IntEnum, Enum


class Model372Enums:
    """Class containing the enums relevant to the Model 372."""
    class OutputMode(IntEnum):
        """Enumeration of the different modes for heater output setup."""

        OFF = 0
        MONITOR_OUT = 1
        OPEN_LOOP = 2
        ZONE = 3
        STILL = 4
        CLOSED_LOOP = 5
        WARMUP = 6

    class InputChannel(Enum):
        """Enumeration of the input channels of the Model 372."""

        NONE = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        SIX = 6
        SEVEN = 7
        EIGHT = 8
        NINE = 9
        TEN = 10
        ELEVEN = 11
        TWELVE = 12
        THIRTEEN = 13
        FOURTEEN = 14
        FIFTEEN = 15
        SIXTEEN = 16
        CONTROL = "A"

    class SensorExcitationMode(IntEnum):
        """Enumeration of the possible excitation modes for an input sensor."""

        VOLTAGE = 0
        CURRENT = 1

    class AutoRangeMode(IntEnum):
        """Enumeration for the possible modes of the auto ranging feature.

            ROX102B mode is a special auto-ranging mode that applies only to Lake Shore ROX-102B sensor.
        """

        OFF = 0
        CURRENT = 1
        ROX102B = 2

    class InputSensorUnits(IntEnum):
        """Enumeration of the units to handle input readings and display in."""

        KELVIN = 1
        OHMS = 2

    class MonitorOutputSource(IntEnum):
        """Enumeration of the source for an output to monitor."""

        OFF = 0
        CS_NEG = 1
        CS_POS = 2
        VCM_NEG = 3
        VCM_POS = 4
        VDIF = 5
        VAD_MEASUREMENT = 6
        VAD_CONTROL = 7

    class RelayControlMode(IntEnum):
        """Enumeration of the control modes of the configurable relays of the 372."""

        RELAY_OFF = 0
        RELAY_ON = 1
        ALARMS = 2
        SAMPLE_HEATER_ZONE = 3
        WARMUP_HEATER_ZONE = 4

    class DisplayMode(IntEnum):
        """Enumeration of the possible information to display."""

        MEASUREMENT_INPUT = 0
        CONTROL_INPUT = 1
        CUSTOM = 2

    class DisplayInfo(IntEnum):
        """Enumeration of the information to a display in the bottom left of the custom display mode."""

        NONE = 0
        SAMPLE_HEATER = 1
        WARMUP_HEATER = 2
        ACTIVE_SCAN_CHANNEL = 3

    class CurveFormat(IntEnum):
        """Enumeration of the units to use in a calibration curve."""

        OHM_PER_KELVIN = 3
        LOGOHM_PER_KELVIN = 4
        OHM_PER_KELVIN_CUBIC_SPLINE = 7

    class DisplayFieldUnits(IntEnum):
        """Enumeration for the possible units to display in a single display field."""

        KELVIN = 1
        OHMS = 2
        QUADRATURE = 3
        MINIMUM_DATA = 4
        MAXIMUM_DATA = 5
        SENSOR_NAME = 6

    class SampleHeaterOutputRange(IntEnum):
        """Enumeration of the output range of the sample heater (output 0)."""
        OFF = 0
        RANGE_31_POINT_6_MICRO_AMPS = 1
        RANGE_100_MICRO_AMPS = 2
        RANGE_316_MICRO_AMPS = 3
        RANGE_1_MILLI_AMP = 4
        RANGE_3_POINT_16_MILLI_AMPS = 5
        RANGE_10_MILLI_AMPS = 6
        RANGE_31_POINT_6_MILLI_AMPS = 7
        RANGE_100_MILLI_AMPS = 8

    class InputFrequency(IntEnum):
        """Defines the enumeration of the excitation frequency of an input."""

        FREQUENCY_9_POINT_8_HZ = 1
        FREQUENCY_13_POINT_7_HZ = 2
        FREQUENCY_16_POINT_2_HZ = 3
        FREQUENCY_11_POINT_6_HZ = 4
        FREQUENCY_18_POINT_2_HZ = 5

    class MeasurementInputVoltageRange(IntEnum):
        """Enumerates the possible voltage ranges for a measurement input."""

        RANGE_2_MICRO_VOLTS = 1
        RANGE_6_POINT_32_MICRO_VOLTS = 2
        RANGE_20_MICRO_VOLTS = 3
        RANGE_63_POINT_2_MICRO_VOLTS = 4
        RANGE_200_MICRO_VOLTS = 5
        RANGE_632_MICRO_VOLTS = 6
        RANGE_2_MILLI_VOLTS = 7
        RANGE_6_POINT_32_MILLI_VOLTS = 8
        RANGE_20_MILLI_VOLTS = 9
        RANGE_63_POINT_2_MILLI_VOLTS = 10
        RANGE_200_MILLI_VOLTS = 11
        RANGE_632_MILLI_VOLTS = 12

    class MeasurementInputCurrentRange(IntEnum):
        """Enumeration of the current range of a measurement input."""

        RANGE_1_PICO_AMP = 1
        RANGE_3_POINT_16_PICO_AMPS = 2
        RANGE_10_PICO_AMPS = 3
        RANGE_31_POINT_6_PICO_AMPS = 4
        RANGE_100_PICO_AMPS = 5
        RANGE_316_PICO_AMPS = 6
        RANGE_1_NANO_AMP = 7
        RANGE_3_POINT_16_NANO_AMPS = 8
        RANGE_10_NANO_AMPS = 9
        RANGE_31_POINT_6_NANO_AMPS = 10
        RANGE_100_NANO_AMPS = 11
        RANGE_316_NANO_AMPS = 12
        RANGE_1_MICRO_AMP = 13
        RANGE_3_POINT_16_MICRO_AMPS = 14
        RANGE_10_MICRO_AMPS = 15
        RANGE_31_POINT_6_MICRO_AMPS = 16
        RANGE_100_MICRO_AMPS = 17
        RANGE_316_MICRO_AMPS = 18
        RANGE_1_MILLI_AMP = 19
        RANGE_3_POINT_16_MILLI_AMPS = 20
        RANGE_10_MILLI_AMPS = 21
        RANGE_31_POINT_6_MILLI_AMPS = 22

    class ControlInputCurrentRange(IntEnum):
        """Enumeration of the current range of the control input. """

        RANGE_316_PICO_AMPS = 1
        RANGE_1_NANO_AMP = 2
        RANGE_3_POINT_16_NANO_AMPS = 3
        RANGE_10_NANO_AMPS = 4
        RANGE_31_POINT_6_NANO_AMPS = 5
        RANGE_100_NANO_AMPS = 6

    class MeasurementInputResistance(IntEnum):
        """Enumeration of the resistance range of a measurement input."""

        RANGE_2_MILLI_OHMS = 1
        RANGE_6_POINT_32_MILLI_OHMS = 2
        RANGE_20_MILLI_OHMS = 3
        RANGE_63_POINT_2_MILLI_OHMS = 4
        RANGE_200_MILLI_OHMS = 5
        RANGE_632_MILLI_OHMS = 6
        RANGE_2_OHMS = 7
        RANGE_6_POINT_32_OHMS = 8
        RANGE_20_OHMS = 9
        RANGE_63_POINT_2_OHMS = 10
        RANGE_200_OHMS = 11
        RANGE_632_OHMS = 12
        RANGE_2_KIL_OHMS = 13
        RANGE_6_POINT_32_KIL_OHMS = 14
        RANGE_20_KIL_OHMS = 15
        RANGE_63_POINT_2_KIL_OHMS = 16
        RANGE_200_KIL_OHMS = 17
        RANGE_632_KIL_OHMS = 18
        RANGE_2_MEGA_OHMS = 19
        RANGE_6_POINT_32_MEGA_OHMS = 20
        RANGE_20_MEGA_OHMS = 21
        RANGE_63_POINT_2_MEGA_OHMS = 22

    class HeaterOutput(IntEnum):
        """Enumeration of  heater output."""

        WARM_UP_HEATER = 1
        STILL_HEATER = 2
