from tests.utils import TestWithFakeModel372
from lakeshore.model_372 import *


class TestBasicReadings(TestWithFakeModel372):

    def test_get_resistance_reading(self):
        self.fake_connection.setup_response('1234.5;0')
        response = self.dut.get_resistance_reading(3)
        self.assertAlmostEqual(response, 1234.5)
        self.assertIn("RDGR? 3", self.fake_connection.get_outgoing_message())

    def test_get_quadrature_reading(self):
        self.fake_connection.setup_response('1234.5;0')
        response = self.dut.get_quadrature_reading(1)
        self.assertAlmostEqual(response, 1234.5)
        self.assertIn("QRDG? 1", self.fake_connection.get_outgoing_message())

    def test_get_excitation_power(self):
        self.fake_connection.setup_response('100;0')
        response = self.dut.get_excitation_power(3)
        self.assertAlmostEqual(response, 100.0)
        self.assertIn("RDGPWR? 3", self.fake_connection.get_outgoing_message())

    def test_get_analog_heater_output(self):
        self.fake_connection.setup_response('20.1;0')
        response = self.dut.get_analog_heater_output(1)
        self.assertAlmostEqual(response, 20.1)
        self.assertIn("AOUT? 1", self.fake_connection.get_outgoing_message())

    def test_get_still_output(self):
        self.fake_connection.setup_response('5.3;0')
        response = self.dut.get_still_output()
        self.assertAlmostEqual(response, 5.3)
        self.assertIn("STILL?", self.fake_connection.get_outgoing_message())

    def test_get_setpoint_kelvin(self):
        self.fake_connection.setup_response("4,0,1,1,0,120;0")
        self.fake_connection.setup_response("1,10,0,5,0,1;0")
        self.fake_connection.setup_response("0")
        self.fake_connection.setup_response("4.32;0")
        self.dut.get_setpoint_kelvin(1)
        self.assertIn("OUTMODE? 1", self.fake_connection.get_outgoing_message())
        self.assertIn("INTYPE? 0", self.fake_connection.get_outgoing_message())
        self.assertIn("INTYPE 0,1,10,0,5,0,1", self.fake_connection.get_outgoing_message())
        self.assertIn("SETP? 1", self.fake_connection.get_outgoing_message())

    def test_get_setpoint_ohms(self):
        self.fake_connection.setup_response("4,0,1,1,0,120;0")
        self.fake_connection.setup_response("1,10,0,5,0,1;0")
        self.fake_connection.setup_response("0")
        self.fake_connection.setup_response("4.32;0")
        self.dut.get_setpoint_ohms(1)
        self.assertIn("OUTMODE? 1", self.fake_connection.get_outgoing_message())
        self.assertIn("INTYPE? 0", self.fake_connection.get_outgoing_message())
        self.assertIn("INTYPE 0,1,10,0,5,0,2", self.fake_connection.get_outgoing_message())
        self.assertIn("SETP? 1", self.fake_connection.get_outgoing_message())

    def test_get_manual_value(self):
        self.fake_connection.setup_response("1,1,2,131,5.5,3.2,50;0")
        response = self.dut.get_analog_manual_value(1)
        self.assertEqual(response, 50)
        self.assertIn("ANALOG? 1", self.fake_connection.get_outgoing_message())


