"""
All Tasks Combined - BRIDGELESS VERSION
ESP32 -> MQTT -> Web App (web app logs to database)
- Task 1: LED auto-control (8pm-7am)
- Task 2: Temperature -> MQTT
- Task 3: Motion -> MQTT
- Task 4: Steam -> local only
- Task 5: Gas -> MQTT
- Task 6: Asthma -> MQTT
- Task 7: RFID -> MQTT
"""

import time
import ntptime
from components import LED, DHT, PIR, WaterSensor, WindowServo, RGBStrip, GasSensor, Fan, LCD, WiFi, MQTT, RFID, Buzzer, DoorServo
from config import TOPICS

# Melbourne timezone offset
MELBOURNE_OFFSET = 11 * 3600

# Initialize components
led = LED()
dht = DHT()
pir = PIR()
water = WaterSensor()
window = WindowServo()
gas = GasSensor()
fan = Fan()
rgb = RGBStrip()
rfid = RFID()
buzzer = Buzzer()
door = DoorServo()
wifi = WiFi()
mqtt = MQTT()

# Initialize LCD last with delay
time.sleep(0.5)
lcd = LCD()

# Connection status
mqtt_connected = False

# Task 1: LED auto-control
previous_led_state = None
last_led_check = 0
LED_CHECK_INTERVAL = 60  # Check every minute

# Task 2: Temperature logging
LOG_INTERVAL = 1800  # 30 minutes
last_log_time = 0

# Task 3: Motion detection
previous_motion = False

# Task 4: Steam detection
previous_steam = False

# Task 5: Gas detection
previous_gas = False

# Task 6: Asthma alert
previous_asthma = False

# Task 7: RFID access control
last_card_id = None
last_scan_time = 0
SCAN_COOLDOWN = 3  # Seconds between same card scans

# ============================================
# HELPER FUNCTIONS
# ============================================

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

def sync_time():
    """Sync time with NTP server"""
    for attempt in range(5):
        try:
            print(f"NTP sync attempt {attempt + 1}/5...")
            ntptime.settime()
            print("Time synced!")
            return True
        except Exception as e:
            print(f"  Failed: {e}")
            if attempt < 4:
                time.sleep(2)
    print("NTP sync failed - LED timing may be off")
    return False

def connect_mqtt():
    """Connect to MQTT broker"""
    global mqtt_connected
    try:
        if mqtt.connect():
            mqtt_connected = True
            print("[MQTT] Connected to HiveMQ!")
            return True
    except Exception as e:
        print(f"[MQTT] Connection failed: {e}")
    mqtt_connected = False
    return False

def publish_mqtt(topic, message):
    """Safely publish to MQTT"""
    global mqtt_connected
    if mqtt_connected:
        try:
            mqtt.publish(topic, message)
            print(f"  [MQTT] -> {topic}")
            return True
        except Exception as e:
            print(f"  [MQTT] Fail: {e}")
            mqtt_connected = False
    else:
        print("  [MQTT] Not connected")
    return False

# ============================================
# TASK 1: LED AUTO-CONTROL
# ============================================

def should_led_be_on():
    """LED ON: 8pm (20:00) to 7am (07:00)"""
    hour = get_melbourne_hour()
    return hour >= 20 or hour < 7

def update_led():
    """Update LED state based on current time"""
    global previous_led_state

    if should_led_be_on():
        led.on()
        state = "ON"
    else:
        led.off()
        state = "OFF"

    if state != previous_led_state:
        print(f"[{get_time_str()}] LED: {state}")
        previous_led_state = state
    return state

def should_check_led():
    """Check if it's time to update LED"""
    global last_led_check
    if last_led_check == 0:
        last_led_check = time.time()
        return True
    elapsed = time.time() - last_led_check
    if elapsed >= LED_CHECK_INTERVAL:
        last_led_check = time.time()
        return True
    return False

# ============================================
# TASK 2: TEMPERATURE LOGGING
# ============================================

def log_temperature():
    """Read and log temperature/humidity via MQTT (DB handled by web app)"""
    global last_log_time

    data = dht.read()
    if data:
        temp = data['temp']
        humidity = data['humidity']

        print(f"[{get_time_str()}] Temp: {temp}C, Humidity: {humidity}%")

        # Publish to MQTT (web app will log to DB)
        publish_mqtt(TOPICS.sensor("temperature"), str(temp))
        publish_mqtt(TOPICS.sensor("humidity"), str(humidity))

        # Update LCD
        if lcd.is_connected():
            lcd.display_alert(f"Temp: {temp}C", f"Humidity: {humidity}%")

        last_log_time = time.time()
        return data
    else:
        print("  DHT read failed")
        return None

def should_log_temperature():
    """Check if it's time to log temperature"""
    if last_log_time == 0:
        return True
    return time.time() - last_log_time >= LOG_INTERVAL

# ============================================
# TASK 3: MOTION DETECTION
# ============================================

def handle_motion_detected():
    """Handle motion detection via MQTT (DB handled by web app)"""
    print("Motion detected!")

    # Light up RGB orange
    rgb.orange()

    # Publish to MQTT (web app will log to DB)
    publish_mqtt(TOPICS.event("motion_detected"), "1")

def handle_motion_stopped():
    """Handle when motion stops"""
    rgb.off()

# ============================================
# TASK 4: STEAM DETECTION (LOCAL ONLY)
# ============================================

def handle_steam_detected():
    """Handle steam detection - local only, no cloud"""
    print("Steam detected! Closing window...")
    window.close()
    rgb.blue()

