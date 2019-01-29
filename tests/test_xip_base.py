import unittest2 as unittest  # Python 2 compatability

# Teslameter is used for these general tests on the HIL rig at this time
from lakeshore import Teslameter, XIPInstrumentException
from tests.utils import TestWithRealDUT, TestWithFakeDUT


class TestDiscovery(unittest.TestCase):
    def test_normal_connection(self):
        Teslameter()  # No checks needed, just make sure no exceptions are thrown

    def test_specified_serial_does_not_exist(self):
        with self.assertRaisesRegexp(XIPInstrumentException,
                                     "No serial connections found with a matching COM port " +
                                     "and/or matching serial number"):
            Teslameter(serial_number='Fake', )

    def test_specified_com_port_does_not_exist(self):
        with self.assertRaisesRegexp(XIPInstrumentException,
                                     "No serial connections found with a matching COM port " +
                                     "and/or matching serial number"):
            Teslameter(com_port='COM99', )

    def test_tcp_connection(self):
        # No checks needed, just make sure no exceptions are thrown
        Teslameter(ip_address='192.168.0.12', tcp_port=7777)


class TestBasicComms(TestWithRealDUT):
    def test_basic_query(self):
        # Primarily tested on fake, just a spot check on real DUT
        response = self.dut.query('*IDN?')

        self.assertEqual(response.split(',')[0], 'Lake Shore')

    def test_timeout(self):
        with self.assertRaisesRegexp(XIPInstrumentException, 'Communication timed out'):
            self.dut.query('FAKEQUERY?', check_errors=False)


class TestCommands(TestWithFakeDUT):
    def test_basic_command(self):
        self.fake_connection.setup_response('No error')
        self.dut.command('*RST')
        self.assertEqual(self.fake_connection.get_outgoing_message(), '*RST;:SYSTem:ERRor:ALL?')

    def test_chained_commands(self):
        self.fake_connection.setup_response('No error')
        self.dut.command('*RST', '*RST')
        self.assertEqual(self.fake_connection.get_outgoing_message(), '*RST;:*RST;:SYSTem:ERRor:ALL?')


class TestQueries(TestWithFakeDUT):
    def test_basic_query(self):
        self.fake_connection.setup_response('LSCI,F41,#######,1.2.3;No error')
        response = self.dut.query('*IDN?')
        self.assertEqual(response, 'LSCI,F41,#######,1.2.3')
        self.assertEqual(self.fake_connection.get_outgoing_message(), '*IDN?;:SYSTem:ERRor:ALL?')

    def test_chained_queries(self):
        self.fake_connection.setup_response('LSCI,F41,#######,1.2.3;GAUSS;No error')
        response = self.dut.query('*IDN?', 'UNIT?')
        self.assertEqual(response, 'LSCI,F41,#######,1.2.3;GAUSS')
        self.assertEqual(self.fake_connection.get_outgoing_message(), '*IDN?;:UNIT?;:SYSTem:ERRor:ALL?')


class TestErrorChecking(TestWithFakeDUT):
    def test_error_is_raised_for_nonexistent_command(self):
        self.fake_connection.setup_response('-113,"Undefined header;FAKEQUERY?;"')
        with self.assertRaisesRegexp(XIPInstrumentException, 'Undefined header;FAKEQUERY\?;'):
            self.dut.query('FAKEQUERY?')

    def test_query_no_error_check(self):
        self.fake_connection.setup_response('LSCI,F41,#######,1.2.3')
        response = self.dut.query('*IDN?', check_errors=False)
        self.assertEqual(response, 'LSCI,F41,#######,1.2.3')
        self.assertEqual(self.fake_connection.get_outgoing_message(), '*IDN?')

    def test_command_no_error_check(self):
        self.dut.command('*RST', check_errors=False)
        self.assertEqual(self.fake_connection.get_outgoing_message(), '*RST')