class TestGetBasicSettings(TestWithFakeModel372):

    def test_get_excitation_frequency(self):
        self.fake_connection.setup_response('1;0')
        response = self.dut.get_excitation_frequency(0)
        self.assertAlmostEqual(response, Model372InputFrequency.FREQUENCY_9_POINT_8_HZ)
        self.assertIn("FREQ? 0", self.fake_connection.get_outgoing_message())

    def test_get_alarm_beep_status(self):
        self.fake_connection.setup_response('1;0')
        response = self.dut.get_alarm_beep_status()
        self.assertAlmostEqual(response, True)
        self.assertIn("BEEP?", self.fake_connection.get_outgoing_message())

    def test_get_common_mode_reduction(self):
        self.fake_connection.setup_response('1;0')
        response = self.dut.get_common_mode_reduction()
        self.assertAlmostEqual(response, True)
        self.assertIn("CMR?", self.fake_connection.get_outgoing_message())

    def test_get_filter(self):
        self.fake_connection.setup_response('0,16,80;0')
        response = self.dut.get_filter(2)
        filter_dict = {"state": False,
                       "settle_time": 16,
                       "window": 80}
        self.assertDictEqual(response, filter_dict)

    def test_get_digital_output(self):
        self.fake_connection.setup_response('24;0')
        response = self.dut.get_digital_output()
        register = Model372DigitalOutputRegister.from_integer(24)
        self.assertEqual(response.d_1, register.d_1)
        self.assertEqual(response.d_2, register.d_2)
        self.assertEqual(response.d_3, register.d_3)
        self.assertEqual(response.d_4, register.d_4)
        self.assertEqual(response.d_5, register.d_5)
        self.assertIn("DOUT?", self.fake_connection.get_outgoing_message())

    def test_get_display_mode(self):
        self.fake_connection.setup_response('0,1,2;0')
        response = self.dut.get_display_mode()
        self.assertEqual(response, Model372DisplayMode.MEASUREMENT_INPUT)
        self.assertIn("DISPLAY?", self.fake_connection.get_outgoing_message())


class TestBasicCommands(TestWithFakeModel372):

    def test_set_ieee_interface_parameter(self):
        self.fake_connection.setup_response('0')
        self.dut.set_ieee_interface_parameter(123)
        self.assertIn('IEEE 0,0,123', self.fake_connection.get_outgoing_message())

    def test_set_common_mode_reduction(self):
        self.fake_connection.setup_response('0')
        self.dut.set_common_mode_reduction(False)
        self.assertIn('CMR 0', self.fake_connection.get_outgoing_message())

    def test_set_alarm_beep(self):
        self.fake_connection.setup_response('0')
        self.dut.set_alarm_beep(True)
        self.assertIn('BEEP 1', self.fake_connection.get_outgoing_message())

    def test_set_excitation_frequency(self):
        self.fake_connection.setup_response('0')
        self.dut.set_excitation_frequency(0, Model372InputFrequency(5))
        self.assertIn('FREQ 0,5', self.fake_connection.get_outgoing_message())

    def test_set_relay_for_sample_heater_control_zone(self):
        self.fake_connection.setup_response('0')
        self.dut.set_relay_for_sample_heater_control_zone(1)
        self.assertIn("RELAY 1,3,0,0", self.fake_connection.get_outgoing_message())

    def test_set_relay_for_warmup_heater_control_zone(self):
        self.fake_connection.setup_response('0')
        self.dut.set_relay_for_warmup_heater_control_zone(2)
        self.assertIn("RELAY 2,4,0,0", self.fake_connection.get_outgoing_message())

    def test_set_filter(self):
        self.fake_connection.setup_response('0')
        self.dut.set_filter(3, True, 5, 50)
        self.assertIn("FILTER 3,1,5,50", self.fake_connection.get_outgoing_message())

    def test_set_warmup_output(self):
        self.fake_connection.setup_response("4,0,1,1,0,120;0")
        self.fake_connection.setup_response('0')
        self.fake_connection.setup_response('0')
        self.dut.set_warmup_output(True, 80)
        self.assertIn("OUTMODE? 1", self.fake_connection.get_outgoing_message())
        self.assertIn("OUTMODE 1,6,0,1,1,0,120", self.fake_connection.get_outgoing_message())
        self.assertIn("WARMUP 1,80", self.fake_connection.get_outgoing_message())

    def test_set_digital_output(self):
        self.fake_connection.setup_response('0')
        self.dut.set_digital_output(Model372DigitalOutputRegister(True, False, True, False, True))
        self.assertIn('DOUT 21', self.fake_connection.get_outgoing_message())

    def test_set_display_settings(self):
        self.fake_connection.setup_response('0')
        self.dut.set_display_settings(Model372DisplayMode.MEASUREMENT_INPUT, Model372DisplayFields.LARGE_4,
                                      Model372DisplayInfo.SAMPLE_HEATER)
        self.assertIn("DISPLAY 0,1,1", self.fake_connection.get_outgoing_message())

    def test_disable_input(self):
        self.fake_connection.setup_response('0')
        self.dut.disable_input(12)
        self.assertIn("INSET 12,0,0,0,0,0", self.fake_connection.get_outgoing_message())

    def test_all_off(self):
        self.fake_connection.setup_response('0')
        self.fake_connection.setup_response('0')
        self.fake_connection.setup_response('0')
        self.dut.all_off()
        self.assertIn("RANGE 0,0", self.fake_connection.get_outgoing_message())
        self.assertIn("RANGE 1,0", self.fake_connection.get_outgoing_message())
        self.assertIn("RANGE 2,0", self.fake_connection.get_outgoing_message())

    def test_set_still_output(self):
        self.fake_connection.setup_response("4,0,1,1,0,120;0")
        self.fake_connection.setup_response('0')
        self.fake_connection.setup_response('0')
        self.dut.set_still_output(80)
        self.assertIn("OUTMODE? 2", self.fake_connection.get_outgoing_message())
        self.assertIn("OUTMODE 2,4,0,1,1,0,120", self.fake_connection.get_outgoing_message())
        self.assertIn("STILL 80", self.fake_connection.get_outgoing_message())

    def test_set_setpoint_kelvin(self):
        self.fake_connection.setup_response("4,0,1,1,0,120;0")
        self.fake_connection.setup_response("1,10,0,5,0,1;0")
        self.fake_connection.setup_response("0")
        self.fake_connection.setup_response("0")
        self.dut.set_setpoint_kelvin(1, 4.32)
        self.assertIn("OUTMODE? 1", self.fake_connection.get_outgoing_message())
        self.assertIn("INTYPE? 0", self.fake_connection.get_outgoing_message())
        self.assertIn("INTYPE 0,1,10,0,5,0,1", self.fake_connection.get_outgoing_message())
        self.assertIn("SETP 1,4.32", self.fake_connection.get_outgoing_message())

    def test_set_setpoint_ohms(self):
        self.fake_connection.setup_response("4,0,1,1,0,120;0")
        self.fake_connection.setup_response("1,10,0,5,0,1;0")
        self.fake_connection.setup_response("0")
        self.fake_connection.setup_response("0")
        self.dut.set_setpoint_ohms(1, 4.32)
        self.assertIn("OUTMODE? 1", self.fake_connection.get_outgoing_message())
        self.assertIn("INTYPE? 0", self.fake_connection.get_outgoing_message())
        self.assertIn("INTYPE 0,1,10,0,5,0,2", self.fake_connection.get_outgoing_message())
        self.assertIn("SETP 1,4.32", self.fake_connection.get_outgoing_message())


