import random


class TempHumiSensor():
    def __init__(self):
        self.pin = None

    def get_data(self):
        # read from sensor
        return random.randint(0, 100)