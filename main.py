import multiprocessing
import queue
import time

import dbus
import threading

from gattservice.ble_process import BLEProcess
from gattservice.core_ble.constants import CHARACTERISTIC_SENSOR_UUID, ALERT_NOTIF_UUID
# from sensorservice.alert_process import AlertProcess
from sensorservice.sensor_process import SensorProcess

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

queue_manager = {}
sensor_process = SensorProcess()
queue_manager[CHARACTERISTIC_SENSOR_UUID] = multiprocessing.Queue()
queue_manager[ALERT_NOTIF_UUID] = multiprocessing.Queue()

def main():
    ble_process = BLEProcess(queue_manager)
    ble_process.start()
    
    # uncomment if running in raspberry pi
    # alert_process = AlertProcess(queue_manager[ALERT_NOTIF_UUID])
    # alert_process.start()

    start_time = time.time()  # Record the start time
    while True:
        if time.time() - start_time >= 5:
            start_time = time.time()  # Reset the timer

                #if prev. reading not sent = no data update
            if queue_manager[CHARACTERISTIC_SENSOR_UUID].empty():
                print(f"Adding data to queue for sensor with UUID {CHARACTERISTIC_SENSOR_UUID}")
                # Call function to get sensor data and put it into the queue
                data = sensor_process.get_sensor_data()
                queue_manager[CHARACTERISTIC_SENSOR_UUID].put(data)

        time.sleep(0.1)  # Sleep for a short duration to avoid high CPU usage

if __name__ == "__main__":
    main()