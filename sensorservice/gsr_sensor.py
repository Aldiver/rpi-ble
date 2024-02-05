import random


class GsrSensor():
    def __init__(self):
        self.value = 0

    def get_data(self):
        self.value = random.randint(0, 1023)
        return self.value