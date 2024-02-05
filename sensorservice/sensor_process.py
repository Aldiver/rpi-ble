from gattservice.core_ble.constants import BODY_TEMP_SENSOR_UUID, GSR_SENSOR_UUID, PULSE_SENSOR_UUID, TEMP_HUMI_SENSOR_UUID
from sensorservice.temp_humi_sensor import TempHumiSensor
from sensorservice.gsr_sensor import GsrSensor
from sensorservice.pulse_sensor import PulseSensor
from sensorservice.body_temp_sensor import BodyTempSensor

class SensorProcess():
    def __init__(self):
        self.gsr_sensor = GsrSensor()
        self.pulse_sensor = PulseSensor()
        self.temp_humi_sensor = TempHumiSensor()
        self.body_temp_sensor = BodyTempSensor()

    def get_sensor_data(self, sensor_uuid):
        sensor_mapping = {
            GSR_SENSOR_UUID: self.gsr_sensor.get_data,
            PULSE_SENSOR_UUID: self.pulse_sensor.get_data,
            TEMP_HUMI_SENSOR_UUID: self.temp_humi_sensor.get_data,
            BODY_TEMP_SENSOR_UUID: self.body_temp_sensor.get_data
        }

        sensor_func = sensor_mapping.get(sensor_uuid)
        if sensor_func:
            return sensor_func()
        else:
            raise ValueError("Invalid sensor UUID")