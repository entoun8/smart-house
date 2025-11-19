# Hardware Tests - Complete Guide

This document explains every test file in simple terms.

---

## 🎯 Purpose of Testing

**Why test each component separately?**

Imagine building a car and it doesn't start. What's broken?
- Engine? Battery? Wiring? Wheels?

**Testing individually** = You know EXACTLY what works and what doesn't.

---

## 📋 All Test Files

| Test File | Component | Difficulty | Time |
|-----------|-----------|------------|------|
| `test_led.py` | Yellow LED | ⭐ Easy | 10s |
| `test_buzzer.py` | Buzzer | ⭐ Easy | 5s |
| `test_pir.py` | Motion Sensor | ⭐⭐ Medium | 20s |
| `test_dht.py` | Temp/Humidity | ⭐⭐ Medium | 10s |
| `test_rgb.py` | RGB LEDs | ⭐⭐⭐ Advanced | 15s |
| `test_door.py` | Door Servo | ⭐⭐⭐ Advanced | 15s |
| `test_window.py` | Window Servo | ⭐⭐⭐ Advanced | 15s |
| `test_wifi.py` | WiFi | ⭐⭐ Medium | 10s |
| `test_all_hardware.py` | Everything | ⭐⭐⭐ Advanced | 30s |

---

## 💡 test_led.py - Yellow LED

### What It Does
Blinks the yellow LED 5 times.

### Code Pattern
```python
led = Pin(12, Pin.OUT)  # OUTPUT mode - we control it
led.on()                # Turn ON
led.off()               # Turn OFF
```

### How to Run
```bash
ampy --port COM4 run tests/test_led.py
```

### What You'll See
- Terminal: "Blink 1/5", "Blink 2/5", etc.
- LED: 💡 ⚫ 💡 ⚫ 💡 ⚫ 💡 ⚫ 💡 ⚫

### Key Concepts
- **Digital Output**: ON (3.3V) or OFF (0V)
- **Pin.OUT**: We send signals TO the LED
- **led.on()**: Send HIGH signal (electricity flows)
- **led.off()**: Send LOW signal (no electricity)

### Why This Test First?
- Simplest component
- Visual feedback (you can see it)
- If this works → ESP32, MicroPython, USB all working ✅

### Real-World Use
```python
# Auto night light (8pm-7am)
if hour >= 20 or hour < 7:
    led.on()
```

---

## 🔊 test_buzzer.py - Buzzer

### What It Does
Makes 3 short beeps.

### Code Pattern
```python
buzzer = Pin(25, Pin.OUT)
buzzer.on()   # Beep starts
time.sleep(0.2)
buzzer.off()  # Beep stops
```

### How to Run
```bash
ampy --port COM4 run tests/test_buzzer.py
```

### What You'll Hear
🔊 BEEP! ... BEEP! ... BEEP!

### Key Concepts
- **Same as LED** but makes sound instead of light
- **Timing**: 0.2s beep, 0.5s pause
- **Debounce**: Pause between beeps prevents blur

### Real-World Use
```python
# Gas alarm
if gas_detected:
    buzzer.on()  # ALARM!
```

---

## 👋 test_pir.py - Motion Sensor

### What It Does
Watches for motion for 20 seconds, counts detections.

### Code Pattern
```python
pir = Pin(14, Pin.IN)  # INPUT mode - it tells us
if pir.value() == 1:   # Motion detected
    print("Motion!")
```

### How to Run
```bash
ampy --port COM4 run tests/test_pir.py
```

### What You Do
👋 Wave your hand in front of PIR sensor during test!

### Key Concepts
- **Digital INPUT**: We READ from it (not control)
- **pir.value()**: Returns 1 (motion) or 0 (no motion)
- **Debounce**: Wait 1 sec after detection to prevent spam
- **PIR = Passive Infrared**: Detects heat from moving objects

### Real-World Use
```python
# Motion alert
if pir.value() == 1:
    rgb.fill((255, 165, 0))  # Orange
    log_to_database()
```

---

## 🌡️ test_dht.py - Temperature & Humidity

### What It Does
Reads temperature and humidity 5 times.

### Code Pattern
```python
sensor = dht.DHT11(Pin(17))
sensor.measure()              # Trigger measurement
temp = sensor.temperature()   # Get temp in °C
humidity = sensor.humidity()  # Get humidity in %
```

### How to Run
```bash
ampy --port COM4 run tests/test_dht.py
```

