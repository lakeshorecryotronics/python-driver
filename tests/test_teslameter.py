from tests.test_connection import TestWithDUT


class TestBuffers(TestWithDUT):
    def test_getting_buffered_data(self):
        self.assertEqual(len(self.dut.get_buffered_data_points(1, 10)), 100)


class TestStatusRegisters(TestWithDUT):
    def test_modification_of_register(self):
        self.dut.modify_operation_register_mask('ranging', False)
        response = self.dut.get_operation_event_enable_mask()

        self.assertEqual(response.ranging, False)


class TestBasics(TestWithDUT):
    def TestMeasurementConfiguration(self):
        self.dut.configure_field_measurement_setup(mode="AC")

    def test_fetch_queries(self):
        self.dut.command("SENS:TCOM:TSOURCE NONE")
        self.dut.get_dc_field()
        self.dut.get_dc_field_xyz()
        self.dut.get_max_min()
        self.dut.configure_field_measurement_setup(mode="AC")
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
        self.dut.configure_field_control_output_mode(mode="OPLOOP", output_enabled=False)
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
