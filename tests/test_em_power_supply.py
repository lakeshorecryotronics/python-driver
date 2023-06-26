from tests.utils import TestWithFakeEMPowerSupply


class TestCurrentSettings(TestWithFakeEMPowerSupply):

    def test_set_limits(self):
        self.fake_connection.setup_response("0")
        self.dut.set_limits(22.222, 3.333)
        self.assertIn("LIMIT 22.222, 3.333", self.fake_connection.get_outgoing_message())

    def test_get_limits(self):
        self.fake_connection.setup_response("33.333, 4.444; 0")
        response = self.dut.get_limits()
        self.assertEqual(response, [33.333, 4.444])
        self.assertIn("LIMIT?", self.fake_connection.get_outgoing_message())

    def test_set_ramp_rate(self):
        self.fake_connection.setup_response("0")
        self.dut.set_ramp_rate(7.77)
        self.assertIn("RATE 7.77", self.fake_connection.get_outgoing_message())

    def test_get_ramp_rate(self):
        self.fake_connection.setup_response("9.9; 0")
        response = self.dut.get_ramp_rate()
        self.assertEqual(response, 9.9)
        self.assertIn("RATE?", self.fake_connection.get_outgoing_message())

    def test_set_ramp_segments(self):
        self.fake_connection.setup_response("0")
        self.dut.set_ramp_segment(2, 50, 2.5)
        self.assertIn("RSEGS 2, 50, 2.5", self.fake_connection.get_outgoing_message())

    def test_get_ramp_segments(self):
        self.fake_connection.setup_response("17.5, 2.5; 0")
        response = self.dut.get_ramp_segment(4)
        self.assertEqual(response, [17.5, 2.5])
        self.assertIn("RSEGS?", self.fake_connection.get_outgoing_message())

    def test_set_ramp_segments_enable(self):
        self.fake_connection.setup_response("0")
        self.dut.set_ramp_segments_enable(True)
        self.assertIn("RSEG 1", self.fake_connection.get_outgoing_message())

    def test_get_ramp_segments_enable(self):
        self.fake_connection.setup_response("0; 0")
        response = self.dut.get_ramp_segments_enable()
        self.assertEqual(response, False)
        self.assertIn("RSEG?", self.fake_connection.get_outgoing_message())

    def test_set_current(self):
        self.fake_connection.setup_response("0")
        self.dut.set_current(45.8)
        self.assertIn("SETI 45.8", self.fake_connection.get_outgoing_message())

    def test_get_current(self):
        self.fake_connection.setup_response("65.7; 0")
        response = self.dut.get_current()
        self.assertEqual(response, 65.7)
        self.assertIn("SETI?", self.fake_connection.get_outgoing_message())

    def test_get_measured_current(self):
        self.fake_connection.setup_response("34.689; 0")
        response = self.dut.get_measured_current()
        self.assertEqual(response, 34.689)
        self.assertIn("RDGI?", self.fake_connection.get_outgoing_message())

    def test_get_measured_voltage(self):
        self.fake_connection.setup_response("11.234; 0")
        response = self.dut.get_measured_voltage()
        self.assertEqual(response, 11.234)
        self.assertIn("RDGV?", self.fake_connection.get_outgoing_message())

    def test_stop_output_current_ramp(self):
        self.fake_connection.setup_response("0")
        self.dut.stop_output_current_ramp()
        self.assertIn("STOP", self.fake_connection.get_outgoing_message())


