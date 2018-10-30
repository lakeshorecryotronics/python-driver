import unittest

# Teslameter is used for these general tests on the HIL rig at this time
from lakeshore import Teslameter, XIPInstrumentConnectionException


class TestWithDUT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dut = Teslameter(flow_control=False)  # TODO: Get a dut with flow control for the HIL rig then remove this.

    @classmethod
    def tearDownClass(cls):
        del cls.dut


class TestDiscovery(unittest.TestCase):
    def test_normal_connection(self):
        Teslameter(flow_control=False)  # No checks needed, just make sure no exceptions are thrown

    def test_specified_serial_does_not_exist(self):
        with self.assertRaisesRegexp(XIPInstrumentConnectionException,
                                     "No serial connections found with a matching COM port " +
                                     "and/or matching serial number"):
            Teslameter(serial_number='Fake', flow_control=False)

    def test_specified_com_port_does_not_exist(self):
        with self.assertRaisesRegexp(XIPInstrumentConnectionException,
                                     "No serial connections found with a matching COM port " +
                                     "and/or matching serial number"):
            Teslameter(com_port='COM99', flow_control=False)

    @unittest.skip('Need a dedicated ethernet port for the Teslameter on the HIL rig')
    def test_tcp_connection(self):
        Teslameter('static_ip')  # TODO: Replace with actual IP address


class TestConnectivity(TestWithDUT):
    def test_basic_query(self):
        response = self.dut.query('*IDN?')

        self.assertEqual(response.split(',')[0], 'Lake Shore')

    def test_timeout(self):
        with self.assertRaisesRegexp(XIPInstrumentConnectionException, 'Communication timed out'):
            self.dut.query('FAKEQUERY?', check_errors=False)
        self.dut.query('SYSTEM:ERROR:ALL?', check_errors=False)  # Discard the error we left in the queue


class TestSCPIErrorQueueChecking(TestWithDUT):
    def test_command_does_not_exist(self):
        with self.assertRaisesRegexp(XIPInstrumentConnectionException, 'Undefined header;FAKEQUERY\?;'):
            self.dut.query('FAKEQUERY?')

    def test_query_with_error_check_disabled(self):
        response = self.dut.query('*IDN?', check_errors=False)
        self.assertEqual(response.split(',')[0], 'Lake Shore')


class TestTeslameter(TestWithDUT):
    def test_getting_buffered_data(self):
        self.assertEqual(len(self.dut.get_buffered_data_points(1, 10)), 100)
