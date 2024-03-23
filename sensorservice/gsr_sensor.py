import Adafruit_ADS1x15
import time

class GSRSensor:
    def __init__(self, address=0x49, channel=0):
        self.adc = Adafruit_ADS1x15.ADS1115(address=address)
        self.channel = channel

    def read_gsr(self):
        try:
            # Read analog input from the GSR sensor connected to the specified channel
            gsr_value = self.adc.read_adc(self.channel, gain=1, data_rate=8)  # Set data rate to 3300 SPS
            return gsr_value
        except Exception as e:
            print("Error reading GSR:", e)
            return 0

    def get_data(self):
        return self.read_gsr()
