import multiprocessing
from heartrate_monitor import HeartRateMonitor
import time

class PulseSensor(multiprocessing.Process):
    def __init__(self, pulse_queue, window_size=5):
        super().__init__()
        self.pulse_queue = pulse_queue
        self.hrm = HeartRateMonitor(print_raw=False, print_result=True)
        self.window_size = window_size
        self.heart_rate_window = []

    def run(self):
        self.hrm.start_sensor()
        try:
            while True:
                time.sleep(1)
                heart_rate = self.hrm.get_heart_rate()
                if heart_rate:
                    self.add_to_window(heart_rate)
                    filtered_heart_rate = self.calculate_average()
                    self.pulse_queue.put(filtered_heart_rate)
        except KeyboardInterrupt:
            pass
        finally:
            self.hrm.stop_sensor()

    def add_to_window(self, heart_rate):
        if len(self.heart_rate_window) >= self.window_size:
            self.heart_rate_window.pop(0)
        self.heart_rate_window.append(heart_rate)

    def calculate_average(self):
        if len(self.heart_rate_window) == 0:
            return 0
        return sum(self.heart_rate_window) / len(self.heart_rate_window)