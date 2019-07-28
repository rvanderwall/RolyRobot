from MeccanoModules.Protocol import MeccaProtocol, ID_NOT_ASSIGNED, MODULE_NOT_RESPONDING
from MeccanoModules.Protocol import MODULE_TYPE_SERVO, MODULE_TYPE_LED
from MeccanoModules.Protocol import MAX_NUM_MODULES

from MeccanoModules.ServoModule import ServoModule
from MeccanoModules.LightModule import LightModule

__author__ = 'robert'


class ModuleDiscovery:
    def __init__(self, serial_port):
        self.protocol = MeccaProtocol(serial_port)
        self.modules = [None] * MAX_NUM_MODULES

    def discover_modules_in_channel(self):
        print("Discover modules")
        self.protocol.set_initialization_sequence()

        for module_id in range(MAX_NUM_MODULES):
            ok = self.__discover_one_module(module_id)
            if not ok:
                # We know that modules are chained, if not OK, nothing left in chain
                break

        return self.modules

    def __discover_one_module(self, module_id):
        """
            Assumes that data was initially set to the initialization sequence in the protocol
            Assumes that modules before module_id have been discovered
        :param module_id:
        :return:
        """
        found = False
        counter = 0
        while not found and counter < 10:
            # print("Top of module discovery loop {} for module {}".format(counter, module_id))

            resp = self.protocol.send_data_and_get_response(module_id)
            # print("Got resp {} from module {}".format(hex(resp), module_id))

            if resp == MODULE_NOT_RESPONDING:
                print("ERROR: Module {} not responding to discovery query".format(module_id))

            if resp == ID_NOT_ASSIGNED:
                print("Module {} has responded to discovery query".format(module_id))
                found = True

            counter += 1

        if not found:
            return False

        self.protocol.set_report_type_instruction(module_id)
        found = False
        counter = 0
        while not found and counter < 2:
            # print("Top of module type discovery loop {} for module {}".format(counter, module_id))
            resp = self.protocol.send_data_and_get_response(module_id)
            # print("Got resp {} from module {}".format(hex(resp), module_id))

            if resp == MODULE_TYPE_SERVO:
                module = ServoModule(self.protocol, module_id)
                module.set_color(0, 0, 1)   # Set to Blue initially
                self.modules[module_id] = module
                found = True

            if resp == MODULE_TYPE_LED:
                module = LightModule(self.protocol, module_id)
                module.set_color(0, 7, 0, 7)   # Set to Green initially
                self.modules[module_id] = module
                found = True

            counter += 1

        if not found:
            return False

        return True


if __name__ == "__main__":
    from Serial.SerialPort import SerialPort
    print("Meccano Module")
    port = SerialPort(pin=4, bit_compensation=77)
    md = ModuleDiscovery(port)
    md.discover_modules_in_channel()

    m1 = md.modules[0]
    m1.set_position(50)

    m2 = md.modules[1]
    m2.set_color(1, 0, 0)
