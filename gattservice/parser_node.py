import queue

from gattservice.core_ble.service import Service

def Parser(data: queue.Queue):
    curr_value = data.get(timeout=1)
    while True:
        try:
            curr_value = data.get(False)
        except queue.Empty:
            return False

