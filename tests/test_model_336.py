from tests.utils import TestWithFakeModel336
from lakeshore import InstrumentException
from lakeshore.model_336 import *


class TestBasicReadings(TestWithFakeModel336):

    def test_get_kelvin_reading(self):
        self.fake_connection.setup_response('10.32;0')
        response = self.dut.get_kelvin_reading("A")
        self.assertEqual(response, 10.32)
        self.assertIn("KRDG? A", self.fake_connection.get_outgoing_message())

    def test_get_celsius_reading(self):
        self.fake_connection.setup_response('68.65;0')
        response = self.dut.get_celsius_reading("A")
        self.assertAlmostEqual(response, 68.65)
        self.assertIn("CRDG? A", self.fake_connection.get_outgoing_message())

    def test_get_all_kelvin_reading(self):
        self.fake_connection.setup_response('26.36,98.57,2.07,55.68;0')
        response = self.dut.get_all_kelvin_reading()

        self.assertAlmostEqual(response[0], 26.36)
        self.assertAlmostEqual(response[1], 98.57)
        self.assertAlmostEqual(response[2], 2.07)
        self.assertAlmostEqual(response[3], 55.68)

        self.assertIn("KRDG? 0", self.fake_connection.get_outgoing_message())

    def test_get_all_sensor_reading(self):
        self.fake_connection.setup_response('0.5823,0.4568,0.5781,0.4698;0')
        response = self.dut.get_all_sensor_reading()

        self.assertAlmostEqual(response[0], 0.5823)
        self.assertAlmostEqual(response[1], 0.4568)
        self.assertAlmostEqual(response[2], 0.5781)
        self.assertAlmostEqual(response[3], 0.4698)

        self.assertIn("SRDG? 0", self.fake_connection.get_outgoing_message())

    def test_get_thermocouple_junction_temp(self):
        self.fake_connection.setup_response('218.65;0')
        response = self.dut.get_thermocouple_junction_temp()
        self.assertAlmostEqual(response, 218.65)
        self.assertIn("TEMP?", self.fake_connection.get_outgoing_message())


