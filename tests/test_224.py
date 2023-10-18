from lakeshore import Model224AlarmParameters, Model224CurveHeader, Model224InputSensorSettings
from tests.utils import TestWithFakeModel224


class TestBasicReadings(TestWithFakeModel224):
    def test_get_celsius_reading(self):
        self.fake_connection.setup_response('32.0;0')
        response = self.dut.get_celsius_reading("A")
        self.assertAlmostEqual(response, 32.0)
        self.assertIn("CRDG? A", self.fake_connection.get_outgoing_message())

    def test_get_sensor_reading(self):
        self.fake_connection.setup_response('123.4;0')
        response = self.dut.get_sensor_reading("C1")
        self.assertAlmostEqual(response, 123.4)
        self.assertIn("SRDG? C1", self.fake_connection.get_outgoing_message())

    def test_get_kelvin_reading(self):
        self.fake_connection.setup_response("567.8;0")
        response = self.dut.get_kelvin_reading("D4")
        self.assertAlmostEqual(response, 567.8)
        self.assertIn("KRDG? D4", self.fake_connection.get_outgoing_message())

    def test_get_all_inputs_celsius_reading(self):
        dict_expected = {'input_a_reading': 32.0,
                         'input_b_reading': 0.0,
                         'input_c1_reading': 1.0,
                         'input_c2_reading': 2.0,
                         'input_c3_reading': 276.0,
                         'input_c4_reading': -10.0,
                         'input_c5_reading': 0.0,
                         'input_d1_reading': 1.0,
                         'input_d2_reading': -2.0,
                         'input_d3_reading': 32.0,
                         'input_d4_reading': 44.0,
                         'input_d5_reading': 55.5}
        self.fake_connection.setup_response('32.0,0.0,1.0,2.0,276.0,-10.0,0.0,1.0,-2.0,32.0,44.0,55.5;0')
        response = self.dut.get_all_inputs_celsius_reading()
        self.assertDictEqual(response, dict_expected)
        self.assertIn("CRDG? 0", self.fake_connection.get_outgoing_message())

    def test_get_input_diode_excitation_current(self):
        self.fake_connection.setup_response('0;0')
        response = self.dut.get_input_diode_excitation_current("B")
        self.assertAlmostEqual(response, self.dut.DiodeExcitationCurrent.TEN_MICRO_AMPS)
        self.assertIn("DIOCUR? B", self.fake_connection.get_outgoing_message())

    def test_get_min_max_data(self):
        expected_dict = {'minimum': 0.01,
                         'maximum': 234.0}
        self.fake_connection.setup_response('0.01,234.0;0')
        response = self.dut.get_min_max_data("A")
        self.assertDictEqual(response, expected_dict)
        self.assertIn("MDAT? A", self.fake_connection.get_outgoing_message())


