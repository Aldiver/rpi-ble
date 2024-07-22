import Adafruit_ADS1x15
from sensorservice.filter_util import MovingAverageFilter

class GSRSensor:
    def __init__(self, address=0x4a, channel=0, filter_window_size=5):
        self.adc = Adafruit_ADS1x15.ADS1115(address=address)
        self.channel = channel
        self.filter = MovingAverageFilter(window_size=filter_window_size)

    def read_gsr(self):
        try:
            # Read analog input from the GSR sensor connected to the specified channel
            gsr_value = self.adc.read_adc(self.channel, gain=1, data_rate=8)  # Set data rate to 3300 SPS
            return gsr_value
        except Exception as e:
            print("Error reading GSR:", e)
            return 0

    def adjust_skin_resistance(self, gsr_value):
        # Adjust skin resistance based on the GSR value
        if gsr_value > 21000:
            return 1
        else:
            return 0

    def get_data(self):
        gsr_value = self.read_gsr()
        filtered_gsr = self.filter.add_data(gsr_value)
        averaged_gsr = self.filter.get_average()
        skin_resistance = self.adjust_skin_resistance(filtered_gsr)
        return skin_resistance
