from tests.utils import TestWithFakeModel372
from lakeshore import temperature_controllers, InstrumentException
from lakeshore.temperature_controllers import CurveFormat, CurveTemperatureCoefficient, CurveHeader, \
    StandardEventRegister, OperationEvent


class TestBasicMethods(TestWithFakeModel372):
    def test_get_kelvin_reading(self):
        self.fake_connection.setup_response('273.2;0')
        response = self.dut.get_kelvin_reading("1")
        self.assertAlmostEqual(response, 273.2)
        self.assertIn("KRDG? 1", self.fake_connection.get_outgoing_message())

    def test_set_filter(self):
        self.fake_connection.setup_response('0;0')
        self.dut._set_filter("A", True, 2, 50,)
        self.assertIn('FILTER A,1,2,50', self.fake_connection.get_outgoing_message())

    def test_set_curve_data_point(self):
        self.fake_connection.setup_response('0;0')
        self.dut.set_curve_data_point(2, 50, 1.2, 3.4)
        self.assertIn('CRVPT 2,50,1.2,3.4', self.fake_connection.get_outgoing_message())

    def test_set_sensor_name(self):
        self.fake_connection.setup_response('0;0')
        self.dut.set_sensor_name(1, "MySensor")
        self.assertIn('INNAME 1,\"MySensor\"', self.fake_connection.get_outgoing_message())

    def test_delete_curve(self):
        self.fake_connection.setup_response('0;0')
        self.dut.delete_curve(2)
        self.assertIn('CRVDEL 2', self.fake_connection.get_outgoing_message())

    def test_set_curve_header(self):
        self.fake_connection.setup_response('0;0')
        curve_header = CurveHeader('Curve1', '1234',
                                   CurveFormat.VOLTS_PER_KELVIN,
                                   12.3, CurveTemperatureCoefficient.NEGATIVE)
        self.dut.set_curve_header(2, curve_header)
        self.assertIn('CRVHDR 2,"Curve1","1234",2,12.3,1;*ESR?', self.fake_connection.get_outgoing_message())

    def test_get_temperature_limit(self):
        self.fake_connection.setup_response('1234;0')
        # Send 0 to satisfy error checking in command/query methods
        self.fake_connection.setup_response('0')
        response = self.dut.get_temperature_limit("A")
        self.assertAlmostEqual(response, 1234)
        self.assertIn('TLIMIT? A', self.fake_connection.get_outgoing_message())

    def test_set_temperature_limit(self):
        self.fake_connection.setup_response('0;0')
        self.dut.set_temperature_limit("A", 1234)
        self.assertIn('TLIMIT A,1234', self.fake_connection.get_outgoing_message())

    def test_set_control_setpoint(self):
        self.fake_connection.setup_response('0')
        self.dut.set_control_setpoint(2, 4.56)
        self.assertIn('SETP 2,4.56', self.fake_connection.get_outgoing_message())

    def test_get_control_setpoint(self):
        self.fake_connection.setup_response('4.56;0')
        # Send 0 to satisfy error checking in command/query methods
        self.fake_connection.setup_response('0')
        response = self.dut.get_control_setpoint(2)
        self.assertAlmostEqual(response, 4.56)
        self.assertIn('SETP? 2', self.fake_connection.get_outgoing_message())

    def test_get_relay_status(self):
        self.fake_connection.setup_response('0;0')
        # Send 0 to satisfy error checking in command/query methods
        self.fake_connection.setup_response('0')
        response = self.dut.get_relay_status(2)
        self.assertEqual(response, False)
        self.assertIn('RELAYST? 2', self.fake_connection.get_outgoing_message())

    def test_get_setpoint_ramp_status(self):
        self.fake_connection.setup_response('0;0')
        # Send 0 to satisfy error checking in command/query methods
        self.fake_connection.setup_response('0')
        response = self.dut.get_setpoint_ramp_status(1)
        self.assertEqual(response, False)
        self.assertIn('RAMPST? 1', self.fake_connection.get_outgoing_message())

    def test_get_manual_output(self):
        self.fake_connection.setup_response('1.23;0')
        # Send 0 to satisfy error checking in command/query methods
        self.fake_connection.setup_response('0')
        response = self.dut.get_manual_output(1)
        self.assertAlmostEqual(response, 1.23)
        self.assertIn('MOUT? 1', self.fake_connection.get_outgoing_message())

    def test_set_manual_output(self):
        self.fake_connection.setup_response('0;0')
        self.dut.set_manual_output(1, 1.23)
        self.assertIn('MOUT 1,1.23', self.fake_connection.get_outgoing_message())

    def test_get_led_state(self):
        self.fake_connection.setup_response('0;0')
        response = self.dut.get_led_state()
        self.assertEqual(response, False)
        self.assertIn('LEDS?', self.fake_connection.get_outgoing_message())

    def test_set_led_state(self):
        self.fake_connection.setup_response('0;0')
        self.dut.set_led_state(False)
        self.assertIn('LEDS 0', self.fake_connection.get_outgoing_message())

    def test_get_ieee_488(self):
        self.fake_connection.setup_response('123;0')
        # Send 0 to satisfy error checking in command/query methods
        self.fake_connection.setup_response('0')
        response = self.dut.get_ieee_488()
        self.assertAlmostEqual(response, 123)
        self.assertIn('IEEE?', self.fake_connection.get_outgoing_message())

    def test_set_ieee_488(self):
        self.fake_connection.setup_response('0;0')
        self.dut.set_ieee_488(123)
        self.assertIn('IEEE 123', self.fake_connection.get_outgoing_message())

    def test_get_heater_output(self):
        self.fake_connection.setup_response('4.567;0')
        # Send 0 to satisfy error checking in command/query methods
        self.fake_connection.setup_response('0')
        response = self.dut.get_heater_output(2)
        self.assertAlmostEqual(response, 4.567)
        self.assertIn('HTR? 2', self.fake_connection.get_outgoing_message())

    def test_reset_alarm_status(self):
        self.fake_connection.setup_response('0;0')
        self.dut.reset_alarm_status()
        self.assertIn('ALMRST', self.fake_connection.get_outgoing_message())

    def test_get_input_curve(self):
        self.fake_connection.setup_response('24;0')
        response = self.dut.get_input_curve('A')
        self.assertEqual(response, 24)
        self.assertIn('INCRV? A', self.fake_connection.get_outgoing_message())

    def test_set_input_curve_normal_input(self):
        # Satisfy the rate limit query
        self.fake_connection.setup_response('1')
        self.fake_connection.setup_response('24;0')
        self.dut.set_input_curve("A", 24)
        self.assertIn('INCRV A,24', self.fake_connection.get_outgoing_message())

    def test_set_input_curve_0_input(self):
        # Checks that 0 is handled as a valid input and doesn't throw the exception
        self.fake_connection.setup_response('0;0')
        self.dut.set_input_curve("A", 0)
        self.assertIn('INCRV A,0', self.fake_connection.get_outgoing_message())

    def test_set_input_curve_exception_thrown(self):
        # OPC rate limit
        self.fake_connection.setup_response('1')
        # get input curve response
        self.fake_connection.setup_response('0;0')
        with self.assertRaisesRegex(InstrumentException, r'The specified curve type does not match the configured '
                                                         r'input type'):
            self.dut.set_input_curve("A", 24)

    def test_get_filter(self):
        expected_response = {'filter_enable': True,
                             'data_points': 20,
                             'reset_threshold': 10}
        self.fake_connection.setup_response('1,20,10;0')
        response = self.dut._get_filter(1)
        self.assertDictEqual(response, expected_response)
        self.assertIn("FILTER? 1", self.fake_connection.get_outgoing_message())

    def test_get_sensor_reading(self):
        self.fake_connection.setup_response('123.45;0')
        response = self.dut.get_sensor_reading(2)
        self.assertAlmostEqual(response, 123.45)
        self.assertIn("SRDG? 2", self.fake_connection.get_outgoing_message())

    def test_get_sensor_name(self):
        self.fake_connection.setup_response('MySensor;0')
        response = self.dut.get_sensor_name(1)
        self.assertAlmostEqual(response, 'MySensor')
        self.assertIn("INNAME? 1", self.fake_connection.get_outgoing_message())

    def test_get_curve_data_point(self):
        data_point = (123.0, 456.0)
        self.fake_connection.setup_response('123,456;0')
        response = self.dut.get_curve_data_point(1, 2)
        self.assertAlmostEqual(response, data_point)
        self.assertIn("CRVPT? 1,2", self.fake_connection.get_outgoing_message())

    def test_get_curve_header(self):
        curve_header = CurveHeader('Curve1', '1234', CurveFormat.VOLTS_PER_KELVIN, 12.3,
                                   CurveTemperatureCoefficient.NEGATIVE)
        self.fake_connection.setup_response('Curve1,1234,2,12.3,1;0')
        response = self.dut.get_curve_header(2)

        self.assertEqual(response.curve_name, curve_header.curve_name)
        self.assertEqual(response.serial_number, curve_header.serial_number)
        self.assertEqual(response.temperature_limit, curve_header.temperature_limit)
        self.assertAlmostEqual(response.curve_data_format, curve_header.curve_data_format)
        self.assertEqual(response.coefficient, curve_header.coefficient)

        self.assertIn("CRVHDR? 2", self.fake_connection.get_outgoing_message())


