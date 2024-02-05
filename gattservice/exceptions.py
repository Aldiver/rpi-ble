import dbus.exceptions


class InvalidArgsException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.freedesktop.DBus.Error.InvalidArgs"


class BluetoothNotFoundException(Exception):
    def __init__(
        self,
    ):
        super().__init__("Bluetooth service was not found, your Bluetooth is most likely off")


class AdvertisementException(Exception):
    def __init__(self):
        super().__init__("Advertisement Registration Error occurred")
