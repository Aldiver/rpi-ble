import Adafruit_ADS1x15

class GSRSensor:
    def __init__(self, address=0x49, channel=0):
        self.adc = Adafruit_ADS1x15.ADS1115(address=address)
        self.channel = channel

    def read_gsr(self):
        try:
            # Read analog input from the GSR sensor connected to the specified channel
            gsr_value = self.adc.read_adc(self.channel, gain=1, data_rate=8)  # Set data rate to 3300 SPS
            print("GSR VALUE: ", gsr_value)
            return gsr_value
        except Exception as e:
            print("Error reading GSR:", e)
            return 0

    def adjust_skin_resistance(self, gsr_value):
        # Adjust skin resistance based on the GSR value
        if gsr_value > 9000:
            return 1
        else:
            return 0

    def get_data(self):
        gsr_value = self.read_gsr()
        skin_resistance = self.adjust_skin_resistance(gsr_value)
        return skin_resistance
