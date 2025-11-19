# config.py - Complete Guide

## 🎯 What is config.py?

**Simple answer**: A central "settings file" where you define all pin numbers, WiFi credentials, and configuration once.

**Like**: A phone's contact list - instead of typing phone numbers everywhere, you save them once and use the name.

---

## 🤔 Why Do We Need It?

### The Problem Without config.py

**Imagine you have 10 files that use the LED:**

```python
# motion_detection.py
led = Pin(12, Pin.OUT)

# gas_alert.py
led = Pin(12, Pin.OUT)

# temperature_logger.py
led = Pin(12, Pin.OUT)

# ... 7 more files with Pin(12) ...
```

**What if LED breaks and you move it to pin 15?**
- ❌ Edit 10 files
- ❌ Easy to miss one
- ❌ Code breaks mysteriously

---

### The Solution WITH config.py

**Define once:**
```python
# config.py
LED_PIN = 12
```

**Use everywhere:**
```python
# motion_detection.py
from config import LED_PIN
led = Pin(LED_PIN, Pin.OUT)

# gas_alert.py
from config import LED_PIN
led = Pin(LED_PIN, Pin.OUT)
```

**LED breaks? Change ONE line:**
```python
# config.py
LED_PIN = 15  # Changed! Now ALL files use pin 15 ✅
```

---

## 📋 Your config.py Structure

### 1. Pin Assignments - OUTPUTS (You Control These)

```python
LED_PIN = 12              # Yellow LED
RGB_LED_PIN = 26          # RGB LED Strip (4 LEDs)
BUZZER_PIN = 25           # Buzzer/Alarm
FAN_PIN1 = 19             # Fan Motor Wire 1
FAN_PIN2 = 18             # Fan Motor Wire 2
WINDOW_SERVO_PIN = 5      # Window Motor
DOOR_SERVO_PIN = 13       # Door Motor
```

**What these do**: Control devices (turn on/off, move, change color)

**Think of it like**: Light switches - you control them

---

### 2. Pin Assignments - INPUTS (They Tell You Information)

```python
DHT_PIN = 17              # Temperature & Humidity Sensor
WATER_SENSOR_PIN = 34     # Steam/Water Sensor
GAS_SENSOR_PIN = 23       # Gas/Smoke Sensor
PIR_SENSOR_PIN = 14       # Motion Sensor
```

**What these do**: Give you data (temperature, motion detected, etc.)

**Think of it like**: Thermometers and alarms - they tell you things

---

### 3. I2C Pins (LCD Display)

```python
I2C_SCL_PIN = 22          # I2C Clock
I2C_SDA_PIN = 21          # I2C Data
```

**What these do**: Communicate with LCD screen using I2C protocol

**Why two pins?**
- SCL = Clock (timing)
- SDA = Data (actual information)

---

### 4. RGB LED Settings

```python
RGB_LED_COUNT = 4         # Number of LEDs in strip
```

**Why needed?** NeoPixel library needs to know how many LEDs to control

---

### 5. WiFi Credentials

```python
WIFI_SSID = "CyFi"
WIFI_PASSWORD = "SecurityA40"
```

**Why here?**
- Change WiFi password in ONE place
- Easy to switch networks
- Don't hardcode secrets in main code

---

### 6. MQTT Settings

```python
MQTT_BROKER = "broker.hivemq.com"  # Server address
MQTT_PORT = 1883                   # Standard MQTT port
MQTT_CLIENT_ID = "smart_home_esp32" # Your device name
MQTT_TOPIC_BASE = "smart_home"     # Topic prefix
```

**What these do**: Configure how ESP32 connects to MQTT broker for messaging

---

## 🔧 How to Use config.py

### In Your Main Program

```python
# main.py
from config import *  # Import ALL settings

# Now use them
led = Pin(LED_PIN, Pin.OUT)
pir = Pin(PIR_SENSOR_PIN, Pin.IN)
rgb = neopixel.NeoPixel(Pin(RGB_LED_PIN), RGB_LED_COUNT)

wlan.connect(WIFI_SSID, WIFI_PASSWORD)
mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
```

**Benefits**:
- Clear code: `LED_PIN` instead of `12`
- One place to change settings
- Easy to share (just change config.py)

---

### In Individual Files

```python
# temperature_logger.py
from config import DHT_PIN, MQTT_BROKER

sensor = dht.DHT11(Pin(DHT_PIN))
mqtt = MQTTClient("temp", MQTT_BROKER)
```

**Import only what you need** - keeps it clean

---

## 🎨 Design Patterns

### Pattern 1: Don't Repeat Yourself (DRY)

**Bad** ❌:
```python
# file1.py: led = Pin(12, Pin.OUT)
# file2.py: led = Pin(12, Pin.OUT)
# file3.py: led = Pin(12, Pin.OUT)
```

**Good** ✅:
```python
# config.py: LED_PIN = 12
# file1.py: led = Pin(LED_PIN, Pin.OUT)
# file2.py: led = Pin(LED_PIN, Pin.OUT)
```

---

### Pattern 2: Single Source of Truth

**One authoritative source** for each setting.

**LED pin = 12?** Defined ONCE in config.py
**WiFi password?** Defined ONCE in config.py

**Benefits**:
- No conflicts
- No "which one is correct?"
- Update once = updates everywhere