class TestDictionaryMethods(TestWithFakeModel372):
    def test_get_alarm_status(self):
        alarm_status = {'high_state_enabled': False,
                        'low_state_enabled': True}

        self.fake_connection.setup_response('0,1;0')
        response = self.dut.get_alarm_status(1)
        self.assertDictEqual(response, alarm_status)
        self.assertIn('ALARMST? 1', self.fake_connection.get_outgoing_message())

    def test_set_keypad_lock(self):
        self.fake_connection.setup_response('0')
        self.dut.set_keypad_lock(False, 123)
        self.assertIn('LOCK 0,123', self.fake_connection.get_outgoing_message())

    def test_get_keypad_lock(self):
        keypad_lock = {'state': True,
                       'code': 123}
        self.fake_connection.setup_response('1,123;0')
        response = self.dut.get_keypad_lock()
        self.assertDictEqual(keypad_lock, response)
        self.assertIn('LOCK?', self.fake_connection.get_outgoing_message())

    def test_get_min_max_data(self):
        min_max = {'minimum': 123.456,
                   'maximum': 1567.89}
        self.fake_connection.setup_response('123.456,1567.89;0')
        response = self.dut.get_min_max_data(1)
        self.assertDictEqual(response, min_max)
        self.assertIn('MDAT? 1', self.fake_connection.get_outgoing_message())

    def test_set_heater_pid(self):
        self.fake_connection.setup_response('0')
        self.dut.set_heater_pid(1, 34.56, 56.78, 98.76)
        self.assertIn('PID 1,34.56,56.78,98.76', self.fake_connection.get_outgoing_message())

    def test_get_heater_pid(self):
        pid = {'gain': 34.56,
               'integral': 56.78,
               'ramp_rate': 98.76}

        self.fake_connection.setup_response('34.56,56.78,98.76;0')
        response = self.dut.get_heater_pid(2)
        self.assertDictEqual(response, pid)
        self.assertIn('PID? 2', self.fake_connection.get_outgoing_message())

    def test_set_setpoint_ramp_parameter(self):
        self.fake_connection.setup_response('0')
        self.dut.set_setpoint_ramp_parameter(0, True, 99.99)
        self.assertIn('RAMP 0,1,99.99', self.fake_connection.get_outgoing_message())

    def test_get_setpoint_ramp_parameter(self):
        ramp = {'ramp_enable': True,
                'rate_value': 99.99}
        self.fake_connection.setup_response('1,99.99;0')
        response = self.dut.get_setpoint_ramp_parameter(2)
        self.assertDictEqual(response, ramp)
        self.assertIn('RAMP? 2', self.fake_connection.get_outgoing_message())


