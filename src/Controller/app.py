import time

from MeccanoModules.ModuleDiscovery import ModuleDiscovery
from Serial.SerialPort import SerialPort

__author__ = 'robert'


def run_demo():
    print("Meccano Module Demo")
    port = SerialPort(pin=4, bit_compensation=77)
    md = ModuleDiscovery(port)

    md.discover_modules_in_channel()

    if md.modules[0] is None:
        print("FAILED TO DISCOVER MECCA SERVOS")
        exit()
  
    print("Found modules.  Lets exercise them")

    #
    # Run the 2 servos through some tasks
    commands = [
        (50,  (1, 0, 0)),
        (75,  (0, 1, 0)),
        (100, (0, 0, 1)),
        (125, (1, 0, 0)),
        (150, (0, 1, 0)),
        (175, (0, 0, 1)),
    ]

    m1 = md.modules[0]
    m2 = md.modules[1]
    for i in range(30):
        idx = i % len(commands)
        p = commands[idx][0]
        r, g, b = commands[idx][1]
        m1.set_position(p)
        m2.set_color(r, g, b)
        time.sleep(1)


if __name__ == "__main__":
    run_demo()
