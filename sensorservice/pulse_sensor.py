import multiprocessing
import Adafruit_ADS1x15
import time

class PulseSensor(multiprocessing.Process):
    def __init__(self, output_queue: multiprocessing.Queue):
        super().__init__()
        self.pulse = 0
        self.output_queue = output_queue
        self.filter_window = 5  # Adjust this value to change the window size of the moving average filter
        self.signal_buffer = deque(maxlen=self.filter_window)  # Using deque to efficiently maintain the moving window

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
            self.signal_buffer.append(Signal)  # Add the current signal reading to the buffer
            filtered_signal = sum(self.signal_buffer) / len(self.signal_buffer)  # Calculate the moving average

            sampleCounter += int(time.time()*1000) - lastTime
            lastTime = int(time.time()*1000)
            N = sampleCounter - lastBeatTime

            if filtered_signal > th and filtered_signal > P:
                P = filtered_signal
            if filtered_signal < th and N > (IBI/5.0)*3.0:
                if filtered_signal < T:
                    T = filtered_signal
            if N > 250:
                if filtered_signal > th and Pulse == False and N > (IBI/5.0)*3.0:
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
                    if self.output_queue.empty():
                        print("ADDING PULSE DATA TO QUEUE")
                        self.output_queue.put(round(BPM))

            if filtered_signal < th and Pulse:
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
            time.sleep(0.005)

    def get_data(self):
        return self.pulse