---

### Pattern 3: Separation of Concerns

**config.py** = WHAT (settings)
**main.py** = HOW (logic)

```python
# config.py - WHAT
LED_PIN = 12

# main.py - HOW
led = Pin(LED_PIN, Pin.OUT)
if motion_detected:
    led.on()
```

---

## 💡 Real-World Analogy

### Phone Contacts

**Without config.py** (no contacts):
```
Text Mom: "Text to 555-1234"
Email Mom: "Email to 555-1234"
Call Mom: "Call 555-1234"

Mom changes number → Update 50 places 😰
```

**With config.py** (saved contact):
```
Save contact: "Mom = 555-1234"

Text: "Text Mom"
Email: "Email Mom"
Call: "Call Mom"

Mom changes number → Update contact ONCE ✅
```

---

## 🔍 Common Use Cases

### Use Case 1: Moving to Different Hardware

**Your KS5009 board → New custom board**

Old board: LED on pin 12
New board: LED on pin 15

**Change**:
```python
# config.py
LED_PIN = 15  # Was 12, now 15
```

**Done!** All files now use pin 15 automatically.

---

### Use Case 2: Switching WiFi Networks

**At school**: WiFi = "SchoolWiFi"
**At home**: WiFi = "HomeWiFi"

**Change**:
```python
# config.py
WIFI_SSID = "HomeWiFi"      # Changed
WIFI_PASSWORD = "home123"   # Changed
```

**Done!** ESP32 connects to new network.

---

### Use Case 3: Testing Different MQTT Brokers

**Development**: Use free public broker
**Production**: Use private broker

**Change**:
```python
# config.py
MQTT_BROKER = "mqtt.mycompany.com"  # Changed
```

---

## 📊 Comparison Table

| Aspect | Without config.py | With config.py |
|--------|-------------------|----------------|
| **Pin 12 defined** | 10 times (scattered) | 1 time (config.py) |
| **Change LED pin** | Edit 10 files | Edit 1 line |
| **WiFi password** | In multiple files | One place |
| **Code readability** | `Pin(12)` - what is 12? | `Pin(LED_PIN)` - clear! |
| **Sharing project** | Edit many files | Edit config.py only |

---

## 🎯 Best Practices

### 1. Use UPPERCASE for Constants

```python
# Good ✅
LED_PIN = 12
WIFI_SSID = "CyFi"

# Bad ❌
led_pin = 12  # Lowercase looks like variable
```

**Why?** Convention: UPPERCASE = constant (doesn't change during runtime)

---

### 2. Group Related Settings

```python
# Good ✅
# OUTPUTS
LED_PIN = 12
BUZZER_PIN = 25

# INPUTS
PIR_PIN = 14
DHT_PIN = 17

# Bad ❌ - Random order
LED_PIN = 12
PIR_PIN = 14
BUZZER_PIN = 25
DHT_PIN = 17
```

**Why?** Organized = easier to find and maintain

---

### 3. Add Comments

```python
# Good ✅
LED_PIN = 12              # Yellow LED

# Bad ❌
LED_PIN = 12
```

**Why?** 6 months later, you'll forget which LED is which

---

### 4. Don't Put Logic in config.py

```python
# Bad ❌ - Don't do this!
LED_PIN = 12
if some_condition:
    LED_PIN = 15

# Good ✅ - Only definitions
LED_PIN = 12
```

**Why?** Config = data only, not logic

---

## 🚀 Advanced: Environment-Specific Configs

**Future enhancement** (not needed now):

```python
# config.py
import os

ENV = os.getenv('ENV', 'development')

if ENV == 'development':
    MQTT_BROKER = "test.mosquitto.org"
elif ENV == 'production':
    MQTT_BROKER = "mqtt.mycompany.com"
```

**Why?** Different settings for testing vs production

---

## 🎓 Key Takeaways

### Why config.py Exists

1. **Single Source of Truth** - Define once, use everywhere
2. **Easy Maintenance** - Change settings in one place
3. **Readable Code** - Names better than numbers
4. **Flexibility** - Swap hardware/networks easily

### When to Use It

✅ Pin numbers
✅ WiFi credentials
✅ MQTT settings
✅ Any constant used in multiple files
✅ Hardware-specific values

### When NOT to Use It

❌ Variables that change during runtime
❌ Temporary values
❌ Logic/functions
❌ File-specific constants

---

## 📝 Quick Reference

### Import Everything
```python
from config import *
```

### Import Specific Items
```python
from config import LED_PIN, WIFI_SSID
```

### Use in Code
```python
led = Pin(LED_PIN, Pin.OUT)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)
```

### Common Changes

**Change WiFi:**
```python
WIFI_SSID = "NewNetwork"
WIFI_PASSWORD = "NewPassword"
```

**Change Pin:**
```python
LED_PIN = 15  # Was 12
```

**Change MQTT:**
```python
MQTT_BROKER = "new.broker.com"
```

---

## 🎊 Summary

**config.py is your project's "settings menu"**

- All pins defined once
- All credentials in one place
- Change once, applies everywhere
- Makes code clean and maintainable

**Think of it as**: The ingredient list at the top of a recipe - you don't want ingredients scattered in the cooking instructions!

---

**Now you understand why config.py exists and how to use it!** 🎉
