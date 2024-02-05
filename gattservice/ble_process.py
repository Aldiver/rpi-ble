import enum
import queue
from multiprocessing import Process, Manager
from signal import SIGINT, SIGTERM, signal
from typing import Any

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service
from gi.repository import GLib

from gattservice.core_ble.advertisement import Advertisement
from gattservice.core_ble.application import Application
from gattservice.core_ble.constants import ALERT_NOTIF_UUID, BLUEZ_SERVICE_NAME, BODY_TEMP_SENSOR_UUID, GATT_MANAGER_IFACE, GSR_SENSOR_UUID, PULSE_SENSOR_UUID, TEMP_HUMI_SENSOR_UUID
from gattservice.core_ble.service import Service
from gattservice.exceptions import BluetoothNotFoundException
from gattservice.util import find_adapter


def register_app_cb():
    print("Bluetooth service registered")


def register_app_error_cb(error):
    print("Failed to register application: " + str(error))


class BLEProcess(Process):
    def __init__(self, output_queue: {}) -> None:
        super().__init__()
        self._system_bus = None
        self._mainloop = None
        self._advertisement = None
        self._services = []
        self._sensor_queues = {}
        self.output_queue = output_queue

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
            name="HEATGUARD",
        )
        # Create the application and add the service to it
        app = Application(self._system_bus)
        
        #Sensor Service
        Sensor_Service = Service(
            bus=self._system_bus,
            index=0,
            uuid="00001811-0000-1000-8000-00805f9b34fb",
            primary=True,
        )

        Sensor_Service.add_characteristic(
            PULSE_SENSOR_UUID, ["read", "notify"], "Pulse Characteristic", "Heart Rate", self.output_queue[PULSE_SENSOR_UUID]
        )

        Sensor_Service.add_characteristic(
            BODY_TEMP_SENSOR_UUID, ["read", "notify"], "BodyTemp Characteristic", "35", self.output_queue[BODY_TEMP_SENSOR_UUID]
        )

        Sensor_Service.add_characteristic(
            GSR_SENSOR_UUID, ["read", "notify"], "GSR Characteristic", "232", self.output_queue[GSR_SENSOR_UUID]
        )        
        
        Sensor_Service.add_characteristic(
            TEMP_HUMI_SENSOR_UUID, ["read", "notify"], "TempHumid Characteristic", "37", self.output_queue[TEMP_HUMI_SENSOR_UUID]
        )

        #Alert Service
        Rasp_Service = Service(
            bus=self._system_bus,
            index=1,
            uuid="00001811-0000-1000-8000-00123f9b34fb",
            primary=True,
        )
        Rasp_Service.add_characteristic(
            ALERT_NOTIF_UUID, ["write", "notify"], "Alert Characteristic", "", self.output_queue[ALERT_NOTIF_UUID]
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
        # print(self._advertisement.get_properties())
        self._mainloop.run()