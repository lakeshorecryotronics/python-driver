import unittest2 as unittest  # Python 2 compatability
from lakeshore.requires_firmware_version import requires_firmware_version
from lakeshore import XIPInstrumentException


class TestRequiresFirmwareVersion(unittest.TestCase):
    def test_version_lesser(self):
        class FakeInstrument:
            def __init__(self):
                self.firmware_version = '1.2.1'

            @requires_firmware_version('1.2.3')
            def fake_method(self):
                pass

        dut = FakeInstrument()

        with self.assertRaises(XIPInstrumentException):
            dut.fake_method()

    def test_version_equal(self):
        class FakeInstrument:
            def __init__(self):
                self.firmware_version = '1.2.3'

            @requires_firmware_version('1.2.3')
            def fake_method(self):
                pass

        dut = FakeInstrument()

        try:
            dut.fake_method()
        except XIPInstrumentException:
            self.fail('Exception raised unexpectedly.')

    def test_version_greater(self):
        class FakeInstrument:
            def __init__(self):
                self.firmware_version = '1.3.0'

            @requires_firmware_version('1.2.3')
            def fake_method(self):
                pass

        dut = FakeInstrument()

        try:
            dut.fake_method()
        except XIPInstrumentException:
            self.fail('Exception raised unexpectedly.')
