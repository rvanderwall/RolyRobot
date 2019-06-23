__author__ = 'robert'

import time
from time import sleep
import datetime as dt

try:
    import RPi.GPIO as GPIO
    print("Imported GPIO")
except:
    from Serial.MockGPIO import MockGPIO
    GPIO = MockGPIO()

BIT_DELAY = 417  # 417 us per bit
MAX_DELAY = BIT_DELAY * 8

class SerialPort:
    '''
    This class uses a GPIO port as a serial port for the Meccano smart module.
    Send to the modules ar 2400 baud (417 microseconds per bit)
    Recieve from the module at 1.1 mSec per bit
    '''
    def __init__(self, pin = 4):
        print("Set mode to BCM and use pin {}".format(pin))
        GPIO.setmode(GPIO.BCM)
        self.pin = pin

    def send_many_bytes(self, bytes):
        print("Send many bytes")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        for byte in bytes:
            self.__send(byte)
        GPIO.cleanup()

    def send_one_byte(self, byte):
        print("Send one byte")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.__send(byte)
        GPIO.cleanup()

    def receive_one_byte(self):
        '''
            Returns one byte or -1 if no module is responding.
        :return:
        '''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        byte = self.__receive()
        GPIO.cleanup()
        return byte

    def __send(self, byte):
        print("Send byte {}".format(byte))
        start = dt.datetime.now()
        self.__output_bit(0)        # Start bit


        bit_mask = 0x01
        while bit_mask < 0x100:
            if byte & bit_mask:
                self.__output_bit(1)
            else:
                self.__output_bit(0)
            bit_mask = bit_mask << 1

        self.__output_bit(1)        # Stop bits
        self.__output_bit(1)
        end = dt.datetime.now()
        print("Byte time = {} ({})".format((end-start).microseconds, 11 * BIT_DELAY))


    def __output_bit(self, value):
        start = dt.datetime.now()
        if value:
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            GPIO.output(self.pin, GPIO.LOW)

	# Compensate for time it takes to get now()
        end = self.__delay_in_microseconds(start, BIT_DELAY - 60)
        # print("Bit time = {}".format(end - start))
        # print("Excess Bit time = {}".format((end - start).microseconds - BIT_DELAY))

    def __delay_in_microseconds(self, start, delay):
        now = dt.datetime.now()
        while (now - start).microseconds < delay:
            now = dt.datetime.now()
        # print("Delay time = {}".format(now-start))
        return now

    def __receive(self):
        byte = 0
        mask = 0x80
        while mask > 0:
            bit = self.__get_bit()
            if bit == 1:
                byte |= mask
            mask = mask >> 1
        return byte

    def __get_bit(self):

        in_pin = GPIO.input(self.pin)
        counter = 0
        while in_pin == 0 and counter < 100:
            in_pin = GPIO.input(self.pin)
            counter += 1

        start_high = dt.datetime.now()
        counter = 0
        while in_pin == 1 and counter < 100:
            in_pin = GPIO.input(self.pin)
            counter += 1

        start_low = dt.datetime.now()
        counter = 0
        while in_pin == 0 and counter < 100:
            in_pin = GPIO.input(self.pin)
            counter += 1

        end_low = dt.datetime.now()

        high_time = (start_low - start_high).microseconds
        low_time = (end_low - start_low).microseconds

        if low_time > high_time:
            return 0
        else:
            return 1




def test_timing():
    microsecond = 1.0 / 1000000
    for _ in range(100):
        then = dt.datetime.now()
        time.sleep(0 * microsecond)
        now = dt.datetime.now()
        print("Time sleeping = {}".format(now-then))
    # Sleep		Actual
    # 1000000	1,001,150
    # 100000	100,270
    # 10000         10,250
    # 1000		1,150		# 1 mSec
    # 500		610		#
    # 400		513
    # 300		420
    # 200		315
    # 100		220
    # 50		165
    # 10		120
    # 0		45
    # None		35 (17)

if __name__ == "__main__":
    print("Serial Port")
    port = SerialPort(pin=4)
    port.send_one_byte(0xA5)
#    for i in range(10):
#        port.send_one_byte(0xff)
#    port.send_many_bytes([0xAA,0x55,0xAA,0x55])

#    for i in range(10):
#        byte=port.receive_one_byte()
#        print("Got one byte: {}".format(byte))

