"""
All Tasks Combined - Runs Task 1, 2, 3, 4, 5, 6, and 7 simultaneously
Simple version that handles:
- Task 1: LED auto-control (8pm-7am)
- Task 2: Temperature logging
- Task 3: Motion detection
- Task 4: Steam detection
- Task 5: Gas detection
- Task 6: Asthma alert
- Task 7: RFID access control
"""

import time
import ntptime
from components import LED, DHT, PIR, WaterSensor, WindowServo, RGBStrip, GasSensor, Fan, LCD, WiFi, MQTT, RFID, Buzzer, DoorServo
from utils.database import Database
from config import TOPICS

# Melbourne timezone offset
MELBOURNE_OFFSET = 11 * 3600

# Initialize all components
led = LED()
dht = DHT()
pir = PIR()
water = WaterSensor()
window = WindowServo()
gas = GasSensor()
fan = Fan()
rgb = RGBStrip()
lcd = LCD()
wifi = WiFi()
mqtt = MQTT()
db = Database()
rfid = RFID()
buzzer = Buzzer()
door = DoorServo()

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
# TASK 1: LED AUTO-CONTROL FUNCTIONS
# ============================================

def get_melbourne_hour():
    """Get current hour in Melbourne (0-23)"""
    utc = time.time()
    melbourne = utc + MELBOURNE_OFFSET
    t = time.localtime(int(melbourne))
    return t[3]

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

    # Only print when state changes
    if state != previous_led_state:
        print(f"💡 [{get_time_str()}] LED auto-control: {state}")
        previous_led_state = state

    return state

def should_check_led():
    """Check if it's time to update LED (every minute)"""
    global last_led_check

    if last_led_check == 0:
        last_led_check = time.time()
        return True  # First run

    elapsed = time.time() - last_led_check
    if elapsed >= LED_CHECK_INTERVAL:
        last_led_check = time.time()
        return True

    return False

# ============================================
# TASK 2: TEMPERATURE FUNCTIONS
# ============================================

