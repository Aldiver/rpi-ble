import random


class BodyTempSensor():
    def __init__(self):
        self._temperature = 0

    def get_data(self):
        return random.randint(35, 40)

    def set_temperature(self, temperature):
        self._temperature = temperature