class TestGetAndSetBasicSettings(TestWithFakeModel224):
    def test_set_input_diode_excitation_current(self):
        self.fake_connection.setup_response('0')
        self.dut.set_input_diode_excitation_current("C1", self.dut.DiodeExcitationCurrent.ONE_MILLI_AMP)
        self.assertIn("DIOCUR C1,1", self.fake_connection.get_outgoing_message())

    def test_set_ieee_488(self):
        self.fake_connection.setup_response('0')
        self.dut.set_ieee_488(12)
        self.assertIn("IEEE 12", self.fake_connection.get_outgoing_message())

    def test_get_ieee_488(self):
        self.fake_connection.setup_response('12;0')
        response = self.dut.get_ieee_488()
        self.assertEqual(response, 12)
        self.assertIn("IEEE?", self.fake_connection.get_outgoing_message())

    def test_set_led_state(self):
        self.fake_connection.setup_response('0')
        self.dut.set_led_state(True)
        self.assertIn("LEDS 1", self.fake_connection.get_outgoing_message())

    def test_get_led_state(self):
        self.fake_connection.setup_response('0;0')
        response = self.dut.get_led_state()
        self.assertEqual(response, False)
        self.assertIn("LEDS?", self.fake_connection.get_outgoing_message())

    def test_set_keypad_lock(self):
        self.fake_connection.setup_response('0')
        self.dut.set_keypad_lock(False, 123)
        self.assertIn("LOCK 0,123", self.fake_connection.get_outgoing_message())

    def test_get_keypad_lock(self):
        expected_response = {'state': True,
                             'code': 123}
        self.fake_connection.setup_response('1,123;0')
        response = self.dut.get_keypad_lock()
        self.assertDictEqual(response, expected_response)
        self.assertIn("LOCK?", self.fake_connection.get_outgoing_message())

    def test_reset_min_max_data(self):
        self.fake_connection.setup_response('0')
        self.dut.reset_min_max_data()
        self.assertIn("MNMXRST", self.fake_connection.get_outgoing_message())

    def test_get_relay_status(self):
        self.fake_connection.setup_response('0;0')
        response = self.dut.get_relay_status(1)
        self.assertFalse(response)
        self.assertIn("RELAYST? 1", self.fake_connection.get_outgoing_message())

    def test_set_filter(self):
        self.fake_connection.setup_response('0')
        self.dut.set_filter("B", True, 6, 2)
        self.assertIn("FILTER B,1,6,2", self.fake_connection.get_outgoing_message())

    def test_get_filter(self):
        expected_response = {'filter_enabled': True,
                             'number_of_points': 20,
                             'filter_reset_threshold': 7}
        self.fake_connection.setup_response("1,20,7;0")
        response = self.dut.get_filter("D2")
        self.assertDictEqual(response, expected_response)
        self.assertIn("FILTER? D2", self.fake_connection.get_outgoing_message())

    def test_set_website_login(self):
        self.fake_connection.setup_response('0')
        self.dut.set_website_login("username", "password")
        self.assertIn('WEBLOG "username","password"', self.fake_connection.get_outgoing_message())

    def test_get_website_login(self):
        expected_dict = {'username': 'username',
                         'password': 'password'}
        self.fake_connection.setup_response('  "username"  ,"  password  ";0')
        response = self.dut.get_website_login()
        self.assertDictEqual(response, expected_dict)
        self.assertIn("WEBLOG?", self.fake_connection.get_outgoing_message())

    def test_get_display_contrast(self):
        self.fake_connection.setup_response("30;0")
        response = self.dut.get_display_contrast()
        self.assertAlmostEqual(response, 30)
        self.assertIn("BRIGT?", self.fake_connection.get_outgoing_message())

    def test_set_display_contrast(self):
        self.fake_connection.setup_response('0')
        self.dut.set_display_contrast(15)
        self.assertIn("BRIGT 15", self.fake_connection.get_outgoing_message())

    def test_set_sensor_name(self):
        self.fake_connection.setup_response('0')
        self.dut.set_sensor_name("C3", "My Sensor")
        self.assertIn('INNAME C3,"My Sensor"', self.fake_connection.get_outgoing_message())

    def test_get_sensor_name(self):
        self.fake_connection.setup_response('My Sensor;0')
        response = self.dut.get_sensor_name("A")
        self.assertEqual(response, "My Sensor")
        self.assertIn('INNAME? A', self.fake_connection.get_outgoing_message())


class TestCurveMethods(TestWithFakeModel224):
    def test_set_input_curve(self):
        # Add fake connection setup response for internal error check in method
        self.fake_connection.setup_response("22;0")
        self.fake_connection.setup_response('22;0')
        self.dut.set_input_curve("D3", 22)
        self.assertIn("INCRV D3,22", self.fake_connection.get_outgoing_message())

    def test_get_input_curve(self):
        self.fake_connection.setup_response("12;0")
        response = self.dut.get_input_curve("B")
        self.assertEqual(response, 12)
        self.assertIn("INCRV? B", self.fake_connection.get_outgoing_message())

    def test_generate_soft_cal_curve(self):
        self.fake_connection.setup_response('0')
        self.dut.generate_and_apply_soft_cal_curve(self.dut.SoftCalSensorTypes.DT_400, 50, "ABC123",
                                                   (276, 100.0), (345, 125.0))
        self.assertIn("SCAL 1,50,ABC123,276,100.0,345,125.0,0,0", self.fake_connection.get_outgoing_message())

    def test_set_curve_header(self):
        self.fake_connection.setup_response('0')
        curve_header = Model224CurveHeader("My_Curve", "ABC123", self.dut.CurveFormat.VOLTS_PER_KELVIN,
                                                     300.0, self.dut.CurveTemperatureCoefficients.POSITIVE)
        self.dut.set_curve_header(22, curve_header)
        self.assertIn('CRVHDR 22,My_Curve,ABC123,2,300.0,2', self.fake_connection.get_outgoing_message())

    def test_get_curve_header(self):
        self.fake_connection.setup_response('DT-123,001122,3,222.2,1;0')
        response = self.dut.get_curve_header(23)
        self.assertEqual(response.curve_name, "DT-123")
        self.assertEqual(response.serial_number, "001122")
        self.assertEqual(response.curve_data_format, self.dut.CurveFormat(3))
        self.assertAlmostEqual(response.temperature_limit, 222.2)
        self.assertEqual(response.coefficient, self.dut.CurveTemperatureCoefficients.NEGATIVE)
        self.assertIn('CRVHDR? 23', self.fake_connection.get_outgoing_message())

    def test_get_curve_data_point(self):
        self.fake_connection.setup_response('0.10101,123.45;0')
        response = self.dut.get_curve_data_point(25, 13)
        self.assertAlmostEqual(response[0], 0.10101)
        self.assertAlmostEqual(response[1], 123.45)
        self.assertIn('CRVPT? 25,13', self.fake_connection.get_outgoing_message())

    def test_set_curve_data_point(self):
        self.fake_connection.setup_response('0')
        self.dut.set_curve_data_point(30, 11, 1.234, 99.99)
        self.assertIn('CRVPT 30,11,1.234,99.99', self.fake_connection.get_outgoing_message())

    def test_delete_curve(self):
        self.fake_connection.setup_response('0')
        self.dut.delete_curve(55)
        self.assertIn('CRVDEL 55', self.fake_connection.get_outgoing_message())


