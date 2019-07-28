from time import sleep

__author__ = 'robert'


HEADER = 0xFF

ID_NOT_ASSIGNED = 0xFE      # No module at this position
ERASE_ID_AND_RESET = 0xFD
REPORT_TYPE = 0xFC          # Instruct module to report its type
RESERVED_1 = 0xFB

MODULE_NOT_RESPONDING = -1

MODULE_TYPE_UNKNOWN = 0
MODULE_TYPE_SERVO = 1
MODULE_TYPE_LED = 2

MIN_MODULE_ID = 0
MAX_NUM_MODULES = 4


class MeccaProtocol:
    """
        Each channel sends data to a chain of up to 4 daisy chained modules
        The first servo plugged in is 0.  The next servo is 1.  The third servo is 2.
        The last servo in a chain of 4 servos is 3.
        Data is 6 bytes : header, 4 data bytes, checksum
        Header is 0xff so no other databyte can have that value

        We can send data to all four modules in a chain with one send but
        we can only get a response from one of the modules at a time.

        Typically, you'd send motion and light data while you rotate through
        the module getting position data.
    """
    def __init__(self, serial_port):
        self.data = [0] * MAX_NUM_MODULES
        self.port = serial_port

    def set_initialization_sequence(self):
        self.data = [ID_NOT_ASSIGNED] * MAX_NUM_MODULES

    def set_reset_data(self, module_id):
        assert MIN_MODULE_ID <= module_id < MAX_NUM_MODULES
        self.data[module_id] = ERASE_ID_AND_RESET

    def set_report_type_instruction(self, module_id):
        assert MIN_MODULE_ID <= module_id < MAX_NUM_MODULES
        self.data[module_id] = REPORT_TYPE

    def set_data(self, module_id, data):
        assert MIN_MODULE_ID <= module_id < MAX_NUM_MODULES
        assert 0 <= data < RESERVED_1
        self.data[module_id] = data

    def send_data(self, module_id):
        """
            Sends the current data to all four modules and does not
            get a response
        :param module_id:
        :return:
        """
        assert MIN_MODULE_ID <= module_id < MAX_NUM_MODULES
        self.__send_data_to_module_chain(module_id)
        sleep(0.10)

    def send_data_and_get_response(self, module_id):
        """
            Sends the current data to all four modules and gets
            the response from the selected module
        :param module_id:
        :return:
        """
        assert MIN_MODULE_ID <= module_id < MAX_NUM_MODULES
        self.__send_data_to_module_chain(module_id)
        resp = self.__get_data_from_chain()
        sleep(0.10)
        return resp

    def __send_data_to_module_chain(self, module_id):
        data = [HEADER] + self.data + [self.__calculate_checksum(module_id), ]
        self.port.send_many_bytes(data)

    def __get_data_from_chain(self):
        input_byte = self.port.receive_one_byte()
        if input_byte == -1:
            input_byte = MODULE_NOT_RESPONDING
        return input_byte

    def __calculate_checksum(self, module_id):
        checksum = self.data[0] + self.data[1] + self.data[2] + self.data[3]
        checksum += (checksum >> 8)
        checksum += (checksum << 4)
        checksum &= 0xF0
        checksum |= module_id
        return checksum


if __name__ == "__main__":
    print("MeccanoModule")
