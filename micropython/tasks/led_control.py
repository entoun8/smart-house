"""Task 1: LED Auto-Control (8pm-7am)"""

import time
from components import LED

MELBOURNE_OFFSET = 11 * 3600
CHECK_INTERVAL = 60  # Check every minute


class LEDControlTask:
    def __init__(self):
        self.led = LED()
        self.previous_state = None
        self.last_check = 0

    def _get_hour(self):
        """Get current hour in Melbourne (0-23)"""
        melbourne = time.time() + MELBOURNE_OFFSET
        return time.localtime(int(melbourne))[3]

    def _should_be_on(self):
        """LED ON: 8pm (20:00) to 7am (07:00)"""
        hour = self._get_hour()
        return hour >= 20 or hour < 7

    def update(self):
        """Check and update LED state - call this in main loop"""
        # Only check every CHECK_INTERVAL seconds
        now = time.time()
        if self.last_check != 0 and now - self.last_check < CHECK_INTERVAL:
            return
        self.last_check = now

        # Update LED
        if self._should_be_on():
            self.led.on()
            state = "ON"
        else:
            self.led.off()
            state = "OFF"

        # Log state changes
        if state != self.previous_state:
            print(f"[LED] {state}")
            self.previous_state = state

    def cleanup(self):
        """Clean up - call on shutdown"""
        self.led.off()
