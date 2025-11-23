# Test 2: Buzzer
# Tests if buzzer can make sounds

from machine import Pin
import time
from config import BUZZER_PIN

print("=" * 40)
print("TEST 2: BUZZER")
print("=" * 40)
print(f"Pin: GPIO {BUZZER_PIN}")
print("Starting test...\n")

# Create buzzer pin as OUTPUT
buzzer = Pin(BUZZER_PIN, Pin.OUT)

# Make 3 short beeps
for i in range(3):
    print(f"  Beep {i+1}/3")
    buzzer.on()  # Turn buzzer on
    time.sleep(0.2)  # Short beep
    buzzer.off()  # Turn buzzer off
    time.sleep(0.5)  # Pause between beeps

print("\n✓ Test complete!")
print("Did you hear 3 short beeps?")
print("=" * 40)
