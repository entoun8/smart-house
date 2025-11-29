# System Architecture

## Complete System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER LAYER                               │
│  User (via web browser)                                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
│  Next.js Web App (React)                                        │
│  - Dashboard (view sensor data)                                 │
│  - Controls (control devices)                                   │
│  - RFID Logs (view access history)                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ API Calls + MQTT WebSocket
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA & MESSAGING LAYER                     │
│                                                                 │
│  ┌────────────────────┐          ┌────────────────────┐        │
│  │ Supabase Database  │          │ HiveMQ Cloud MQTT  │        │
│  │ (PostgreSQL)       │          │ Broker             │        │
│  │ - 5 tables         │          │ - 10 topics        │        │
│  └────────────────────┘          └────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                             ▲
                             │
                             │ WiFi (MQTT over TLS)
                             │
┌─────────────────────────────────────────────────────────────────┐
│                    EDGE DEVICE LAYER                            │
│  ESP32 Smart Home (MicroPython)                                 │
│  - Reads sensors continuously                                   │
│  - Controls actuators                                           │
│  - Publishes sensor data & events to MQTT                       │
│  - Subscribes to device commands from web                       │
│  - Publishes device state updates                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ GPIO Pins
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    HARDWARE LAYER                               │
│  Physical Components                                            │
│  - Sensors (PIR, DHT11, Gas, Water, RFID)                       │
│  - Actuators (LED, Buzzer, Fan, Servos, RGB)                    │
│  - Displays (LCD1602)                                           │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Examples

### Example 1: Temperature Monitoring

```
1. DHT11 Sensor measures temperature
           ↓
2. ESP32 reads sensor (every 15 minutes)
   temp = dht.read()  # {"temp": 23, "humidity": 41}
           ↓
3. ESP32 publishes to MQTT
   mqtt.publish("ks5009/house/sensors/climate", '{"temp": 23, "humidity": 41}')
           ↓
4. HiveMQ Cloud MQTT Broker receives message
           ↓
5. Web App subscribed to topic receives message
   {"temp": 23, "humidity": 41}
           ↓
6. Web App logs to Supabase
   INSERT INTO temperature_logs (temp, humidity)
           ↓
7. Web App displays on dashboard
   "🌡️ 23°C, 💧 41%"
```

### Example 2: Remote Door Control

```
1. User clicks "Open Door" on web app
           ↓
2. Web App publishes MQTT message
   mqtt.publish("ks5009/house/devices/door/command", "open")
           ↓
3. HiveMQ Cloud routes message
           ↓
4. ESP32 subscribed to "ks5009/house/devices/+/command"
   Receives: "open" on door/command topic
           ↓
5. ESP32 executes command
   door_servo.open()
           ↓
6. Door physically opens
           ↓
7. ESP32 publishes state confirmation
   mqtt.publish("ks5009/house/devices/door/state", "open")
           ↓
8. Web App receives state update
   Updates UI: "Door: OPEN ✅"
```

### Example 3: Motion Detection

```
1. PIR sensor detects motion
           ↓
2. ESP32 task processes event
   - Sets RGB to orange
   - Publishes MQTT: "1"
           ↓
3. MQTT message sent to broker
           ↓
4. Web app receives message
   - Increments motion counter
   - Logs to database
           ↓
5. Dashboard shows updated count
```

## Component Relationships

### Runtime Flow

```
ESP32 Power On
  ↓
main.py loads
  ↓
Initialize components (WiFi, MQTT, sensors, actuators)
  ↓
Connect to WiFi
  ↓
Connect to MQTT Broker
  ↓
Initialize all 8 tasks
  ↓
Enter main loop:
  ├── Task 1: Check LED (every 60s)
  ├── Task 2: Log temperature (every 15 min)
  ├── Task 3: Check motion (continuous)
  ├── Task 4: Check steam (continuous)
  ├── Task 5: Check gas (continuous + 30s warmup)
  ├── Task 6: Check asthma (depends on Task 2)
  ├── Task 7: Check RFID (continuous)
  ├── Task 8: Listen for commands (MQTT callback)
  └── Sleep 0.1s, repeat forever
```

### Task Dependencies

```
Temperature Task (Task 2)
    ↓ provides data
Asthma Task (Task 6)
    ↓ uses temp/humidity
LCD Display + MQTT publish

Device Control Task (Task 8)
    ↓ can override
Steam Task (Task 4) & Gas Task (Task 5)
    ↓ automatic device control
Door, Window, Fan

RGB Controller
    ↑ used by
Motion (Task 3), Steam (Task 4), Gas (Task 5), RFID (Task 7)
    ↓ manages priority
NeoPixel RGB LEDs
```

