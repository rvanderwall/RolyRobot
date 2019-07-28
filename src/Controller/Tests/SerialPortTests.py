from datetime import datetime
import unittest

from Serial.SerialPort import SerialPort, NOMINAL_BIT_DELAY

__author__ = 'robert'


class SerialPortTests(unittest.TestCase):

    def setUp(self):
        pin = 4
        self.port = SerialPort(pin=pin, bit_compensation=10)

    def test_can_sent_byte_of_0(self):
        # Arrange

        # Act
        self.port.send_one_byte(0x00)

        # Assert
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

    def test_can_sent_byte_of_FF(self):
        # Arrange

        # Act
        self.port.send_one_byte(0xFF)

        # Assert
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

    test_cases = [
        (0x01, [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1]),  # Start bit, 1000 0000 Stop Bits
        (128,  [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]),  # Start bit, 0000 0001 Stop bits
        (0x55, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]),  # Start bit, 0000 0001 Stop bits
        (0xAA, [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1]),  # Start bit, 0000 0001 Stop bits
        (0xFF, [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),  # Start bit, 0000 0001 Stop bits
    ]

    def test_can_send_one_byte(self):
        for data, expected in self.test_cases:
            # Arrange

            # Act
            self.port.send_one_byte(data)

            # Assert
            from Serial.MockGPIO import gpio_output

            # Start bit, 1000 0000 Stop Bits
            self.assertEquals(gpio_output, expected, "Wrong output for input:" + '%02x' % data)

    def test_time_to_sent(self):
        start = datetime.now()
        self.port.send_one_byte(0x00)
        end = datetime.now()

        expected = NOMINAL_BIT_DELAY * 11
        actual = (end - start).microseconds

        self.assertAlmostEqual(expected, actual, delta=100)

    def test_can_receive_byte(self):
        in_byte = self.port.receive_one_byte()

        # We don't get a start bit with the mock.
        self.assertEqual(in_byte, -1)