def handle_steam_stopped():
    """Handle when steam stops"""
    rgb.off()

# ============================================
# TASK 5: GAS DETECTION
# ============================================

def handle_gas_detected():
    """Handle gas detection via MQTT (DB handled by web app)"""
    print("GAS DETECTED!")

    # Turn on fan
    fan.on()

    # Solid RGB red
    rgb.red()

    # Publish to MQTT (web app will log to DB)
    publish_mqtt(TOPICS.event("gas_detected"), "1")

def handle_gas_cleared():
    """Handle when gas clears"""
    print("Gas cleared")
    fan.off()
    rgb.off()
    publish_mqtt(TOPICS.event("gas_detected"), "0")

# ============================================
# TASK 6: ASTHMA ALERT
# ============================================

def check_asthma_conditions(temp, humidity):
    """Check if asthma alert conditions are met"""
    return humidity > 50 and temp > 27

def handle_asthma_alert():
    """Handle asthma alert - LCD + MQTT"""
    print("ASTHMA ALERT! (H>50% & T>27C)")

    if lcd.is_connected():
        lcd.display_alert("! ASTHMA ALERT !", "H>50% T>27C")

    publish_mqtt(TOPICS.event("asthma_alert"), "1")

def handle_asthma_cleared(temp, humidity):
    """Handle when alert clears"""
    print("Asthma alert cleared")

    if lcd.is_connected():
        lcd.display_alert(f"Temp: {temp}C", f"Humidity: {humidity}%")

    publish_mqtt(TOPICS.event("asthma_alert"), "0")

# ============================================
# TASK 7: RFID ACCESS CONTROL
# ============================================

def handle_rfid_scan(card_id):
    """Handle RFID scan via MQTT (auth checked by web app callback)"""
    print(f"RFID scanned: {card_id}")

    # Publish to MQTT - web app will check auth and respond
    publish_mqtt(TOPICS.event("rfid_scan"), f'{{"card":"{card_id}","action":"check"}}')

    # For now, flash green as acknowledgment (web app controls actual auth)
    rgb.green()
    time.sleep(1)
    rgb.off()

def handle_authorized_access(card_id):
    """Handle authorized RFID - open door"""
    door.open()
    rgb.green()
    time.sleep(2)
    rgb.off()
    time.sleep(3)
    door.close()

def handle_unauthorized_access(card_id):
    """Handle unauthorized RFID - flash red + buzz"""
    for _ in range(3):
        rgb.red()
        buzzer.on()
        time.sleep(0.3)
        rgb.off()
        buzzer.off()
        time.sleep(0.3)

# ============================================
# MAIN PROGRAM
# ============================================

print("=" * 50)
print("SMART HOUSE - BRIDGELESS MODE")
print("Direct ESP32 to Cloud")
print("=" * 50)

# Connect WiFi
print("\nConnecting to WiFi...")
if wifi.connect():
    print("WiFi connected!")
else:
    print("WiFi failed - continuing offline")

# Sync time
print("\nSyncing time...")
sync_time()

# Connect MQTT
print("\nConnecting to MQTT...")
connect_mqtt()

print(f"\nTask 1: LED auto (8pm-7am)")
print(f"Task 2: Temperature (every 30 min) -> DB + MQTT")
print("Task 3: Motion -> DB + MQTT")
print("Task 4: Steam -> local only")
print("Task 5: Gas -> DB + MQTT")
print("Task 6: Asthma -> LCD + MQTT")
print("Task 7: RFID -> DB + MQTT")
print("=" * 50)

# Initial setup
print(f"\nTime: {get_time_str()}")
update_led()
log_temperature()
door.close()

print("\nRunning...")
print("=" * 50)

# Main loop
while True:
    try:
        # Task 1: LED
        if should_check_led():
            update_led()

        # Task 2 & 6: Temperature + Asthma check
        if should_log_temperature():
            data = log_temperature()
            if data:
                temp = data['temp']
                humidity = data['humidity']

                asthma_alert = check_asthma_conditions(temp, humidity)

                if asthma_alert and not previous_asthma:
                    handle_asthma_alert()
                elif not asthma_alert and previous_asthma:
                    handle_asthma_cleared(temp, humidity)

                previous_asthma = asthma_alert

        # Task 3: Motion
        motion = pir.motion_detected()
        if motion and not previous_motion:
            handle_motion_detected()
        elif not motion and previous_motion:
            handle_motion_stopped()
        previous_motion = motion

        # Task 4: Steam
        steam = water.is_wet()
        if steam and not previous_steam:
            handle_steam_detected()
        elif not steam and previous_steam:
            handle_steam_stopped()
        previous_steam = steam

        # Task 5: Gas
        gas_detected = gas.is_detected()
        if gas_detected and not previous_gas:
            handle_gas_detected()
        elif not gas_detected and previous_gas:
            handle_gas_cleared()
        previous_gas = gas_detected

        # Task 7: RFID
        card_id = rfid.scan()
        current_time = time.time()
        if card_id and (card_id != last_card_id or current_time - last_scan_time > SCAN_COOLDOWN):
            handle_rfid_scan(card_id)
            last_card_id = card_id
            last_scan_time = current_time

        # Check MQTT messages and reconnect if needed
        if mqtt_connected:
            mqtt.check_messages()
        else:
            # Try to reconnect every loop iteration
            connect_mqtt()

        time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopping...")
        led.off()
        rgb.off()
        fan.off()
        buzzer.off()
        door.close()
        lcd.clear()
        mqtt.disconnect()
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)
