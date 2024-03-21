import Adafruit_ADS1x15
import time

# Create an ADS1115 ADC instance with address 0x49
adc = Adafruit_ADS1x15.ADS1115(address=0x49)

# Define the ADC channel where the GSR sensor is connected (e.g., A0)
GSR_CHANNEL = 0

def read_gsr():
    try:
        while True:
            # Read analog input from the GSR sensor connected to the specified channel
            gsr_value = adc.read_adc(GSR_CHANNEL, gain=1)
            
            # Process the GSR value (e.g., print or further analysis)
            print("GSR Value:", gsr_value)
            
            time.sleep(0.5)  # Adjust sampling interval as needed

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    read_gsr()
