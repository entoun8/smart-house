"""Debug version - test LCD after full init"""
import time

print("=" * 40)
print("DEBUG: Testing LCD in main context")
print("=" * 40)

# Step 1: WiFi
print("\n[1] WiFi...")
from components import WiFi
wifi = WiFi()
wifi.connect()

# Step 2: MQTT
print("\n[2] MQTT...")
from components import MQTT
mqtt = MQTT()
try:
    mqtt.connect()
except:
    print("MQTT failed (ok)")

# Step 3: RGB
print("\n[3] RGB...")
from components import RGBStrip
rgb = RGBStrip()

# Step 4: LCD
print("\n[4] LCD...")
time.sleep(1)
from components import LCD
lcd = LCD()
print(f"LCD connected: {lcd.is_connected()}")

# Step 5: DHT
print("\n[5] DHT...")
from components import DHT
dht = DHT()
data = dht.read()
if data:
    print(f"Temp: {data['temp']}C, Humidity: {data['humidity']}%")
    if lcd.is_connected():
        lcd.display_alert(f"Temp: {data['temp']}C", f"Humidity: {data['humidity']}%")
        print("LCD updated!")
    else:
        print("LCD not connected!")
else:
    print("DHT failed")

# Step 6: RFID (this might cause conflict)
print("\n[6] RFID...")
from components import RFID
rfid = RFID()

# Step 7: Check LCD again
print("\n[7] LCD check after RFID...")
print(f"LCD still connected: {lcd.is_connected()}")
if lcd.is_connected():
    lcd.display_alert("After RFID", "Init test")

print("\n" + "=" * 40)
print("DEBUG DONE")
