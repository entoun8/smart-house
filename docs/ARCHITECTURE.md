# System Architecture - Visual Guide

## 🏗️ Complete System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER LAYER                               │
│  👤 You (via web browser or mobile)                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
│  🌐 Next.js Web App (React)                                     │
│  - Dashboard (view data)                                        │
│  - Controls (open door, turn on fan)                            │
│  - History (charts, logs)                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ API Calls + MQTT Subscribe
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
│  💾 Supabase (PostgreSQL Database)                              │
│  - temperature_logs                                             │
│  - motion_logs                                                  │
│  - gas_logs                                                     │
│  - rfid_scans                                                   │
│  - users                                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Database Triggers / API
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   COMMUNICATION LAYER                           │
│  📡 HiveMQ Cloud MQTT Broker (Message Hub)                      │
│  Topics:                                                        │
│    - ks5009/house/sensors/climate                               │
│    - ks5009/house/events/motion_detected                        │
│    - ks5009/house/events/gas_detected                           │
│    - ks5009/house/devices/door/command                          │
│    - ks5009/house/devices/door/state                            │
│    - ks5009/house/devices/fan/command                           │
│    - ks5009/house/devices/fan/state                             │
│    - ks5009/house/devices/window/command                        │
│    - ks5009/house/devices/window/state                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ WiFi (MQTT over TLS)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EDGE DEVICE LAYER                            │
│  🏠 ESP32 Smart Home (MicroPython)                              │
│  - Reads sensors every 0.5s                                     │
│  - Controls actuators                                           │
│  - Publishes sensor data & events to MQTT                       │
│  - Subscribes to device commands                                │
│  - Publishes device state updates                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ GPIO Pins
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    HARDWARE LAYER                               │
│  ⚡ Physical Components                                         │
│  - Sensors (PIR, DHT11, Gas, Water)                             │
│  - Actuators (LED, Buzzer, Fan, Servos, RGB)                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Examples

### Example 1: Temperature Monitoring

```
1. DHT11 Sensor measures temperature
           ↓
2. ESP32 reads sensor (every 15 minutes)
   temp = dht.temperature()  # 23°C
           ↓
3. ESP32 publishes to MQTT
   mqtt.publish("ks5009/house/sensors/climate", '{"temp": 23, "humidity": 41}')
           ↓
4. HiveMQ Cloud MQTT Broker receives message
           ↓
5. Next.js Web App subscribed to topic
   Receives: {"temp": 23, "humidity": 41}
           ↓
6. Web App stores in Supabase
   INSERT INTO temperature_logs (temp, humidity, timestamp)
           ↓
7. Web App displays on dashboard
   User sees: "🌡️ 23°C, 💧 41%"
```

**Developer Note**: This is a **direct ESP32-to-Cloud pattern** - No Python bridge needed. ESP32 connects directly to cloud MQTT broker.

---

### Example 2: Remote Door Control

```
1. User clicks "Open Door" button on web app
           ↓
2. Web App publishes MQTT message
   mqtt.publish("ks5009/house/devices/door/command", "open")
           ↓
3. HiveMQ Cloud MQTT Broker routes message
           ↓
4. ESP32 subscribed to "ks5009/house/devices/+/command"
   Receives: "open" on door/command topic
           ↓
5. ESP32 executes command
   door_servo.duty(128)  # Rotate to open position
           ↓
6. Door physically opens
           ↓
7. ESP32 publishes state confirmation
   mqtt.publish("ks5009/house/devices/door/state", "open")
           ↓
8. Web App receives state update
   Updates UI: "Door: OPEN ✅" (green)
```

**Developer Note**: This is **bidirectional communication** with state feedback - commands go down, state confirmations come back up.

---

## 🧩 Component Relationships

### File Dependencies

```
main.py
  ├── imports config.py (for pin numbers, WiFi credentials)
  ├── imports lib/neopixel.py (for RGB LED control)
  ├── uses machine.Pin (for GPIO control)
  ├── uses network (for WiFi connection)
  ├── uses umqtt.simple (for MQTT communication)
  └── uses dht (for temperature sensor)
```

### Runtime Dependencies

```
ESP32 Power On
  ↓
MicroPython boots
  ↓
Runs main.py
  ↓
Connects to WiFi
  ↓
Connects to MQTT Broker
  ↓
Enters main loop:
  ├── Read sensors
  ├── Check for commands
  ├── Update actuators
  ├── Publish data
  └── Repeat forever
```

---

## 🔌 Pin Connection Map

### Visual Pin Layout

