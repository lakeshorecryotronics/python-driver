from lakeshore.xip_instrument import XIPInstrumentConnectionException
from distutils.version import LooseVersion


def requires_firmware_version(required_version):
    """Decorator for raising an error when the instrument firmware
    is not up to date with the function's required version."""

    def decorator_version_check(func):
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