class TestObjectMethods(TestWithFakeModel372):
    def test_set_alarm_parameters(self):
        alarm_settings = temperature_controllers.AlarmSettings(15.5, 1.34, 3.14, False, False, True)
        self.fake_connection.setup_response('0')
        self.dut.set_alarm_parameters(1, True, alarm_settings)
        self.assertIn('ALARM 1,1,15.5,1.34,3.14,0,0,1', self.fake_connection.get_outgoing_message())

    def test_get_alarm_parameters(self):
        alarm_settings = temperature_controllers.AlarmSettings(15.5, 1.34, 3.14, False, False, True)
        self.fake_connection.setup_response('1,15.5,1.34,3.14,0,0,1;0')
        response = self.dut.get_alarm_parameters(1)
        # Compare all variables
        self.assertAlmostEqual(response.high_value, alarm_settings.high_value)
        self.assertAlmostEqual(response.low_value, alarm_settings.low_value)
        self.assertAlmostEqual(response.deadband, alarm_settings.deadband)
        self.assertEqual(response.latch_enable, alarm_settings.latch_enable)
        self.assertEqual(response.visible, alarm_settings.visible)
        self.assertEqual(response.audible, alarm_settings.audible)

        self.assertIn('ALARM? 1', self.fake_connection.get_outgoing_message())

    def test_get_heater_status(self):
        heater_status = temperature_controllers.HeaterError(2)
        self.fake_connection.setup_response('2;0')
        response = self.dut.get_heater_status(2)
        self.assertEqual(response, heater_status)
        self.assertIn('HTRST? 2', self.fake_connection.get_outgoing_message())

    def test_set_remote_interface_mode(self):
        interface_mode = temperature_controllers.InterfaceMode(2)
        self.fake_connection.setup_response('0')
        self.dut.set_remote_interface_mode(interface_mode)
        self.assertIn('MODE 2', self.fake_connection.get_outgoing_message())

    def test_set_remote_interface_mode_with_int(self):
        interface_mode = 1
        self.fake_connection.setup_response('0')
        self.dut.set_remote_interface_mode(interface_mode)
        self.assertIn('MODE 1', self.fake_connection.get_outgoing_message())

    def test_get_remote_interface_mode(self):
        interface_mode = temperature_controllers.InterfaceMode(2)
        self.fake_connection.setup_response('2;0')
        response = self.dut.get_remote_interface_mode()
        self.assertEqual(response, interface_mode)
        self.assertIn('MODE?', self.fake_connection.get_outgoing_message())

    def test_set_relay_control_parameter_alarms(self):
        self.fake_connection.setup_response('0')
        self.dut.set_relay_alarms(1, "B", temperature_controllers.RelayControlAlarm.BOTH_ALARMS)
        self.assertIn("RELAY 1,2,B,2", self.fake_connection.get_outgoing_message())

    def test_set_relay_control_parameter_no_alarms(self):
        self.fake_connection.setup_response('0')
        self.dut.turn_relay_on(1)
        self.assertIn("RELAY 1,1,,", self.fake_connection.get_outgoing_message())

    def test_get_relay_alarm_control_parameters(self):
        self.fake_connection.setup_response("2,D1,0;0")
        expected_response = {'activating_input_channel': "D1",
                             'alarm_relay_trigger_type': temperature_controllers.RelayControlAlarm.LOW_ALARM}
        response = self.dut.get_relay_alarm_control_parameters(2)
        self.assertDictEqual(response, expected_response)
        self.assertIn("RELAY? 2", self.fake_connection.get_outgoing_message())

    def test_get_relay_control_mode(self):
        self.fake_connection.setup_response('1,0,0;0')
        response = self.dut.get_relay_control_mode(1)
        self.assertEqual(response, temperature_controllers.RelayControlMode.RELAY_ON)
        self.assertIn("RELAY? 1", self.fake_connection.get_outgoing_message())