class TestBasicSettings(TestWithFakeModel336):

    def test_set_operation_event_enable(self):
        self.fake_connection.setup_response('0')
        bits = Model336OperationEvent(False, True, False, True, False, True, False, True)
        self.dut.set_operation_event_enable(bits)
        self.assertIn("OPSTE 170", self.fake_connection.get_outgoing_message())

    def test_get_operation_event_enable(self):
        self.fake_connection.setup_response('68;0')
        response = self.dut.get_operation_event_enable()

        self.assertEqual(response.alarm, False)
        self.assertEqual(response.sensor_overload, False)
        self.assertEqual(response.loop_2_ramp_done, True)
        self.assertEqual(response.loop_1_ramp_done, False)
        self.assertEqual(response.new_sensor_reading, False)
        self.assertEqual(response.autotune_process_completed, False)
        self.assertEqual(response.calibration_error, True)
        self.assertEqual(response.processor_communication_error, False)

        self.assertIn("OPSTE?", self.fake_connection.get_outgoing_message())

    def test_get_operation_condition(self):
        self.fake_connection.setup_response('115;0')
        response = self.dut.get_operation_condition()

        self.assertEqual(response.alarm, True)
        self.assertEqual(response.sensor_overload, True)
        self.assertEqual(response.loop_2_ramp_done, False)
        self.assertEqual(response.loop_1_ramp_done, False)
        self.assertEqual(response.new_sensor_reading, True)
        self.assertEqual(response.autotune_process_completed, True)
        self.assertEqual(response.calibration_error, True)
        self.assertEqual(response.processor_communication_error, False)

        self.assertIn("OPST?", self.fake_connection.get_outgoing_message())

    def test_get_operation_event(self):
        self.fake_connection.setup_response('255;0')
        response = self.dut.get_operation_event()

        self.assertEqual(response.alarm, True)
        self.assertEqual(response.sensor_overload, True)
        self.assertEqual(response.loop_2_ramp_done, True)
        self.assertEqual(response.loop_1_ramp_done, True)
        self.assertEqual(response.new_sensor_reading, True)
        self.assertEqual(response.autotune_process_completed, True)
        self.assertEqual(response.calibration_error, True)
        self.assertEqual(response.processor_communication_error, True)

        self.assertIn("OPSTR?", self.fake_connection.get_outgoing_message())

    def test_set_network_settings(self):
        self.fake_connection.setup_response('0')
        self.dut.set_network_settings(True, False, "192.16.254.1", "255.255.255.0", "10.0.1.1", "0.0.0.0", "0.0.0.0",
                                      "Preferred Host", "Prefered Domain Name", "Description")
        self.assertIn("NET 1,0,192.16.254.1,255.255.255.0,10.0.1.1,0.0.0.0,0.0.0.0," + \
                      "\"Preferred Host\",\"Prefered Domain Name\",\"Description\"",
                      self.fake_connection.get_outgoing_message())

    def test_get_network_settings(self):
        self.fake_connection.setup_response('1,0,192.16.254.1,255.255.255.0,10.0.1.1,0.0.0.0,0.0.0.0,' + \
                                            'Preferred Host,Prefered Domain Name,Description;0')
        response = self.dut.get_network_settings()
        network_settings = {"dhcp_enable": True,
                            "auto_ip_enable": False,
                            "ip_address": "192.16.254.1",
                            "sub_mask": "255.255.255.0",
                            "gateway": "10.0.1.1",
                            "primary_dns": "0.0.0.0",
                            "secondary_dns": "0.0.0.0",
                            "pref_host": "Preferred Host",
                            "pref_domain": "Prefered Domain Name",
                            "description": "Description"}
        self.assertEqual(response, network_settings)
        self.assertIn("NET?", self.fake_connection.get_outgoing_message())

    def test_get_network_configuration(self):
        self.fake_connection.setup_response('0,192.16.254.1,255.255.255.0,10.0.1.1,0.0.0.0,0.0.0.1,' + \
                                            '9C-35-58-5F-4C-D7,Host name,Domain;0')
        response = self.dut.get_network_configuration()
        network_configuration= {"lan_status": Model336LanStatus.STATIC_IP,
                                "ip_address": "192.16.254.1",
                                "sub_mask": "255.255.255.0",
                                "gateway": "10.0.1.1",
                                "primary_dns": "0.0.0.0",
                                "secondary_dns": "0.0.0.1",
                                "hostname": "Host name",
                                "domain": "Domain",
                                "mac_address": "9C-35-58-5F-4C-D7"}
        self.assertDictEqual(response, network_configuration)
        self.assertIn("NETID?", self.fake_connection.get_outgoing_message())


