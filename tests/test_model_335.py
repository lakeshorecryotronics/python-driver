from tests.utils import TestWithFakeModel335
from lakeshore import InstrumentException
from lakeshore.model_335 import *


class TestBasicReadings(TestWithFakeModel335):

    def test_get_celsius_reading(self):
        self.fake_connection.setup_response('0.05;0')
        response = self.dut.get_celsius_reading("A")
        self.assertAlmostEqual(response, 0.05)
        self.assertIn("CRDG? A", self.fake_connection.get_outgoing_message())

    def test_get_thermocouple_junction_temp(self):
        self.fake_connection.setup_response('35.658;0')
        response = self.dut.get_thermocouple_junction_temp()
        self.assertAlmostEqual(response, 35.658)
        self.assertIn("TEMP?", self.fake_connection.get_outgoing_message())


class TestBasicSettings(TestWithFakeModel335):

    def test_set_operation_event_enable(self):
        self.fake_connection.setup_response('0')
        bits = Model335OperationEvent(True, True, False, False, False, True, True, True)
        self.dut.set_operation_event_enable(bits)
        self.assertIn("OPSTE 227", self.fake_connection.get_outgoing_message())

    def test_get_operation_event_enable(self):
        self.fake_connection.setup_response('227;0')
        response = self.dut.get_operation_event_enable()

        self.assertEqual(response.alarm, True)
        self.assertEqual(response.sensor_overload, True)
        self.assertEqual(response.loop_2_ramp_done, False)
        self.assertEqual(response.loop_1_ramp_done, False)
        self.assertEqual(response.new_sensor_reading, False)
        self.assertEqual(response.autotune_process_completed, True)
        self.assertEqual(response.calibration_error, True)
        self.assertEqual(response.processor_communication_error, True)

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

    def test_set_brightness(self):
        self.fake_connection.setup_response('0')
        self.dut.set_brightness(Model335BrightnessLevel.HALF)
        self.assertIn("BRIGT 1", self.fake_connection.get_outgoing_message())


