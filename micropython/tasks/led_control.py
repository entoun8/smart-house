import time
import ntptime
from components import LED, WiFi

MELBOURNE_OFFSET = 11 * 3600

led = LED()
wifi = WiFi()

def sync_time():
    """Sync time with NTP server"""
    try:
        ntptime.settime()
        print("✅ Time synced!")
        return True
    except Exception as e:
        print(f"⚠️  Time sync failed: {e}")
        return False

def get_melbourne_hour():
    """Get current hour in Melbourne (0-23)"""
    utc = time.time()
    melbourne = utc + MELBOURNE_OFFSET
    t = time.localtime(int(melbourne))
    return t[3]

def get_time_str():
    """Get Melbourne time as string (HH:MM)"""
    utc = time.time()
    melbourne = utc + MELBOURNE_OFFSET
    t = time.localtime(int(melbourne))
    return f"{t[3]:02d}:{t[4]:02d}"

def should_led_be_on():
    """
    LED ON: 8pm (20:00) to 7am (07:00)
    LED OFF: 7am (07:00) to 8pm (20:00)
    """
    hour = get_melbourne_hour()
    return hour >= 20 or hour < 7

def update_led():
    """Update LED state based on current time"""
    if should_led_be_on():
        led.on()
        return "ON"
    else:
        led.off()
        return "OFF"

print("=" * 50)
print("TASK 1: LED AUTO CONTROL (8pm - 7am)")
print("=" * 50)

print("\n🌐 Connecting to WiFi...")
wifi.connect()

print("⏰ Syncing time...")
sync_time()

print(f"\n📊 Current time: {get_time_str()}")
print("📅 LED Schedule:")
print("   ON:  8pm (20:00) to 7am (07:00)")
print("   OFF: 7am (07:00) to 8pm (20:00)")
print("=" * 50)

state = update_led()
print(f"\n[{get_time_str()}] LED is {state}")

print("\n✅ LED auto-control running...")
print("=" * 50)

previous_state = state

while True:
    try:
        current_state = update_led()

        if current_state != previous_state:
            print(f"\n[{get_time_str()}] LED switched to {current_state}")
            previous_state = current_state

        time.sleep(60)

    except KeyboardInterrupt:
        print("\n\n🛑 Stopping LED auto-control...")
        led.off()
        break
    except Exception as e:
        print(f"\n❌ Error: {e}")
        time.sleep(60)
