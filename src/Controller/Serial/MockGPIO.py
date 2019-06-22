

gpio_output = []

class MockGPIO:
    def __init__(self):
        self.BCM = 1
        self.OUT = 2
        self.IN = 3
        self.HIGH = 4
        self.LOW = 5
        self.cur_mode = 0
        self.cur_pin = 0
        self.out_bits = []

    def setmode(self, mode):
        assert mode == self.BCM
        self.cur_mode = mode

    def setup(self, pin, mode):
        self.out_bits = []
        self.cur_pin = pin
        assert mode == self.OUT or mode == self.IN

    def cleanup(self):
        global gpio_output
        gpio_output = self.out_bits

    def output(self, pin, value):
        assert pin == self.cur_pin
        if value == self.HIGH:
            self.out_bits.append(1)
        elif value == self.LOW:
            self.out_bits.append(0)
        else:
            raise Exception("Invalid value")

    def input(self, pin):
        assert pin == self.cur_pin
        return 1
