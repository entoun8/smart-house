import time
from components import LCD, DHT

print("Test start")

lcd = LCD()
print(f"LCD connected: {lcd.is_connected()}")

if lcd.is_connected():
    dht = DHT()
    data = dht.read()
    if data:
        print(f"Temp: {data['temp']}C, Humidity: {data['humidity']}%")
        lcd.display_alert(f"Temp: {data['temp']}C", f"Humidity: {data['humidity']}%")
        print("LCD should show temp now!")
    else:
        print("DHT read failed")
        lcd.display_alert("DHT Failed", "Check sensor")
else:
    print("LCD not connected!")

print("Test done")
