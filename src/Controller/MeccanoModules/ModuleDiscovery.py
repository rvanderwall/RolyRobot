__author__ = 'robert'

from time import sleep

from MeccanoModules.Protocol import MeccaProtocol, ID_NOT_ASSIGNED, MODULE_NOT_RESPONDING
from MeccanoModules.Protocol import MODULE_TYPE_SERVO, MODULE_TYPE_LED
from MeccanoModules.Protocol import MIN_MODULE_ID, MAX_NUM_MODULES

from MeccanoModules.ServoModule import ServoModule
from MeccanoModules.LightModule import LightModule


class ModuleDiscovery:
    def __init__(self, port):
        self.protocol = MeccaProtocol(port)
        self.modules = [None] * MAX_NUM_MODULES

    def discover_modules_in_channel(self):
        print("Discover modules")

        self.protocol.set_initialization_sequence()

        # for module_id in range(MIN_MODULE_ID, MAX_NUM_MODULES):
        for module_id in range(2):
            ok = self.__discover_one_module(module_id)
            if not ok:
                break

    def __discover_one_module(self, module_id):
        found = False
        counter = 0

        while not found and counter < 2:
            print("Top of module discovery loop {} for module {}".format(counter, module_id))
            resp = self.protocol.send_data_and_get_response(module_id)
            print("Got resp {} from module {}".format(hex(resp), module_id))

            if resp == MODULE_NOT_RESPONDING:
                print("ERROR: Module {} not responding".format(module_id))

            if resp == ID_NOT_ASSIGNED:
                found = True

            counter += 1


        self.protocol.set_report_type_instruction(module_id)

        found = False
        counter = 0
        while not found and counter < 2:
            print("Top of module type discovery loop {} for module {}".format(counter, module_id))
            resp = self.protocol.send_data_and_get_response(module_id)
            print("Got resp {} from module {}".format(hex(resp), module_id))

            if resp == MODULE_TYPE_SERVO:
                module = ServoModule(self.protocol, module_id)
                self.modules[module_id] = module
                module.set_color(0,0,1)
                found = True

            if resp == MODULE_TYPE_LED:
                module = LightModule(self.protocol, module_id)
                self.modules[module_id] = module
                found = True

            counter += 1

        return True


if __name__ == "__main__":
    from Serial.SerialPort import SerialPort
    print("Meccano Module")
    port = SerialPort(4)
    md = ModuleDiscovery(port)
    md.discover_modules_in_channel()

    m1 = md.modules[0]
    m1.set_position(50)

