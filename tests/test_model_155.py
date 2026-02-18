from tests.utils import TestWithFakePrecisionSource


class TestOutputValidation(TestWithFakePrecisionSource):

    def test_output_dc_current_non_numeric_raises(self):
        with self.assertRaises(ValueError):
            self.dut.output_dc_current("abc")

    def test_output_dc_current_bool_raises(self):
        with self.assertRaises(ValueError):
            self.dut.output_dc_current(True)

    def test_output_dc_voltage_non_numeric_raises(self):
        with self.assertRaises(ValueError):
            self.dut.output_dc_voltage("abc")

    def test_output_dc_voltage_bool_raises(self):
        with self.assertRaises(ValueError):
            self.dut.output_dc_voltage(True)

    def test_output_sine_current_non_numeric_amplitude_raises(self):
        with self.assertRaises(ValueError):
            self.dut.output_sine_current("abc", 1000)

    def test_output_sine_current_non_numeric_frequency_raises(self):
        with self.assertRaises(ValueError):
            self.dut.output_sine_current(0.01, "abc")

    def test_output_sine_voltage_non_numeric_amplitude_raises(self):
        with self.assertRaises(ValueError):
            self.dut.output_sine_voltage("abc", 1000)

    def test_output_sine_voltage_bool_amplitude_raises(self):
        with self.assertRaises(ValueError):
            self.dut.output_sine_voltage(True, 1000)


class TestLimitValidation(TestWithFakePrecisionSource):

    def test_set_current_limit_non_numeric_raises(self):
        with self.assertRaises(ValueError):
            self.dut.set_current_limit("abc")

    def test_set_current_limit_too_high_raises(self):
        with self.assertRaises(ValueError):
            self.dut.set_current_limit(0.2)

    def test_set_current_limit_negative_raises(self):
        with self.assertRaises(ValueError):
            self.dut.set_current_limit(-0.01)

    def test_set_current_limit_valid(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_current_limit(0.05)
        self.assertIn("SOURCE:CURRENT:LIMIT 0.05", self.fake_connection.get_outgoing_message())

    def test_set_voltage_limit_non_numeric_raises(self):
        with self.assertRaises(ValueError):
            self.dut.set_voltage_limit("abc")

    def test_set_voltage_limit_too_high_raises(self):
        with self.assertRaises(ValueError):
            self.dut.set_voltage_limit(101)

    def test_set_voltage_limit_negative_raises(self):
        with self.assertRaises(ValueError):
            self.dut.set_voltage_limit(-1)

    def test_set_voltage_limit_valid(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_voltage_limit(50)
        self.assertIn("SOURCE:VOLTAGE:LIMIT 50", self.fake_connection.get_outgoing_message())

    def test_set_current_mode_voltage_protection_too_low_raises(self):
        with self.assertRaises(ValueError):
            self.dut.set_current_mode_voltage_protection(0.5)

    def test_set_current_mode_voltage_protection_too_high_raises(self):
        with self.assertRaises(ValueError):
            self.dut.set_current_mode_voltage_protection(101)

    def test_set_current_mode_voltage_protection_valid(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_current_mode_voltage_protection(50)
        self.assertIn("SOURCE:CURRENT:PROTECTION 50", self.fake_connection.get_outgoing_message())

    def test_set_voltage_mode_current_protection_negative_raises(self):
        with self.assertRaises(ValueError):
            self.dut.set_voltage_mode_current_protection(-1)

    def test_set_voltage_mode_current_protection_non_numeric_raises(self):
        with self.assertRaises(ValueError):
            self.dut.set_voltage_mode_current_protection("abc")

    def test_set_voltage_mode_current_protection_valid(self):
        self.fake_connection.setup_response('No error')
        self.dut.set_voltage_mode_current_protection(0.05)
        self.assertIn("SOURCE:VOLTAGE:PROTECTION 0.05", self.fake_connection.get_outgoing_message())