## Pin Connection Map

### ESP32 Pin Layout

```
               ESP32 Board
         ┌──────────────────┐
         │                  │
   3V3 ──┤                  │
   GND ──┤                  │
GPIO 5 ──┤  (Window Servo)  │
GPIO 12 ─┤  (Yellow LED)    │
GPIO 13 ─┤  (Door Servo)    │
GPIO 14 ─┤  (PIR Sensor)    │
GPIO 17 ─┤  (DHT11)         │
GPIO 18 ─┤  (Fan Pin 2)     │
GPIO 19 ─┤  (Fan Pin 1)     │
GPIO 21 ─┤  (I2C SDA)       │
GPIO 22 ─┤  (I2C SCL)       │
GPIO 23 ─┤  (Gas Sensor)    │
GPIO 25 ─┤  (Buzzer)        │
GPIO 26 ─┤  (RGB NeoPixel)  │
GPIO 34 ─┤  (Water Sensor)  │
         │                  │
         └──────────────────┘
```

## Code Execution Flow

### Main Program Structure

```python
# main.py

# 1. IMPORTS
from components import WiFi, MQTT, DHT, PIR, etc.
from tasks import *

# 2. INITIALIZATION
wifi = WiFi()
mqtt = MQTT()
rgb_controller = RGBController()

# Initialize all tasks
task1 = LEDControlTask()
task2 = TemperatureTask(mqtt)
task3 = MotionTask(mqtt, rgb_controller)
# ... etc

# 3. CONNECT
wifi.connect()
mqtt.connect()

# 4. MAIN LOOP
while True:
    task1.update()
    task2.update()
    task3.update()
    task4.update()
    task5.update()
    task6.update()
    task7.update()
    task8.update()

    mqtt.check_messages()
    time.sleep(0.1)
```

## MQTT Topic Structure

```
ks5009/house/
├── sensors/
│   └── climate                    {"temp": 23, "humidity": 41}
├── events/
│   ├── motion_detected            "1"
│   ├── gas_detected               "1" or "0"
│   ├── asthma_alert               "1" or "0"
│   └── rfid_scan                  {"card": "0x...", "status": "..."}
└── devices/
    ├── door/
    │   ├── command                "open" or "close"
    │   └── state                  "open" or "close"
    ├── window/
    │   ├── command                "open" or "close"
    │   └── state                  "open" or "close"
    └── fan/
        ├── command                "on" or "off"
        └── state                  "on" or "off"
```

## Database Schema

```sql
users (id, name, rfid_card, created_at)
    ↓ referenced by
rfid_scans (id, card_id, success, user_id, timestamp)

temperature_logs (id, temp, humidity, timestamp)

motion_logs (id, timestamp)

gas_logs (id, value, timestamp)
```

## Security Considerations

### Current Setup
```
ESP32 → WiFi → TLS/SSL → MQTT Broker (encrypted + authenticated)
                              ↕
                          Web App (user login TBD)
```

**Implemented:**
- MQTT over TLS (encrypted communication)
- Username/password for MQTT
- Hardcoded authorized RFID card

**To Improve:**
- User authentication for web app
- Environment variables for credentials
- Multiple authorized RFID cards in database

## Scalability Path

### Phase 1: Single House (Current)
```
1 ESP32 → MQTT Broker → Web App → Database
```

### Phase 2: Multiple Rooms
```
ESP32 (Living Room) ──┐
ESP32 (Bedroom)      ─┼→ MQTT Broker → Web App → Database
ESP32 (Kitchen)      ─┘

Topics:
- ks5009/living_room/sensors/climate
- ks5009/bedroom/sensors/climate
- ks5009/kitchen/sensors/climate
```

### Phase 3: Multiple Houses
```
House 1 ESP32 ──┐
House 2 ESP32  ─┼→ MQTT Broker → Load Balancer → Database Cluster
House 3 ESP32  ─┘                     ↑
                                Multiple Web Apps
```

## Key Takeaways

**Full-Stack IoT:**
- Hardware layer (sensors, actuators)
- Firmware layer (MicroPython on ESP32)
- Network layer (WiFi, MQTT)
- Application layer (Next.js web app)
- Data layer (Supabase database)

**Direct ESP32-to-Cloud:**
- No Python bridge required
- ESP32 connects directly to MQTT broker
- Web app handles database logging
- Simpler architecture, easier to maintain

**Real-Time Communication:**
- MQTT for instant updates
- WebSocket connection to broker
- Bi-directional control (web ↔ ESP32)

**Modular Design:**
- Separate task files
- Reusable component classes
- Centralized configuration
- Clean separation of concerns
