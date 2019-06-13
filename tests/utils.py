import logging
from collections import deque

import unittest2 as unittest

from lakeshore import Teslameter

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


class TestWithFakeDUT(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeDutConnection()
        self.fake_connection.setup_response('LSCI,FakeModel,FakeSerial,999.999.999')  # Simulate maximum version so all methods are allowed
        self.dut = Teslameter(connection=self.fake_connection)
        self.fake_connection.reset()  # Clear startup activity


class TestWithRealDUT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Teslameter is used for these general tests on the HIL rig at this time
        cls.dut = Teslameter(flow_control=False)  # TODO: Get a dut with flow control for the HIL rig then remove this.

    @classmethod
    def tearDownClass(cls):
        del cls.dut

    def tearDown(self):
        self.dut.query('SYSTEM:ERROR:ALL?', check_errors=False)  # Discard any errors left in the queue