```
               ESP32 Board
         ┌──────────────────┐
         │                  │
   3V3 ──┤ 1            39  ├── GND
   GND ──┤ 2            38  ├── GPIO 26 (RGB LED)
   ─────┤ ...          ...  ├──
GPIO 5 ──┤ 10  (Window)  29 ├── GPIO 17 (DHT11)
   ─────┤ ...          ...  ├──
GPIO 12 ─┤ 14   (LED)    25 ├── GPIO 14 (PIR)
GPIO 13 ─┤ 15   (Door)   24 ├── GPIO 25 (Buzzer)
   ─────┤ ...          ...  ├──
GPIO 18 ─┤ 19  (Fan2)    21 ├── GPIO 23 (Gas)
GPIO 19 ─┤ 20  (Fan1)    20 ├── GPIO 34 (Water)
         │                  │
         └──────────────────┘
```

### Sensor Wiring Pattern

```
Sensor (e.g., PIR Motion)
  ├── VCC → ESP32 3.3V
  ├── GND → ESP32 GND
  └── OUT → ESP32 GPIO 14
```

### Actuator Wiring Pattern

```
Actuator (e.g., LED)
  ├── Positive → ESP32 GPIO 12
  └── Negative → Resistor → GND
```

---

## 📊 Code Execution Flow

### Main Program Structure

```python
# ========================================
# INITIALIZATION (runs once)
# ========================================

from machine import Pin
import network
import time
from config import *

# 1. Set up hardware
led = Pin(LED_PIN, Pin.OUT)
pir = Pin(PIR_SENSOR_PIN, Pin.IN)
# ... more components

# 2. Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

# 3. Connect to MQTT
mqtt_client = MQTTClient(...)
mqtt_client.connect()

# ========================================
# MAIN LOOP (runs forever)
# ========================================

while True:
    # 4. Read sensors
    motion = pir.value()
    temp = dht.temperature()

    # 5. Make decisions
    if motion == 1:
        # Turn RGB orange
        # Log to database

    if temp > 27:
        # Send alert

    # 6. Check for commands
    mqtt_client.check_msg()  # Receives commands from web app

    # 7. Brief pause
    time.sleep(0.1)  # Run loop 10 times per second
```

**Developer Note**: This is an **event-driven loop** - continuously checking sensors and responding to events.

---

## 🎯 Feature Implementation Map

### Feature: Motion Detection → RGB Orange

```
┌────────────────┐
│ PIR Sensor     │ Detects motion
└────┬───────────┘
     │ value() = 1
     ▼
┌────────────────┐
│ ESP32 main.py  │ if pir.value() == 1:
└────┬───────────┘       rgb.set_color(ORANGE)
     │                   mqtt.publish("home/motion", "detected")
     ├─────────────────────────┬────────────────┐
     ▼                         ▼                ▼
┌────────────────┐    ┌──────────────┐  ┌─────────────┐
│ RGB LED        │    │ MQTT Broker  │  │ Database    │
│ Turns ORANGE   │    │ Routes msg   │  │ Logs event  │
└────────────────┘    └──────┬───────┘  └─────────────┘
                             ▼
                      ┌──────────────┐
                      │ Web App      │
                      │ Shows alert  │
                      └──────────────┘
```

### Feature: Auto LED (8pm - 7am)

```
┌────────────────┐
│ ESP32 Clock    │ Gets current time
└────┬───────────┘
     │ hour = 21 (9pm)
     ▼
┌────────────────┐
│ main.py        │ if hour >= 20 or hour < 7:
└────┬───────────┘       led.on()
     │             else:
     │                   led.off()
     ▼
┌────────────────┐
│ Yellow LED     │ Lights up
└────────────────┘
```

### Feature: Gas Detection → Fan + Alert

```
┌────────────────┐
│ Gas Sensor     │ Detects gas
└────┬───────────┘
     │ value() = 1
     ▼
┌────────────────┐
│ main.py        │ if gas.value() == 1:
└────┬───────────┘       fan.on()
     │                   rgb.set_color(RED)
     │                   mqtt.publish("home/alert", "GAS")
     ├──────────┬──────────┬────────────┐
     ▼          ▼          ▼            ▼
┌────────┐ ┌───────┐ ┌─────────┐ ┌──────────┐
│  Fan   │ │  RGB  │ │  MQTT   │ │ Database │
│  ON    │ │  RED  │ │  Alert  │ │  Log     │
└────────┘ └───────┘ └────┬────┘ └──────────┘
                          ▼
                    ┌──────────┐
                    │ Web App  │
                    │ 🚨 ALERT │
                    └──────────┘
```

---

## 🔐 Security Considerations

### Current Setup (Development)
```
ESP32 → WiFi → Internet → MQTT Broker (unencrypted)
                              ↕
                          Web App (can read/write)
```

**Issues**:
- ❌ MQTT not encrypted (anyone on network can intercept)
- ❌ No authentication (anyone can send commands)
- ❌ WiFi password in plain text

### Production Setup (Future)
```
ESP32 → WiFi → TLS/SSL → MQTT Broker (encrypted + authenticated)
                              ↕
                          Web App (user login required)
```

