"""Implements the BaseModule class used with the Measure and Source Modules of the M81."""

from lakeshore.xip_instrument import RegisterBase


class SSMSystemModuleQuestionableRegister(RegisterBase):
    """Class object representing the questionable status register of a module."""

    bit_names = [
        "read_error",
        "unrecognized_pod_error",
        "port_direction_error",
        "factory_calibration_failure",
        "self_calibration_failure"
    ]

    def __init__(
            self,
            read_error=False,
            unrecognized_pod_error=False,
            port_direction_error=False,
            factory_calibration_failure=False,
            self_calibration_failure=False):
        self.read_error = read_error
        self.unrecognized_pod_error = unrecognized_pod_error
        self.port_direction_error = port_direction_error
        self.factory_calibration_failure = factory_calibration_failure
        self.self_calibration_failure = self_calibration_failure


class BaseModule:
    """Class for interaction with a specific channel, not specific to source or measure."""

    def __init__(self, module_number, device):
        self.module_number = module_number
        self.device = device
        self.questionable_register = SSMSystemModuleQuestionableRegister
        self.firmware_version = self.device.firmware_version