class TestObjectSettingsMethods(TestWithFakeModel224):
    def test_get_alarm_parameters(self):
        expected_settings = Model224AlarmParameters(200.0, 10.0, 50.0, True, True, True)
        self.fake_connection.setup_response("1,200.0,10.0,50.0,1,1,1;0")
        response = self.dut.get_alarm_parameters("A")
        # Assert equals variable by variable
        self.assertEqual(response['alarm_enable'], True)
        self.assertAlmostEqual(response['alarm_settings'].high_value, 200.0)
        self.assertAlmostEqual(response['alarm_settings'].low_value, 10.0)
        self.assertAlmostEqual(response['alarm_settings'].deadband, 50.0)
        self.assertAlmostEqual(response['alarm_settings'].latch_enable, True)
        self.assertAlmostEqual(response['alarm_settings'].audible, True)
        self.assertAlmostEqual(response['alarm_settings'].visible, True)
        self.assertIn("ALARM? A", self.fake_connection.get_outgoing_message())

    def test_set_alarm_parameters_no_optional_parameters(self):
        self.fake_connection.setup_response('0')
        alarm_settings = Model224AlarmParameters(200.0, 10.0, 50.0, True)
        self.dut.set_alarm_parameters("A", True, alarm_settings)
        self.assertIn("ALARM A,1,200.0,10.0,50.0,1,0,0", self.fake_connection.get_outgoing_message())

    def test_set_alarm_parameters_with_optional_parameters(self):
        self.fake_connection.setup_response('0')
        alarm_settings = Model224AlarmParameters(200.0, 10.0, 50.0, True, False, True)
        self.dut.set_alarm_parameters("A", True, alarm_settings)
        self.assertIn("ALARM A,1,200.0,10.0,50.0,1,0,1", self.fake_connection.get_outgoing_message())

    def test_set_alarm_parameters_disable_alarm(self):
        self.fake_connection.setup_response('0')
        self.dut.set_alarm_parameters("A", False)
        self.assertIn("ALARM A,0,0,0,0,0,0", self.fake_connection.get_outgoing_message())

    def test_configure_input(self):
        self.fake_connection.setup_response('0')
        settings = Model224InputSensorSettings(self.dut.InputSensorType.NTC_RTD,
                                                         self.dut.InputSensorUnits.CELSIUS,
                                                         self.dut.NTCRTDSensorResistanceRange.ONE_KILOHM)
        self.dut.configure_input("B", settings)
        self.assertIn("INTYPE B,3,0,4,0,2", self.fake_connection.get_outgoing_message())

    def test_disable_input(self):
        self.fake_connection.setup_response('0')
        self.dut.disable_input("C1")
        self.assertIn("INTYPE C1,0,0,0,0,0", self.fake_connection.get_outgoing_message())

    def test_get_input_configuration(self):
        self.fake_connection.setup_response("2,0,5,0,1;0")
        response = self.dut.get_input_configuration("A")
        self.assertEqual(response.sensor_type, self.dut.InputSensorType(2))
        self.assertEqual(response.autorange_enabled, False)
        self.assertEqual(response.sensor_range, self.dut.PlatinumRTDSensorResistanceRange(5))
        self.assertEqual(response.compensation, False)
        self.assertEqual(response.preferred_units, self.dut.InputSensorUnits(1))
        self.assertIn("INTYPE? A", self.fake_connection.get_outgoing_message())

    def test_select_remote_interface(self):
        self.fake_connection.setup_response('0')
        self.dut.select_remote_interface(self.dut.RemoteInterface.USB)
        self.assertIn("INTSEL 0", self.fake_connection.get_outgoing_message())

    def test_get_remote_interface(self):
        self.fake_connection.setup_response("2;0")
        response = self.dut.get_remote_interface()
        self.assertEqual(response, self.dut.RemoteInterface.IEEE_488)
        self.assertIn("INTSEL?", self.fake_connection.get_outgoing_message())

    def test_select_interface_mode(self):
        self.fake_connection.setup_response('0')
        self.dut.select_interface_mode(self.dut.InterfaceMode.REMOTE)
        self.assertIn("MODE 1", self.fake_connection.get_outgoing_message())

    def test_get_interface_mode(self):
        self.fake_connection.setup_response("0;0")
        response = self.dut.get_interface_mode()
        self.assertEqual(response, self.dut.InterfaceMode(0))
        self.assertIn("MODE?", self.fake_connection.get_outgoing_message())

    def test_set_relay_control_parameter_alarms(self):
        self.fake_connection.setup_response('0')
        self.dut.set_relay_alarms(1, "B", self.dut.RelayControlAlarm.BOTH_ALARMS)
        self.assertIn("RELAY 1,2,B,2", self.fake_connection.get_outgoing_message())

    def test_set_relay_control_parameter_no_alarms(self):
        self.fake_connection.setup_response('0')
        self.dut.turn_relay_on(1)
        self.assertIn("RELAY 1,1,0,0", self.fake_connection.get_outgoing_message())

    def test_get_relay_alarm_control_parameters(self):
        self.fake_connection.setup_response("2,D1,0;0")
        expected_response = {'activating_input_channel': "D1",
                             'alarm_relay_trigger_type': self.dut.RelayControlAlarm.LOW_ALARM}
        response = self.dut.get_relay_alarm_control_parameters(2)
        self.assertDictEqual(response, expected_response)
        self.assertIn("RELAY? 2", self.fake_connection.get_outgoing_message())

    def test_get_relay_control_mode(self):
        self.fake_connection.setup_response('1,0,0;0')
        response = self.dut.get_relay_control_mode(1)
        self.assertEqual(response, self.dut.RelayControlMode.RELAY_ON)
        self.assertIn("RELAY? 1", self.fake_connection.get_outgoing_message())