### What You'll See
```
Temperature: 23°C
Humidity: 41%
```

### Key Concepts
- **Complex sensor**: Uses special 1-wire protocol
- **Library required**: `import dht`
- **Two readings**: Temperature AND humidity
- **sensor.measure()**: Must call BEFORE reading values

### Real-World Use
```python
# Asthma alert
if temp > 27 and humidity > 50:
    lcd.display("⚠️ ASTHMA ALERT!")
```

---

## 🌈 test_rgb.py - RGB LED Strip

### What It Does
Displays different colors and rainbow animation on 4 LEDs.

### Code Pattern
```python
np = neopixel.NeoPixel(Pin(26), 4)
np[0] = (255, 0, 0)   # LED 0 = Red (R, G, B)
np[1] = (0, 255, 0)   # LED 1 = Green
np.write()            # Update LEDs
```

### How to Run
```bash
ampy --port COM4 run tests/test_rgb.py
```

### What You'll See
🔴 🟢 🔵 🟠 (and rainbow animation!)

### Key Concepts
- **RGB = Red + Green + Blue**: Mix to make any color
- **(R, G, B)**: Each 0-255
- **np.write()**: MUST call to update LEDs
- **Individual control**: Each LED different color

### Color Cheat Sheet
```python
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)  # Motion detection!
WHITE = (255, 255, 255)
OFF = (0, 0, 0)
```

### Real-World Use
```python
# Motion → Orange, Gas → Red, Steam → Blue
if motion:
    np.fill((255, 165, 0))
    np.write()
```

---

## 🚪 test_door.py - Door Servo

### What It Does
Moves door through positions: closed → half → open → smooth close → smooth open → closed.

### Code Pattern
```python
servo = PWM(Pin(13), freq=50)
servo.duty(26)   # 0° (closed)
servo.duty(77)   # 90° (half)
servo.duty(128)  # 180° (open)
```

### How to Run
```bash
ampy --port COM4 run tests/test_door.py
```

### What You'll See
Door physically moving through all positions!

### Key Concepts
- **PWM = Pulse Width Modulation**: Controls servo angle
- **duty value = angle**: 26=0°, 77=90°, 128=180°
- **freq=50**: Standard for servos (50Hz)
- **Smooth motion**: Loop to gradually change angle

### Duty Value Guide
| Duty | Angle | Position |
|------|-------|----------|
| 26 | 0° | Closed \| |
| 77 | 90° | Half / |
| 128 | 180° | Open ─ |

### Real-World Use
```python
# RFID access
if card_valid:
    servo.duty(128)  # Open door
    time.sleep(5)
    servo.duty(26)   # Close door
```

---

## 🪟 test_window.py - Window Servo

### What It Does
Same as door, but includes **steam detection simulation**.

### Code Pattern
```python
servo = PWM(Pin(5), freq=50)

# Auto-close (steam detected!)
for duty in range(128, 26, -5):
    servo.duty(duty)
    time.sleep(0.1)
```

### How to Run
```bash
ampy --port COM4 run tests/test_window.py
```

### What You'll See
Window closes smoothly when "steam detected"

### Key Difference from Door
**Step 4**: Simulates automatic closing when water detected
- This is your required feature!
- "If steam sensor detects moisture, close window"

### Real-World Use
```python
# Auto-close on rain
if water_sensor.read() > 2000:
    for duty in range(128, 26, -5):
        servo.duty(duty)
        time.sleep(0.1)
    flash_rgb_blue()
```

---

## 📡 test_wifi.py - WiFi Connection

### What It Does
Connects ESP32 to WiFi and shows IP address.

### Code Pattern
```python
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("CyFi", "SecurityA40")
```

### How to Run
```bash
ampy --port COM4 run tests/test_wifi.py
```

### What You'll See
```
✓ Connected to WiFi!
IP Address: 10.52.126.70
```

### Key Concepts
- **STA_IF**: Station mode (connects to router)
- **wlan.connect()**: Join network
- **wlan.isconnected()**: Check if connected
- **wlan.ifconfig()**: Get IP address, gateway, etc.

### Real-World Use
```python
# Connect WiFi, then MQTT
wlan.connect(WIFI_SSID, WIFI_PASSWORD)
mqtt.connect(MQTT_BROKER)
```

---

## 🎯 test_all_hardware.py - Complete Test

### What It Does
Tests ALL components in one run.

