import random

class PulseSensor():
    def __init__(self):
        self.pulse = 0

    def get_data(self):
        return random.randint(0, 100)