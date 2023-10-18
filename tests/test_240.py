from tests.utils import TestWithFakeModel240
from lakeshore import Model240, Model240ProfiSlot, Model240InputParameter


class TestBasicTempReadings(TestWithFakeModel240):

    def test_get_kelvin_reading(self):
        self.fake_connection.setup_response('123.45')
        response = self.dut.get_kelvin_reading("1")
        self.assertAlmostEqual(response, 123.45)
        self.assertIn("KRDG? 1", self.fake_connection.get_outgoing_message())

    def test_get_celsius_reading(self):
        self.fake_connection.setup_response('123')
        response = self.dut.get_celsius_reading("1")
        self.assertEqual(response, '123')
        self.assertIn("CRDG? 1", self.fake_connection.get_outgoing_message())

    def test_get_fahrenheit_reading(self):
        self.fake_connection.setup_response('123')
        response = self.dut.get_fahrenheit_reading("1")
        self.assertEqual(response, '123')
        self.assertIn("FRDG? 1", self.fake_connection.get_outgoing_message())


class TestBasicQueryMethods(TestWithFakeModel240):

    def test_get_modname(self):
        self.fake_connection.setup_response('MyModname')
        response = self.dut.get_modname()
        self.assertEqual(response, 'MyModname')
        self.assertIn("MODNAME?", self.fake_connection.get_outgoing_message())

    def test_get_profibus_slot_count(self):
        self.fake_connection.setup_response('1')
        response = self.dut.get_profibus_slot_count()
        self.assertEqual(response, "1")
        self.assertIn("PROFINUM?", self.fake_connection.get_outgoing_message())

    def test_get_profibus_address(self):
        self.fake_connection.setup_response('12345')
        response = self.dut.get_profibus_address()
        self.assertEqual(response, 12345)
        self.assertIn("ADDR?", self.fake_connection.get_outgoing_message())

    def test_get_profibus_slot_configuration(self):
        slot_configuration = Model240ProfiSlot(1, Model240.Units.CELSIUS)
        self.fake_connection.setup_response('1,2')
        response = self.dut.get_profibus_slot_configuration(1)

        self.assertEqual(response.slot_channel, slot_configuration.slot_channel)
        self.assertEqual(response.slot_units, Model240.Units.CELSIUS)

        self.assertIn("PROFISLOT? 1", self.fake_connection.get_outgoing_message())

    def test_get_profibus_connection_status(self):
        self.fake_connection.setup_response('1: Waiting on parameterization.')
        response = self.dut.get_profibus_connection_status()
        self.assertEqual(response, '1: Waiting on parameterization.')
        self.assertIn("PROFISTAT?", self.fake_connection.get_outgoing_message())

    def test_get_sensor_name(self):
        self.fake_connection.setup_response('MySensor')
        response = self.dut.get_sensor_name(1)
        self.assertEqual(response, 'MySensor')
        self.assertIn("INNAME?", self.fake_connection.get_outgoing_message())

    def test_get_filter(self):
        self.fake_connection.setup_response('100')
        response = self.dut.get_filter("1")
        self.assertEqual(response, '100')
        self.assertIn("FILTER? 1", self.fake_connection.get_outgoing_message())

    def test_get_sensor_units_channel_reading(self):
        self.fake_connection.setup_response('12345')
        response = self.dut.get_sensor_units_channel_reading("1")
        self.assertEqual(response, '12345')
        self.assertIn("SRDG? 1", self.fake_connection.get_outgoing_message())

    def test_get_channel_reading_status(self):
        self.fake_connection.setup_response('12345')

    def test_get_input_parameter(self):
        self.fake_connection.setup_response('2,1,2,1,2,1')
        response = self.dut.get_input_parameter(1)

        self.assertEqual(response.sensor_type, Model240.SensorTypes.PLATINUM_RTD)
        self.assertEqual(response.auto_range_enable, True)
        self.assertEqual(response.input_range, Model240.InputRange.RANGE_NTCRTD_100_OHMS)
        self.assertEqual(response.current_reversal_enable, True)
        self.assertEqual(response.temperature_unit, Model240.Units.CELSIUS)
        self.assertEqual(response.input_enable, True)

        self.assertIn("INTYPE? 1", self.fake_connection.get_outgoing_message())


class TestBasicCommandMethods(TestWithFakeModel240):

    def test_set_sensor_name(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_sensor_name(1, "MySensor")
        self.assertIn('INNAME 1,MySensor', self.fake_connection.get_outgoing_message())

    def test_set_modname(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_modname("MyModule")
        self.assertIn('MODNAME MyModule', self.fake_connection.get_outgoing_message())

    def test_set_filter(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_filter(2, 50)
        self.assertIn('FILTER 2,50', self.fake_connection.get_outgoing_message())

    def test_set_curve_data_point(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_curve_data_point(2, 50, 1.2, 3.4)
        self.assertIn('CRVPT 2,50,1.2,3.4', self.fake_connection.get_outgoing_message())

    def test_set_profibus_slot_configuration(self):
        slot_configuration = Model240ProfiSlot(2, 2)
        self.dut.set_profibus_slot_configuration("1", slot_configuration)
        self.assertIn("PROFISLOT 1,2,2", self.fake_connection.get_outgoing_message())

    def test_set_profibus_address(self):
        self.fake_connection.setup_response('0')
        self.dut.set_profibus_address(50)
        self.assertIn('ADDR 50', self.fake_connection.get_outgoing_message())

    def test_set_profibus_slot_count(self):
        self.fake_connection.setup_response('0')
        self.dut.set_profibus_slot_count(5)
        self.assertIn('PROFINUM 5', self.fake_connection.get_outgoing_message())

    def test_set_input_parameter(self):
        in_parameter = Model240InputParameter(Model240.SensorTypes.NTC_RTD,
                                                        False,
                                                        True,
                                                        Model240.Units.CELSIUS,
                                                        True,
                                                        Model240.InputRange.RANGE_NTCRTD_100_OHMS)
        self.dut.set_input_parameter(2, in_parameter)
        self.assertIn('INTYPE 2,3,0,2,1,2,1', self.fake_connection.get_outgoing_message())

    def test_set_factory_defaults(self):
        self.fake_connection.setup_response('0')
        self.dut.set_factory_defaults()
        self.assertIn('DFLT 99', self.fake_connection.get_outgoing_message())