class TestErrorChecking(TestWithFakeModel372):
    def test_execution_error(self):
        # Response for command call with status register error
        self.fake_connection.setup_response('123;16')
        with self.assertRaisesRegex(InstrumentException, r'Execution Error: Instrument not able to execute command or '
                                                         r'query.'):
            self.dut.get_temperature_limit('A')

    def test_command_error(self):
        # Response for command call with status register error
        self.fake_connection.setup_response('123;32')
        with self.assertRaisesRegex(InstrumentException, r'Command Error: Invalid Command or Query'):
            self.dut.get_temperature_limit('A')

    def test_query_error(self):
        # Response for command call with status register error
        self.fake_connection.setup_response('123;4')
        with self.assertRaisesRegex(InstrumentException, r'Query Error'):
            self.dut.get_temperature_limit('A')

    def test_query_error_precedence_over_execution_error(self):
        # Test checks to make sure a query error takes precedence over a execution error
        # Response for command call with status register error
        self.fake_connection.setup_response('123;20')
        with self.assertRaisesRegex(InstrumentException, r'Query Error'):
            self.dut.get_temperature_limit('A')

    def test_query_error_precedence_over_command_error(self):
        # Test checks to make sure a query error takes precedence over a execution error
        # Response for command call with status register error
        self.fake_connection.setup_response('123;36')
        with self.assertRaisesRegex(InstrumentException, r'Query Error'):
            self.dut.get_temperature_limit('A')

    def test_command_error_precedence_over_execution_error(self):
        # Test checks to make sure a command error takes precedence over a execution error
        # Response for command call with status register error
        self.fake_connection.setup_response('123;48')
        with self.assertRaisesRegex(InstrumentException, r'Command Error: Invalid Command or Query'):
            self.dut.get_temperature_limit('A')

    def test_query_error_precedence(self):
        # Test checks that query error has precedence over both other errors
        # Response for command call with status register error
        self.fake_connection.setup_response('123;52')
        with self.assertRaisesRegex(InstrumentException, r'Query Error'):
            self.dut.get_temperature_limit('A')