class TestBasicQueries(TestWithFakeModel336):

    def test_get_alarm_parameters(self):
        self.fake_connection.setup_response('1,320.15,210.54,3,0,1,1;0')
        response = self.dut.get_alarm_parameters('A')
        alarm_settings = Model336AlarmSettings(320.15, 210.54, 3, False, True, True, True)

        self.assertEqual(alarm_settings.high_value, response.high_value)
        self.assertEqual(alarm_settings.low_value, response.low_value)
        self.assertEqual(alarm_settings.deadband, response.deadband)
        self.assertEqual(alarm_settings.latch_enable, response.latch_enable)
        self.assertEqual(alarm_settings.audible, response.audible)
        self.assertEqual(alarm_settings.visible, response.visible)
        self.assertEqual(alarm_settings.alarm_enable, response.alarm_enable)

        self.assertIn("ALARM? A", self.fake_connection.get_outgoing_message())

    def test_get_alarm_status(self):
        self.fake_connection.setup_response('1,1;0')
        response = self.dut.get_alarm_status('A')
        alarm_status = {"high_state_enabled": True,
                        "low_state_enabled": True}
        self.assertDictEqual(response, alarm_status)

    def test_get_monitor_output_heater(self):
        self.fake_connection.setup_response('4,2,+236.54,+200.36,1;0')
        response = self.dut.get_monitor_output_heater(3)
        analog_heater_settings = {"channel": Model336InputChannel.CHANNEL_D,
                                  "units": Model336InputSensorUnits.CELSIUS,
                                  "high_value": 236.54,
                                  "low_value": 200.36,
                                  "polarity": Model336Polarity.BIPOLAR}
        self.assertDictEqual(response, analog_heater_settings)
        self.assertIn("ANALOG? 3", self.fake_connection.get_outgoing_message())

    def test_get_analog_output_percentage(self):
        self.fake_connection.setup_response('55.89;0')
        response = self.dut.get_analog_output_percentage(3)
        self.assertEqual(response, 55.89)
        self.assertIn("AOUT? 3", self.fake_connection.get_outgoing_message())

    def test_get_contrast_level(self):
        self.fake_connection.setup_response('32;0')
        response = self.dut.get_contrast_level()
        self.assertEqual(response, 32)
        self.assertIn("BRIGT?", self.fake_connection.get_outgoing_message())

    def test_get_curve_header(self):
        self.fake_connection.setup_response('some_curve,5555444411,2,325,1;0')
        response = self.dut.get_curve_header(22)

        self.assertEqual(response.curve_name, "some_curve")
        self.assertEqual(response.serial_number, "5555444411")
        self.assertEqual(response.curve_data_format, Model336CurveFormat.VOLTS_PER_KELVIN)
        self.assertEqual(response.temperature_limit, 325)
        self.assertEqual(response.coefficient, Model336CurveTemperatureCoefficients.NEGATIVE)

        self.assertIn("CRVHDR? 22", self.fake_connection.get_outgoing_message())

    def test_get_curve_data_point(self):
        self.fake_connection.setup_response('0.521,4.35;0')
        response = self.dut.get_curve_data_point(22, 150)
        self.assertEqual(response, (0.521, 4.35))
        self.assertIn("CRVPT? 22,150", self.fake_connection.get_outgoing_message())

    def test_get_diode_excitation_current(self):
        self.fake_connection.setup_response('0;0')
        response = self.dut.get_diode_excitation_current("A")
        self.assertAlmostEqual(response, Model336DiodeCurrent.TEN_MICROAMPS)
        self.assertIn("DIOCUR? A", self.fake_connection.get_outgoing_message())

    def test_get_display_field_settings(self):
        self.fake_connection.setup_response('1,2;0')
        response = self.dut.get_display_field_settings(2)
        display_field = {'input_channel': Model336InputChannel.CHANNEL_A,
                         'display_units': Model336DisplayUnits.CELSIUS}
        self.assertDictEqual(response, display_field)
        self.assertIn('DISPFLD? 2', self.fake_connection.get_outgoing_message())

    def test_get_display_setup(self):
        self.fake_connection.setup_response('3,0,0;0')
        response = self.dut.get_display_setup()
        display_setup = {"mode": Model336DisplaySetupMode.INPUT_D,
                         "num_fields": None,
                         "displayed_output": None}
        self.assertDictEqual(response, display_setup)

        self.assertIn("DISPLAY?", self.fake_connection.get_outgoing_message())

    def test_get_display_setup_custom(self):
        self.fake_connection.setup_response('4,1,1;0')
        response = self.dut.get_display_setup()
        display_setup = {"mode": Model336DisplaySetupMode.CUSTOM,
                         "num_fields": Model336DisplayFields.LARGE_4,
                         "displayed_output": 1}
        self.assertDictEqual(response, display_setup)

        self.assertIn("DISPLAY?", self.fake_connection.get_outgoing_message())

    def test_get_display_setup_all_inputs(self):
        self.fake_connection.setup_response('6,0,0;0')
        response = self.dut.get_display_setup()
        display_setup = {"mode": Model336DisplaySetupMode.ALL_INPUTS,
                         "num_fields": Model336DisplayFieldsSize.SMALL,
                         "displayed_output": None}
        self.assertDictEqual(response, display_setup)

        self.assertIn("DISPLAY?", self.fake_connection.get_outgoing_message())

    def test_get_heater_output(self):
        self.fake_connection.setup_response('55.63;0')
        response = self.dut.get_heater_output(1)
        self.assertEqual(response, 55.63)
        self.assertIn("HTR? 1", self.fake_connection.get_outgoing_message())

    def test_get_filter(self):
        self.fake_connection.setup_response('1,26,5;0')
        response = self.dut.get_filter("A")
        filter_parameters = {"filter_enable": True,
                             "data_points": 26,
                             "reset_threshold": 5}

        self.assertDictEqual(response, filter_parameters)

    def test_get_input_curve(self):
        self.fake_connection.setup_response('53;0')
        response = self.dut.get_input_curve("A")
        self.assertEqual(response, 53)
        self.assertIn("INCRV?", self.fake_connection.get_outgoing_message())

    def test_get_sensor_name(self):
        self.fake_connection.setup_response("Some_Channel;0")
        response = self.dut.get_sensor_name("A")
        self.assertEqual(response, "Some_Channel")
        self.assertIn("INNAME? A", self.fake_connection.get_outgoing_message())

    def test_get_heater_setup_custom(self):
        self.fake_connection.setup_response('1,0,0.75,1;0')
        response = self.dut.get_heater_setup(2)
        heater_output = {"heater_resistance": Model336HeaterResistance.HEATER_25_OHM,
                         "max_current": 0.75,
                         "output_display_mode": Model336HeaterOutputUnits.CURRENT}
        self.assertDictEqual(response, heater_output)

        self.assertIn("HTRSET? 2", self.fake_connection.get_outgoing_message())

    def test_get_heater_setup_user(self):
        self.fake_connection.setup_response('1,2,0,1;0')
        response = self.dut.get_heater_setup(2)
        heater_output = {"heater_resistance": Model336HeaterResistance.HEATER_25_OHM,
                         "max_current": 1.0,
                         "output_display_mode": Model336HeaterOutputUnits.CURRENT}
        self.assertDictEqual(response, heater_output)

        self.assertIn("HTRSET? 2", self.fake_connection.get_outgoing_message())

    def test_get_heater_status(self):
        self.fake_connection.setup_response('2;0')
        response = self.dut.get_heater_status(1)
        self.assertEqual(response, Model336HeaterError.HEATER_SHORT)
        self.assertIn("HTRST? 1", self.fake_connection.get_outgoing_message())

    def test_get_ieee_488(self):
        self.fake_connection.setup_response('25;0')
        response = self.dut.get_ieee_488()
        self.assertEqual(response, 25)
        self.assertIn("IEEE?", self.fake_connection.get_outgoing_message())

    def test_get_interface(self):
        self.fake_connection.setup_response("2;0")
        response = self.dut.get_interface()
        self.assertEqual(response, Model336Interface.IEEE488)
        self.assertIn("INTSEL?", self.fake_connection.get_outgoing_message())

    def test_get_input_sensor(self):
        self.fake_connection.setup_response('4,0,0,1,2;0')
        response = self.dut.get_input_sensor("A")
        sensor_parameters = Model336InputSensorSettings(Model336InputSensorType.THERMOCOUPLE, False, True,
                                                        Model336InputSensorUnits.CELSIUS,
                                                        Model336ThermocoupleRange.FIFTY_MILLIVOLT)

        self.assertEqual(response.sensor_type, sensor_parameters.sensor_type)
        self.assertEqual(response.autorange_enable, sensor_parameters.autorange_enable)
        self.assertEqual(response.compensation, sensor_parameters.compensation)
        self.assertEqual(response.units, sensor_parameters.units)
        self.assertEqual(response.input_range, sensor_parameters.input_range)

        self.assertIn("INTYPE? A", self.fake_connection.get_outgoing_message())

    def test_get_led_state(self):
        self.fake_connection.setup_response('1;0')
        response = self.dut.get_led_state()
        self.assertEqual(response, True)
        self.assertIn('LEDS?', self.fake_connection.get_outgoing_message())

    def test_get_keypad_lock(self):
        self.fake_connection.setup_response('1,123;0')
        response = self.dut.get_keypad_lock()
        keypad_lock = {'state': True,
                       'code': 123}
        self.assertDictEqual(response, keypad_lock)
        self.assertIn('LOCK?', self.fake_connection.get_outgoing_message())

    def test_get_min_max_data(self):
        self.fake_connection.setup_response('50.26,98.57;0')
        response = self.dut.get_min_max_data('A')
        min_max = {"minimum": 50.26,
                   "maximum": 98.57}
        self.assertDictEqual(response, min_max)
        self.assertIn('MDAT? A', self.fake_connection.get_outgoing_message())

    def test_get_remote_interface_mode(self):
        self.fake_connection.setup_response('2;0')
        response = self.dut.get_remote_interface_mode()
        self.assertEqual(response, Model336InterfaceMode.REMOTE_LOCAL_LOCK)
        self.assertIn('MODE?', self.fake_connection.get_outgoing_message())

    def test_get_manual_output(self):
        self.fake_connection.setup_response('24.3;0')
        response = self.dut.get_manual_output(1)
        self.assertEqual(response, 24.3)
        self.assertIn('MOUT? 1', self.fake_connection.get_outgoing_message())

    def test_get_heater_output_mode(self):
        self.fake_connection.setup_response('4,3,1;0')
        response = self.dut.get_heater_output_mode(1)
        heater_output_settings = {"mode": Model336HeaterOutputMode.MONITOR_OUT,
                                  "channel": Model336InputChannel.CHANNEL_C,
                                  "powerup_enable": True}
        self.assertDictEqual(response, heater_output_settings)

        self.assertIn("OUTMODE? 1", self.fake_connection.get_outgoing_message())

    def test_get_heater_pid(self):
        self.fake_connection.setup_response('4.25,6.1,0;0')
        response = self.dut.get_heater_pid(1)
        pid_settings = {"gain": 4.25,
                        "integral": 6.1,
                        "ramp_rate": 0}
        self.assertDictEqual(response, pid_settings)
        self.assertIn("PID? 1", self.fake_connection.get_outgoing_message())

    def test_get_heater_range(self):
        self.fake_connection.setup_response('2;0')
        response = self.dut.get_heater_range(1)
        self.assertEqual(response, Model336HeaterRange.MEDIUM)
        self.assertIn("RANGE? 1", self.fake_connection.get_outgoing_message())

    def test_get_setpoint_ramp_parameter(self):
        self.fake_connection.setup_response('0,45;0')
        response = self.dut.get_setpoint_ramp_parameter(2)
        ramp_settings = {"ramp_enable": False,
                         "rate_value": 45.0}
        self.assertDictEqual(response, ramp_settings)
        self.assertIn("RAMP? 2", self.fake_connection.get_outgoing_message())

    def test_get_relay_alarm_control_parameters(self):
        self.fake_connection.setup_response('0,A,2;0')
        response = self.dut.get_relay_alarm_control_parameters(1)
        relay_alarm = {'activating_input_channel': "A",
                       'alarm_relay_trigger_type': Model336RelayControlAlarm.BOTH_ALARMS}
        self.assertDictEqual(response, relay_alarm)
        self.assertIn("RELAY? 1", self.fake_connection.get_outgoing_message())

    def test_get_relay_control_mode(self):
        self.fake_connection.setup_response('2,A,2;0')
        response = self.dut.get_relay_control_mode(1)
        self.assertEqual(response, Model336RelayControlMode.ALARMS)
        self.assertIn("RELAY? 1", self.fake_connection.get_outgoing_message())

    def test_get_relay_status(self):
        self.fake_connection.setup_response('1;0')
        response = self.dut.get_relay_status(1)
        self.assertEqual(response, True)
        self.assertIn("RELAYST? 1", self.fake_connection.get_outgoing_message())

    def test_get_input_reading_status(self):
        self.fake_connection.setup_response('64;0')
        response = self.dut.get_input_reading_status("A")
        input_reading_status = Model336InputReadingStatus(False, False, False, True, False)

        self.assertEqual(response.invalid_reading, input_reading_status.invalid_reading)
        self.assertEqual(response.temp_underrange, input_reading_status.temp_underrange)
        self.assertEqual(response.temp_overrange, input_reading_status.temp_overrange)
        self.assertEqual(response.sensor_units_zero, input_reading_status.sensor_units_zero)

        self.assertIn("RDGST? A", self.fake_connection.get_outgoing_message())

    def test_get_control_setpoint(self):
        self.fake_connection.setup_response('2.35;0')
        response = self.dut.get_control_setpoint(1)
        self.assertEqual(response, 2.35)
        self.assertIn("SETP? 1", self.fake_connection.get_outgoing_message())

    def test_get_temperature_limit(self):
        self.fake_connection.setup_response('12.51;0')
        response = self.dut.get_temperature_limit('A')
        self.assertEqual(response, 12.51)
        self.assertIn("TLIMIT?", self.fake_connection.get_outgoing_message())

    def test_get_tuning_control_status(self):
        self.fake_connection.setup_response('1,1,0,04;0')
        response = self.dut.get_tuning_control_status()
        tuning_control = {"active_tuning_enable": True,
                          "output": 1,
                          "tuning_error": False,
                          "stage_status": 4}
        self.assertDictEqual(response, tuning_control)

        self.assertIn("TUNEST?", self.fake_connection.get_outgoing_message())

    def test_get_warmup_supply(self):
        self.fake_connection.setup_response('0,65.3;0')
        response = self.dut.get_warmup_supply_parameter(3)
        warmup_supply_config = {"control": Model336ControlTypes.AUTO_OFF,
                                "percentage": 65.3}
        self.assertDictEqual(response, warmup_supply_config)

        self.assertIn("WARMUP? 3", self.fake_connection.get_outgoing_message())

    def test_get_website_login(self):
        self.fake_connection.setup_response('MyUsername,MyPassword;0')
        response = self.dut.get_website_login()
        website_login = {"username": "MyUsername",
                         "password": "MyPassword"}
        self.assertDictEqual(response, website_login)
        self.assertIn("WEBLOG?", self.fake_connection.get_outgoing_message())

    def test_get_control_loop_zone_table(self):
        self.fake_connection.setup_response('25.36,11,18,1.6,54,1,3,55.68;0')
        response = self.dut.get_control_loop_zone_table(2, 9)

        self.assertEqual(response.upper_bound, 25.36)
        self.assertEqual(response.proportional, 11)
        self.assertEqual(response.integral, 18)
        self.assertEqual(response.derivative, 1.6)
        self.assertEqual(response.manual_out_value, 54)
        self.assertEqual(response.heater_range, Model336HeaterRange.LOW)
        self.assertEqual(response.channel, Model336InputChannel.CHANNEL_C)
        self.assertEqual(response.rate, 55.68)

        self.assertIn("ZONE? 2,9", self.fake_connection.get_outgoing_message())


