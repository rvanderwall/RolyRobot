__author__ = 'robert'


SERVO_LIM_MODE = 0xFA
RESERVED_2 = 0xF9
RESERVED_3 = 0xF8

# 0xF0 - 0xF7 Servo LED colors
SERVO_COLOR_WHITE = 0xF7
SERVO_COLOR_TEAL = 0xF6
SERVO_COLOR_PURPLE = 0xF5
SERVO_COLOR_BLUE = 0xF4
SERVO_COLOR_YELLOW = 0xF3
SERVO_COLOR_GREEN = 0xF2
SERVO_COLOR_RED = 0xF1
SERVO_COLOR_OFF = 0xF0

class ServoModule():
    def __init__(self, protocol, module_id):
        assert 0 <= module_id <= 3
        self.protocol = protocol
        self.module_id = module_id

        self.protocol.set_data(module_id, SERVO_COLOR_BLUE)

    def set_color(self, red, green, blue):
        '''
            0xF7 = R, G, B - all On
            0xF6 = G, B - On; R - Off
            0xF5 = R, B - On; G - Off
            0xF4 = B - On; R, G - Off
            0xF3 = R, G - On; B - Off
            0xF2 = G - On; R, B - Off
            0xF1 = R - On; G, B - Off
            0xF0 = R, G, B - all off
        '''
        assert 0 <= red <= 1
        assert 0 <= green <= 1
        assert 0 <= blue <= 1
        data = 0xF | (red) | (green << 1) | (blue << 2)
        self.__set_data(data)

    def set_position(self, position):
        '''
            0x00 = full clockwise
            0xEF = full counter clockwise
        :param position:
        :return:
        '''
        if position < 0x18:
            position = 0x18
        if position > 0xE8:
            position = 0xE8
        self.__set_data(position)

    def set_LIM_mode(self):
        '''
            sets a specific servo to LIM mode
            LIM stands for Learned Intelligent Movement.  It is a special mode where
            the servo IC stops driving the motor and just sends back the position of the servo.
        :return:
        '''
        position = self.__set_data(SERVO_LIM_MODE)
        return position

    def get_position(self):
        resp = self.set_LIM_mode()
        return resp

    def __set_data(self, data):
        self.protocol.set_data(self.module_id, data)
        resp = self.protocol.send_data_and_get_response(self.module_id)
        return resp