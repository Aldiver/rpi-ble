import multiprocessing
import queue
from typing import Any, Dict, List

import dbus

from gattservice.core_ble.characteristic import Characteristic
from gattservice.core_ble.constants import DBUS_PROP_IFACE, GATT_SERVICE_IFACE
from gattservice.exceptions import InvalidArgsException
from gattservice.util import check_flags


class Service(dbus.service.Object):
    """
    org.bluez.GattService1 interface implementation
    """

    PATH_BASE = "/org/bluez/heatguard/service"

    def __init__(self, bus, index, uuid, primary):
        self.path = self.PATH_BASE + str(index)
        self.bus = bus
        self.uuid = uuid
        self.primary = primary
        self.characteristics = []
        dbus.service.Object.__init__(self, bus, self.path)
        
    def get_properties(self) -> Dict[str, Dict[str, Any]]:
        return {
            GATT_SERVICE_IFACE: {
                "UUID": self.uuid,
                "Primary": self.primary,
                "characteristics": dbus.Array(self.get_characteristic_paths(), signature="o"),
            }
        }

    def get_path(self) -> dbus.ObjectPath:
        return dbus.ObjectPath(self.path)

    def add_characteristic(self, uuid: str, flags: List[str], description: str, default_value: Any, sensor_queue: multiprocessing.Queue):
        check_flags(flags)

        characteristic = Characteristic(
            self.bus,
            len(self.characteristics),
            uuid,
            flags,
            self,
            description,
            default_value,
            sensor_queue,
        )

        self.characteristics.append(characteristic)

    def write_to_characteristic(self, value: Any, uuid: str):
        # self.characteristic_queues[uuid].put(value)
        print(f"Writing to characteristic with UUID {uuid}: {value}")

    def get_characteristic_paths(self) -> List[dbus.ObjectPath]:
        result = []
        for characteristic in self.characteristics:
            result.append(characteristic.get_path())
        return result

    def get_characteristics(self) -> List[Characteristic]:
        """
        Returns the characteristics of the service.

        Returns:
            List[Characteristic]: The characteristics of the service.
        """
        return self.characteristics

    @dbus.service.method(DBUS_PROP_IFACE, in_signature="s", out_signature="a{sv}")
    def GetAll(self, interface) -> Dict[str, Any]:
        """
        Returns all the properties of the service.

        Args:
            interface (str): The interface of the service.

        Raises:
            InvalidArgsException: If the interface is not the GATT service interface.

        Returns:
            Dict[str, Any]: All the properties of the service.
        """
        if interface != GATT_SERVICE_IFACE:
            raise InvalidArgsException()

        return self.get_properties()[GATT_SERVICE_IFACE]
