import multiprocessing
import queue
from sensorservice.temp_humi_sensor import TempHumiSensor
from sensorservice.gsr_sensor import GSRSensor
from sensorservice.pulse_sensor import PulseSensor
from sensorservice.body_temp_sensor import BodyTempSensor
import random
import dbus


class SensorProcess():
    def __init__(self, pulse_queue ):
        self.gsr_sensor = GSRSensor()
        
        self.temp_humi_sensor = TempHumiSensor()
        self.body_temp_sensor = BodyTempSensor()
        self.byte_array = dbus.Array([], signature=dbus.Signature("y"))
        # Start the PulseSensor process
        self.pulse_queue = pulse_queue
        self.pulse_sensor = PulseSensor(self.pulse_queue)
        self.pulse_sensor.start()

    def get_sensor_data(self):
        self.byte_array = dbus.Array([], signature=dbus.Signature("y")) #reset byte array

        # Get sensor data
        heartRate = 0
        heartRate = self.pulse_queue.get()
        print("Check Heart Rate:", heartRate)

        self.append_to_dbus_array(min(heartRate, 208))

        skinRes = self.gsr_sensor.get_data()
        self.append_to_dbus_array(skinRes)

        skinTempData = self.body_temp_sensor.read_temperature()
        self.parse_decimal(skinTempData)

        ambientHumidity = self.temp_humi_sensor.get_humidity_data()
        self.append_to_dbus_array(ambientHumidity)

        ambientTempData = self.temp_humi_sensor.get_temperature_data()
        self.parse_decimal(ambientTempData)

        return self.byte_array
        
    def get_sensor_data_test(self):
        byte1 = random.randint(1, 100) #value for heart rate
        byte2 = random.randint(0, 1) #skin res 0 or 1
        byte3 = random.randint(0, 1) #skin temp multiplier (pos or negative)
        byte4 = random.randint(1, 100) #skin temp value Whole number
        byte5 = random.randint(1, 100) #skin temp value decimal 
        byte6 = random.randint(0, 100) #ambient humidity
        byte7 = random.randint(0, 1) #ambient temp multiplier (pos or negative)
        byte8 = random.randint(1, 100) #ambient temp value Whole number
        byte9 = random.randint(1, 100) #ambient temp value decimal

        byte1_bytes = byte1.to_bytes(1, byteorder='big')
        byte2_bytes = byte2.to_bytes(1, byteorder='big')
        byte3_bytes = byte3.to_bytes(1, byteorder='big')
        byte4_bytes = byte4.to_bytes(1, byteorder='big')
        byte5_bytes = byte5.to_bytes(1, byteorder='big')
        byte6_bytes = byte6.to_bytes(1, byteorder='big')
        byte7_bytes = byte7.to_bytes(1, byteorder='big')
        byte8_bytes = byte8.to_bytes(1, byteorder='big')
        byte9_bytes = byte9.to_bytes(1, byteorder='big')

        byte_array = dbus.Array([], signature=dbus.Signature("y"))
        byte_array.append(dbus.Byte(byte1_bytes))
        byte_array.append(dbus.Byte(byte2_bytes))
        byte_array.append(dbus.Byte(byte3_bytes))
        byte_array.append(dbus.Byte(byte4_bytes))
        byte_array.append(dbus.Byte(byte5_bytes))
        byte_array.append(dbus.Byte(byte6_bytes))
        byte_array.append(dbus.Byte(byte7_bytes))
        byte_array.append(dbus.Byte(byte8_bytes))
        byte_array.append(dbus.Byte(byte9_bytes))

        print("\nByte array:")
        print(byte_array)

        return byte_array
    
    def parse_decimal(self, value):
        sign = 0 if value >= 0 else 1
        value = abs(value)
        whole_number = int(value)
        decimal = int((value - whole_number) * 100)  # Convert decimal to two decimal places

        self.append_to_dbus_array(sign)
        self.append_to_dbus_array(whole_number)
        self.append_to_dbus_array(decimal)
    
    def append_to_dbus_array(self, value):
        self.byte_array.append(dbus.Byte(value.to_bytes(1, byteorder='big')))


# -37.5 === (-), (37), (5)