import smbus
import time

class TempHumiSensor:
    def __init__(self, address=0x38):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.init_sensor()

    def init_sensor(self):
        init_cmd = [0xE1, 0x08, 0x00]
        self.bus.write_i2c_block_data(self.address, 0x00, init_cmd)
        time.sleep(0.1)

    def read_data(self):
        measure_cmd = [0xAC, 0x33, 0x00]
        self.bus.write_i2c_block_data(self.address, 0x00, measure_cmd)
        time.sleep(0.1)
        data = self.bus.read_i2c_block_data(self.address, 0x00, 6)
        if (data[0] & 0x80) == 0:
            humidity = ((data[1] << 12) + (data[2] << 4) + (data[3] >> 4)) * 100 / (2**20 - 1)
            temperature = (((data[3] & 0x0F) << 16) + (data[4] << 8) + data[5]) * 200 / (2**20 - 1) - 50
            return temperature, humidity
        else:
            return None, None
        
    def get_humidity_data(self):
        temperature, humidity = self.read_data()
        return round(humidity)

    def get_temperature_data(self):
        temperature, humidity = self.read_data()
        return temperature

