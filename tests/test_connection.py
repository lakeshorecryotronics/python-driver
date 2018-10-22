import unittest

# Teslameter is used for these general tests on the HIL rig at this time
from lakeshore import Teslameter, XIPInstrumentConnectionException


class TestDiscovery(unittest.TestCase):
    def test_normal_connection(self):
        Teslameter(flow_control=False)  # No checks needed, just make sure no exceptions are thrown

    def test_target_does_not_exist(self):
        with self.assertRaises(XIPInstrumentConnectionException):
            Teslameter(serial_number='Fake', flow_control=False)


class TestConnectivity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dut = Teslameter(flow_control=False)  # TODO: Get a dut with flow control for the HIL rig then remove this.

    def test_basic_query(self):
        response = self.dut.query('*IDN?')

        self.assertEqual(response.split(',')[0], 'Lake Shore')

    def test_timeout(self):
        with self.assertRaises(XIPInstrumentConnectionException):
            self.dut.query('FAKEQUERY?')
