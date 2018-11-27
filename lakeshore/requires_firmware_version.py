"""Decorator for ensuring an error is raised if the instrument firmware does not support the called function."""

import functools
from distutils.version import LooseVersion

from lakeshore.xip_instrument import XIPInstrumentConnectionException


def requires_firmware_version(required_version):
    """Decorator for raises an error when the instrument firmware
    is not up to date with the function's required version."""

    def decorator_version_check(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Raise an error if the instrument version is earlier than the required version.
            if LooseVersion(required_version) > LooseVersion(self.firmware_version):
                raise XIPInstrumentConnectionException(func.__name__ + ' requires instrument firmware version ' +
                                                       str(required_version) +
                                                       ' or later. Please update your instrument.')

            value = func(self, *args, **kwargs)

            return value

        return wrapper

    return decorator_version_check
