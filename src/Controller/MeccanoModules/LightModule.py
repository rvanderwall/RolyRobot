__author__ = 'robert'



class LightModule():
    def __init__(self, protocol, module_id):
        assert 0 <= module_id <= 3
        self.protocol = protocol
        self.module_id = module_id
        LED_byte1 = 0x00
        LED_byte2 = 0x7F   # Blue with long fade.
        self.__set_data(LED_byte1)
        self.__set_data(LED_byte2)


    def set_color(self, red, green, blue, fade_time):
        '''
            The bytes RED, GREEN and BLUE  should have a value from 0 - 7   =  a total of 512 options.
            There are 8 levels of brightness for each color where 0 is OFF and 7 is full brightness.

            The byte FADETIME should have a value from 0 - 7.
            These are preset time values to transition between the current color to the new color.
            0 -  0 seconds (no fade, change immediately)
            1 -  200ms   (very very fast fade)
            2 -  500ms   (very fast fade)
            3 -  800ms  (fast fade)
            4 -  1 second (normal fade)
            5 -  2 seconds (slow fade)
            6  - 3 seconds (very slow fade)
            7 -  4 seconds  (very very slow fade)
        :param red:
        :param green:
        :param blue:
        :param fade_time:
        :return:
        '''
        assert 0 <= red <= 0x7
        assert 0 <= green <= 0x7
        assert 0 <= blue <= 0x7
        assert 0 <= fade_time <= 0x7
        LED_byte1 = (green<<3) | red
        LED_byte2 = 0x40 | (fade_time<<3) | blue
        self.__set_data(LED_byte1)
        self.__set_data(LED_byte2)

    def __set_data(self, data):
        self.protocol.set_data(self.module_id, data)
        resp = self.protocol.send_data_and_get_response(self.module_id)
        return resp