class TestDictionaryReturnMethods(TestWithFakeModel372):

    def test_get_all_input_readings_control(self):
        readings = {"kelvin": 1.234,
                    "resistance": 4.56,
                    "power": 5.67}
        self.fake_connection.setup_response('1.234;0')
        self.fake_connection.setup_response('4.56;0')
        self.fake_connection.setup_response('5.67;0')
        response = self.dut.get_all_input_readings("A")
        self.assertDictEqual(response, readings)

    def test_get_all_input_readings_measurement(self):
        readings = {"kelvin": 1.234,
                    "resistance": 4.56,
                    "power": 5.67,
                    "quadrature": 9.87}
        self.fake_connection.setup_response('1.234;0')
        self.fake_connection.setup_response('4.56;0')
        self.fake_connection.setup_response('5.67;0')
        self.fake_connection.setup_response('9.87;0')
        response = self.dut.get_all_input_readings(3)
        self.assertDictEqual(response, readings)

    def test_set_scanner_status(self):
        self.fake_connection.setup_response('0')
        self.dut.set_scanner_status(3, False)
        self.assertIn('SCAN 3,0', self.fake_connection.get_outgoing_message())

    def test_get_scanner_status(self):
        scan = {'input_channel': 4,
                'status': True}
        self.fake_connection.setup_response('4,1;0')
        response = self.dut.get_scanner_status()
        self.assertDictEqual(response, scan)
        self.assertIn("SCAN?", self.fake_connection.get_outgoing_message())

    def test_set_website_login(self):
        self.fake_connection.setup_response('0')
        self.dut.set_website_login("user", "password")
        self.assertIn('WEBLOG "user","password"', self.fake_connection.get_outgoing_message())

    def test_get_website_login(self):
        login = {'username': 'user',
                 'password': 'password'}
        self.fake_connection.setup_response('user,password;0')
        response = self.dut.get_website_login()
        self.assertDictEqual(response, login)
        self.assertIn('WEBLOG?', self.fake_connection.get_outgoing_message())

    def test_get_heater_output_range_output_0(self):
        self.fake_connection.setup_response("3;0")
        response = self.dut.get_heater_output_range(0)
        self.assertAlmostEqual(response, Model372SampleHeaterOutputRange(3))
        self.assertIn("RANGE? 0", self.fake_connection.get_outgoing_message())

    def test_get_heater_output_range_output_1(self):
        self.fake_connection.setup_response("1;0")
        response = self.dut.get_heater_output_range(1)
        self.assertEqual(response, True)
        self.assertIn("RANGE? 1", self.fake_connection.get_outgoing_message())

    def test_get_heater_output_range_output_2(self):
        self.fake_connection.setup_response("0;0")
        response = self.dut.get_heater_output_range(2)
        self.assertEqual(response, False)
        self.assertIn("RANGE? 2", self.fake_connection.get_outgoing_message())

    def test_set_heater_output_range_output_0(self):
        self.fake_connection.setup_response('0')
        self.dut.set_heater_output_range(0, Model372SampleHeaterOutputRange(6))
        self.assertIn("RANGE 0,6", self.fake_connection.get_outgoing_message())

    def test_set_heater_output_range_output_1(self):
        self.fake_connection.setup_response('0')
        self.dut.set_heater_output_range(1, False)
        self.assertIn("RANGE 1,0", self.fake_connection.get_outgoing_message())

    def test_set_heater_output_range_output_2(self):
        self.fake_connection.setup_response('0')
        self.dut.set_heater_output_range(2, True)
        self.assertIn("RANGE 2,1", self.fake_connection.get_outgoing_message())

    def test_get_custom_display_settings(self):
        self.fake_connection.setup_response('1,0,2;0')
        response = self.dut.get_custom_display_settings()
        self.assertEqual(response['mode'], Model372DisplayMode.CONTROL_INPUT)
        self.assertEqual(response['number_of_fields'], Model372DisplayFields.LARGE_2)
        self.assertEqual(response['displayed_info'], Model372DisplayInfo.WARMUP_HEATER)
        self.assertIn("DISPLAY?", self.fake_connection.get_outgoing_message())

    def test_get_warmup_output(self):
        self.fake_connection.setup_response('1,50;0')
        response = self.dut.get_warmup_output()
        output_dictionary = {'auto_control': True,
                             'current': 50}
        self.assertDictEqual(response, output_dictionary)
        self.assertIn("WARMUP?", self.fake_connection.get_outgoing_message())

    def test_get_analog_monitor_output_settings(self):
        self.fake_connection.setup_response("1,1,7,1,10,5,0;0")
        response = self.dut.get_analog_monitor_output_settings()
        output_dictionary = {'source': Model372InputSensorUnits.KELVIN,
                             'high_value': 10,
                             'low_value': 5}
        self.assertDictEqual(response, output_dictionary)
        self.assertIn("ANALOG? 2", self.fake_connection.get_outgoing_message())