class TestBasicQueries(TestWithFakeModel335):

    def test_get_monitor_output_heater(self):
        self.fake_connection.setup_response('1,1,+236.54,+200.36,1;0')
        response = self.dut.get_monitor_output_heater()
        monitor_out = {"channel": Model335InputSensor.CHANNEL_A,
                       "units": Model335MonitorOutUnits.KELVIN,
                       "high_value": 236.54,
                       "low_value": 200.36,
                       "polarity": Model335Polarity.BIPOLAR}

        self.assertDictEqual(response, monitor_out)
        self.assertIn("ANALOG? 2", self.fake_connection.get_outgoing_message())

    def test_get_diode_excitation_current(self):
        self.fake_connection.setup_response('1;0')
        response = self.dut.get_diode_excitation_current("A")
        self.assertEqual(response, Model335DiodeCurrent.ONE_MILLIAMP)
        self.assertIn("DIOCUR? A", self.fake_connection.get_outgoing_message())

    def test_get_display_setup(self):
        self.fake_connection.setup_response('2;0')
        response = self.dut.get_display_setup()
        self.assertEqual(response.name, "TWO_INPUT_A")
        self.assertIn("DISPLAY?", self.fake_connection.get_outgoing_message())

    def test_get_display_field_settings(self):
        self.fake_connection.setup_response('1,1;0')
        response = self.dut.get_display_field_settings(4)
        display_field = {'input_channel': Model335DisplayInputChannel.INPUT_A,
                         'display_units': Model335DisplayFieldUnits.KELVIN}
        self.assertDictEqual(response, display_field)
        self.assertIn("DISPFLD? 4", self.fake_connection.get_outgoing_message())

    def test_get_filter(self):
        self.fake_connection.setup_response('1,32,5;0')
        response = self.dut._get_filter("A")
        filter_settings = {"filter_enable": True,
                           "data_points": 32,
                           "reset_threshold": 5}
        self.assertDictEqual(response, filter_settings)
        self.assertIn("FILTER? A", self.fake_connection.get_outgoing_message())

    def test_get_heater_output(self):
        self.fake_connection.setup_response('55.62;0')
        response = self.dut.get_heater_output(1)
        self.assertEqual(response, 55.62)
        self.assertIn("HTR? 1", self.fake_connection.get_outgoing_message())

    def test_get_heater_status(self):
        self.fake_connection.setup_response('1;0')
        response = self.dut.get_heater_status(1)
        self.assertEqual(response, Model335HeaterError.HEATER_OPEN_LOAD)
        self.assertIn("HTRST? 1", self.fake_connection.get_outgoing_message())

    def test_get_heater_setup_user(self):
        self.fake_connection.setup_response('0,2,0,1.03,2;0')
        response = self.dut.get_heater_setup(1)
        heater_setup = {"output_type": Model335HeaterOutType.CURRENT,
                        "heater_resistnace": Model335HeaterResistance.HEATER_50_OHM,
                        "max_current": 1.03,
                        "output_display_mode": Model335HeaterOutputDisplay.POWER}
        self.assertDictEqual(response, heater_setup)
        self.assertIn("HTRSET? 1", self.fake_connection.get_outgoing_message())

    def test_get_heater_setup_non_user_current(self):
        self.fake_connection.setup_response('0,1,1,0,2;0')
        response = self.dut.get_heater_setup(1)
        heater_setup = {"output_type": Model335HeaterOutType.CURRENT,
                        "heater_resistnace": Model335HeaterResistance.HEATER_25_OHM,
                        "max_current": 0.707,
                        "output_display_mode": Model335HeaterOutputDisplay.POWER}
        self.assertDictEqual(response, heater_setup)
        self.assertIn("HTRSET? 1", self.fake_connection.get_outgoing_message())

    def test_get_input_curve(self):
        self.fake_connection.setup_response('53;0')
        response = self.dut.get_input_curve("A")
        self.assertEqual(response, 53)
        self.assertIn("INCRV?", self.fake_connection.get_outgoing_message())

    def test_get_ieee_488(self):
        self.fake_connection.setup_response('25;0')
        response = self.dut.get_ieee_488()
        self.assertEqual(response, 25)
        self.assertIn('IEEE?', self.fake_connection.get_outgoing_message())

    def test_get_input_sensor(self):
        self.fake_connection.setup_response('1,0,0,1,1;0')
        response = self.dut.get_input_sensor("A")
        sensor_parameters = Model335InputSensorSettings(Model335InputSensorType.DIODE, False,
                                                        True, Model335InputSensorUnits.KELVIN,
                                                        Model335DiodeRange.TWO_POINT_FIVE_VOLTS)

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
        self.assertEqual(response, Model335InterfaceMode.REMOTE_LOCAL_LOCK)
        self.assertIn('MODE?', self.fake_connection.get_outgoing_message())

    def test_get_manual_output(self):
        self.fake_connection.setup_response('24.3;0')
        response = self.dut.get_manual_output(1)
        self.assertEqual(response, 24.3)
        self.assertIn('MOUT? 1', self.fake_connection.get_outgoing_message())

    def test_get_heater_output_mode(self):
        self.fake_connection.setup_response('1,1,0;0')
        response = self.dut.get_heater_output_mode(1)

        heater_output_settings = {"mode": Model335HeaterOutputMode.CLOSED_LOOP,
                                  "channel": Model335InputSensor.CHANNEL_A,
                                  "powerup_enable": False}
        self.assertDictEqual(response, heater_output_settings)
        self.assertIn("OUTMODE? 1", self.fake_connection.get_outgoing_message())

    def test_get_heater_pid(self):
        self.fake_connection.setup_response('4.25,6.1,0;0')
        response = self.dut.get_heater_pid(1)
        pid_settings = {"gain": 4.25,
                        "integral": 6.1,
                        "derivative": 0}
        self.assertDictEqual(response, pid_settings)

    def test_get_output_2_polarity(self):
        self.fake_connection.setup_response('1;0')
        response = self.dut.get_output_2_polarity()
        self.assertEqual(response, Model335Polarity.BIPOLAR)
        self.assertIn("POLARITY?", self.fake_connection.get_outgoing_message())

    def test_get_heater_range(self):
        self.fake_connection.setup_response('1;0')
        self.fake_connection.setup_response('1;0')
        response = self.dut.get_heater_range(2)
        self.assertEqual(response, Model335HeaterVoltageRange.VOLTAGE_ON)
        self.assertIn("RANGE? 2", self.fake_connection.get_outgoing_message())

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
                       'alarm_relay_trigger_type': Model335RelayControlAlarm.BOTH_ALARMS}
        self.assertDictEqual(response, relay_alarm)
        self.assertIn("RELAY? 1", self.fake_connection.get_outgoing_message())

    def test_get_relay_control_mode(self):
        self.fake_connection.setup_response('2,A,2;0')
        response = self.dut.get_relay_control_mode(1)
        self.assertEqual(response, Model335RelayControlMode.ALARMS)
        self.assertIn("RELAY? 1", self.fake_connection.get_outgoing_message())

    def test_get_relay_status(self):
        self.fake_connection.setup_response('1;0')
        response = self.dut.get_relay_status(1)
        self.assertEqual(response, True)
        self.assertIn("RELAYST? 1", self.fake_connection.get_outgoing_message())

    def test_get_input_reading_status(self):
        self.fake_connection.setup_response('128;0')
        response = self.dut.get_input_reading_status("A")

        self.assertEqual(response.invalid_reading, False)
        self.assertEqual(response.temp_underrange, False)
        self.assertEqual(response.temp_overrange, False)
        self.assertEqual(response.sensor_units_zero, False)
        self.assertEqual(response.sensor_units_overrange, True)

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
        self.fake_connection.setup_response('0,1,1,7;0')
        response = self.dut.get_tuning_control_status()
        tuning_control = {"active_tuning_enable": False,
                          "output": 1,
                          "tuning_error": True,
                           "stage_status": 7}
        self.assertDictEqual(response, tuning_control)
        self.assertIn("TUNEST?", self.fake_connection.get_outgoing_message())

    def test_get_warmup_supply(self):
        self.fake_connection.setup_response('0,56.35;0')
        response = self.dut.get_warmup_supply()
        warmup_supply = {"control": Model335WarmupControl.AUTO_OFF,
                         "percentage": 56.35}
        self.assertDictEqual(response, warmup_supply)
        self.assertIn("WARMUP? 2", self.fake_connection.get_outgoing_message())

    def test_get_control_loop_zone_table(self):
        self.fake_connection.setup_response('+000.00,+0050.0,+0020.0,+000.0,+000.00,0,0,+000.0;0')
        response = self.dut.get_control_loop_zone_table(1, 5)
        control_loop_zone = Model335ControlLoopZoneSettings(0.0, 50, 20, 0.0, 0, Model335HeaterRange.OFF,
                                                            Model335InputSensor.NONE, 0.0)

        self.assertAlmostEqual(response.upper_bound, control_loop_zone.upper_bound)
        self.assertAlmostEqual(response.proportional, control_loop_zone.proportional)
        self.assertAlmostEqual(response.integral, control_loop_zone.integral)
        self.assertAlmostEqual(response.derivative, control_loop_zone.derivative)
        self.assertAlmostEqual(response.manual_output_value, control_loop_zone.manual_output_value)
        self.assertEqual(response.heater_range.name, control_loop_zone.heater_range.name)
        self.assertEqual(response.channel.name, control_loop_zone.channel.name)
        self.assertEqual(response.ramp_rate, control_loop_zone.ramp_rate)

        self.assertIn("ZONE? 1,5", self.fake_connection.get_outgoing_message())


