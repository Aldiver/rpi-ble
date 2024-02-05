# import RPi.GPIO as GPIO

# class PulseSensor:
#     def __init__(self, gpio_pin):
#         self.gpio_pin = gpio_pin
#         self.pulse_count = 0
#         self.last_pulse_time = None
#         self.setup_gpio()

#     def setup_gpio(self):
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#         GPIO.add_event_detect(self.gpio_pin, GPIO.RISING, callback=self.pulse_detected)

#     def pulse_detected(self, channel):
#         pulse_time = time.time()
#         if self.last_pulse_time is not None:
#             time_since_last_pulse = pulse_time - self.last_pulse_time
#             if time_since_last_pulse > 0.1:
#                 self.pulse_count += 1
#         self.last_pulse_time = pulse_time

#     def get_pulse_count(self):
#         return self.pulse_count

#     def reset_pulse_count(self):
#         self.pulse_count = 0

#     def cleanup(self):
#         GPIO.remove_event_detect(self.gpio_pin)
#         GPIO.cleanup()