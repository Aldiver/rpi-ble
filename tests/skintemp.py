import smbus
import time

# Define I2C bus
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

# I2C address of CJMCU30205 sensor
address = 0x49  # Change this address if needed

# Function to read temperature from sensor
def read_temperature():
    # Read temperature data from sensor (2 bytes)
    data = bus.read_i2c_block_data(address, 0x00, 2)
    
    # Convert temperature data to Celsius
    temperature = ((data[0] << 8) + data[1]) / 256.0
    
    return temperature

try:
    while True:
        # Read temperature
        temp_celsius = read_temperature()
        print("Temperature: {:.2f} °C".format(temp_celsius))
        
        # Wait for some time before taking the next measurement
        time.sleep(1)

except KeyboardInterrupt:
    pass
