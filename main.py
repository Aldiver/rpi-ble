import multiprocessing
import queue
import time

import dbus
import threading

from gattservice.ble_process import BLEProcess
from gattservice.core_ble.constants import GSR_SENSOR_UUID, PULSE_SENSOR_UUID, TEMP_HUMI_SENSOR_UUID, BODY_TEMP_SENSOR_UUID, ALERT_NOTIF_UUID
from sensorservice.sensor_process import SensorProcess

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

queue_manager = {}
sensor_process = SensorProcess()

def main():
    queue_manager[GSR_SENSOR_UUID] = multiprocessing.Queue()
    queue_manager[PULSE_SENSOR_UUID] = multiprocessing.Queue()
    queue_manager[TEMP_HUMI_SENSOR_UUID] = multiprocessing.Queue()  
    queue_manager[BODY_TEMP_SENSOR_UUID] = multiprocessing.Queue()
    queue_manager[ALERT_NOTIF_UUID] = multiprocessing.Queue()

    output_queue = multiprocessing.Queue()
    test = multiprocessing.Queue()
    ble_process = BLEProcess(queue_manager)
    ble_process.start()

    start_time = time.time()  # Record the start time
    while True:
        if time.time() - start_time >= 2:
            start_time = time.time()  # Reset the timer
            # Iterate over sensor UUIDs and add data to the queue if it's empty
            for sensor_uuid in [PULSE_SENSOR_UUID]:
                if queue_manager[sensor_uuid].empty():
                    print(f"Adding data to queue for sensor with UUID {sensor_uuid}")
                    data = sensor_process.get_sensor_data(sensor_uuid)
                    queue_manager[sensor_uuid].put(data)
        time.sleep(0.1)  # Sleep for a short duration to avoid high CPU usage

if __name__ == "__main__":
    main()