class TestGeneralSettings(TestWithFakeEMPowerSupply):

    def test_set_internal_water(self):
        self.fake_connection.setup_response("0")
        self.dut.set_internal_water(3)
        self.assertIn("INTWTR 3", self.fake_connection.get_outgoing_message())

    def test_get_internal_water(self):
        self.fake_connection.setup_response("2; 0")
        response = self.dut.get_internal_water()
        self.assertEqual(response, 2)
        self.assertIn("INTWTR?", self.fake_connection.get_outgoing_message())

    def test_set_magnet_water(self):
        self.fake_connection.setup_response("0")
        self.dut.set_magnet_water(0)
        self.assertIn("MAGWTR 0", self.fake_connection.get_outgoing_message())

    def test_get_magnet_water(self):
        self.fake_connection.setup_response("1; 0")
        response = self.dut.get_magnet_water()
        self.assertEqual(response, 1)
        self.assertIn("MAGWTR?", self.fake_connection.get_outgoing_message())

    def test_set_display_brightness(self):
        self.fake_connection.setup_response("0")
        self.dut.set_display_brightness(2)
        self.assertIn("DISP 2", self.fake_connection.get_outgoing_message())

    def test_get_display_brightness(self):
        self.fake_connection.setup_response("3; 0")
        response = self.dut.get_display_brightness()
        self.assertEqual(response, 3)
        self.assertIn("DISP?", self.fake_connection.get_outgoing_message())

    def test_set_front_panel_lock(self):
        self.fake_connection.setup_response("0")
        self.dut.set_front_panel_lock(1, 123)
        self.assertIn("LOCK 1,123", self.fake_connection.get_outgoing_message())

    def test_get_front_panel_lock_status(self):
        self.fake_connection.setup_response("3; 0")
        response = self.dut.get_front_panel_status()
        self.assertEqual(response, 3)
        self.assertIn("LOCK?", self.fake_connection.get_outgoing_message())

    def test_get_front_panel_lock_code(self):
        self.fake_connection.setup_response("777; 0")
        response = self.dut.get_front_panel_status()
        self.assertEqual(response, 777)
        self.assertIn("LOCK?", self.fake_connection.get_outgoing_message())

    def test_set_programming_mode(self):
        self.fake_connection.setup_response("0")
        self.dut.set_programming_mode(2)
        self.assertIn("XPGM 2", self.fake_connection.get_outgoing_message())

    def test_get_programming_mode(self):
        self.fake_connection.setup_response("1; 0")
        response = self.dut.get_programming_mode()
        self.assertEqual(response, 1)
        self.assertIn("XPGM?", self.fake_connection.get_outgoing_message())


class TestIEEE488Settings(TestWithFakeEMPowerSupply):

    def test_set_ieee_488_config(self):
        self.fake_connection.setup_response("0")
        self.dut.set_ieee_488(0, 0, 8)
        self.assertIn("IEEE 0,0,8", self.fake_connection.get_outgoing_message())

    def test_get_ieee_488_config(self):
        self.fake_connection.setup_response("1,0,12; 0")
        response = self.dut.get_iee_488()
        self.assertEqual(response, [1, 0, 12])
        self.assertIn("IEEE?", self.fake_connection.get_outgoing_message())

    def test_set_ieee_488_interface_mode(self):
        self.fake_connection.setup_response("0")
        self.dut.set_ieee_interface_mode(2)
        self.assertIn("MODE 2", self.fake_connection.get_outgoing_message())

    def test_get_ieee_488_interface_mode(self):
        self.fake_connection.setup_response("1; 0")
        response = self.dut.get_ieee_interface_mode()
        self.assertEqual(response, 1)
        self.assertIn("MODE?", self.fake_connection.get_outgoing_message())


class TestResets(TestWithFakeEMPowerSupply):

    def test_set_factory_defaults(self):
        self.fake_connection.setup_response("0")
        self.dut.set_factory_defaults()
        self.assertIn("DFLT 99", self.fake_connection.get_outgoing_message())

    def test_reset_instrument(self):
        self.fake_connection.setup_response("0")
        self.dut.reset_instrument()
        self.assertIn("*RST", self.fake_connection.get_outgoing_message())

    def test_clear_interface(self):
        self.fake_connection.setup_response("0")
        self.dut.clear_interface()
        self.assertIn("*CLS", self.fake_connection.get_outgoing_message())

    def test_get_self_test(self):
        self.fake_connection.setup_response("1; 0")
        response = self.dut.get_self_test()
        self.assertEqual(response, 1)
        self.assertIn("*TST?", self.fake_connection.get_outgoing_message())


