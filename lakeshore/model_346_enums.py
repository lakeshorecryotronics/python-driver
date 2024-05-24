"""Implements a class containing the enums relevant to the Model 346."""
from enum import IntEnum


class Model346Enums:
    """Class containing the enums relevant to the Model 346."""

    class AlarmType(IntEnum):
        """Enumeration for possible alarm output types"""
        NONE = 0
        RELAY = 1
        FRONT_DISPLAY = 2
        FRONT_AUDIO = 3