def sync_time():
    """Sync time with NTP server - with retry logic"""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            print(f"NTP sync attempt {attempt + 1}/{max_retries}...")
            ntptime.settime()
            print("✅ Time synced successfully!")
            return True
        except Exception as e:
            print(f"   Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("   Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("❌ All NTP sync attempts failed!")
                print("⚠️  LED time-based control will NOT work correctly!")
                return False
    return False

def get_time_str():
    """Get Melbourne time as string (HH:MM)"""
    utc = time.time()
    melbourne = utc + MELBOURNE_OFFSET
    t = time.localtime(int(melbourne))
    return f"{t[3]:02d}:{t[4]:02d}"

def read_temperature():
    """Read and log temperature/humidity - also updates LCD for Task 6"""
    global last_log_time

    print(f"\n[{get_time_str()}] Reading DHT sensor...")

    data = dht.read()

    if data:
        temp = data['temp']
        humidity = data['humidity']

        # Print for bridge to detect
        print(f"  Temperature: {temp}°C")
        print(f"  Humidity: {humidity}%")

        # Update LCD display (Task 6)
        if lcd.is_connected():
            lcd.display_alert(f"Temp: {temp}C", f"Humidity: {humidity}%")
            print(f"  LCD updated")

        # Note: Bridge handles MQTT and database logging
        # ESP32 just prints to serial for bridge to detect

        last_log_time = time.time()
        return True
    else:
        print("  Failed to read sensor")
        return False

def should_log_temperature():
    """Check if it's time to log temperature"""
    if last_log_time == 0:
        return True  # First run

    elapsed = time.time() - last_log_time
    return elapsed >= LOG_INTERVAL

# ============================================
# TASK 3: MOTION FUNCTIONS
# ============================================

def handle_motion_detected():
    """Handle motion detection event"""
    print("🚶 Motion detected!")

    # Light up RGB orange
    rgb.orange()

    # Note: Bridge handles MQTT and database logging
    # ESP32 just prints to serial for bridge to detect

def handle_motion_stopped():
    """Handle when motion stops"""
    rgb.off()

# ============================================
# TASK 4: STEAM DETECTION FUNCTIONS
# ============================================

def handle_steam_detected():
    """Handle steam/moisture detection event"""
    print("💧 Steam detected!")

    # Close window
    window.close()

    # Flash RGB blue
    rgb.blue()

    # Note: Task 4 is simple - no database or MQTT required

def handle_steam_stopped():
    """Handle when steam stops"""
    rgb.off()

# ============================================
# TASK 5: GAS DETECTION FUNCTIONS
# ============================================

def handle_gas_detected():
    """Handle gas detection event"""
    print("🔥 Gas detected!")

    # Turn on fan
    fan.on()

    # Solid RGB red
    rgb.red()

    # Note: Bridge handles MQTT and database logging
    # ESP32 just prints to serial for bridge to detect

def handle_gas_cleared():
    """Handle when gas clears"""
    print("✅ Gas cleared!")
    fan.off()
    rgb.off()

# ============================================
# TASK 6: ASTHMA ALERT FUNCTIONS
# ============================================

def check_asthma_conditions(temp, humidity):
    """Check if asthma alert conditions are met"""
    return humidity > 50 and temp > 27

def handle_asthma_alert():
    """Handle asthma alert - display on LCD and publish MQTT"""
    print("⚠️  ASTHMA ALERT!")
    print("   Conditions: High humidity + High temperature")

    # Display on LCD
    if lcd.is_connected():
        lcd.display_alert("! ASTHMA ALERT !", "H>50% T>27C")

    # Publish to MQTT for web dashboard
    if mqtt.is_connected():
        mqtt.publish(TOPICS.event("asthma_alert"), "1")

def handle_asthma_cleared(temp, humidity):
    """Handle when alert conditions clear - show normal readings"""
    print("✅ Asthma alert cleared")

    # Display normal readings on LCD
    if lcd.is_connected():
        lcd.display_alert(f"Temp: {temp}C", f"Humidity: {humidity}%")

    # Publish to MQTT
    if mqtt.is_connected():
        mqtt.publish(TOPICS.event("asthma_alert"), "0")

def update_normal_display(temp, humidity):
    """Update LCD with current readings when no alert"""
    if lcd.is_connected():
        lcd.display_alert(f"Temp: {temp}C", f"Humidity: {humidity}%")

# ============================================
# TASK 7: RFID ACCESS CONTROL FUNCTIONS
# ============================================

def handle_rfid_scan(card_id):
    """Handle RFID card scan - send to bridge for authorization"""
    print(f"\nRFID card scanned: {card_id}")
    print(f"RFID check request: {card_id}")
    # Bridge will handle authorization and log to database

def handle_authorized_access(card_id):
    """Handle authorized RFID card - open door"""
    print(f"RFID authorized: {card_id}")

    # Open door
    door.open()

    # Flash RGB green
    rgb.green()
    time.sleep(2)
    rgb.off()

    # Close door after 5 seconds
    time.sleep(3)
    door.close()

    print(f"RFID authorized complete: {card_id}")

def handle_unauthorized_access(card_id):
    """Handle unauthorized RFID card - flash red and buzz"""
    print(f"RFID unauthorized: {card_id}")

    # Flash RGB red and buzz
    for _ in range(3):
        rgb.red()
        buzzer.on()
        time.sleep(0.3)
        rgb.off()
        buzzer.off()
        time.sleep(0.3)

    print(f"RFID unauthorized complete: {card_id}")

# ============================================
# MAIN PROGRAM
# ============================================

print("=" * 50)
print("ALL TASKS - Task 1 + 2 + 3 + 4 + 5 + 6 + 7")
print("=" * 50)

# Connect WiFi
print("\nConnecting to WiFi...")
wifi.connect()

# Sync time for Task 1
print("Syncing time for LED auto-control...")
sync_time()

# Note: MQTT and Database handled by PC bridge
# ESP32 just prints to serial, no direct internet needed

print(f"\nTask 1: LED auto-control (8pm-7am)")
print(f"Task 2: Temperature logging every {LOG_INTERVAL // 60} minutes")
print("Task 3: Motion detection (continuous)")
print("Task 4: Steam detection (continuous)")
print("Task 5: Gas detection (continuous)")
print("Task 6: Asthma alert (H>50% & T>27°C)")
print("Task 7: RFID access control (continuous)")
print("Bridge mode: Serial output only")
print("=" * 50)

# Do initial LED check
print(f"\nCurrent time: {get_time_str()}")
update_led()

# Do initial temperature reading
print("\nInitial temperature reading...")
read_temperature()

# Close door at start (Task 7)
door.close()

print("\nSetup complete! All tasks monitoring...")
print("=" * 50)

# Main loop - runs all tasks
while True:
    try:
        # TASK 1: Check LED state (every minute)
        if should_check_led():
            update_led()

        # TASK 2 & 6: Check if time to log temperature and check asthma
        if should_log_temperature():
            data = dht.read()
            if data:
                temp = data['temp']
                humidity = data['humidity']

                # Print for bridge to detect (Task 2)
                print(f"  Temperature: {temp}°C")
                print(f"  Humidity: {humidity}%")
                last_log_time = time.time()

                # TASK 6: Check asthma conditions
                asthma_alert = check_asthma_conditions(temp, humidity)

                if asthma_alert and not previous_asthma:
                    handle_asthma_alert()
                elif not asthma_alert and previous_asthma:
                    handle_asthma_cleared(temp, humidity)
                elif not asthma_alert:
                    # Update normal display with current readings
                    update_normal_display(temp, humidity)

                previous_asthma = asthma_alert
            else:
                print("  Failed to read sensor")

        # TASK 3: Check for motion
        motion = pir.motion_detected()

        if motion and not previous_motion:
            handle_motion_detected()
        elif not motion and previous_motion:
            handle_motion_stopped()

        previous_motion = motion

        # TASK 4: Check for steam
        steam = water.is_wet()

        if steam and not previous_steam:
            handle_steam_detected()
        elif not steam and previous_steam:
            handle_steam_stopped()

        previous_steam = steam

        # TASK 5: Check for gas
        gas_detected = gas.is_detected()

        if gas_detected and not previous_gas:
            handle_gas_detected()
        elif not gas_detected and previous_gas:
            handle_gas_cleared()

        previous_gas = gas_detected

        # TASK 7: Check for RFID card
        card_id = rfid.scan()
        current_time = time.time()

        if card_id and (card_id != last_card_id or current_time - last_scan_time > SCAN_COOLDOWN):
            handle_rfid_scan(card_id)
            last_card_id = card_id
            last_scan_time = current_time

        # Check MQTT messages
        mqtt.check_messages()

        # Sleep briefly
        time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n\nStopping all tasks...")
        led.off()
        rgb.off()
        fan.off()
        buzzer.off()
        door.close()
        lcd.clear()
        mqtt.disconnect()
        break
    except Exception as e:
        print(f"\nError: {e}")
        time.sleep(1)
