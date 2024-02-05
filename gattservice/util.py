from typing import List, Optional

import dbus

from gattservice.core_ble.constants import (
    BLUEZ_SERVICE_NAME,
    DBUS_OM_IFACE,
    GATT_MANAGER_IFACE,
)


def check_flags(flags: List[str]):
    for flag in flags:
        if flag not in ["read", "write", "notify"]:
            raise ValueError("unknown flag")


def byte_arr_to_str(byte_array: dbus.Array) -> str:
    byte_list = [bytes([v]) for v in byte_array]
    try:
        decoded_list = [str(v, "ascii") for v in byte_list]
        # Returns the array as a single string
        final_string = "".join(decoded_list)
    except Exception:
        raise ValueError
    return final_string


def str_to_byte_arr(text: str) -> dbus.Array:
    ascii_values = dbus.Array([], signature=dbus.Signature("y"))
    for character in text:
        ascii_values.append(dbus.Byte(ord(character)))
    return ascii_values


def find_adapter(bus: dbus.SystemBus) -> Optional[dbus.service.Object]:
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, "/"), DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    for o, props in objects.items():
        if GATT_MANAGER_IFACE in props.keys():
            return o

    return None
