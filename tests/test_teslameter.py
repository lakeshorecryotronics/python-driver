from tests.test_xip_base import TestWithDUT
from time import sleep


class TestBufferedFieldData(TestWithDUT):
    def test_stream_buffered_data_provides_correct_number_of_points(self):
        iterable = self.dut.stream_buffered_data(1, 10)

        self.assertEqual(len(list(iterable)), 100)

    def test_get_buffered_data_provides_correct_number_of_points(self):
        points = self.dut.get_buffered_data_points(1, 10)

        self.assertEqual(len(points), 100)


class TestStatusRegisters(TestWithDUT):
    def test_modification_of_operation_register(self):
        self.dut.modify_operation_register_mask('ranging', False)

        response = self.dut.get_operation_event_enable_mask()

        self.assertEqual(response.ranging, False)


class TestBasics(TestWithDUT):
    def setUp(self):
        self.dut.configure_field_measurement_setup(mode="AC")
        sleep(1)

    def test_methods_provide_responses(self):
        # Methods that expect responses (method, args, kwargs)
        dut_methods = [(self.dut.get_dc_field, [], {}),
                       (self.dut.get_dc_field_xyz, [], {}),
                       (self.dut.get_rms_field, [], {}),
                       (self.dut.get_rms_field_xyz, [], {}),
                       (self.dut.get_frequency, [], {}),
                       (self.dut.get_max_min, [], {}),
                       (self.dut.get_temperature, [], {}),
                       (self.dut.get_probe_information, [], {}),
                       (self.dut.get_relative_field, [], {}),
                       (self.dut.get_relative_field_baseline, [], {}),
                       (self.dut.get_field_measurement_setup, [], {}),
                       (self.dut.get_temperature_compensation_source, [], {}),
                       (self.dut.get_temperature_compensation_manual_temp, [], {}),
                       (self.dut.get_field_units, [], {}),
                       (self.dut.get_field_control_limits, [], {}),
                       (self.dut.get_field_control_output_mode, [], {}),
                       (self.dut.get_field_control_pid, [], {}),
                       (self.dut.get_field_control_setpoint, [], {}),
                       (self.dut.get_field_control_open_loop_voltage, [], {}),
                       (self.dut.get_analog_output, [], {})]

        for method_to_call, args, kwargs in dut_methods:
            with self.subTest(method=method_to_call):
                response = method_to_call(*args, **kwargs)

                self.assertIsNotNone(response)  # Ensure that no exception was raised, and a response was provided

    def test_methods_do_not_raise_exceptions(self):
        # Methods that don't expect responses (method, args, kwargs)
        dut_methods = [(self.dut.tare_relative_field, [], {}),
                       (self.dut.set_relative_field_baseline, [12.3], {}),
                       (self.dut.configure_field_measurement_setup, [], {"mode": "AC"}),
                       (self.dut.configure_temperature_compensation, [], {"manual_temperature": 23.45}),
                       (self.dut.configure_field_units, [], {}),
                       (self.dut.configure_field_control_limits, [], {}),
                       (self.dut.configure_field_control_output_mode, [], {"mode": "OPLOOP", "output_enabled": False}),
                       (self.dut.configure_field_control_pid, [], {"gain": 1, "integral": 0.1, "ramp_rate": 10}),
                       (self.dut.set_field_control_setpoint, [1], {}),
                       (self.dut.set_field_control_open_loop_voltage, [1], {}),
                       (self.dut.set_analog_output, ["X"], {})]

        for method_to_call, args, kwargs in dut_methods:
            with self.subTest(method=method_to_call):
                method_to_call(*args, **kwargs)  # Just ensure that no exception was raised