class TestBasicCommands(TestWithFakeModel335):

    def test_set_monitor_output_heater(self):
        # check error response from command
        self.fake_connection.setup_response('0')
        self.dut.set_monitor_output_heater(Model335InputSensor.CHANNEL_A, 236.54, 200.36,
                                           Model335MonitorOutUnits.KELVIN,
                                           Model335Polarity.BIPOLAR)
        self.assertIn("ANALOG 2,1,1,236.54,200.36,1", self.fake_connection.get_outgoing_message())

    def test_set_autotune(self):
        self.fake_connection.setup_response('0')
        self.fake_connection.setup_response('1,1,0;0')
        self.dut.set_autotune(1, Model335AutoTuneMode.P_I)
        self.assertIn("ATUNE 1,1", self.fake_connection.get_outgoing_message())

    def test_set_diode_excitation_current(self):
        self.fake_connection.setup_response('0')
        self.dut.set_diode_excitation_current("A", Model335DiodeCurrent.TEN_MICROAMPS)
        self.assertIn("DIOCUR A,0", self.fake_connection.get_outgoing_message())

    def test_set_display_setup(self):
        self.fake_connection.setup_response('0')
        self.dut.set_display_setup(Model335DisplaySetup.TWO_INPUT_A)
        self.assertIn("DISPLAY 2", self.fake_connection.get_outgoing_message())

    def test_set_display_field(self):
        self.fake_connection.setup_response('0')
        self.dut.set_display_field_settings(1, Model335DisplayInputChannel.SETPOINT_2,
                                            Model335DisplayFieldUnits.CELSIUS)
        self.assertIn("DISPFLD 1,4,2", self.fake_connection.get_outgoing_message())

    def test_set_filter(self):
        self.fake_connection.setup_response('0')
        self.dut._set_filter("A", True, 35, 7)
        self.assertIn("FILTER A,1,35,7", self.fake_connection.get_outgoing_message())

    def test_set_heater_setup_one(self):
        self.fake_connection.setup_response('0')
        self.dut.set_heater_setup_one(Model335HeaterResistance.HEATER_50_OHM, 1.35,
                                      Model335HeaterOutputDisplay.POWER)
        self.assertIn("HTRSET 1,0,2,0,1.35,2", self.fake_connection.get_outgoing_message())

    def test_set_heater_setup_two(self):
        self.fake_connection.setup_response('0')
        self.dut.set_heater_setup_two(Model335HeaterOutType.CURRENT,
                                      Model335HeaterResistance.HEATER_25_OHM,
                                      1.85, Model335HeaterOutputDisplay.CURRENT)
        self.assertIn("HTRSET 2,0,1,0,1.85,1", self.fake_connection.get_outgoing_message())

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

    def test_set_input_sensor(self):
        self.fake_connection.setup_response('0')
        sensor_parameters = Model335InputSensorSettings(Model335InputSensorType.DIODE, False, True,
                                                        Model335InputSensorUnits.KELVIN,
                                                        Model335DiodeRange.TWO_POINT_FIVE_VOLTS)
        self.dut.set_input_sensor("A", sensor_parameters)
        self.assertIn("INTYPE A,1,0,0,1,1", self.fake_connection.get_outgoing_message())

    def test_set_ieee_488(self):
        self.fake_connection.setup_response('0')
        self.dut.set_ieee_488(25)
        self.assertIn('IEEE 25', self.fake_connection.get_outgoing_message())

    def test_set_led_state(self):
        self.fake_connection.setup_response('0')
        self.dut.set_led_state(True)
        self.assertIn('LEDS 1', self.fake_connection.get_outgoing_message())

    def test_set_keypad_lock(self):
        self.fake_connection.setup_response('0')
        self.dut.set_keypad_lock(True, 123)
        self.assertIn('LOCK 1,123', self.fake_connection.get_outgoing_message())

    def test_reset_min_max_data(self):
        self.fake_connection.setup_response('0')
        self.dut.reset_min_max_data()
        self.assertIn('MNMXRST', self.fake_connection.get_outgoing_message())

    def test_set_remote_interface_mode(self):
        self.fake_connection.setup_response('0')
        self.dut.set_remote_interface_mode(Model335InterfaceMode.REMOTE)
        self.assertIn('MODE 1', self.fake_connection.get_outgoing_message())

    def test_set_manual_output(self):
        self.fake_connection.setup_response('0')
        self.dut.set_manual_output(1, 98)
        self.assertIn('MOUT 1,98', self.fake_connection.get_outgoing_message())

    def test_set_heater_output_mode(self):
        self.fake_connection.setup_response('0')
        self.dut.set_heater_output_mode(1, Model335HeaterOutputMode.CLOSED_LOOP,
                                        Model335InputSensor.CHANNEL_A, False)
        self.assertIn("OUTMODE 1,1,1,0", self.fake_connection.get_outgoing_message())

    def test_set_heater_pid(self):
        self.fake_connection.setup_response('0')
        self.dut.set_heater_pid(1, 10, 6.9, 8.7)
        self.assertIn("PID 1,10,6.9,8.7", self.fake_connection.get_outgoing_message())

    def test_set_output_two_polarity(self):
        self.fake_connection.setup_response('0')
        self.dut.set_output_two_polarity(Model335Polarity.UNIPOLAR)
        self.assertIn("POLARITY 2,0", self.fake_connection.get_outgoing_message())

    def test_set_setpoint_ramp_parameter(self):
        self.fake_connection.setup_response('0')
        self.dut.set_setpoint_ramp_parameter(2, True, 55)
        self.assertIn("RAMP 2,1,55", self.fake_connection.get_outgoing_message())

    def test_set_heater_range(self):
        self.fake_connection.setup_response('0')
        self.dut.set_heater_range(1, Model335HeaterRange.MEDIUM)
        self.assertIn("RANGE 1,2", self.fake_connection.get_outgoing_message())

    def test_turn_relay_on(self):
        self.fake_connection.setup_response('0')
        self.dut.turn_relay_on(1)
        self.assertIn("RELAY 1,1,,", self.fake_connection.get_outgoing_message())

    def test_turn_relay_off(self):
        self.fake_connection.setup_response('0')
        self.dut.turn_relay_off(1)
        self.assertIn("RELAY 1,0,,", self.fake_connection.get_outgoing_message())

    def test_set_relay_alarms(self):
        self.fake_connection.setup_response('0')
        self.dut.set_relay_alarms(1, "A", Model335RelayControlAlarm.HIGH_ALARM)
        self.assertIn("RELAY 1,2,A,1", self.fake_connection.get_outgoing_message())

    def test_set_soft_cal_curve_dt_470(self):
        self.fake_connection.setup_response('0')
        self.dut.set_soft_cal_curve_dt_470(21, 2563847891, (45.6, 1.025), (65.3, 1.05), (72.9, 0.95))
        self.assertIn("SCAL 1,21,2563847891,45.6,1.025,65.3,1.05,72.9,0.95",
                      self.fake_connection.get_outgoing_message())

    def test_set_soft_cal_curve_pt_100(self):
        self.fake_connection.setup_response('0')
        self.dut.set_soft_cal_curve_pt_100(21, 2563847891, (45.6, 1.025), (65.3, 1.05), (72.9, 0.95))
        self.assertIn("SCAL 6,21,2563847891,45.6,1.025,65.3,1.05,72.9,0.95",
                      self.fake_connection.get_outgoing_message())

    def test_set_soft_cal_curve_pt_1000(self):
        self.fake_connection.setup_response('0')
        self.dut.set_soft_cal_curve_pt_1000(21, 2563847891, (45.6, 1.025), (65.3, 1.05), (72.9, 0.95))
        self.assertIn("SCAL 7,21,2563847891,45.6,1.025,65.3,1.05,72.9,0.95",
                      self.fake_connection.get_outgoing_message())

    def test_set_control_setpoint(self):
        self.fake_connection.setup_response('0')
        self.dut.set_control_setpoint(1, 210)
        self.assertIn("SETP 1,210", self.fake_connection.get_outgoing_message())

    def test_set_temperature_limit(self):
        self.fake_connection.setup_response('0')
        self.dut.set_temperature_limit('A', 200)
        self.assertIn("TLIMIT A,200", self.fake_connection.get_outgoing_message())

    def test_set_warmup_supply(self):
        # Output 2 in voltage mode HTRSET? query
        self.fake_connection.setup_response('1,2,1,+0.100,2;0')
        self.fake_connection.setup_response('0')
        self.dut.set_warmup_supply(Model335WarmupControl.AUTO_OFF, 50.45)
        self.assertIn("HTRSET? 2", self.fake_connection.get_outgoing_message())
        self.assertIn("WARMUP 2,0,50.45", self.fake_connection.get_outgoing_message())

    def test_set_control_loop_zone_table(self):
        self.fake_connection.setup_response('0')
        control_loop = Model335ControlLoopZoneSettings(256.21, 523.6, 23.152, 6.358, 98.6, Model335HeaterRange.LOW,
                                                        Model335InputSensor.CHANNEL_A, 26.8)
        self.dut.set_control_loop_zone_table(1, 5, control_loop)
        self.assertIn("ZONE 1,5,256.21,523.6,23.152,6.358,98.6,1,1,26.8", self.fake_connection.get_outgoing_message())