class TestBasicCommands(TestWithFakeModel336):

    def test_set_alarm_parameters(self):
        self.fake_connection.setup_response('0')
        alarm = AlarmSettings(320.15, 210.54, 3, False, True, True)
        self.dut.set_alarm_parameters('A', True, alarm)
        self.assertIn("ALARM A,1,320.15,210.54,3,0,1,1", self.fake_connection.get_outgoing_message())

    def test_set_monitor_output_heater(self):
        self.fake_connection.setup_response('0')
        self.dut.set_monitor_output_heater(4, Model336InputChannel.CHANNEL_D, Model336InputSensorUnits.SENSOR,
                                            236.54, 200.36, Model336Polarity.BIPOLAR)
        self.assertIn("ANALOG 4,4,3,236.54,200.36,1", self.fake_connection.get_outgoing_message())

    def test_set_autotune(self):
        self.fake_connection.setup_response('0')
        self.fake_connection.setup_response('0,0,0;0')
        self.dut.set_autotune(2, Model336AutoTuneMode.P_I)
        self.assertIn("ATUNE 2,1", self.fake_connection.get_outgoing_message())

    def test_set_brightness(self):
        self.fake_connection.setup_response('0')
        self.dut.set_contrast_level(15)
        self.assertIn("BRIGT 15", self.fake_connection.get_outgoing_message())

    def test_set_curve_header(self):
        self.fake_connection.setup_response('0')
        curve_header = Model336CurveHeader("some_curve", "5555444411", Model336CurveFormat.MILLIVOLT_PER_KELVIN, 15.65,
                                           Model336CurveTemperatureCoefficients.NEGATIVE)
        self.dut.set_curve_header(25, curve_header)
        self.assertIn("CRVHDR 25,\"some_curve\",\"5555444411\",1,1", self.fake_connection.get_outgoing_message())

    def test_set_curve_data_point(self):
        self.fake_connection.setup_response('0')
        self.dut.set_curve_data_point(25, 150, 0.5214, 4.35)
        self.assertIn("CRVPT 25,150,0.5214,4.35", self.fake_connection.get_outgoing_message())

    def test_set_diode_excitation_current(self):
        self.fake_connection.setup_response('0')
        self.dut.set_diode_excitation_current("A", Model336DiodeCurrent.TEN_MICROAMPS)
        self.assertIn("DIOCUR A,0", self.fake_connection.get_outgoing_message())

    def test_set_display_field_settings(self):
        self.fake_connection.setup_response('0')
        self.dut.set_display_field_settings(4, Model336InputChannel.CHANNEL_C, Model336DisplayUnits.KELVIN)
        self.assertIn("DISPFLD 4,3,1", self.fake_connection.get_outgoing_message())

    def test_set_display_setup_custom(self):
        self.fake_connection.setup_response('0')
        self.dut.set_display_setup(Model336DisplaySetupMode.CUSTOM, Model336DisplayFields.LARGE_4, 1)
        self.assertIn("DISPLAY 4,1,1", self.fake_connection.get_outgoing_message())

    def test_set_display_setup_all_inputs(self):
        self.fake_connection.setup_response('0')
        self.dut.set_display_setup(Model336DisplaySetupMode.ALL_INPUTS, Model336DisplayFieldsSize.SMALL)
        self.assertIn("DISPLAY 6,0,", self.fake_connection.get_outgoing_message())

    def test_set_display_setup(self):
        self.fake_connection.setup_response('0')
        self.dut.set_display_setup(Model336DisplaySetupMode.FOUR_LOOP)
        self.assertIn("DISPLAY 5,,", self.fake_connection.get_outgoing_message())

    def test_set_filter(self):
        self.fake_connection.setup_response('0')
        self.dut.set_filter("A", True, 15, 2)
        self.assertIn("FILTER A,1,15,2", self.fake_connection.get_outgoing_message())

    def test_set_heater_setup(self):
        self.fake_connection.setup_response('0')
        self.dut.set_heater_setup(1, Model336HeaterResistance.HEATER_50_OHM, 0.75, Model336HeaterOutputUnits.POWER)
        self.assertIn("HTRSET 1,2,0,0.75,2", self.fake_connection.get_outgoing_message())

    def test_set_ieee_488(self):
        self.fake_connection.setup_response('0')
        self.dut.set_ieee_488(25)
        self.assertIn("IEEE 25", self.fake_connection.get_outgoing_message())

    def test_set_input_curve_no_error(self):
        self.fake_connection.setup_response('0')
        self.fake_connection.setup_response('22;0')
        self.dut.set_input_curve(1, 22)
        self.assertIn('INCRV 1,22', self.fake_connection.get_outgoing_message())

    def test_set_input_curve_error(self):
        self.fake_connection.setup_response('0')
        self.fake_connection.setup_response('0;0')
        with self.assertRaisesRegex(InstrumentException, r'The specified curve type does not match the configured '
                                                         r'input type'):
            self.dut.set_input_curve(1, 22)
        self.assertIn("INCRV 1,22", self.fake_connection.get_outgoing_message())

    def test_set_interface(self):
        self.fake_connection.setup_response('0')
        self.dut.set_interface(Model336Interface.ETHERNET)
        self.assertIn("INTSEL 1", self.fake_connection.get_outgoing_message())

    def test_set_input_sensor(self):
        self.fake_connection.setup_response('0')
        sensor_parameters = Model336InputSensorSettings(Model336InputSensorType.NTC_RTD, False, True,
                                                        Model336InputSensorUnits.KELVIN,
                                                        Model336RTDRange.THREE_THOUSAND_OHM)
        self.dut.set_input_sensor("C", sensor_parameters)
        self.assertIn("INTYPE C,3,0,5,1,1", self.fake_connection.get_outgoing_message())

    def test_set_led_state(self):
        self.fake_connection.setup_response('0')
        self.dut.set_led_state(True)
        self.assertIn('LEDS 1', self.fake_connection.get_outgoing_message())

    def test_set_keypad_lock(self):
        self.fake_connection.setup_response('0')
        self.dut.set_keypad_lock(True, 123)
        self.assertIn('LOCK 1,123', self.fake_connection.get_outgoing_message())

    def test_set_remote_interface_mode(self):
        self.fake_connection.setup_response('0')
        self.dut.set_remote_interface_mode(Model336InterfaceMode.REMOTE)
        self.assertIn('MODE 1', self.fake_connection.get_outgoing_message())

    def test_set_manual_output(self):
        self.fake_connection.setup_response('0')
        self.dut.set_manual_output(1, 98)
        self.assertIn('MOUT 1,98', self.fake_connection.get_outgoing_message())

    def test_set_heater_output_mode(self):
        self.fake_connection.setup_response('0')
        self.dut.set_heater_output_mode(1, Model336HeaterOutputMode.MONITOR_OUT,
                                        Model336InputChannel.CHANNEL_B, True)
        self.assertIn("OUTMODE 1,4,2,1", self.fake_connection.get_outgoing_message())

    def test_set_heater_pid(self):
        self.fake_connection.setup_response('0')
        self.dut.set_heater_pid(1, 10, 6.9, 8.7)
        self.assertIn("PID 1,10,6.9,8.7", self.fake_connection.get_outgoing_message())

    def test_set_heater_range(self):
        self.fake_connection.setup_response('0')
        self.dut.set_heater_range(3, Model336HeaterVoltageRange.VOLTAGE_ON)
        self.assertIn("RANGE 3,1", self.fake_connection.get_outgoing_message())

    def test_set_setpoint_ramp_parameter(self):
        self.fake_connection.setup_response('0')
        self.dut.set_setpoint_ramp_parameter(2, True, 55)
        self.assertIn("RAMP 2,1,55", self.fake_connection.get_outgoing_message())

    def test_turn_relay_on(self):
        self.fake_connection.setup_response('0')
        self.dut.turn_relay_on(2)
        self.assertIn("RELAY 2,1,,", self.fake_connection.get_outgoing_message())

    def test_turn_relay_off(self):
        self.fake_connection.setup_response('0')
        self.dut.turn_relay_off(2)
        self.assertIn("RELAY 2,0,,", self.fake_connection.get_outgoing_message())

    def test_set_relay_alarms(self):
        self.fake_connection.setup_response('0')
        self.dut.set_relay_alarms(1, "A", Model336RelayControlAlarm.HIGH_ALARM)
        self.assertIn("RELAY 1,2,A,1", self.fake_connection.get_outgoing_message())

    def test_set_soft_cal_curve_dt_470(self):
        self.fake_connection.setup_response('0')
        self.dut.set_soft_cal_curve_dt_470(25, 1111111111, (54.65, 0.658), (65.36, 0.589), (78.95, 0.521))
        self.assertIn("SCAL 1,25,1111111111,54.65,0.658,65.36,0.589,78.95,0.521",
                      self.fake_connection.get_outgoing_message())

    def test_set_soft_cal_curve_pt_100(self):
        self.fake_connection.setup_response('0')
        self.dut.set_soft_cal_curve_pt_100(25, 1111111111, (54.65, 0.658), (65.36, 0.589), (78.95, 0.521))
        self.assertIn("SCAL 6,25,1111111111,54.65,0.658,65.36,0.589,78.95,0.521",
                      self.fake_connection.get_outgoing_message())

    def test_set_soft_cal_curve_pt_1000(self):
        self.fake_connection.setup_response('0')
        self.dut.set_soft_cal_curve_pt_1000(25, 1111111111, (54.65, 0.658), (65.36, 0.589), (78.95, 0.521))
        self.assertIn("SCAL 7,25,1111111111,54.65,0.658,65.36,0.589,78.95,0.521",
                      self.fake_connection.get_outgoing_message())

    def test_set_control_setpoint(self):
        self.fake_connection.setup_response('0')
        self.dut.set_control_setpoint(1, 210)
        self.assertIn("SETP 1,210", self.fake_connection.get_outgoing_message())

    def test_set_temperature_limit(self):
        self.fake_connection.setup_response('0')
        self.dut.set_temperature_limit('A', 200)
        self.assertIn("TLIMIT A,200", self.fake_connection.get_outgoing_message())

    def test_set_warmup_supply_parameter(self):
        self.fake_connection.setup_response('0')
        self.dut.set_warmup_supply_parameter(3, Model336ControlTypes.CONTINUOUS, 50.5)
        self.assertIn("WARMUP 3,1,50.5", self.fake_connection.get_outgoing_message())

    def test_set_website_login(self):
        self.fake_connection.setup_response('0')
        self.dut.set_website_login("MyUsername", "MyPassword")
        self.assertIn("WEBLOG \"MyUsername\",\"MyPassword\"", self.fake_connection.get_outgoing_message())

    def test_set_control_loop_zone_table(self):
        self.fake_connection.setup_response('0')
        control_loop_zone_parameters = Model336ControlLoopZoneSettings(215.36, 10, 15, 3.2, 65,
                                                                       Model336HeaterRange.HIGH,
                                                                       Model336InputChannel.CHANNEL_A, 25.36)
        self.dut.set_control_loop_zone_table(1, 5, control_loop_zone_parameters)
        self.assertEqual("ZONE 1,5,215.36,10,15,3.2,65,3,1,25.36;*ESR?", self.fake_connection.get_outgoing_message())