class TestEnumMethods(TestWithFakeModel372):

    def test_set_interface_int(self):
        self.fake_connection.setup_response('0')
        self.dut.set_interface(1)
        self.assertIn('INTSEL 1', self.fake_connection.get_outgoing_message())

    def test_set_interface_enum(self):
        self.fake_connection.setup_response('0')
        self.dut.set_interface(Model372Interface(0))
        self.assertIn('INTSEL 0', self.fake_connection.get_outgoing_message())

    def test_get_interface(self):
        interface = Model372Interface(1)
        self.fake_connection.setup_response('1;0')
        response = self.dut.get_interface()
        self.assertEqual(response, interface)
        self.assertIn("INTSEL?", self.fake_connection.get_outgoing_message())

    def test_get_ieee_interface_mode(self):
        ieee = Model372InterfaceMode(2)
        self.fake_connection.setup_response('2;0')
        response = self.dut.get_ieee_interface_mode()
        self.assertEqual(response, ieee)
        self.assertIn("MODE?", self.fake_connection.get_outgoing_message())

    def test_set_ieee_interface_mode_int(self):
        self.fake_connection.setup_response('0')
        self.dut.set_ieee_interface_mode(2)
        self.assertIn("MODE 2", self.fake_connection.get_outgoing_message())

    def test_set_ieee_interface_mode_enum(self):
        self.fake_connection.setup_response('0')
        self.dut.set_ieee_interface_mode(Model372InterfaceMode(1))
        self.assertIn("MODE 1", self.fake_connection.get_outgoing_message())

    def test_get_ieee_interface_parameter(self):
        self.fake_connection.setup_response('4;0')
        response = self.dut.get_ieee_interface_parameter()
        self.assertEqual(response, 4)
        self.assertIn("IEEE?", self.fake_connection.get_outgoing_message())

    def test_get_monitor_output_source(self):
        source = Model372MonitorOutputSource(1)
        self.fake_connection.setup_response('1;0')
        response = self.dut.get_monitor_output_source()
        self.assertEqual(source, response)
        self.assertIn("MONITOR?", self.fake_connection.get_outgoing_message())

    def test_set_monitor_output_source_int(self):
        self.fake_connection.setup_response('0')
        self.dut.set_monitor_output_source(1)
        self.assertIn("MONITOR 1", self.fake_connection.get_outgoing_message())

    def test_set_monitor_output_source_enum(self):
        self.fake_connection.setup_response('0')
        self.dut.set_monitor_output_source(Model372MonitorOutputSource(5))
        self.assertIn("MONITOR 5", self.fake_connection.get_outgoing_message())

    def test_setup_warmup_heater(self):
        self.fake_connection.setup_response('0')
        self.dut.setup_warmup_heater(Model372HeaterResistance.HEATER_50_OHM, 0.707, Model372HeaterOutputUnits.CURRENT)
        self.assertIn("HTRSET 1,2,0,0.707,1", self.fake_connection.get_outgoing_message())

    def test_setup_sample_heater(self):
        self.fake_connection.setup_response('0')
        self.dut.setup_sample_heater(55.0, Model372HeaterOutputUnits.POWER)
        self.assertIn("HTRSET 0,55.0,0,0,2", self.fake_connection.get_outgoing_message())

    def test_get_warmup_heater_setup_preset_current(self):
        self.fake_connection.setup_response("1,1,0,2;0")
        response = self.dut.get_warmup_heater_setup()
        self.assertEqual(response['resistance'], Model372HeaterResistance.HEATER_25_OHM)
        self.assertAlmostEqual(response['max_current'], 0.45)
        self.assertEqual(response['units'], Model372HeaterOutputUnits.POWER)
        self.assertIn("HTRSET? 1", self.fake_connection.get_outgoing_message())

    def test_get_warmup_heater_setup_user_specified_current(self):
        self.fake_connection.setup_response("2,0,0.5,1;0")
        response = self.dut.get_warmup_heater_setup()
        self.assertEqual(response['resistance'], Model372HeaterResistance.HEATER_50_OHM)
        self.assertAlmostEqual(response['max_current'], 0.5)
        self.assertEqual(response['units'], Model372HeaterOutputUnits.CURRENT)
        self.assertIn("HTRSET? 1", self.fake_connection.get_outgoing_message())

    def test_get_sample_heater_setup(self):
        self.fake_connection.setup_response("123.4,0,0,1;0")
        response = self.dut.get_sample_heater_setup()
        self.assertAlmostEqual(response['resistance'], 123.4)
        self.assertEqual(response['units'], Model372HeaterOutputUnits.CURRENT)
        self.assertIn("HTRSET? 0", self.fake_connection.get_outgoing_message())


