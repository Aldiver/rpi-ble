import enum
import queue
from multiprocessing import Process
from signal import SIGINT, SIGTERM, signal

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service
from gi.repository import GLib

from gattservice.core_ble.advertisement import Advertisement
from gattservice.core_ble.application import Application
from gattservice.core_ble.constants import BLUEZ_SERVICE_NAME, GATT_MANAGER_IFACE
from gattservice.core_ble.service import Service
from gattservice.exceptions import BluetoothNotFoundException
from gattservice.util import find_adapter


def register_app_cb():
    print("Bluetooth service registered")


def register_app_error_cb(error):
    print("Failed to register application: " + str(error))


class BLEProcess(Process):
    def __init__(self, output_queue: queue.Queue) -> None:
        super().__init__()
        self._system_bus = None
        self._mainloop = None
        self._advertisement = None
        self._output_queue = output_queue

    def _shutdown_handler(self, sig: enum, frame: enum) -> None:
        self._mainloop.quit()
        self._advertisement.release()

    def run(self) -> None:

        # The mainloop initialized here handles the asynchronous communication over dbus documentation can be found
        # here: https://docs.gtk.org/glib/main-loop.html
        self._mainloop = GLib.MainLoop()

        # register shutdown handler
        signal(SIGTERM, self._shutdown_handler)
        signal(SIGINT, self._shutdown_handler)

        # create the shared system bus object and find the main bluez adapter
        self._system_bus = dbus.SystemBus()
        adapter = find_adapter(self._system_bus)

        if not adapter:
            raise BluetoothNotFoundException()

        adapter_obj = self._system_bus.get_object(bus_name=BLUEZ_SERVICE_NAME, object_path=adapter)

        service_manager = dbus.Interface(adapter_obj, GATT_MANAGER_IFACE)

        # Create the advertisement
        self._advertisement = Advertisement(
            bus=self._system_bus,
            index=0,
            adapter_obj=adapter_obj,
            uuid="0000180d-aaaa-1000-8000-0081239b35fb",
            name="Thesis RPI0",
        )

        # Create the application and add the service to it
        app = Application(self._system_bus)
        
        #Sensor Service
        Sensor_Service = Service(
            bus=self._system_bus,
            index=0,
            uuid="00001812-0000-1000-8000-00805f9b34fb",
            primary=True,
            output_queue=self._output_queue,
        )

        Sensor_Service.add_characteristic(
            "00000540-0000-1000-8000-00805f9b34fb", ["read", "notify"], "Pulse Characteristic", "Heart Rate"
        )

        Sensor_Service.add_characteristic(
            "00000541-0000-1000-8000-00805f9b34fb", ["read", "notify"], "BodyTemp Characteristic", "35"
        )

        Sensor_Service.add_characteristic(
            "00000542-0000-1000-8000-00805f9b34fb", ["read", "notify"], "GSR Characteristic", "232"
        )        
        
        Sensor_Service.add_characteristic(
            "00000543-0000-1000-8000-00805f9b34fb", ["read", "notify"], "TempHumid Characteristic", "37"
        )

        #Alert Service
        Rasp_Service = Service(
            bus=self._system_bus,
            index=1,
            uuid="00001802-0000-1000-8000-00805f9b34fb",
            primary=True,
            output_queue=self._output_queue,
        )
        Rasp_Service.add_characteristic(
            "00002a06-0000-1000-8000-00805f9b34fb", ["write", "notify"], "Alert Characteristic", ""
        )

        app.add_service(Sensor_Service)
        app.add_service(Rasp_Service)

        # Initialise the advertisement
        self._advertisement.init_advertisement()

        # Register the application
        service_manager.RegisterApplication(
            app.get_path(),
            {},
            reply_handler=register_app_cb,
            error_handler=register_app_error_cb,
        )

        # Blocking call to run the main event loop
        self._mainloop.run()