class TestRegisterCommands(TestWithFakeEMPowerSupply):

    def test_set_service_request_enable_mask(self):
        self.fake_connection.setup_response("0")
        service_request_enable_mask = self.dut.EMPowerSupplyServiceRequestEnableRegister.from_integer(4)
        self.dut.set_service_request_enable_mask(service_request_enable_mask)
        self.assertIn("*SRE 4", self.fake_connection.get_outgoing_message())

    def test_get_service_request_enable_mask(self):
        self.fake_connection.setup_response("16; 0")
        response = self.dut.get_service_request_enable_mask()
        self.assertEqual(response.to_integer(), 16)
        self.assertIn("SRE?", self.fake_connection.get_outgoing_message())

    def test_get_status_byte(self):
        self.fake_connection.setup_response("4; 0")
        response = self.dut.get_status_byte()
        self.assertEqual(response.to_integer(), 4)
        self.assertIn("STB?", self.fake_connection.get_outgoing_message())

    def test_set_standard_event_status_enable_mask(self):
        self.fake_connection.setup_response("0")
        standard_event_status_enable_mask = self.dut.EMPowerSupplyStandardEventStatusRegister.from_integer(4)
        self.dut.set_standard_event_status_enable_mask(standard_event_status_enable_mask)
        self.assertIn("*ESE 4", self.fake_connection.get_outgoing_message())

    def test_get_standard_event_status_enable_mask(self):
        self.fake_connection.setup_response("16; 0")
        response = self.dut.get_standard_event_status_enable_mask()
        self.assertEqual(response.to_integer(), 16)
        self.assertIn("ESE?", self.fake_connection.get_outgoing_message())

    def test_get_standard_event_status_event(self):
        self.fake_connection.setup_response("4; 0")
        response = self.dut.get_standard_event_status_event()
        self.assertEqual(response.to_integer(), 4)
        self.assertIn("ESR?", self.fake_connection.get_outgoing_message())

    def test_set_operation_event_enable_mask(self):
        self.fake_connection.setup_response("0")
        operation_event_enable_mask = self.dut.EMPowerSupplyOperationEventRegister.from_integer(4)
        self.dut.set_operation_event_enable_mask(operation_event_enable_mask)
        self.assertIn("OPSTE 4", self.fake_connection.get_outgoing_message())

    def test_get_operation_event_enable_mask(self):
        self.fake_connection.setup_response("4; 0")
        response = self.dut.get_operation_event_enable_mask()
        self.assertEqual(response.to_integer(), 4)
        self.assertIn("OPSTE?", self.fake_connection.get_outgoing_message())

    def test_get_operation_event_condition(self):
        self.fake_connection.setup_response("2; 0")
        response = self.dut.get_operation_event_condition()
        self.assertEqual(response.to_integer(), 2)
        self.assertIn("OPSTR?", self.fake_connection.get_outgoing_message())

    def test_get_operation_event(self):
        self.fake_connection.setup_response("1; 0")
        response = self.dut.get_operation_event_event()
        self.assertEqual(response.to_integer(), 1)
        self.assertIn("OPST?", self.fake_connection.get_outgoing_message())

    def test_set_hardware_error_enable_mask(self):
        self.fake_connection.setup_response("0,0; 0")
        self.fake_connection.setup_response("0")
        hardware_error_enable_mask = self.dut.EMPowerSupplyHardwareErrorsRegister.from_integer(4)
        self.dut.set_hardware_error_enable_mask(hardware_error_enable_mask)
        self.fake_connection.get_outgoing_message()
        self.assertIn("ERSTE 4", self.fake_connection.get_outgoing_message())

    def test_get_hardware_error_enable_mask(self):
        self.fake_connection.setup_response("4,0; 0")
        response = self.dut.get_hardware_error_enable_mask()
        self.assertEqual(response.to_integer(), 4)
        self.assertIn("ERSTE?", self.fake_connection.get_outgoing_message())

    def test_get_hardware_error_condition(self):
        self.fake_connection.setup_response("2,0; 0")
        response = self.dut.get_hardware_error_condition()
        self.assertEqual(response.to_integer(), 2)
        self.assertIn("ERST?", self.fake_connection.get_outgoing_message())

    def test_get_hardware_error_event(self):
        self.fake_connection.setup_response("1,0; 0")
        response = self.dut.get_hardware_error_event()
        self.assertEqual(response.to_integer(), 1)
        self.assertIn("ERSTR?", self.fake_connection.get_outgoing_message())

    def test_set_operational_error_enable_mask(self):
        self.fake_connection.setup_response("1,0; 0")
        self.fake_connection.setup_response("0")
        operational_error_enable_mask = self.dut.EMPowerSupplyOperationalErrorsRegister.from_integer(4)
        self.dut.set_operational_error_enable_mask(operational_error_enable_mask)
        self.fake_connection.get_outgoing_message()
        self.assertIn("ERSTE 4", self.fake_connection.get_outgoing_message())

    def test_get_operational_error_enable_mask(self):
        self.fake_connection.setup_response("0,4; 0")
        response = self.dut.get_operational_error_enable_mask()
        self.assertEqual(response.to_integer(), 4)
        self.assertIn("ERSTE?", self.fake_connection.get_outgoing_message())

    def test_get_operational_error_condition(self):
        self.fake_connection.setup_response("0,2; 0")
        response = self.dut.get_operational_error_condition()
        self.assertEqual(response.to_integer(), 2)
        self.assertIn("ERST?", self.fake_connection.get_outgoing_message())

    def test_get_operational_error_event(self):
        self.fake_connection.setup_response("0,1; 0")
        response = self.dut.get_operational_error_event()
        self.assertEqual(response.to_integer(), 1)
        self.assertIn("ERSTR?", self.fake_connection.get_outgoing_message())
