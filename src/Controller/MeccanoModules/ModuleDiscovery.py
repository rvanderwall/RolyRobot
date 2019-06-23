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
        self.protocol.set_inititlization_sequence()

        for module_id in range(MIN_MODULE_ID, MAX_NUM_MODULES):
            ok = self.__discover_one_module(module_id)
            if not ok:
                break

    def __discover_one_module(self, module_id):
        still_discovering = True
        while still_discovering:
            resp = self.protocol.send_data_and_get_response(module_id)
            print("Got {} from module string".format(resp))
            if resp == MODULE_NOT_RESPONDING:
                return False

            if resp == ID_NOT_ASSIGNED:
                self.protocol.set_report_type_instruction(module_id)

            if resp == MODULE_TYPE_SERVO:
                module = ServoModule(self.protocol, module_id)
                self.modules[module_id] = module
                still_discovering = False

            if resp == MODULE_TYPE_LED:
                module = LightModule(self.protocol, module_id)
                self.modules[module_id] = module
                still_discovering = False

            sleep(5)


if __name__ == "__main__":
    from Serial.SerialPort import SerialPort
    port = SerialPort(4)
    print("Meccano Module")
    md = ModuleDiscovery(port)
    md.discover_modules_in_channel()