**Improvements**:
- ✅ MQTT over TLS (encrypted communication)
- ✅ Username/password for MQTT
- ✅ User authentication for web app
- ✅ Environment variables for secrets

---

## 📈 Scalability Path

### Phase 1: Single House (Current)
```
1 ESP32 → 1 MQTT Broker → 1 Web App → 1 Database
```

### Phase 2: Multiple Rooms
```
ESP32 (Living Room) ──┐
ESP32 (Bedroom)      ─┼→ 1 MQTT Broker → 1 Web App → 1 Database
ESP32 (Kitchen)      ─┘
```

### Phase 3: Multiple Houses
```
House 1 ESP32 ──┐
House 2 ESP32  ─┼→ MQTT Broker Cluster → Load Balancer → Database Cluster
House 3 ESP32  ─┘                             ↑
                                        Multiple Web Apps
```

**Developer Note**: MQTT topics help organize multiple devices:
- `house1/living_room/temperature`
- `house2/bedroom/motion`

---

## 🧪 Testing Strategy

### Unit Testing (Component Level)
```
test_led.py          → Tests ONLY the LED
test_pir.py          → Tests ONLY the motion sensor
test_dht.py          → Tests ONLY temperature sensor
```

**Purpose**: Isolate and verify each piece works

### Integration Testing (System Level)
```
test_all_hardware.py → Tests all components together
test_wifi.py         → Tests network connectivity
```

**Purpose**: Verify components work together

### End-to-End Testing (Full Stack)
```
User clicks button → Web app → MQTT → ESP32 → Door opens
```

**Purpose**: Verify entire system works as expected

---

## 🎓 Debugging Guide

### Problem: Feature not working

**Step 1**: Test hardware
```bash
ampy --port COM5 run tests/test_pir.py
```
Does the component work in isolation?

**Step 2**: Check logs
```python
# Add print statements
if pir.value() == 1:
    print("Motion detected!")  # ← Add this
    rgb.set_color(ORANGE)
```

**Step 3**: Verify MQTT
```bash
# Subscribe to all topics to see what ESP32 publishes
mosquitto_sub -h broker.hivemq.com -t "home/#" -v
```

**Step 4**: Check web app console
```javascript
// Browser console shows errors
console.log("Received MQTT message:", message)
```

---

## 🚀 Development Roadmap

### Week 1: Core Functionality
- [ ] Build `main.py` with all features
- [ ] Test each feature individually
- [ ] Ensure ESP32 runs 24/7 without crashes

### Week 2: Backend Setup
- [ ] Create Supabase database
- [ ] Set up MQTT broker (HiveMQ Cloud)
- [ ] Test ESP32 → MQTT → Database flow

### Week 3: Frontend Development
- [ ] Initialize Next.js project
- [ ] Build dashboard page
- [ ] Build controls page
- [ ] Connect to MQTT

### Week 4: Integration & Polish
- [ ] End-to-end testing
- [ ] Fix bugs
- [ ] Add error handling
- [ ] Deploy to production

---

## 💻 Command Cheat Sheet

### Development Commands
```bash
# Upload code to ESP32
ampy --port COM5 put micropython/main.py

# Run code temporarily (for testing)
ampy --port COM5 run tests/test_led.py

# Download file from ESP32
ampy --port COM5 get main.py

# List files on ESP32
ampy --port COM5 ls

# Connect to ESP32 console (for debugging)
python -m serial.tools.miniterm COM5 115200

# Flash MicroPython firmware (only once during setup)
python -m esptool --chip esp32 --port COM5 write_flash 0x1000 firmware.bin
```

### MQTT Testing
```bash
# Subscribe to all topics
mosquitto_sub -h broker.hivemq.com -t "home/#"

# Publish test message
mosquitto_pub -h broker.hivemq.com -t "home/test" -m "Hello"
```

---

## 🎯 Key Takeaways

### What You Now Understand

1. **Full-Stack IoT Development**
   - Hardware layer (sensors, actuators)
   - Firmware layer (MicroPython on ESP32)
   - Network layer (WiFi, MQTT)
   - Application layer (Next.js web app)
   - Data layer (Supabase database)

2. **Embedded Systems**
   - How code runs on microcontrollers
   - GPIO pin control
   - Sensor reading
   - Actuator control

3. **IoT Protocols**
   - MQTT publish/subscribe
   - WiFi connectivity
   - Serial communication

4. **System Architecture**
   - Separation of concerns
   - Modular design
   - Configuration management

### Skills You Can Now Apply

- Build IoT devices from scratch
- Interface software with hardware
- Design real-time systems
- Implement publish/subscribe patterns
- Debug embedded systems
- Structure complex projects

---

**You're ready to build professional IoT applications!** 🎉
