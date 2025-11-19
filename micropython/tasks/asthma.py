import time
from components import DHT, LCD, WiFi, MQTT
from config import TOPICS

dht = DHT()
lcd = LCD()
wifi = WiFi()
mqtt = MQTT()

previous_alert = False

def check_asthma_conditions(temp, humidity):
    """Check if asthma alert conditions are met"""
    return humidity > 50 and temp > 27

def handle_asthma_alert():
    """Handle asthma alert - display on LCD and publish MQTT"""
    print("⚠️  ASTHMA ALERT!")
    print("   Conditions: High humidity + High temperature")

    if lcd.is_connected():
        lcd.display_alert("! ASTHMA ALERT !", "H>50% T>27C")

    if mqtt.is_connected():
        mqtt.publish(TOPICS.event("asthma_alert"), "1")

def handle_alert_cleared(temp, humidity):
    """Handle when alert conditions clear - show normal readings"""
    print("✅ Asthma alert cleared")

    if lcd.is_connected():
        lcd.display_alert(f"Temp: {temp}C", f"Humidity: {humidity}%")

    if mqtt.is_connected():
        mqtt.publish(TOPICS.event("asthma_alert"), "0")

def update_normal_display(temp, humidity):
    """Update LCD with current readings when no alert"""
    if lcd.is_connected():
        lcd.display_alert(f"Temp: {temp}C", f"Humidity: {humidity}%")

print("=" * 50)
print("ASTHMA ALERT SYSTEM - TASK 6")
print("=" * 50)

print("\nConnecting to WiFi...")
if not wifi.is_connected():
    if wifi.connect():
        print(f"WiFi connected! IP: {wifi.get_ip()}")
    else:
        print("WiFi connection failed!")
else:
    print(f"WiFi already connected! IP: {wifi.get_ip()}")

time.sleep(2)

print("Connecting to MQTT...")
if mqtt.connect():
    print("MQTT connected!")
else:
    print("MQTT connection failed! Bridge will handle publishing.")

print("Checking LCD...")
if lcd.is_connected():
    print(f"LCD connected at address 0x{lcd.addr:02X}")
    lcd.clear()
else:
    print("⚠️  LCD not connected! Alert will only show in serial/MQTT")

print("\nSetup complete! Monitoring for asthma conditions...")
print("Alert triggers when: Humidity > 50% AND Temperature > 27°C")
print("=" * 50)

last_display_update = 0
DISPLAY_UPDATE_INTERVAL = 5  

while True:
    try:
        data = dht.read()

        if data:
            temp = data['temp']
            humidity = data['humidity']

            alert_active = check_asthma_conditions(temp, humidity)

            if int(time.time()) % 10 == 0:
                print(f"\n[{time.localtime()[3]:02d}:{time.localtime()[4]:02d}:{time.localtime()[5]:02d}] T: {temp}°C, H: {humidity}%")

            if alert_active and not previous_alert:
                handle_asthma_alert()
            elif not alert_active and previous_alert:
                handle_alert_cleared(temp, humidity)

            elif not alert_active:
                current_time = time.time()
                if current_time - last_display_update >= DISPLAY_UPDATE_INTERVAL:
                    update_normal_display(temp, humidity)
                    last_display_update = current_time

            previous_alert = alert_active

        mqtt.check_messages()

        time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nStopping asthma alert system...")
        lcd.clear()
        mqtt.disconnect()
        break
    except Exception as e:
        print(f"\nError: {e}")
        time.sleep(1)