class TestDisplayMethods(TestWithFakeModel224):
    def test_set_display_field(self):
        self.fake_connection.setup_response('0')
        self.dut.set_display_field_settings(4, self.dut.InputChannel.INPUT_C2,
                                            self.dut.DisplayFieldUnits.SENSOR)
        self.assertIn("DISPFLD 4,9,3", self.fake_connection.get_outgoing_message())

    def test_get_display_field(self):
        expected_response = {'input_channel': self.dut.InputChannel(1),
                             'display_units': self.dut.DisplayFieldUnits(5)}
        self.fake_connection.setup_response("1,5;0")
        response = self.dut.get_display_field_settings(2)
        self.assertDictEqual(response, expected_response)
        self.assertIn("DISPFLD? 2", self.fake_connection.get_outgoing_message())

    def test_configure_display_custom(self):
        self.fake_connection.setup_response('0')
        self.dut.configure_display(self.dut.DisplayMode.CUSTOM,
                                   self.dut.NumberOfFields.LARGE_4)
        self.assertIn("DISPLAY 4,0", self.fake_connection.get_outgoing_message())

    def test_configure_display_without_number_of_fields(self):
        self.fake_connection.setup_response('0')
        self.dut.configure_display(self.dut.DisplayMode.ALL_INPUTS)
        self.assertIn("DISPLAY 5,", self.fake_connection.get_outgoing_message())

    def test_get_display_configuration_custom(self):
        expected_response = {'display_mode': self.dut.DisplayMode.CUSTOM,
                             'number_of_fields': self.dut.NumberOfFields(2)}
        self.fake_connection.setup_response("4,2;0")
        response = self.dut.get_display_configuration()
        self.assertDictEqual(response, expected_response)
        self.assertIn("DISPLAY?", self.fake_connection.get_outgoing_message())

    def test_get_display_configuration_without_number_of_fields(self):
        expected_response = {'display_mode': self.dut.DisplayMode(1),
                             'number_of_fields': None}
        self.fake_connection.setup_response("1,0;0")
        response = self.dut.get_display_configuration()
        self.assertDictEqual(response, expected_response)
        self.assertIn("DISPLAY?", self.fake_connection.get_outgoing_message())
