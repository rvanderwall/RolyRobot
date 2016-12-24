__author__ = 'robert'

HEADER = 0xFF

ID_NOT_ASSIGNED = 0xFE
ERASE_RESET_ID = 0xFD
REPORT_TYPE = 0xFC
RESERVED_1 = 0xFB
SERVO_LIM_MODE = 0xFA
RESERVED_2 = 0xF9
RESERVED_3 = 0xF8
# 0xF0 - 0xF7 Servo LED colors

MODULE_TYPE_SERVO = 1
MODULE_TYPE_LED = 2

# The byte SERVONUM refers to the order of the servo in the chain.  The first servo plugged into your Arduino is 0.
# The next servo is 1.  The third servo is 2.   The last servo in a chain of 4 servos is 3.


'''
    Each channel sends data to a daisy chain of modules
    Data is 6 bytes : header, 4 data bytes, checksum
    Header is 0xff so no other databyte can be that value
'''
class MeccaBrainModule:
    def __init__(self, moduleID, channel):
        self.data = [0, 0, 0, 0]
        self.moduleID = moduleID
        self.channel = channel
        assert 0 <= moduleID <= 0xf
        assert 1 <= channel <= 8

    def reset_modules_in_channel(self):
        self.data = [ERASE_RESET_ID, ERASE_RESET_ID, ERASE_RESET_ID, ERASE_RESET_ID]
        self.__send_data_to_servo()

    def set_module1_data(self, data):
        self.__set_data(0, data)

    def setModule2Data(self, data):
        self.__set_data(1, data)

    def setModule3Data(self, data):
        self.__set_data(2, data)

    def setModule4Data(self, data):
        self.__set_data(3, data)

    def __set_data(self, module, data):
        assert 0 <= data <= 0xfe
        data[module] = data

    def __send_data_to_servo(self):
        self.send_one_byte(HEADER)
        self.send_one_byte(self.data[0])
        self.send_one_byte(self.data[1])
        self.send_one_byte(self.data[2])
        self.send_one_byte(self.data[3])
        self.send_one_byte(self.calculate_checksum())

    def calculate_checksum(self):
        checksum = 0x0
        checksum_byte= checksum << 4 + self.moduleID
        assert 0 <= checksum_byte <= 0xfe

    def send_one_byte(self, byte):
        '''
        Each bit is ~417 microseconds
        a low start bit, data, 2 high stop bits
        0-start bit - bit0 - bit1 ... bit7 - 1-stop - 1-stop
        :param byte:
        :return:
        '''
        pass