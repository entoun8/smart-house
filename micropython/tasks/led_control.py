import time
from components import LED

MELBOURNE_OFFSET = 11 * 3600
CHECK_INTERVAL = 60  

class LEDControlTask:
    def __init__(self):
        self.led = LED()
        self.previous_state = None
        self.last_check = 0

    def _get_hour(self):
        melbourne = time.time() + MELBOURNE_OFFSET
        return time.localtime(int(melbourne))[3]

    def _should_be_on(self):
        hour = self._get_hour()
        return hour >= 20 or hour < 7

    def update(self):
        now = time.time()
        if self.last_check != 0 and now - self.last_check < CHECK_INTERVAL:
            return
        self.last_check = now

        if self._should_be_on():
            self.led.on()
            state = "ON"
        else:
            self.led.off()
            state = "OFF"

        if state != self.previous_state:
            self.previous_state = state

    def cleanup(self):
        self.led.off()
