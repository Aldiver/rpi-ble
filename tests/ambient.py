import smbus
import time

# Define I2C bus
bus = smbus.SMBus(1)  # Raspberry Pi 3 uses I2C bus 1

# AHT10 I2C address
AHT10_ADDR = 0x38

# Commands
INIT_CMD = [0xE1, 0x08, 0x00]
MEASURE_CMD = [0xAC, 0x33, 0x00]

def init_aht10():
    # Initialize AHT10 sensor
    bus.write_i2c_block_data(AHT10_ADDR, 0x00, INIT_CMD)
    time.sleep(0.1)

def read_aht10_data():
    # Send measure command
    bus.write_i2c_block_data(AHT10_ADDR, 0x00, MEASURE_CMD)
    time.sleep(0.1)

    # Read data from sensor (6 bytes: status + humidity_high + humidity_low + temperature_high + temperature_low + checksum)
    data = bus.read_i2c_block_data(AHT10_ADDR, 0x00, 6)

    # Check if data is valid
    if (data[0] & 0x80) == 0:
        humidity = ((data[1] << 12) + (data[2] << 4) + (data[3] >> 4)) * 100 / (2**20 - 1)
        temperature = (((data[3] & 0x0F) << 16) + (data[4] << 8) + data[5]) * 200 / (2**20 - 1) - 50
        return temperature, humidity
    else:
        return None, None

def main():
    init_aht10()
    while True:
        temperature, humidity = read_aht10_data()
        if temperature is not None and humidity is not None:
            print("Temperature: {:.2f} °C, Humidity: {:.2f} %".format(temperature, humidity))
        else:
            print("Failed to read data from AHT10 sensor")
        time.sleep(1)

if __name__ == "__main__":
    main()