class TestCurveMethods(TestWithFakeModel372):
    def test_set_curve_data_point(self):
        self.fake_connection.setup_response('0')
        self.dut.set_curve_data_point(22,1,2.86,9.252)
        self.assertIn("CRVPT 22,1,2.86,9.252", self.fake_connection.get_outgoing_message())

    def test_set_curve_data_point_curvature(self):
        self.fake_connection.setup_response('0')
        self.dut.set_curve_data_point(22, 1, 2.86, 9.252, 12.15)
        self.assertIn("CRVPT 22,1,2.86,9.252,12.15", self.fake_connection.get_outgoing_message())

    def test_get_curve_data_point(self):
        self.fake_connection.setup_response('2.58,9.68;0')
        response = self.dut.get_curve_data_point(15, 7)
        self.assertAlmostEqual(response, (2.58, 9.68))
        self.assertIn("CRVPT? 15,7", self.fake_connection.get_outgoing_message())

    def test_get_curve_data_point_curvature(self):
        self.fake_connection.setup_response('2.58,9.68,15.84;0')
        response = self.dut.get_curve_data_point(15, 7)
        self.assertAlmostEqual(response, (2.58, 9.68, 15.84))
        self.assertIn("CRVPT? 15,7", self.fake_connection.get_outgoing_message())


