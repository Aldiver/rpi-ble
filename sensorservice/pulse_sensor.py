import multiprocessing
from sensorservice.heartrate_monitor import HeartRateMonitor
import time

class PulseSensor(multiprocessing.Process):
    def __init__(self, pulse_queue):
        super().__init__()
        self.pulse_queue = pulse_queue
        self.hrm = HeartRateMonitor(print_raw=False, print_result=True)
    
    def run(self):
        self.hrm.start_sensor()
        try:
            while True:
                time.sleep(1)
                heart_rate = self.hrm.get_heart_rate()
                if heart_rate:
                    self.pulse_queue.put(heart_rate)
        except KeyboardInterrupt:
            pass
        finally:
            self.hrm.stop_sensor()
