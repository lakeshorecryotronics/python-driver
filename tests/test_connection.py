import unittest

# Teslameter is used for these general tests on the HIL rig at this time
from lakeshore import Teslameter, XIPInstrumentException


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
        with self.assertRaisesRegexp(XIPInstrumentException,
                                     "No serial connections found with a matching COM port " +
                                     "and/or matching serial number"):
            Teslameter(serial_number='Fake', flow_control=False)

    def test_specified_com_port_does_not_exist(self):
        with self.assertRaisesRegexp(XIPInstrumentException,
                                     "No serial connections found with a matching COM port " +
                                     "and/or matching serial number"):
            Teslameter(com_port='COM99', flow_control=False)

    def test_tcp_connection(self):
        Teslameter(ip_address='192.168.0.12')


class TestConnectivity(TestWithDUT):
    def test_basic_query(self):
        response = self.dut.query('*IDN?')

        self.assertEqual(response.split(',')[0], 'Lake Shore')

    def test_multiple_queries(self):
        response = self.dut.query('*IDN?', 'SENSe:RELative:BASEline?', 'UNIT?', check_errors=False)

        self.assertEqual(len(response.split(';')), 3)

    def test_timeout(self):
        with self.assertRaisesRegexp(XIPInstrumentException, 'Communication timed out'):
            self.dut.query('FAKEQUERY?', check_errors=False)
        self.dut.query('SYSTEM:ERROR:ALL?', check_errors=False)  # Discard the error we left in the queue


class TestSCPIErrorQueueChecking(TestWithDUT):
    def test_command_does_not_exist(self):
        with self.assertRaisesRegexp(XIPInstrumentException, 'Undefined header;FAKEQUERY\?;'):
            self.dut.query('FAKEQUERY?')

    def test_query_with_error_check_disabled(self):
        response = self.dut.query('*IDN?', check_errors=False)
        self.assertEqual(response.split(',')[0], 'Lake Shore')


class TestTeslameter(TestWithDUT):
    def test_getting_buffered_data(self):
        self.assertEqual(len(self.dut.get_buffered_data_points(1, 10)), 100)


class TestStatusRegisters(TestWithDUT):
    def test_modification_of_register(self):
        self.dut.modify_operation_register_mask('ranging', False)
        response = self.dut.get_operation_event_enable_mask()

        self.assertEqual(response.ranging, False)


class TestTeslameterBasics(TestWithDUT):
    def TestMeasurementConfiguration(self):
        self.dut.configure_field_measurement_setup(mode="AC")

    def test_fetch_queries(self):
        self.dut.get_dc_field()
        self.dut.get_dc_field_xyz()
        self.dut.get_max_min()
        self.dut.get_frequency()
        self.dut.get_rms_field()
        self.dut.get_rms_field_xyz()
        self.dut.get_temperature()

    def test_relative_field(self):
        self.dut.get_relative_field()
        self.dut.tare_relative_field()
        self.dut.get_relative_field_baseline()
        self.dut.set_relative_field_baseline(12.3)

    def test_probe_data(self):
        self.dut.get_probe_information()

    def test_temperature_compensation(self):
        self.dut.configure_temperature_compensation(manual_temperature=23.45)
        self.dut.get_temperature_compensation_manual_temp()
        self.dut.get_temperature_compensation_source()

    def test_field_control(self):
        self.dut.configure_field_control_limits()
        self.dut.get_field_control_limits()
        self.dut.configure_field_control_output_mode(mode="OPEN", output_enabled=False)
        self.dut.get_field_control_output_mode()
        self.dut.configure_field_control_pid(gain=1, integral=0.1, ramp_rate=10)
        self.dut.get_field_control_pid()
        self.dut.set_field_control_setpoint(1)
        self.dut.get_field_control_setpoint()
        self.dut.set_field_control_open_loop_voltage(1)
        self.dut.get_field_control_open_loop_voltage()

    def test_analog_out(self):
        self.dut.set_analog_output("X")
        self.dut.get_analog_output()
