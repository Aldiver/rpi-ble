import multiprocessing
import Adafruit_ADS1x15
import time

class PulseSensor(multiprocessing.Process):
    def __init__(self, output_queue: multiprocessing.Queue):
        super().__init__()
        self.pulse = 0
        self.output_queue = output_queue

    def run(self):
        CUSTOM_ADDRESS = 0x49  # Change this to your desired address
        adc = Adafruit_ADS1x15.ADS1115(address=CUSTOM_ADDRESS)
        rate = [0]*10
        amp = 100
        GAIN = 2/3  
        curState = 0
        stateChanged = 0

        firstBeat = True
        secondBeat = False
        sampleCounter = 0
        lastBeatTime = 0
        lastTime = int(time.time()*1000)
        th = 525
        P = 512
        T = 512
        IBI = 600
        Pulse = False  
        while True:
            Signal = adc.read_adc(1, gain=GAIN)   
            sampleCounter += int(time.time()*1000) - lastTime
            lastTime = int(time.time()*1000)
            N = sampleCounter - lastBeatTime

            if Signal > th and Signal > P:
                P = Signal
            if Signal < th and N > (IBI/5.0)*3.0:
                if Signal < T:
                    T = Signal
            if N > 250:
                if Signal > th and Pulse == False and N > (IBI/5.0)*3.0:
                    Pulse = True
                    IBI = sampleCounter - lastBeatTime
                    lastBeatTime = sampleCounter
                    if secondBeat:
                        secondBeat = False
                        for i in range(0, 10):
                            rate[i] = IBI
                    if firstBeat:
                        firstBeat = False
                        secondBeat = True
                        continue
                    runningTotal = 0
                    for i in range(0, 9):
                        rate[i] = rate[i+1]
                        runningTotal += rate[i]
                    rate[9] = IBI
                    runningTotal += rate[9]
                    runningTotal /= 10
                    BPM = 60000/runningTotal
                    print("BPM:", BPM)
                    # print("IBI:", IBI)
                    if self.output_queue.empty():
                        print(" ADDING PULSE DATA TO QUEUE")
                        self.output_queue.put(round(BPM))

            if Signal < th and Pulse:
                amp = P - T
                th = amp/2 + T
                T = th
                P = th
                Pulse = False
            if N > 2500:
                th = 512
                T = th
                P = th
                lastBeatTime = sampleCounter
                firstBeat = False
                secondBeat = False
                print("No beats found")
                # self.pulse = 0
            time.sleep(0.005)

    def get_data(self):
        return self.pulse