class TestRegisterMethods(TestWithFakeModel372):
    # TODO: Add instrument specific register tests once merged

    def test_get_standard_event_enable_mask(self):
        self.fake_connection.setup_response('20')
        response = self.dut.get_standard_event_enable_mask()
        register = StandardEventRegister(False, True, True, False, False)
        self.assertEqual(register.operation_complete, response.operation_complete)
        self.assertEqual(register.query_error, response.query_error)
        self.assertEqual(register.execution_error, response.execution_error)
        self.assertEqual(register.command_error, response.command_error)
        self.assertEqual(register.power_on, response.power_on)
        self.assertIn("*ESE?", self.fake_connection.get_outgoing_message())

    def test_set_standard_event_enable_mask(self):
        self.fake_connection.setup_response('0')
        register = StandardEventRegister(True, False, False, True, False)
        self.dut.set_standard_event_enable_mask(register)
        self.assertIn("*ESE 33", self.fake_connection.get_outgoing_message())

    def test_get_operation_condition(self):
        self.fake_connection.setup_response('28;0')
        register = OperationEvent(False, False, True, True, True, False, False, False) # LSB to MSB
        response = self.dut._get_operation_condition()
        self.assertEqual(register.alarm, response.alarm)
        self.assertEqual(register.sensor_overload, response.sensor_overload)
        self.assertEqual(register.loop_2_ramp_done, response.loop_2_ramp_done)
        self.assertEqual(register.loop_1_ramp_done, response.loop_1_ramp_done)
        self.assertEqual(register.new_sensor_reading, response.new_sensor_reading)
        self.assertEqual(register.autotune_process_completed, response.autotune_process_completed)
        self.assertEqual(register.calibration_error, response.calibration_error)
        self.assertEqual(register.processor_communication_error, response.processor_communication_error)
        self.assertIn("OPST?", self.fake_connection.get_outgoing_message())

    def test_get_operation_event_enable(self):
        self.fake_connection.setup_response('208;0')
        register = OperationEvent(False, False, False, False, True, False, True, True)
        response = self.dut._get_operation_event_enable()
        self.assertEqual(register.alarm, response.alarm)
        self.assertEqual(register.sensor_overload, response.sensor_overload)
        self.assertEqual(register.loop_2_ramp_done, response.loop_2_ramp_done)
        self.assertEqual(register.loop_1_ramp_done, response.loop_1_ramp_done)
        self.assertEqual(register.new_sensor_reading, response.new_sensor_reading)
        self.assertEqual(register.autotune_process_completed, response.autotune_process_completed)
        self.assertEqual(register.calibration_error, response.calibration_error)
        self.assertEqual(register.processor_communication_error, response.processor_communication_error)
        self.assertIn("OPSTE?", self.fake_connection.get_outgoing_message())

    def test_set_operation_event_enable(self):
        self.fake_connection.setup_response('0')
        register = OperationEvent(True, False, True, False, True, False, True, False)
        self.dut._set_operation_event_enable(register)
        self.assertIn("OPSTE 85", self.fake_connection.get_outgoing_message())

    def test_get_operation_event_enable(self):
        self.fake_connection.setup_response('142;0')
        register = OperationEvent(False, True, True, True, False, False, False, True)
        response = self.dut._get_operation_event()
        self.assertEqual(register.alarm, response.alarm)
        self.assertEqual(register.sensor_overload, response.sensor_overload)
        self.assertEqual(register.loop_2_ramp_done, response.loop_2_ramp_done)
        self.assertEqual(register.loop_1_ramp_done, response.loop_1_ramp_done)
        self.assertEqual(register.new_sensor_reading, response.new_sensor_reading)
        self.assertEqual(register.autotune_process_completed, response.autotune_process_completed)
        self.assertEqual(register.calibration_error, response.calibration_error)
        self.assertEqual(register.processor_communication_error, response.processor_communication_error)
        self.assertIn("OPSTR?", self.fake_connection.get_outgoing_message())
