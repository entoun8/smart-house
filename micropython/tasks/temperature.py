import time
import ntptime
from components import DHT, WiFi, MQTT
from utils.database import Database
from config import TOPICS

MELBOURNE_OFFSET = 11 * 3600

dht = DHT()
wifi = WiFi()
mqtt = MQTT()
db = Database()

LOG_INTERVAL = 1800  # 30 minutes

last_log_time = 0

def sync_time():
    """Sync time with NTP server"""
    try:
        ntptime.settime()
        print("Time synced!")
        return True
    except Exception as e:
        print(f"Time sync failed: {e}")
        return False

def get_time_str():
    """Get Melbourne time as string (HH:MM)"""
    utc = time.time()
    melbourne = utc + MELBOURNE_OFFSET
    t = time.localtime(int(melbourne))
    return f"{t[3]:02d}:{t[4]:02d}"

def read_and_log():
    """Read DHT sensor and log to MQTT + Database"""
    global last_log_time

    print(f"\n[{get_time_str()}] Reading DHT sensor...")

    data = dht.read()

    if data:
        temp = data['temp']
        humidity = data['humidity']

        print(f"  Temperature: {temp}°C")
        print(f"  Humidity: {humidity}%")

        mqtt.publish(TOPICS.sensor("temperature"), str(temp))
        mqtt.publish(TOPICS.sensor("humidity"), str(humidity))

        db.log_temperature(temp, humidity)

        last_log_time = time.time()

        return True
    else:
        print("  Failed to read sensor")
        return False

def should_log_now():
    """Check if it's time to log (every 30 minutes)"""
    if last_log_time == 0:
        return True  

    elapsed = time.time() - last_log_time
    return elapsed >= LOG_INTERVAL

print("=" * 50)
print("TEMPERATURE & HUMIDITY LOGGING - TASK 2")
print("=" * 50)

print("\nConnecting to WiFi...")
wifi.connect()

print("Connecting to MQTT...")
mqtt.connect()

print("Syncing time...")
sync_time()

print(f"\nCurrent time: {get_time_str()}")
print(f"Logging interval: {LOG_INTERVAL // 60} minutes")
print("=" * 50)

print("\nStarting initial reading...")
read_and_log()

print("\nSetup complete! Logging every 30 minutes...")
print("=" * 50)

while True:
    try:
        if should_log_now():
            read_and_log()

        mqtt.check_messages()

        time.sleep(60)

    except KeyboardInterrupt:
        print("\n\nStopping temperature logger...")
        mqtt.disconnect()
        break
    except Exception as e:
        print(f"\nError: {e}")
        time.sleep(60) 
