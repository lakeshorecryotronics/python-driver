import unittest

# Teslameter is used for these general tests on the HIL rig at this time
from lakeshore import Teslameter, XIPInstrumentException, InstrumentException
from tests.utils import TestWithFakeTeslameter


class TestDiscovery(unittest.TestCase):
    def test_specified_serial_does_not_exist(self):
        with self.assertRaisesRegex(InstrumentException,
                                    r'No serial connections found with a matching COM port '
                                    r'and/or matching serial number'):
            Teslameter(serial_number='Fake')

    def test_specified_com_port_does_not_exist(self):
        with self.assertRaisesRegex(InstrumentException,
                                    r'No serial connections found with a matching COM port '
                                    r'and/or matching serial number'):
            Teslameter(com_port='COM99')


class TestCommands(TestWithFakeTeslameter):
    def test_basic_command(self):
        self.fake_connection.setup_response('No error')
        self.dut.command('*RST')
        self.assertEqual(self.fake_connection.get_outgoing_message(), '*RST;:SYSTem:ERRor:ALL?')

    def test_chained_commands(self):
        self.fake_connection.setup_response('No error')
        self.dut.command('*RST', '*RST')
        self.assertEqual(self.fake_connection.get_outgoing_message(), '*RST;:*RST;:SYSTem:ERRor:ALL?')


class TestQueries(TestWithFakeTeslameter):
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


class TestErrorChecking(TestWithFakeTeslameter):
    def test_error_is_raised_for_nonexistent_command(self):
        self.fake_connection.setup_response('-113,"Undefined header;FAKEQUERY?;"')
        with self.assertRaisesRegex(XIPInstrumentException, r'Undefined header;FAKEQUERY\?;'):
            self.dut.query('FAKEQUERY?')

    def test_query_no_error_check(self):
        self.fake_connection.setup_response('LSCI,F41,#######,1.2.3')
        response = self.dut.query('*IDN?', check_errors=False)
        self.assertEqual(response, 'LSCI,F41,#######,1.2.3')
        self.assertEqual(self.fake_connection.get_outgoing_message(), '*IDN?')

    def test_command_no_error_check(self):
        self.dut.command('*RST', check_errors=False)
        self.assertEqual(self.fake_connection.get_outgoing_message(), '*RST')
