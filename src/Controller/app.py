from MeccanoModules.ModuleDiscovery import ModuleDiscovery
from Serial.SerialPort import SerialPort

__author__ = 'robert'


def run_demo():
    print("Meccano Module Demo")
    port = SerialPort(pin=4, bit_compensation=77)
    md = ModuleDiscovery(port)
    md.discover_modules_in_channel()

    m1 = md.modules[0]
    m1.set_position(50)

    m2 = md.modules[1]
    m2.set_color(1, 0, 0)

if __name__ == "__main__":
    run_demo()
