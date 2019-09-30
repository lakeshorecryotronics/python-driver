from tempfile import TemporaryFile
from time import sleep

from tests.utils import TestWithRealTeslameter, TestWithFakeTeslameter


class TestBufferedFieldData(TestWithRealTeslameter):
    def test_stream_buffered_data_provides_correct_number_of_points(self):
        iterable = self.dut.stream_buffered_data(1, 10)

        self.assertEqual(len(list(iterable)), 100)

    def test_get_buffered_data_provides_correct_number_of_points(self):
        points = self.dut.get_buffered_data_points(1, 10)

        self.assertEqual(len(points), 100)

    def test_log_to_csv_has_expected_number_of_rows(self):
        with TemporaryFile(mode='w+') as log_file:
            self.dut.log_buffered_data_to_file(1, 10, log_file)

            log_file.seek(0)
            lines = log_file.readlines()
            self.assertEqual(len(lines), 101)  # 1 header, 100 points

    def test_log_to_csv_has_expected_length(self):
        with TemporaryFile(mode='w+') as log_file:
            self.dut.log_buffered_data_to_file(1, 10, log_file)

            log_file.seek(0)
            lines = log_file.readlines()

            for row in lines[:-1]:
                self.assertEqual(len(row.split(',')), 9)


class TestBasicReadings(TestWithFakeTeslameter):
    def test_get_dc_field(self):
        self.fake_connection.setup_response('123.456;No error')
        response = self.dut.get_dc_field()
        self.assertAlmostEqual(response, 123.456)
        self.assertIn('FETCH:DC?', self.fake_connection.get_outgoing_message())

    def test_get_dc_field_xyz(self):
        self.fake_connection.setup_response('12,34,56;No error')
        response = self.dut.get_dc_field_xyz()
        for expected, actual in zip([12, 34, 56], response):
            self.assertAlmostEqual(expected, actual)
        self.assertIn('FETCH:DC? ALL', self.fake_connection.get_outgoing_message())

    def test_get_rms_field(self):
        self.fake_connection.setup_response('123.456;No error')
        response = self.dut.get_rms_field()
        self.assertAlmostEqual(response, 123.456)
        self.assertIn('FETCH:RMS?', self.fake_connection.get_outgoing_message())

    def test_get_rms_field_xyz(self):
        self.fake_connection.setup_response('12,34,56;No error')
        response = self.dut.get_rms_field_xyz()
        for expected, actual in zip([12, 34, 56], response):
            self.assertAlmostEqual(expected, actual)
        self.assertIn('FETCH:RMS? ALL', self.fake_connection.get_outgoing_message())

    def test_get_frequency(self):
        self.fake_connection.setup_response('123.456;No error')
        response = self.dut.get_frequency()
        self.assertAlmostEqual(response, 123.456)
        self.assertIn('FETCH:FREQ?', self.fake_connection.get_outgoing_message())

    def test_get_max_min(self):
        self.fake_connection.setup_response('10;-10;No error')
        response = self.dut.get_max_min()
        for expected, actual in zip([10, -10], response):
            self.assertAlmostEqual(expected, actual)
        self.assertIn('FETCH:MAX?;:FETCH:MIN?', self.fake_connection.get_outgoing_message())

    def test_reset_max_min(self):
        self.fake_connection.setup_response('No error')
        self.dut.reset_max_min()
        self.assertIn('SENS:MRESET', self.fake_connection.get_outgoing_message())

    def test_get_relative_field(self):
        self.fake_connection.setup_response('123.456;No error')
        response = self.dut.get_relative_field()
        self.assertAlmostEqual(response, 123.456)
        self.assertIn('FETCH:RELATIVE?', self.fake_connection.get_outgoing_message())

    def test_tare_relative_field(self):
        self.fake_connection.setup_response('No error')
        self.dut.tare_relative_field()
        self.assertIn('SENS:RELATIVE:TARE', self.fake_connection.get_outgoing_message())

    def test_get_relative_field_baseline(self):
        self.fake_connection.setup_response('123.456;No error')
        response = self.dut.get_relative_field_baseline()
        self.assertAlmostEqual(response, 123.456)
        self.assertIn('SENS:RELATIVE:BASELINE?', self.fake_connection.get_outgoing_message())

    def test_set_relative_field_baseline(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_relative_field_baseline(123.456)
        self.assertIn('SENS:RELATIVE:BASELINE 123.456', self.fake_connection.get_outgoing_message())


class TestTemperatureCompensation(TestWithFakeTeslameter):
    def test_get_temperature(self):
        self.fake_connection.setup_response('23.5;No error')
        response = self.dut.get_temperature()
        self.assertAlmostEqual(response, 23.5)
        self.assertIn('FETCH:TEMP?', self.fake_connection.get_outgoing_message())

    def test_configure_temperature_compensation_defaults(self):
        self.fake_connection.setup_response('No error')

        self.dut.configure_temperature_compensation()

        self.assertIn('SENS:TCOM:TSOURCE PROBE', self.fake_connection.get_outgoing_message())

    def test_configure_temperature_compensation(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')

        self.dut.configure_temperature_compensation(temperature_source='MTEMP', manual_temperature=77.1)

        self.assertIn('SENS:TCOM:TSOURCE MTEMP', self.fake_connection.get_outgoing_message())
        self.assertIn('SENS:TCOM:MTEM 77.1', self.fake_connection.get_outgoing_message())

    def test_get_temperature_compensation_source(self):
        self.fake_connection.setup_response('MTEMP;No error')
        response = self.dut.get_temperature_compensation_source()
        self.assertEqual(response, 'MTEMP')
        self.assertIn('SENS:TCOM:TSOURCE?', self.fake_connection.get_outgoing_message())

    def test_get_temperature_compensation_manual_temp(self):
        self.fake_connection.setup_response('77.1;No error')
        response = self.dut.get_temperature_compensation_manual_temp()
        self.assertAlmostEqual(response, 77.1)
        self.assertIn('SENS:TCOM:MTEM?', self.fake_connection.get_outgoing_message())


class TestProbeInformation(TestWithFakeTeslameter):
    def test_get_probe_information(self):
        probe_data = {'model_number': '7547',
                      'serial_number': '1234567',
                      'probe_type': 'FLINT',
                      'sensor_type': 'FLINT',
                      'sensor_orientation': 'VERTICAL',
                      'number_of_axes': '3',
                      'calibration_date': '2/1/2019'}

        self.fake_connection.setup_response(probe_data['model_number'] + ';No error')
        self.fake_connection.setup_response(probe_data['serial_number'] + ';No error')
        self.fake_connection.setup_response(probe_data['probe_type'] + ';No error')
        self.fake_connection.setup_response(probe_data['sensor_type'] + ';No error')
        self.fake_connection.setup_response(probe_data['sensor_orientation'] + ';No error')
        self.fake_connection.setup_response(probe_data['number_of_axes'] + ';No error')
        self.fake_connection.setup_response(probe_data['calibration_date'] + ';No error')

        response = self.dut.get_probe_information()

        self.assertDictEqual(probe_data, response)


class TestFieldMeasurementConfiguration(TestWithFakeTeslameter):
    def test_configure_field_measurement_defaults(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')

        self.dut.configure_field_measurement_setup()

        self.assertIn('SENS:MODE DC', self.fake_connection.get_outgoing_message())
        self.assertIn('SENS:RANGE:AUTO 1', self.fake_connection.get_outgoing_message())
        self.assertIn('SENS:AVERAGE:COUNT 20', self.fake_connection.get_outgoing_message())

    def test_configure_field_measurement(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')

        self.dut.configure_field_measurement_setup(mode='AC', autorange=False, expected_field=123.456, averaging_samples=100)

        self.assertIn('SENS:MODE AC', self.fake_connection.get_outgoing_message())
        self.assertIn('SENS:RANGE:AUTO 0', self.fake_connection.get_outgoing_message())
        self.assertIn('SENS:RANGE 123.456', self.fake_connection.get_outgoing_message())
        self.assertIn('SENS:AVERAGE:COUNT 100', self.fake_connection.get_outgoing_message())

    def test_get_field_measurement_setup(self):
        setup = {'mode': 'DC',
                 'autorange': False,
                 'expected_field': 123.456,
                 'averaging_samples': 100}

        self.fake_connection.setup_response(setup['mode'] + ';No error')
        self.fake_connection.setup_response(str(int(setup['autorange'])) + ';No error')
        self.fake_connection.setup_response(str(setup['expected_field']) + ';No error')
        self.fake_connection.setup_response(str(setup['averaging_samples']) + ';No error')

        response = self.dut.get_field_measurement_setup()

        self.assertDictEqual(response, setup)

    def test_configure_field_units(self):
        self.fake_connection.setup_response('No error')
        self.dut.configure_field_units('TESLA')
        self.assertIn('UNIT:FIELD TESLA', self.fake_connection.get_outgoing_message())

    def test_get_field_units(self):
        self.fake_connection.setup_response('GAUSS;No error')
        response = self.dut.get_field_units()
        self.assertEqual(response, 'GAUSS')
        self.assertIn('UNIT:FIELD?', self.fake_connection.get_outgoing_message())


class TestFieldControl(TestWithFakeTeslameter):
    def test_configure_field_control_limits(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')

        self.dut.configure_field_control_limits(voltage_limit=7.3, slew_rate_limit=1.5)

        self.assertIn('SOURCE:FIELD:VLIMIT 7.3', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURCE:FIELD:SLEW 1.5', self.fake_connection.get_outgoing_message())

    def test_get_field_control_limits(self):
        limits = {'voltage_limit': 5.3,
                  'slew_rate_limit': 6.8}

        self.fake_connection.setup_response(str(limits['voltage_limit']) + ';No error')
        self.fake_connection.setup_response(str(limits['slew_rate_limit']) + ';No error')

        response = self.dut.get_field_control_limits()

        self.assertDictEqual(response, limits)

    def test_configure_field_control_output_mode_defaults(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')

        self.dut.configure_field_control_output_mode()

        self.assertIn('SOURCE:FIELD:MODE CLLOOP', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURCE:FIELD:STATE 1', self.fake_connection.get_outgoing_message())

    def test_configure_field_control_output_mode(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')

        self.dut.configure_field_control_output_mode(mode='OPLOOP', output_enabled=False)

        self.assertIn('SOURCE:FIELD:MODE OPLOOP', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURCE:FIELD:STATE 0', self.fake_connection.get_outgoing_message())

    def test_get_field_control_output_mode(self):
        output_state = {'mode': 'OPLOOP',
                        'output_enabled': False}

        self.fake_connection.setup_response(output_state['mode'] + ';No error')
        self.fake_connection.setup_response(str(int(output_state['output_enabled'])) + ';No error')

        response = self.dut.get_field_control_output_mode()

        self.assertDictEqual(response, output_state)

    def test_configure_field_control_pid(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')

        self.dut.configure_field_control_pid(gain=1.5, integral=5.3, ramp_rate=1234.56)

        self.assertIn('SOURCE:FIELD:CLL:GAIN 1.5', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURCE:FIELD:CLL:INTEGRAL 5.3', self.fake_connection.get_outgoing_message())
        self.assertIn('SOURCE:FIELD:CLL:RAMP 1234.56', self.fake_connection.get_outgoing_message())

    def test_get_field_control_pid(self):
        pid = {'gain': 1.2,
               'integral': 0.51,
               'ramp_rate': 123.456}

        self.fake_connection.setup_response(str(pid['gain']) + ';No error')
        self.fake_connection.setup_response(str(pid['integral']) + ';No error')
        self.fake_connection.setup_response(str(pid['ramp_rate']) + ';No error')

        response = self.dut.get_field_control_pid()

        self.assertDictEqual(response, pid)

    def test_set_field_control_setpoint(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_field_control_setpoint(5000.7)
        self.assertIn('SOURCE:FIELD:CLL:SETPOINT 5000.7', self.fake_connection.get_outgoing_message())

    def test_get_field_control_setpoint(self):
        self.fake_connection.setup_response('12.3456;No error')
        response = self.dut.get_field_control_setpoint()
        self.assertAlmostEqual(response, 12.3456)
        self.assertIn('SOURCE:FIELD:CLL:SETPOINT?', self.fake_connection.get_outgoing_message())

    def test_set_field_control_open_loop_voltage(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_field_control_open_loop_voltage(1.23)
        self.assertIn('SOURCE:FIELD:OPL:VOLTAGE 1.23', self.fake_connection.get_outgoing_message())

    def test_get_field_control_open_loop_voltage(self):
        self.fake_connection.setup_response('-6.8;No error')
        response = self.dut.get_field_control_open_loop_voltage()
        self.assertAlmostEqual(response, -6.8)
        self.assertIn('SOURCE:FIELD:OPL:VOLTAGE?', self.fake_connection.get_outgoing_message())


class TestAnalogOut(TestWithFakeTeslameter):
    def test_set_analog_output_signal(self):

        self.fake_connection.setup_response('No error')
        self.dut.set_analog_output_signal('YRAW')
        self.assertIn('SOURCE:AOUT YRAW', self.fake_connection.get_outgoing_message())

    def test_get_analog_output(self):
        self.fake_connection.setup_response('ZRAW;No error')
        response = self.dut.get_analog_output_signal()
        self.assertEqual(response, 'ZRAW')
        self.assertIn('SOURCE:AOUT?', self.fake_connection.get_outgoing_message())

    def test_configure_analog_out_scaling(self):
        self.fake_connection.setup_response('No error')
        self.dut.configure_corrected_analog_output_scaling(1, 0)
        self.assertIn('SOURCE:AOUT:SFACTOR 1;:SOURCE:AOUT:BASELINE 0', self.fake_connection.get_outgoing_message())


class TestResets(TestWithFakeTeslameter):
    def test_reset_measurement_settings(self):
        self.fake_connection.setup_response('No error')
        self.dut.reset_measurement_settings()
        self.assertIn('SYSTEM:PRESET', self.fake_connection.get_outgoing_message())

    def test_factory_reset(self):
        self.fake_connection.setup_response('No error')
        self.dut.factory_reset()
        self.assertIn('SYSTEM:FACTORYRESET', self.fake_connection.get_outgoing_message())


class TestStatusRegisters(TestWithRealTeslameter):
    def test_modification_of_operation_register(self):
        self.dut.modify_operation_register_mask('ranging', False)

        response = self.dut.get_operation_event_enable_mask()

        self.assertEqual(response.ranging, False)


class TestFilters(TestWithFakeTeslameter):
    def test_enable_high_frequency_filters(self):
        self.fake_connection.setup_response('No error')
        self.dut.enable_high_frequency_filters()
        self.assertIn('SENSE:FILT 1', self.fake_connection.get_outgoing_message())

    def test_disable_high_frequency_filters(self):
        self.fake_connection.setup_response('No error')
        self.dut.disable_high_frequency_filters()
        self.assertIn('SENSE:FILT 0', self.fake_connection.get_outgoing_message())

    def test_set_frequency_filter_type(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_frequency_filter_type("HPASS")
        self.assertIn('SENSE:FILT:TYPE HPASS', self.fake_connection.get_outgoing_message())

    def test_get_frequency_filter_type(self):
        self.fake_connection.setup_response('HPASS;No error')
        response = self.dut.get_frequency_filter_type()
        self.assertEqual(response, 'HPASS')
        self.assertIn('SENSE:FILTER:TYPE?', self.fake_connection.get_outgoing_message())

    def test_get_low_pass_filter_cutoff(self):
        self.fake_connection.setup_response('1234;No error')
        response = self.dut.get_low_pass_filter_cutoff()
        self.assertEqual(response, 1234)
        self.assertIn('SENSE:FILTER:LPASS:CUTOFF?', self.fake_connection.get_outgoing_message())

    def test_set_low_pass_filter_cutoff(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_low_pass_filter_cutoff(1234)
        self.assertIn('SENSE:FILTER:LPASS:CUTOFF 1234', self.fake_connection.get_outgoing_message())

    def test_get_high_pass_filter_cutoff(self):
        self.fake_connection.setup_response('4321;No error')
        response = self.dut.get_high_pass_filter_cutoff()
        self.assertEqual(response, 4321)
        self.assertIn('SENSE:FILTER:HPASS:CUTOFF?', self.fake_connection.get_outgoing_message())

    def test_set_high_pass_filter_cutoff(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_high_pass_filter_cutoff(4321)
        self.assertIn('SENSE:FILTER:HPASS:CUTOFF 4321', self.fake_connection.get_outgoing_message())

    def test_get_band_pass_filter_center(self):
        self.fake_connection.setup_response('8675;No error')
        self.fake_connection.setup_response('2;No error')
        response = self.dut.get_band_pass_filter_center()
        self.assertEqual(response, 8675)
        self.assertIn('SENSE:FILTER:BPASS:CENTER?', self.fake_connection.get_outgoing_message())

    def test_set_band_pass_filter_center(self):
        self.fake_connection.setup_response('No error')
        self.fake_connection.setup_response('No error')
        self.dut.set_band_pass_filter_center(8675)
        self.assertIn('SENSE:FILTER:BPASS:CENTER 8675', self.fake_connection.get_outgoing_message())


class TestQualifier(TestWithFakeTeslameter):
    def test_enable_qualifier(self):
        self.fake_connection.setup_response('No error')
        self.dut.enable_qualifier()
        self.assertIn('SENSE:QUALIFIER 1', self.fake_connection.get_outgoing_message())

    def test_disable_qualifier(self):
        self.fake_connection.setup_response('No error')
        self.dut.disable_qualifier()
        self.assertIn('SENSE:QUALIFIER 0', self.fake_connection.get_outgoing_message())

    def test_is_qualifier_condition_met(self):
        self.fake_connection.setup_response('0;No error')
        response = self.dut.is_qualifier_condition_met()
        self.assertEqual(response, False)
        self.assertIn('SENSE:QUALIFIER:CONDITION?', self.fake_connection.get_outgoing_message())

    def test_enable_qualifier_latching(self):
        self.fake_connection.setup_response('No error')
        self.dut.enable_qualifier_latching()
        self.assertIn('SENSE:QUALIFIER:LATCH 1', self.fake_connection.get_outgoing_message())

    def test_disable_qualifier_latching(self):
        self.fake_connection.setup_response('No error')
        self.dut.disable_qualifier_latching()
        self.assertIn('SENSE:QUALIFIER:LATCH 0', self.fake_connection.get_outgoing_message())

    def test_reset_qualifier_latch(self):
        self.fake_connection.setup_response('No error')
        self.dut.reset_qualifier_latch()
        self.assertIn('SENSE:QUALIFIER:LRESET', self.fake_connection.get_outgoing_message())

    def test_get_qualifier_threshold(self):
        self.fake_connection.setup_response('BETWeen,-1.23,4.56;No error')
        response = self.dut.get_qualifier_threshold()
        self.assertEqual(response, ('BETWeen', -1.23, 4.56))
        self.assertIn('SENSE:QUALIFIER:THRESHOLD?', self.fake_connection.get_outgoing_message())

    def test_set_qualifier_threshold(self):
        self.fake_connection.setup_response('No error')
        self.dut.configure_qualifier_threshold('OUTSIDE', -1.23, 4.56)
        self.assertIn('SENSE:QUALIFIER:THRESHOLD OUTSIDE,-1.23,4.56', self.fake_connection.get_outgoing_message())
