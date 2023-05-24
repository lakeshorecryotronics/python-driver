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
