__author__ = 'robert'

from datetime import datetime
import unittest


from Serial.SerialPort import SerialPort, BIT_DELAY


class SerialPortTests(unittest.TestCase):

    def setUp(self):
        self.port = SerialPort()

    def test_can_sent_0_byte(self):
        self.port.send_one_byte(0x00)

        from Serial.MockGPIO import gpio_output
        self.assertEqual(len(gpio_output), 11)
        self.assertEqual(gpio_output[0], 0)         # Start bit
        self.assertEqual(gpio_output[1], 0)         # 1st bit
        self.assertEqual(gpio_output[2], 0)         # 2nd bit
        self.assertEqual(gpio_output[3], 0)         # 3rd bit
        self.assertEqual(gpio_output[4], 0)         # 4th bit
        self.assertEqual(gpio_output[5], 0)         # 5th bit
        self.assertEqual(gpio_output[6], 0)         # 6th bit
        self.assertEqual(gpio_output[7], 0)         # 7th bit
        self.assertEqual(gpio_output[8], 0)         # 8th bit
        self.assertEqual(gpio_output[9], 1)         # stop bit
        self.assertEqual(gpio_output[10], 1)        # stop bit

    def test_can_send_1_byte(self):
        self.port.send_one_byte(0x01)

        from Serial.MockGPIO import gpio_output
        self.assertEqual(len(gpio_output), 11)
        self.assertEqual(gpio_output[0], 0)         # Start bit
        self.assertEqual(gpio_output[1], 1)         # 1st bit
        self.assertEqual(gpio_output[2], 0)         # 2nd bit
        self.assertEqual(gpio_output[3], 0)         # 3rd bit
        self.assertEqual(gpio_output[4], 0)         # 4th bit
        self.assertEqual(gpio_output[5], 0)         # 5th bit
        self.assertEqual(gpio_output[6], 0)         # 6th bit
        self.assertEqual(gpio_output[7], 0)         # 7th bit
        self.assertEqual(gpio_output[8], 0)         # 8th bit
        self.assertEqual(gpio_output[9], 1)         # stop bit
        self.assertEqual(gpio_output[10], 1)        # stop bit

    def test_can_send_128_byte(self):
        self.port.send_one_byte(128)

        from Serial.MockGPIO import gpio_output
        self.assertEqual(len(gpio_output), 11)
        self.assertEqual(gpio_output[0], 0)         # Start bit
        self.assertEqual(gpio_output[1], 0)         # 1st bit
        self.assertEqual(gpio_output[2], 0)         # 2nd bit
        self.assertEqual(gpio_output[3], 0)         # 3rd bit
        self.assertEqual(gpio_output[4], 0)         # 4th bit
        self.assertEqual(gpio_output[5], 0)         # 5th bit
        self.assertEqual(gpio_output[6], 0)         # 6th bit
        self.assertEqual(gpio_output[7], 0)         # 7th bit
        self.assertEqual(gpio_output[8], 1)         # 8th bit
        self.assertEqual(gpio_output[9], 1)         # stop bit
        self.assertEqual(gpio_output[10], 1)        # stop bit

    def test_can_send_255_byte(self):
        self.port.send_one_byte(255)

        from Serial.MockGPIO import gpio_output
        self.assertEqual(len(gpio_output), 11)
        self.assertEqual(gpio_output[0], 0)         # Start bit
        self.assertEqual(gpio_output[1], 1)         # 1st bit
        self.assertEqual(gpio_output[2], 1)         # 2nd bit
        self.assertEqual(gpio_output[3], 1)         # 3rd bit
        self.assertEqual(gpio_output[4], 1)         # 4th bit
        self.assertEqual(gpio_output[5], 1)         # 5th bit
        self.assertEqual(gpio_output[6], 1)         # 6th bit
        self.assertEqual(gpio_output[7], 1)         # 7th bit
        self.assertEqual(gpio_output[8], 1)         # 8th bit
        self.assertEqual(gpio_output[9], 1)         # stop bit
        self.assertEqual(gpio_output[10], 1)        # stop bit

    def test_time_to_sent(self):
        start = datetime.now()
        self.port.send_one_byte(0x00)
        end = datetime.now()

        expected = BIT_DELAY * 11
        actual = (end - start).microseconds

        self.assertAlmostEqual(expected, actual, delta = 100)

    def test_can_recieve_byte(self):
        in_byte = self.port.receive_one_byte()

        self.assertEqual(in_byte, 0xFF)