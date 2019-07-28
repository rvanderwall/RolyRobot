import time
import datetime as dt

try:
    import RPi.GPIO as GPIO
    print("Imported GPIO")
except:
    from Serial.MockGPIO import MockGPIO
    GPIO = MockGPIO()

__author__ = 'robert'


NOMINAL_BIT_DELAY = 417             # 417 us per bit
MAX_RCV_BIT_COUNT = 1000


class SerialPort:
    """
    This class uses a GPIO port as a serial port for the Meccano smart module.
    Send to the modules at 2400 baud (417 microseconds per bit)
    Recieve from the module at 1.1 mSec per bit
    """
    def __init__(self, pin, bit_compensation):
        print("Set mode to BCM and use pin {}".format(pin))
        assert 0 <= pin <= 15
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        self.bit_delay = NOMINAL_BIT_DELAY - bit_compensation

    def send_many_bytes(self, bytes_to_send):
        # print("Send many bytes")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        for byte_to_send in bytes_to_send:
            self.__send(byte_to_send)
        GPIO.cleanup()

    def send_one_byte(self, byte_to_send):
        # print("Send one byte")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.__send(byte_to_send)
        GPIO.cleanup()

    def receive_one_byte(self):
        """
            Returns one byte or -1 if no module is responding.
        :return:
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        received_byte = self.__receive()
        GPIO.cleanup()
        return received_byte

    def __send(self, byte_to_send):
        # print("Send byte {}".format(hex(byte_to_send)))
        self.__output_bit(0)        # Start bit

        bit_mask = 0x01
        while bit_mask < 0x100:
            if byte_to_send & bit_mask:
                self.__output_bit(1)
            else:
                self.__output_bit(0)
            bit_mask <<= 1

        self.__output_bit(1)        # Stop bits
        self.__output_bit(1)

    def __output_bit(self, value):
        start = dt.datetime.now()
        if value:
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            GPIO.output(self.pin, GPIO.LOW)

        end = self.__delay_in_microseconds(start, self.bit_delay)
        return end

    def __delay_in_microseconds(self, start, delay):
        now = dt.datetime.now()
        while (now - start).microseconds < delay:
            now = dt.datetime.now()
        return now

    def __receive(self):
        """
          bits arrive MSB first.  (Doesn't look to be true)
          the 'start bit' is a 0 lasting for about 2 mSec.
          bits are pwm.  They start high and then go low.
          if time_high > time_low, it is a 1 bit
        """
        rcved_byte = 0
        mask = 0x01   # 0x80
        resp = self.__wait_for_start_bit()
        if resp == -1:
            return -1

        while mask < 0x100:  # mask > 0:
            bit = self.__get_bit()
            if bit == -1:
                return -1
            if bit == 1:
                rcved_byte |= mask
            mask <<= 1  # >>= 1
        return rcved_byte

    def __wait_for_start_bit(self):
        counter = 0

        in_pin = GPIO.input(self.pin)
        while in_pin == 1 and counter <= MAX_RCV_BIT_COUNT * 10:
            in_pin = GPIO.input(self.pin)
            counter += 1
        if in_pin == 1:
            print("ERROR: Start Bit not found, time exceeded")
            return -1

        while in_pin == 0 and counter <= MAX_RCV_BIT_COUNT:
            in_pin = GPIO.input(self.pin)
            counter += 1
        if in_pin == 0:
            print("ERROR: Start Bit time exceeded")
            return -1

        # print("Stop bit found with count = {}".format(counter))
        return 0

    def __get_bit(self):
        start_high = dt.datetime.now()
        counter = 0
        in_pin = GPIO.input(self.pin)
        while in_pin == 1 and counter <= MAX_RCV_BIT_COUNT:
            in_pin = GPIO.input(self.pin)
            counter += 1
        if counter >= MAX_RCV_BIT_COUNT:
            print("ERROR: Bit high-time exceeded")
            return -1
        # print("High bit found with count = {}".format(counter))

        start_low = dt.datetime.now()
        counter = 0
        while in_pin == 0 and counter <= MAX_RCV_BIT_COUNT:
            in_pin = GPIO.input(self.pin)
            counter += 1
        if counter >= MAX_RCV_BIT_COUNT:
            print("ERROR: Bit low-time exceeded")
            return -1
        # print("Low bit found with count = {}".format(counter))

        end_low = dt.datetime.now()

        high_time = (start_low - start_high).microseconds
        low_time = (end_low - start_low).microseconds

        if low_time > high_time:
            # print("Got 0 bit")
            return 0
        else:
            # print("Got 1 bit")
            return 1


#
# Run timing tests on actual Raspberry PI to see now long sleep actually lasts
#
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
    port = SerialPort(pin=4, bit_compensation=77)
#    port.send_one_byte(0xA5)
#    port.send_many_bytes([0xAA,0x55,0xAA,0x55])

    print("Send init sequence to get some actual data")
    port.send_many_bytes([0xFF, 0xFE, 0xFE, 0xFE, 0xFE, 0xa0])
    byte = port.receive_one_byte()
    print("byte: {}".format(hex(byte)))
#    for i in range(10):
#        byte=port.receive_one_byte()
#        print("Got one byte: {}".format(byte))