### Components Tested
1. Yellow LED (blinks 3x)
2. Buzzer (beeps 3x)
3. PIR sensor (5 second check)
4. Gas sensor (read value)
5. Water sensor (read value)
6. Fan motor (spins 2 seconds)
7. Window servo (moves)
8. Door servo (moves)

### How to Run
```bash
ampy --port COM4 run tests/test_all_hardware.py
```

### What You'll See
Each component tested in sequence, summary at end:
```
✓ Yellow LED: PASS
✓ Buzzer: PASS
✓ PIR Sensor: PASS
...
RESULTS: 7/8 tests passed
```

### When to Use
- First time setup
- After moving house
- Troubleshooting (which part is broken?)
- Quick health check

---

## 🔄 Testing Workflow

### First Time Setup
```bash
# 1. Test simplest first
ampy --port COM4 run tests/test_led.py

# 2. If LED works, ESP32 is good! Test others
ampy --port COM4 run tests/test_buzzer.py
ampy --port COM4 run tests/test_pir.py
# ... etc

# 3. Test everything at once
ampy --port COM4 run tests/test_all_hardware.py
```

### Quick Health Check
```bash
# Just run complete test
ampy --port COM4 run tests/test_all_hardware.py
```

### Debugging
```bash
# If feature not working, test component individually
# Example: Motion detection not working?
ampy --port COM4 run tests/test_pir.py  # Test PIR alone
ampy --port COM4 run tests/test_rgb.py  # Test RGB alone
```

---

## 🎓 Key Concepts Summary

### OUTPUT vs INPUT

| Type | Mode | We Do | Example |
|------|------|-------|---------|
| **OUTPUT** | `Pin.OUT` | Control it | LED, Buzzer, Servos |
| **INPUT** | `Pin.IN` | Read from it | PIR, DHT11 |

### Digital vs Analog

| Type | Values | Example |
|------|--------|---------|
| **Digital** | 0 or 1 (ON/OFF) | LED, PIR |
| **Analog** | 0-4095 (range) | Water sensor, Gas sensor |

### Control Methods

| Component | Method | Example |
|-----------|--------|---------|
| Simple LED | `.on()` / `.off()` | `led.on()` |
| Servo | `.duty()` | `servo.duty(77)` |
| RGB | `[index] = (R,G,B)` | `np[0] = (255,0,0)` |
| Sensor | `.value()` or `.measure()` | `pir.value()` |

---

## 🆘 Troubleshooting

### Test Fails

**LED doesn't blink:**
- Check pin number (should be 12)
- Check wiring
- Try different LED

**Sensor reads 0 always:**
- Check pin number
- Check if sensor needs power
- Wait 30 seconds (some sensors need warm-up)

**Servo doesn't move:**
- Check pin number
- Check power supply (servos need more power)
- Try different duty values

### Upload Fails

**"Can't connect to COM4":**
```bash
# Unplug and replug ESP32
# Then try again
ampy --port COM4 run tests/test_led.py
```

**"Module not found":**
```bash
# Upload missing library
ampy --port COM4 put micropython/lib/neopixel.py
```

---

## 📊 Your Test Results

When you ran all tests, you got:

| Component | Status | Result |
|-----------|--------|--------|
| Yellow LED | ✅ PASS | Blinked 5 times |
| Buzzer | ✅ PASS | Beeped 3 times |
| PIR Sensor | ✅ PASS | Detected 5 motions |
| DHT11 | ✅ PASS | 23°C, 41% humidity |
| RGB LEDs | ✅ PASS | All colors displayed |
| Door Servo | ✅ PASS | Opened/closed smoothly |
| Window Servo | ✅ PASS | Auto-close worked |
| Gas Sensor | ✅ PASS | Reading values |
| Water Sensor | ✅ PASS | Reading values |
| Fan Motor | ✅ PASS | Spun correctly |
| WiFi | ✅ PASS | IP: 10.52.126.70 |

**11/11 = 100% Working!** 🎉

---

## 🚀 Next Steps

After all tests pass:

1. **Build main.py** with all features:
   - Auto LED (8pm-7am)
   - Motion detection → RGB orange
   - Temperature logging
   - Gas alert → Fan + RGB red
   - Steam → Close window + RGB blue

2. **Set up MQTT** for communication

3. **Build Next.js web app** for control

4. **Deploy to production**

---

**All tests passed! You're ready to build the full smart home!** 🏠✨