class TestObjectMethods(TestWithFakeModel372):

    def test_get_input_channel_parameters(self):
        self.fake_connection.setup_response("1,10,3,0,2;0")
        response = self.dut.get_input_channel_parameters(5)
        # Assert that each variable is equal to expected response
        self.assertEqual(response.enable, True)
        self.assertAlmostEqual(response.dwell_time, 10)
        self.assertAlmostEqual(response.pause_time, 3)
        self.assertAlmostEqual(response.curve_number, 0)
        self.assertEqual(response.temperature_coefficient, Model372CurveTemperatureCoefficient(2))
        # Assert correct response was given
        self.assertIn("INSET? 5", self.fake_connection.get_outgoing_message())

    def test_set_input_channel_settings(self):
        self.fake_connection.setup_response('0')
        settings = Model372InputChannelSettings(True, 34, 15, 22, Model372CurveTemperatureCoefficient.NEGATIVE)
        self.dut.set_input_channel_parameters(3, settings)
        self.assertIn("INSET 3,1,34,15,22,1", self.fake_connection.get_outgoing_message())

    def test_get_input_setup_settings(self):
        self.fake_connection.setup_response("1,10,0,5,0,1;0")
        response = self.dut.get_input_setup_parameters(2)
        # Assert each variable is equal to expected response
        self.assertEqual(response.mode, Model372SensorExcitationMode(1))
        self.assertAlmostEqual(response.excitation_range, Model372MeasurementInputCurrentRange(10))
        self.assertEqual(response.auto_range, Model372AutoRangeMode(0))
        self.assertAlmostEqual(response.resistance_range, Model372MeasurementInputResistance(5))
        self.assertEqual(response.current_source_shunted, False)
        self.assertEqual(response.units, Model372InputSensorUnits.KELVIN)
        # Assert correct query was sent to instrument
        self.assertIn("INTYPE? 2", self.fake_connection.get_outgoing_message())

    def test_set_input_setup_settings_control(self):
        self.fake_connection.setup_response('0')
        settings = Model372InputSetupSettings(Model372SensorExcitationMode.CURRENT,
                                              Model372ControlInputCurrentRange(2), 0, True,
                                              Model372InputSensorUnits.OHMS)
        self.dut.configure_input("A", settings)
        self.assertIn("INTYPE A,1,2,0,0,1,2", self.fake_connection.get_outgoing_message())

    def test_set_input_setup_settings_measurement_voltage(self):
        self.fake_connection.setup_response('0')
        settings = Model372InputSetupSettings(Model372SensorExcitationMode.VOLTAGE,
                                              Model372MeasurementInputVoltageRange(6), 0, True,
                                              Model372InputSensorUnits.OHMS,
                                              resistance_range=Model372MeasurementInputResistance(11))
        self.dut.configure_input(3, settings)
        self.assertIn("INTYPE 3,0,6,0,11,1,2", self.fake_connection.get_outgoing_message())

    def test_set_input_setup_settings_measurement_current(self):
        self.fake_connection.setup_response('0')
        settings = Model372InputSetupSettings(Model372SensorExcitationMode.CURRENT,
                                              Model372MeasurementInputCurrentRange(6), 0,
                                              True, Model372InputSensorUnits.OHMS,
                                              resistance_range=Model372MeasurementInputResistance(11))
        self.dut.configure_input(3, settings)
        self.assertIn("INTYPE 3,1,6,0,11,1,2", self.fake_connection.get_outgoing_message())

    def test_get_heater_output_settings(self):
        self.fake_connection.setup_response("4,0,1,1,0,120;0")
        response = self.dut.get_heater_output_settings(1)
        # Assert that variables of object are correct
        self.assertEqual(response.output_mode, Model372OutputMode["STILL"])
        self.assertEqual(response.input_channel, Model372InputChannel(0))
        self.assertEqual(response.powerup_enable, True)
        self.assertEqual(response.polarity, Model372Polarity.BIPOLAR)
        self.assertEqual(response.reading_filter, False)
        self.assertAlmostEqual(response.delay, 120)
        # Assert that correct query was sent to the instrument
        self.assertIn("OUTMODE? 1", self.fake_connection.get_outgoing_message())

    def test_set_heater_output_settings_with_polarity(self):
        self.fake_connection.setup_response('0')
        settings = Model372HeaterOutputSettings(Model372OutputMode.OPEN_LOOP, 5, True, False, 250,
                                                Model372Polarity.BIPOLAR)
        self.dut.configure_heater(0, settings)
        self.assertIn("OUTMODE 0,2,5,1,1,0,250", self.fake_connection.get_outgoing_message())

    def test_set_heater_output_settings_without_polarity(self):
        self.fake_connection.setup_response('0')
        settings = Model372HeaterOutputSettings(Model372OutputMode.WARMUP, "A", True, False, 250)
        self.dut.configure_heater(1, settings)
        self.assertIn("OUTMODE 1,6,A,1,0,0,250", self.fake_connection.get_outgoing_message())

    def test_get_control_loop_zone_parameters(self):
        self.fake_connection.setup_response("276,250.1,3000,1000,52,1,4,0,1;0")
        settings = self.dut.get_control_loop_zone_parameters(0, 4)
        self.assertAlmostEqual(settings.p_value, 250.1)
        self.assertAlmostEqual(settings.i_value, 3000)
        self.assertAlmostEqual(settings.d_value, 1000)
        self.assertAlmostEqual(settings.manual_output, 52)
        self.assertAlmostEqual(settings.heater_range, Model372SampleHeaterOutputRange(1))
        self.assertAlmostEqual(settings.ramp_rate, 4)
        self.assertEqual(settings.relay_1, False)
        self.assertEqual(settings.relay_2, True)
        self.assertIn("ZONE? 0,4", self.fake_connection.get_outgoing_message())

    def test_set_control_loop_zone_parameters(self):
        self.fake_connection.setup_response('0')
        settings = Model372ControlLoopZoneSettings(276, 123.4, 2500, 1500, 75, False, 5, False, False)
        self.dut.set_control_loop_parameters(1, 5, settings)
        self.assertIn("ZONE 1,5,276,123.4,2500,1500,75,0,5,0,0", self.fake_connection.get_outgoing_message())

    def test_get_alarm_parameters(self):
        self.fake_connection.setup_response('1,0,276,10,100,1,0,0;0')
        response = self.dut.get_alarm_parameters(4)
        self.assertEqual(response['alarm_enable'], True)
        self.assertAlmostEqual(response['alarm_settings'].high_value, 276)
        self.assertAlmostEqual(response['alarm_settings'].low_value, 10)
        self.assertAlmostEqual(response['alarm_settings'].deadband, 100)
        self.assertEqual(response['alarm_settings'].latch_enable, True)
        self.assertEqual(response['alarm_settings'].visible, False)
        self.assertEqual(response['alarm_settings'].audible, False)
        self.assertIn('ALARM? 4', self.fake_connection.get_outgoing_message())

    def test_set_alarm_parameters(self):
        self.fake_connection.setup_response('0')
        alarm_parameters = Model372AlarmParameters(276, 10, 100, True, True, True)
        self.dut.set_alarm_parameters(4, True, alarm_parameters)
        self.assertIn('ALARM 4,1,0,276,10,100,1,1,1', self.fake_connection.get_outgoing_message())

    def test_configure_analog_monitor_output_heater(self):
        self.fake_connection.setup_response('0')
        heater_output_settings = Model372HeaterOutputSettings(Model372OutputMode.WARMUP,
                                                              Model372InputChannel.SEVEN,
                                                              True, True, 125,
                                                              Model372Polarity.BIPOLAR)
        self.dut.configure_analog_monitor_output_heater(Model372InputSensorUnits.KELVIN, 10, 5,
                                                        heater_output_settings)
        self.assertIn("ANALOG 2,1,1,7,1,10,5,0", self.fake_connection.get_outgoing_message())

    def test_configure_analog_heater(self):
        self.fake_connection.setup_response('0')
        heater_settings = Model372HeaterOutputSettings(Model372OutputMode.ZONE,
                                                       Model372InputChannel.SEVEN,
                                                       True,
                                                       True,
                                                       25,
                                                       Model372Polarity.UNIPOLAR)
        self.dut.configure_analog_heater(Model372HeaterOutput.WARM_UP_HEATER,
                                         50,
                                         heater_settings)
        self.assertIn("ANALOG 1,3,0,7,0,0,0,50", self.fake_connection.get_outgoing_message())


class TestRegisterMethods(TestWithFakeModel372):

    def test_get_reading_status(self):
        self.fake_connection.setup_response('56;0')
        response = self.dut.get_reading_status(1)
        register = Model372ReadingStatusRegister.from_integer('56')
        self.assertEqual(response.current_source_overload, register.current_source_overload)
        self.assertEqual(response.voltage_common_mode_stage_overload, register.current_source_overload)
        self.assertEqual(response.voltage_mixer_stage_overload, register.voltage_mixer_stage_overload)
        self.assertEqual(response.voltage_differential_stage_overload, register.voltage_differential_stage_overload)
        self.assertEqual(response.resistance_over, register.resistance_over)
        self.assertEqual(response.resistance_under, register.resistance_under)
        self.assertEqual(response.temperature_over, register.temperature_over)
        self.assertEqual(response.temperature_under, register.temperature_under)
        self.assertIn("RDGST? 1", self.fake_connection.get_outgoing_message())
