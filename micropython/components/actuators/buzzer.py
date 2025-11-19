from machine import Pin
import time
import config


class Buzzer:
    """Buzzer control"""
    def __init__(self):
        self.pin = Pin(config.BUZZER_PIN, Pin.OUT)
        self.state = False

    def on(self):
        self.pin.on()
        self.state = True

    def off(self):
        self.pin.off()
        self.state = False

    def beep(self, duration=0.5):
        self.on()
        time.sleep(duration)
        self.off()

    def alarm(self, times=3):
        """Sound alarm - multiple quick beeps"""
        for _ in range(times):
            self.on()
            time.sleep(0.2)
            self.off()
            time.sleep(0.2)
