import multiprocessing
import time
import RPi.GPIO as GPIO

class AlertProcess(multiprocessing.Process):
    def __init__(self, alert_queue):
        super().__init__()
        self.alert_queue = alert_queue
        self.speaker_pin = 17  # GPIO pin connected to the speaker

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.speaker_pin, GPIO.OUT)
        GPIO.output(self.speaker_pin, GPIO.LOW)

    def run(self):
        while True:  # Continuously monitor the alert queue
            if not self.alert_queue.empty():
                alert = self.alert_queue.get()
                if alert == 1:
                    print("Alert received! Starting beep process...")
                    self.start_beeping()
                elif alert == 0:
                    print("Received stop signal for beeping.")
                    self.stop_beeping()
                else:
                    print(f"Unknown alert value received: {alert}")
            time.sleep(0.1)  # Adjust sleep time as needed

    def start_beeping(self):
        # Start beeping by toggling the GPIO pin
        GPIO.output(self.speaker_pin, GPIO.HIGH)
        time.sleep(5)  # Beep for 5 seconds

    def stop_beeping(self):
        # Stop beeping by turning off the GPIO pin
        GPIO.output(self.speaker_pin, GPIO.LOW)

    def cleanup(self):
        # Cleanup GPIO
        GPIO.cleanup()
