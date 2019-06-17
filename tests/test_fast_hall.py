from tests.utils import TestWithFakeFastHall, TestWithRealFastHall


class TestResets(TestWithFakeFastHall):
    def test_reset_measurement_settings(self):
        self.fake_connection.setup_response('No error')
        self.dut.reset_measurement_settings()
        self.assertIn('SYSTEM:PRESET', self.fake_connection.get_outgoing_message())

    def test_factory_reset(self):
        self.fake_connection.setup_response('No error')
        self.dut.factory_reset()
        self.assertIn('SYSTEM:FACTORYRESET', self.fake_connection.get_outgoing_message())

    def test_contact_check_reset(self):
        self.fake_connection.setup_response('No error')
        self.dut.reset_contact_check_measurement()
        self.assertIn('CCHECK:RESET', self.fake_connection.get_outgoing_message())

    def test_fasthall_reset(self):
        self.fake_connection.setup_response('No error')
        self.dut.reset_fasthall_measurement()
        self.assertIn('FASTHALL:RESET', self.fake_connection.get_outgoing_message())

    def test_four_wire_reset(self):
        self.fake_connection.setup_response('No error')
        self.dut.reset_four_wire_measurement()
        self.assertIn('FWIRE:RESET', self.fake_connection.get_outgoing_message())

    def test_dc_hall_reset(self):
        self.fake_connection.setup_response('No error')
        self.dut.reset_dc_hall_measurement()
        self.assertIn('HALL:DC:RESET', self.fake_connection.get_outgoing_message())

    def test_resisitvity_reset(self):
        self.fake_connection.setup_response('No error')
        self.dut.reset_resistivity_measurement()
        self.assertIn('RESISTIVITY:RESET', self.fake_connection.get_outgoing_message())


class TestRunningStatusFake(TestWithFakeFastHall):
    def test_contact_check_running(self):
        self.fake_connection.setup_response('1;No error')
        response = self.dut.get_contact_check_running_status()
        self.assertAlmostEqual(response, 1)
        self.assertIn('CCHECK:RUNNING?', self.fake_connection.get_outgoing_message())

    def test_fasthall_running(self):
        self.fake_connection.setup_response('1;No error')
        response = self.dut.get_fasthall_running_status()
        self.assertAlmostEqual(response, 1)
        self.assertIn('FASTHALL:RUNNING?', self.fake_connection.get_outgoing_message())

    def test_four_wire_running(self):
        self.fake_connection.setup_response('1;No error')
        response = self.dut.get_four_wire_running_status()
        self.assertAlmostEqual(response, 1)
        self.assertIn('FWIRE:RUNNING?', self.fake_connection.get_outgoing_message())

    def test_dc_hall_running(self):
        self.fake_connection.setup_response('1;No error')
        response = self.dut.get_dc_hall_running_status()
        self.assertAlmostEqual(response, 1)
        self.assertIn('HALL:DC:RUNNING?', self.fake_connection.get_outgoing_message())

    def test_resistivity_running(self):
        self.fake_connection.setup_response('1;No error')
        response = self.dut.get_resistivity_running_status()
        self.assertAlmostEqual(response, 1)
        self.assertIn('RESISTIVITY:RUNNING?', self.fake_connection.get_outgoing_message())