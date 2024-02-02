import multiprocessing
import queue
import time

import dbus
import threading

from gattservice.ble_process import BLEProcess
from gattservice.random_data import generate_random_readings
# from parser_node import Parser

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

def test_func(interval, process):
    threading.Timer(interval, test_func, [interval]).start()
    print("Interval Test hmm")

def main():
    output_queue = multiprocessing.Queue()

    ble_process = BLEProcess(output_queue)
    ble_process.start()
    
    while True:
        try:
            # value = output_queue.put(generate_random_readings(), timeout=1000)
            # Parser(output_queue)
            curr_value = output_queue.get(timeout=1)
            print(f"Value written to Characteristic with UUID {curr_value['uuid']}: {curr_value['value']}")
        except queue.Empty:
            time.sleep(1)

if __name__ == "__main__":
    main()