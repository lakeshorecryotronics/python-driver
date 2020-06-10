import logging
from collections import deque

import unittest2 as unittest
from lakeshore import Teslameter, FastHall, Model372, Model335, Model240, Model224, SSMSystem

fake_dut_comms_log = logging.getLogger('fake_dut_comms')


class FakeDutConnection:
    def __init__(self):
        self.incoming = deque()
        self.outgoing = deque()

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

    def readline(self):
        return self.incoming.popleft().encode('ascii') + b'\n'

    def __getattr__(self, item):
        return lambda: None  # Ignore unimplemented methods


class TestWithFakeTeslameter(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeDutConnection()
        self.fake_connection.setup_response('LSCI,F71,FakeSerial,999.999.999')  # Simulate maximum version so all methods are allowed
        self.fake_connection.setup_response('No error')
        self.dut = Teslameter(connection=self.fake_connection)
        self.fake_connection.reset()  # Clear startup activity


class TestWithRealTeslameter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Teslameter is used for these general tests on the HIL rig at this time
        cls.dut = Teslameter()

    @classmethod
    def tearDownClass(cls):
        del cls.dut

    def tearDown(self):
        self.dut.query('SYSTEM:ERROR:ALL?', check_errors=False)  # Discard any errors left in the queue


class TestWithFakeFastHall(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeDutConnection()
        self.fake_connection.setup_response('LSCI,M91,FakeSerial,999.999.999')  # Simulate maximum version so all methods are allowed
        self.fake_connection.setup_response('No error')
        self.dut = FastHall(connection=self.fake_connection)
        self.fake_connection.reset()  # Clear startup activity


class TestWithRealFastHall(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dut = FastHall(flow_control=False)  # TODO: Get a dut with flow control for the HIL rig then remove this.

    @classmethod
    def tearDownClass(cls):
        del cls.dut

    def tearDown(self):
        self.dut.query('SYSTEM:ERROR:ALL?', check_errors=False)  # Discard any errors left in the queue


class TestWithFakeModel240(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeDutConnection()
        self.fake_connection.setup_response('LSCI,MODEL240/utils.py,LSA22VS,1.4')
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