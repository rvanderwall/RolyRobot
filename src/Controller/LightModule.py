__author__ = 'robert'

from Protocol import MeccaBrainModule

class LightModule():
    def __init__(self, channel, moduleID):
        self.protocol = MeccaBrainModule(moduleID, channel)
        self.LED_byte1 = 0
        self.LED_byte2 = 0


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
        self.LED_byte1 = (green<<3) | red
        self.LED_byte2 = 0x40 | (fade_time<<3) | blue


