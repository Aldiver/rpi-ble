import multiprocessing
import time
import RPi.GPIO as GPIO

class AlertProcess(multiprocessing.Process):
    def __init__(self, alert_queue):
        super().__init__()
        self.alert_queue = alert_queue
        self.speaker_pin = 18  # GPIO pin connected to the piezo buzzer

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.speaker_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.speaker_pin, 1000)  # Set PWM frequency to 1kHz
        self.pwm.start(0.5)  # Start PWM with 0% duty cycle (off)
        
    def run(self):
        while True:  # Continuously monitor the alert queue
            if not self.alert_queue.empty():
                alert = self.alert_queue.get()
                if alert == "1":
                    print("Alert received! Starting beep process...")
                    self.start_pulsating_beep(5)
                elif alert == "0":
                    print("Received stop signal for beeping.")
                    self.stop_beeping()
                else:
                    print(f"Unknown alert value received: {alert}")
            time.sleep(0.1)  # Adjust sleep time as needed

    def start_pulsating_beep(self, cycles: int):
        for _ in range(cycles):  # Number of cycles of beep and silence
            self.pwm.ChangeDutyCycle(50)  # Beep at 50% duty cycle
            time.sleep(1)  # Beep for 1 second
            self.pwm.ChangeDutyCycle(0)  # Silence (0% duty cycle)
            time.sleep(1)  # Silence for 1 second

    def stop_beeping(self):
        # Stop beeping by setting duty cycle to 0%
        self.pwm.ChangeDutyCycle(0)

    def cleanup(self):
        # Cleanup GPIO and stop PWM
        self.pwm.stop()
        GPIO.cleanup()

# Example usage
if __name__ == '__main__':
    alert_queue = multiprocessing.Queue()
    alert_process = AlertProcess(alert_queue)
    alert_process.start()

    # Example to trigger alert
    alert_queue.put("1")
    time.sleep(10)
    alert_queue.put("0")

    alert_process.cleanup()
