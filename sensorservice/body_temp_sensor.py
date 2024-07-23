import smbus

class BodyTempSensor:
    def __init__(self, address=0x4e):
        self.address = address
        self.bus = smbus.SMBus(1)  # Use I2C bus 1

    def read_temperature(self):
        try:
            # Read temperature data from sensor (2 bytes)
            data = self.bus.read_i2c_block_data(self.address, 0x00, 2)
            
            # Convert temperature data to Celsius
            temperature = ((data[0] << 8) + data[1]) / 256.0
            
            print("Body temperature ", temperature)
            return temperature
        except Exception as e:
            print("Error reading temperature:", e)
            return 0  # Return 0 if there's an error