import logging
from collections import deque

import unittest
from lakeshore import Teslameter, FastHall, Model372, Model335, Model240, Model224, Model336, SSMSystem

fake_dut_comms_log = logging.getLogger('fake_dut_comms')


class FakeDutConnection:
    def __init__(self):
        self.incoming = deque()
        self.outgoing = deque()
        self.FAKE_CONNECTION = True

    def setup_response(self, message):
        self.incoming.append(message)
        fake_dut_comms_log.info('Setup fake response: {}'.format(message))

    def get_outgoing_message(self):
        return self.outgoing.popleft()

    def reset(self):
        self.incoming.clear()
        self.outgoing.clear()

    def write(self, data):
        message = data.decode('ascii').rstrip()
        self.outgoing.append(message)
        fake_dut_comms_log.info('Write to dut: {}'.format(message))

    def read_until(self, terminator):
        return self.incoming.popleft().encode('ascii') + terminator

    def __getattr__(self, item):
        return lambda: None  # Ignore unimplemented methods


class TestWithFakeTeslameter(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeDutConnection()
        self.fake_connection.setup_response('LSCI,F71,FakeSerial,999.999.999')  # Simulate maximum version so all methods are allowed
        self.fake_connection.setup_response('No error')
        self.dut = Teslameter(connection=self.fake_connection)
        self.fake_connection.reset()  # Clear startup activity


class TestWithFakeFastHall(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeDutConnection()
        self.fake_connection.setup_response('LSCI,M91,FakeSerial,999.999.999')  # Simulate maximum version so all methods are allowed
        self.fake_connection.setup_response('No error')
        self.dut = FastHall(connection=self.fake_connection)
        self.fake_connection.reset()  # Clear startup activity


class TestWithFakeModel240(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeDutConnection()
        self.fake_connection.setup_response('LSCI,MODEL240,LSA22VS,1.4')
        self.dut = Model240(connection=self.fake_connection)
        self.fake_connection.reset()


class TestWithFakeModel372(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeDutConnection()
        self.fake_connection.setup_response('LSCI,MODEL372,LSA22VS,1.4')
        self.fake_connection.setup_response('1')
        self.dut = Model372(connection=self.fake_connection, baud_rate=56700)
        self.fake_connection.reset()


class TestWithFakeModel335(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeDutConnection()
        self.fake_connection.setup_response('LSCI,MODEL335,FakeSerial/FakeOption,999.999.999')  # Simulate maximum version so all methods are allowed
        self.fake_connection.setup_response('1')
        self.dut = Model335(connection=self.fake_connection, baud_rate=56700)
        self.fake_connection.reset()  # Clear startup activity


class TestWithFakeModel224(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeDutConnection()
        self.fake_connection.setup_response('LSCI,MODEL224,LSA22VS,1.4')
        self.dut = Model224(connection=self.fake_connection)
        self.fake_connection.reset()  # Clear startup activity


class TestWithFakeSSMS(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeDutConnection()
        self.fake_connection.setup_response('LSCI,M81,FakeSerial,999.999.999')  # Simulate maximum version so all methods are allowed
        # These are responses required to instantiate source modules
        self.fake_connection.setup_response('3;No error')
        self.fake_connection.setup_response('3;No error')
        self.dut = SSMSystem(connection=self.fake_connection)
        self.fake_connection.reset()  # Clear startup activity


class TestWithFakeSSMSSourceModule(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeDutConnection()
        self.fake_connection.setup_response('LSCI,M81,FakeSerial,999.999.999')  # Simulate maximum version so all methods are allowed
        # These are responses required to instantiate source modules
        self.fake_connection.setup_response('3;No error')
        self.fake_connection.setup_response('3;No error')
        self.dut_system = SSMSystem(connection=self.fake_connection)
        self.dut_module = self.dut_system.get_source_module(1)
        self.fake_connection.reset()  # Clear startup activity

    def queue_up_many_no_error_responses(self, num_responses):
        """Convenience function for when many commands are sent that require no error responses."""
        for _ in range(num_responses):
            self.fake_connection.setup_response('No error')


class TestWithFakeSSMSMeasureModule(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeDutConnection()
        self.fake_connection.setup_response('LSCI,M81,FakeSerial,999.999.999')  # Simulate maximum version so all methods are allowed
        # These are responses required to instantiate source modules
        self.fake_connection.setup_response('3;No error')
        self.fake_connection.setup_response('3;No error')
        self.dut_system = SSMSystem(connection=self.fake_connection)
        self.dut_module = self.dut_system.get_measure_module(1)
        self.fake_connection.reset()  # Clear startup activity


class TestWithFakeModel336(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeDutConnection()
        self.fake_connection.setup_response('LSCI,MODEL336,FakeSerial/FakeOption,999.999.999')
        self.dut = Model336(connection=self.fake_connection)
        self.fake_connection.reset() # Clear startup activity
