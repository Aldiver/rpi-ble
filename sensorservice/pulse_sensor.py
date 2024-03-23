import multiprocessing
import Adafruit_ADS1x15
import time

class PulseSensor(multiprocessing.Process):
    def __init__(self):
        super().__init__()
        self.pulse = 0
        self.lastBeatTime = 0

    def run(self):
        CUSTOM_ADDRESS = 0x49  # Change this to your desired address
        adc = Adafruit_ADS1x15.ADS1115(address=CUSTOM_ADDRESS)

        firstBeat = True
        secondBeat = False
        sampleCounter = 0
        lastTime = int(time.time()*1000)
        th = 525

        while True:
            Signal = adc.read_adc(1, gain=2/3)
            sampleCounter += int(time.time()*1000) - lastTime
            lastTime = int(time.time()*1000)
            N = sampleCounter - self.lastBeatTime

            if Signal > th and Signal > self.pulse:
                self.pulse = Signal
            if Signal < th and N > 600:  # Adjust IBI duration as needed
                if Signal < th:
                    th = Signal
            if N > 250:
                if Signal > th and not secondBeat and N > 900:  # Adjust IBI threshold as needed
                    secondBeat = True
                    self.pulse = 60000 / (sampleCounter - self.lastBeatTime)
                if firstBeat:
                    firstBeat = False
                    self.lastBeatTime = sampleCounter
                    continue
            if Signal < th and secondBeat:
                th = 525
                firstBeat = True
                secondBeat = False
            time.sleep(0.005)

    def get_data(self):
        return self.pulse
