"""Decorator for ensuring an error is raised if the instrument firmware does not support the called function."""

import functools
from packaging.version import Version

from lakeshore.xip_instrument import XIPInstrumentException


def requires_firmware_version(required_version):
    """Decorator for raising an error when the instrument firmware is not up-to-date with required version."""

    def decorator_version_check(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Raise an error if the instrument version is earlier than the required version.
            if Version(required_version) > Version(self.firmware_version.split('-')[0]):
                raise XIPInstrumentException(func.__name__ + ' requires instrument firmware version ' +
                                             str(required_version) +
                                             ' or later (' +
                                             str(self.firmware_version.split('-')[0]) +
                                             ' < ' +
                                             str(required_version) +
                                             '). Please update your instrument.')

            value = func(self, *args, **kwargs)

            return value

        return wrapper

    return decorator_version_check
