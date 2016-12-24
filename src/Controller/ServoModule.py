__author__ = 'robert'

from Protocol import MeccaBrainModule, SERVO_LIM_MODE

class ServoModule():
    def __init__(self, channel, moduleID):
        self.protocol = MeccaBrainModule(moduleID, channel)
        self.output_byte = 0


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
        self.output_byte = 0xF | (red) | (green << 1) | (blue << 2)

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
        self.output_byte = position

    def set_LIM_mode(self):
        '''
            sets a specific servo to LIM mode
            LIM stands for Learned Intelligent Movement.  It is a special mode where
            the servo IC stops driving the motor and just sends back the position of the servo.
        :return:
        '''
        self.output_byte = SERVO_LIM_MODE
