from typing import Dict

import dbus

from gattservice.core_ble.constants import DBUS_OM_IFACE
from gattservice.core_ble.service import Service


class Application(dbus.service.Object):
    """
    org.bluez.GattApplication1 interface implementation.
    """

    def __init__(self, system_bus: dbus.SystemBus) -> None:
        self.path = "/"
        self.services = []

        dbus.service.Object.__init__(self, system_bus, self.path)

    def get_path(self) -> str:
        return dbus.ObjectPath(self.path)

    def add_service(self, service: Service) -> None:
        self.services.append(service)
    
    @dbus.service.method(DBUS_OM_IFACE, out_signature="a{oa{sa{sv}}}")
    def GetManagedObjects(self) -> Dict[str, dbus.ObjectPath]:
        response = {}

        for service in self.services:
            response[service.get_path()] = service.get_properties()
            characteristics = service.get_characteristics()
            for characteristic in characteristics:
                response[characteristic.get_path()] = characteristic.get_properties()
                descriptors = characteristic.get_descriptors()
                for descriptor in descriptors:
                    response[descriptor.get_path()] = descriptor.get_properties()

        return response
