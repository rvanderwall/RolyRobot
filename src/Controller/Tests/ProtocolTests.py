__author__ = 'robert'

import unittest

from MeccanoModules.Protocol import MeccaProtocol

class mock_port():
    def __init__(self):
        self.bytes = []

    def send_one_byte(self, byte):
        self.bytes.append(byte)

    def receive_one_byte(self):
        return 0xfd

class ProtocolTests(unittest.TestCase):

    def setUp(self):
        self.port = mock_port()
        self.protocol = MeccaProtocol(self.port)

    def test_checksum_with_0s(self):
        self.protocol.data = [0, 0, 0, 0]
        module = 0
        resp = self.protocol.send_data_and_get_response(0)
        self.assertEquals(resp, 0xfd)

        expected_checksum = 0x00
        self.assertEquals(self.port.bytes, [0xFF, 0, 0, 0, 0, expected_checksum])

    def test_checksum_with_non_0s(self):
        self.protocol.data = [1, 2, 3, 4]
        module = 1
        resp = self.protocol.send_data_and_get_response(module)
        self.assertEquals(resp, 0xfd)

        expected_checksum = 0xA1
        self.assertEquals(self.port.bytes, [0xFF, 1, 2, 3, 4, expected_checksum])

    def test_checksum_with_large_values(self):
        self.protocol.data = [0xE0, 0xE0, 0xE0, 0xE0]
        module = 2
        resp = self.protocol.send_data_and_get_response(module)
        self.assertEquals(resp, 0xfd)

        expected_checksum = 0xB2
        self.assertEquals(self.port.bytes, [0xFF, 0xE0, 0xE0, 0xE0, 0xE0, expected_checksum])

