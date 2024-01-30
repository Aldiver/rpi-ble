import multiprocessing
import queue
import time

import dbus

from gattservice.ble_process import BLEProcess
from gattservice.random_data import generate_random_readings

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)


def main():
    output_queue = multiprocessing.Queue()

    ble_process = BLEProcess(output_queue)
    ble_process.start()
    
    while True:
        try:
            # value = output_queue.put(generate_random_readings(), timeout=1000)
            curr_value = output_queue.get(timeout=1)
            print(f"Value written to Characteristic with UUID {curr_value['uuid']}: {curr_value['value']}")
        except queue.Empty:
            time.sleep(1)


if __name__ == "__main__":
    main()
