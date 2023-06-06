from tests.utils import TestWithFakeModel121


class TestCommandAndQuery(TestWithFakeModel121):
    def test_multiple_command(self):
        """Test for multiple commands sent repeatedly
            Note: Multiple blank responses are needed because the commands are called via the query function which will
            clear the buffer (pop the deque).
        """
        for i in range(4):
            self.fake_connection.setup_response('0')
            self.dut.command("LOCK 1")
        self.fake_connection.setup_response('1')
        response = self.dut.query("LOCK?")
        self.assertEqual(response, '1')


class TestCurrentCommands(TestWithFakeModel121):
    def test_set_current(self):
        for i in range(3):
            self.fake_connection.setup_response('')
        self.dut.set_current(0.01)
        self.assertIn('RANGE 13', self.fake_connection.get_outgoing_message())
        self.assertIn('SETI 0.01', self.fake_connection.get_outgoing_message())
        self.assertIn('IENBL 1', self.fake_connection.get_outgoing_message())

    def test_get_current(self):
        self.fake_connection.setup_response('+100.000E-03')
        response = self.dut.get_current()
        self.assertEqual(response, 0.1)
        self.assertIn('SETI?', self.fake_connection.get_outgoing_message())

    def test_enable_current(self):
        self.fake_connection.setup_response('')
        self.dut.enable_current()
        self.assertIn('IENBL 1', self.fake_connection.get_outgoing_message())

    def test_disable_current(self):
        self.fake_connection.setup_response('')
        self.dut.disable_current()
        self.assertIn('IENBL 0', self.fake_connection.get_outgoing_message())


class TestGeneralCommands(TestWithFakeModel121):

    def test_reset_instrument(self):
        self.fake_connection.setup_response('')
        self.dut.reset_instrument()
        self.assertIn('*RST', self.fake_connection.get_outgoing_message())

    def test_set_brightness(self):
        for i in 0, 7, 15:
            with self.subTest(f"Set brightness {i}"):
                self.fake_connection.setup_response('')
                self.dut.set_display_brightness(i)
                self.assertIn(f'BRIGT {i}', self.fake_connection.get_outgoing_message())

    def test_get_brightness(self):
        for i in "00", "07", "15":
            with self.subTest(f"Get brightness {i}"):
                self.fake_connection.setup_response(i)
                response = self.dut.get_display_brightness()
                self.assertEqual(response, int(i))
                self.assertIn('BRIGT?', self.fake_connection.get_outgoing_message())

    def test_compliance_limit_status(self):
        self.fake_connection.setup_response('0')
        response = self.dut.get_compliance_limit_status()
        self.assertEqual(response, False)
        self.assertIn('COMP?', self.fake_connection.get_outgoing_message())

    def test_factory_defaults(self):
        self.fake_connection.setup_response('')
        self.dut.set_factory_defaults()
        self.assertIn('DFLT 99', self.fake_connection.get_outgoing_message())

    def test_enable_keypad(self):
        self.fake_connection.setup_response('')
        self.dut.unlock_front_panel()
        self.assertIn('LOCK 0', self.fake_connection.get_outgoing_message())

    def test_disable_keypad(self):
        self.fake_connection.setup_response('')
        self.dut.lock_front_panel()
        self.assertIn('LOCK 1', self.fake_connection.get_outgoing_message())

    def test_get_keypad_status(self):
        self.fake_connection.setup_response('0')
        response = self.dut.get_front_panel_lock_status()
        self.assertEqual(response, False)
        self.assertIn('LOCK?', self.fake_connection.get_outgoing_message())

    def test_power_up_enable(self):
        self.fake_connection.setup_response('')
        self.dut.set_power_up_enable(True)
        self.assertIn('PWUPENBL 1', self.fake_connection.get_outgoing_message())

    def test_save_state(self):
        self.fake_connection.setup_response('')
        self.dut.save_current_state()
        self.assertIn('SETSAVE', self.fake_connection.get_outgoing_message())
