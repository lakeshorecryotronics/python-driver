"""Contains enumerations specific to the M81."""

from enum import Enum


class SSMSystemEnums:
    """Class for collecting the enumerations specific to the SSMSystem without bulking up that class size."""

    class DataSourceMnemonic(str, Enum):
        """Enumeration of M81 data source mnemonics."""
        RELATIVE_TIME = 'RTIMe'
        SOURCE_AMPLITUDE = 'SAMPlitude'
        SOURCE_OFFSET = 'SOFFset'
        SOURCE_FREQUENCY = 'SFRequency'
        SOURCE_RANGE = 'SRANge'
        SOURCE_VOLTAGE_LIMIT = 'SVLimit'
        SOURCE_CURRENT_LIMIT = 'SILimit'
        SOURCE_IS_SWEEPING = 'SSWeeping'
        MEASURE_DC = 'MDC'
        MEASURE_RMS = 'MRMS'
        MEASURE_POSITIVE_PEAK = 'MPPeak'
        MEASURE_NEGATIVE_PEAK = 'MNPeak'
        MEASURE_PEAK_TO_PEAK = 'MPTPeak'
        MEASURE_X = 'MX'
        MEASURE_Y = 'MY'
        MEASURE_R = 'MR'
        MEASURE_THETA = 'MTHeta'
        MEASURE_RANGE = 'MRANge'
        MEASURE_OVERLOAD = 'MOVerload'
        MEASURE_SETTLING = 'MSETtling'
        MEASURE_UNLOCK = 'MUNLock'
        MEASURE_REFERENCE_FREQUENCY = 'MRFRequency'
        GENERAL_PURPOSE_INPUT_STATES = 'GPIStates'
        GENERAL_PURPOSE_OUTPUT_STATES = 'GPOStates'

        # Gets around having to use .value to access the string
        def __str__(self):
            return str.__str__(self)

    class ReadDataSourceMnemonic(str, Enum):
        """Enumeration of M81 read data source mnemonics."""
        MEASURE_DC = 'MDC'
        MEASURE_RMS = 'MRMs'
        MEASURE_POSITIVE_PEAK = 'MPPeak'
        MEASURE_NEGATIVE_PEAK = 'MNPeak'
        MEASURE_PEAK_TO_PEAK = 'MPTPeak'
        MEASURE_RANGE = 'MRANge'

        # Gets around having to use .value to access the string
        def __str__(self):
            return str.__str__(self)

    class ExcitationType(str, Enum):
        """Class object representing the possible excitation types of a source module."""
        CURRENT = 'CURRENT'
        VOLTAGE = 'VOLTAGE'

        # Gets around having to use .value to access the string
        def __str__(self):
            return str.__str__(self)

    class SourceSweepType(str, Enum):
        """Class representing the available sweep types for a source module."""
        CURRENT_AMPLITUDE = 'CURRent'
        VOLTAGE_AMPLITUDE = 'VOLTage'
        FREQUENCY = 'FREQuency'
        OFFSET = 'OFFSet'

        # Gets around having to use .value to access the string
        def __str__(self):
            return str.__str__(self)

    class SourceSweepSettings:
        """Class to configure a parameter sweep on a source module."""

        class SweepSpacing(str, Enum):
            """Class object representing the possible types of sweep spacing."""
            LINEAR = 'LINEAR'
            LOGARITHMIC = 'LOGARITHMIC'

            # Gets around having to use .value to access the string
            def __str__(self):
                return str.__str__(self)

        class Direction(str, Enum):
            """Class object representing the possible directions for sweeping."""
            DOWN = 'DOWN'
            UP = 'UP'

            # Gets around having to use .value to access the string
            def __str__(self):
                return str.__str__(self)

        def __init__(self, sweep_type, start, stop, points, dwell,
                     direction=Direction.UP, round_trip=False, spacing=SweepSpacing.LINEAR):
            """Constructor for SourceModuleSweepSettings class.

            Args:
                sweep_type (SourceSweepType):
                    The type of sweep to perform.
                start (float):
                    Sets the start value of the source sweep.
                stop (float):
                    Sets the stop value of the source sweep.
                points (int):
                    Sets the number of steps in the source sweep.
                dwell (float):
                    Sets the time spent at each step in the source sweep in seconds.
                    Must be a multiple of 200 microseconds (0.0002).
                direction (Direction):
                    The direction of the sweep.
                    UP begins the sweep at the start and ends at the stop value.
                    DOWN begins the sweep at the stop value and ends at the start value.
                round_trip (bool):
                    The round trip state of the sweep.
                    When True, the sweep will begin and end at the same value.
                spacing (SweepSpacing):
                    The spacing of the sweep.
            """

            self.sweep_type = sweep_type
            self.spacing = spacing
            self.start = start
            self.stop = stop
            self.points = points
            self.dwell = dwell
            self.direction = direction
            self.round_trip = round_trip

    class ReferenceModule(str, Enum):
        """Class object representing the available source modules
        """
        S1 = 'S1'
        S2 = 'S2'
        S3 = 'S3'

        # Gets around having to use .value to access the string
        def __str__(self) -> str:
            return str.__str__(self)

    class ResistanceExcitationType(str, Enum):
        """Class object representing the possible excitation types that create a valid resistance configuration."""
        AC = 'AC'
        DC = 'DC'
        INVALID = 'INVAlid'

        # Gets around having to use .value to access the string
        def __str__(self) -> str:
            return str.__str__(self)

    class ResistanceMode(str, Enum):
        """Class object representing the possible resistance modes."""
        NOISE = 'NOISe'
        POWER = 'POWer'

        # Gets around having to use .value to access the string
        def __str__(self) -> str:
            return str.__str__(self)
