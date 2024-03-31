import multiprocessing
import queue
import time

import dbus
import threading

from gattservice.ble_process import BLEProcess
from gattservice.core_ble.constants import CHARACTERISTIC_SENSOR_UUID, ALERT_NOTIF_UUID
from sensorservice.alert_process import AlertProcess
from sensorservice.sensor_process import SensorProcess

queue_manager = {}
queue_manager[CHARACTERISTIC_SENSOR_UUID] = multiprocessing.Queue()
queue_manager[ALERT_NOTIF_UUID] = multiprocessing.Queue()
queue_manager["pulse"] = multiprocessing.Queue()

def main():
    sensor_process = SensorProcess(queue_manager["pulse"])
    ble_process = BLEProcess(queue_manager)
    ble_process.start()
    
    # uncomment if running in raspberry pi
    alert_process = AlertProcess(queue_manager[ALERT_NOTIF_UUID])
    alert_process.start()

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
            
            if not queue_manager[ALERT_NOTIF_UUID].empty():
                curr_value = queue_manager[ALERT_NOTIF_UUID].get(timeout=1)
                print(f"Value written to Characteristic: {curr_value}")

        time.sleep(0.1)  # Sleep for a short duration to avoid high CPU usage

if __name__ == "__main__":
    main()