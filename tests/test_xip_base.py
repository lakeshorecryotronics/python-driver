import unittest
from collections import deque
# Teslameter is used for these general tests on the HIL rig at this time
from lakeshore import Teslameter, XIPInstrumentException, InstrumentException
from tests.utils import TestWithFakeTeslameter, FakeDutConnection


class ValidFakeUserConnection:
    def __init__(self):
        self.responses = deque()
        self.responses.append('No error')
        self.responses.append('LSCI,F71,FakeSerial,999.999.999')

    def write(self, command):
        return

    def query(self, query):
        return self.responses.pop()

    def clear(self):
        return


class InvalidFakeUserConnection:

    def send(self, command):
        return


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


class TestMultipleConnections(unittest.TestCase):
    def test_two_connections(self):
        with self.assertRaisesRegex(ValueError, "Too many connections. Cannot have IP and serial connection at the same time."):
            Teslameter(ip_address="192.0.2.0", com_port='COM4')

    def test_three_connections(self):
        self.fake_connection = FakeDutConnection()
        with self.assertRaisesRegex(ValueError, "Too many connections. Cannot have IP and serial connection at the same time."):
            Teslameter(ip_address="192.0.2.0", com_port='COM4', connection=self.fake_connection)


class TestUserConnections(unittest.TestCase):
    def test_valid_connection(self):
        provided_connection = ValidFakeUserConnection()
        Teslameter(connection=provided_connection)

    def test_invalid_connection(self):
        provided_connection = InvalidFakeUserConnection()
        with self.assertRaisesRegex(
                ValueError,
                "Invalid connection. Connection must have callable write, query, and clear methods."):
            Teslameter(connection=provided_connection)


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
