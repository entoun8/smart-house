# Smart House Project - Current Status

**Last Updated:** 2025-11-29

## Completion: 100% (8/8 Tasks)

All features implemented, tested, and working.

## Task Summary

### Task 1: LED Auto Control ✅
**Requirement:** LED lights up between 8pm to 7am

**Implementation:**
- File: [tasks/led_control.py](../micropython/tasks/led_control.py)
- Integrated in [main.py](../micropython/main.py)
- Time-based control (no MQTT, no database)
- Check interval: Every 60 seconds

**Status:** Complete

### Task 2: Temperature & Humidity Logging ✅
**Requirements:**
- Log temperature and humidity every 15 minutes
- Display current values on web dashboard
- Store in database

**Implementation:**
- ESP32: [tasks/temperature.py](../micropython/tasks/temperature.py)
- Web: [TemperatureStatus.tsx](../web-app/components/features/dashboard/TemperatureStatus.tsx)
- Web: [HumidityStatus.tsx](../web-app/components/features/dashboard/HumidityStatus.tsx)
- Database: temperature_logs table
- MQTT Topic: ks5009/house/sensors/climate (JSON: temp + humidity)

**How it works:**
1. ESP32 reads DHT11 every 15 minutes (900 seconds)
2. Publishes combined data: `{"temp": 23, "humidity": 41}`
3. Web app receives MQTT and logs to database
4. Dashboard displays current readings

**Status:** Complete

### Task 3: PIR Motion Detection ✅
**Requirements:**
- RGB orange when motion detected
- Log to database
- Display count on web dashboard

**Implementation:**
- ESP32: [tasks/motion.py](../micropython/tasks/motion.py)
- Web: [MotionStatus.tsx](../web-app/components/features/dashboard/MotionStatus.tsx)
- Database: motion_logs table
- MQTT Topic: ks5009/house/events/motion_detected

**How it works:**
1. PIR sensor detects motion
2. RGB LED turns orange (via RGBController)
3. ESP32 publishes "1" to MQTT
4. Web app logs to database and increments counter

**Status:** Complete

### Task 4: Steam Detection ✅
**Requirements:**
- Close window when moisture detected
- Flash RGB blue

**Implementation:**
- ESP32: [tasks/steam.py](../micropython/tasks/steam.py)
- No database or web dashboard required
- Publishes window state to MQTT for Task 8 tracking

**How it works:**
1. Water sensor detects moisture
2. Window servo closes automatically
3. RGB LED turns blue (via RGBController)
4. Publishes window state "close"

**Status:** Complete

### Task 5: Gas Detection ✅
**Requirements:**
- Turn on fan when gas detected
- RGB solid red
- Log to database
- Show alert on web

**Implementation:**
- ESP32: [tasks/gas.py](../micropython/tasks/gas.py)
- Web: [GasStatus.tsx](../web-app/components/features/dashboard/GasStatus.tsx)
- Database: gas_logs table
- MQTT Topics: ks5009/house/events/gas_detected, ks5009/house/devices/fan/state

**How it works:**
1. Gas sensor detects gas (30s warmup + debouncing)
2. Fan turns on automatically
3. RGB LED turns solid red
4. ESP32 publishes "1" to gas_detected topic
5. ESP32 publishes fan state "on"
6. Web app logs to database and shows alert

**Status:** Complete

### Task 6: Asthma Alert ✅
**Requirements:**
- Show alert on LCD if humidity > 50% AND temp > 27°C
- Show alert on web dashboard

**Implementation:**
- ESP32: [tasks/asthma.py](../micropython/tasks/asthma.py)
- Web: [AsthmaAlert.tsx](../web-app/components/features/dashboard/AsthmaAlert.tsx)
- MQTT Topic: ks5009/house/events/asthma_alert
- No database logging required

**How it works:**
1. AsthmaTask reads temperature data from TemperatureTask
2. Checks if humidity > 50% AND temp > 27°C
3. If true: LCD shows alert, publishes "1" to MQTT
4. If false: LCD shows temp/humidity, publishes "0" to MQTT
5. Web app shows/hides alert based on MQTT

**Status:** Complete

### Task 7: RFID Access Control ✅
**Requirements:**
- Check RFID card against authorized value
- Open door for authorized cards
- Buzzer + RGB flash for unauthorized cards
- Log all scans to database
- Show scan list on web

**Implementation:**
- ESP32: [tasks/access_control.py](../micropython/tasks/access_control.py)
- Web: [app/rfid/page.tsx](../web-app/app/(main)/rfid/page.tsx)
- Database: rfid_scans table, users table
- MQTT Topics: ks5009/house/events/rfid_scan, ks5009/house/devices/door/state
- Authorized card: 0x7cdab502 (hardcoded)

**How it works:**
1. RFID reader scans card
2. ESP32 checks if card == 0x7cdab502
3. **Authorized:** Opens door 3 seconds, green LED, publishes states
4. **Unauthorized:** Flashes RGB red + buzzer 3 times
5. All scans published as JSON: `{"card":"0x...", "status":"authorized"}`
6. Web app logs to database and displays history

**Status:** Complete

### Task 8: Device Control (Web App) ✅
**Requirements:**
- Open/close window and door via web app
- Turn on/off fan via web app
- Show real-time device status

**Implementation:**
- ESP32: [tasks/device_control.py](../micropython/tasks/device_control.py)
- Web: Device control components in [components/features/controls/](../web-app/components/features/controls/)
- MQTT Topics (Command): ks5009/house/devices/{device}/command
- MQTT Topics (State): ks5009/house/devices/{device}/state

**How it works:**
1. User clicks button on web (e.g., "Open Door")
2. Web app publishes "open" to ks5009/house/devices/door/command
3. ESP32 subscribed to ks5009/house/devices/+/command receives message
4. ESP32 executes command (opens door)
5. ESP32 publishes "open" to ks5009/house/devices/door/state
6. Web app receives state and displays "Door: OPEN ✅"

**Features:**
- Real-time status display
- Status updates from both manual and automated tasks
- Gas detection, steam detection, RFID all update device states

**Status:** Complete

## Current Project Structure

```
smart-house/
├── micropython/                ESP32 code
│   ├── main.py                Main entry point (all tasks)
│   ├── config.py              Pin & WiFi configuration
│   ├── components/            Hardware component classes
│   │   ├── sensors/
│   │   ├── actuators/
│   │   ├── connectivity/
│   │   │   ├── mqtt.py
│   │   │   └── mqtt_wrapper.py
│   │   └── displays/
│   └── tasks/                 Task implementations
│       ├── led_control.py     Task 1
│       ├── temperature.py     Task 2
│       ├── motion.py          Task 3
│       ├── steam.py           Task 4
│       ├── gas.py             Task 5
│       ├── asthma.py          Task 6
│       ├── access_control.py  Task 7
│       ├── device_control.py  Task 8
│       └── rgb_controller.py  Shared RGB manager
│
├── web-app/                   Next.js web dashboard
│   ├── app/(main)/
│   │   ├── page.tsx           Home redirect
│   │   ├── dashboard/         Main dashboard page
│   │   ├── rfid/              RFID logs page
│   │   └── controls/          Device controls page
│   ├── components/features/
│   │   ├── dashboard/         Dashboard components
│   │   └── controls/          Control components
│   └── lib/
│       ├── mqtt.ts            MQTT client
│       └── supabase.ts        Database client
│
└── database/
    └── schema.sql             Complete database schema
```

## Database Schema

### Tables (5)

1. **users** - RFID authorized users
   - id, name, rfid_card, created_at

2. **temperature_logs** - Temperature & humidity readings
   - id, temp, humidity, timestamp

3. **motion_logs** - PIR motion events
   - id, timestamp

4. **gas_logs** - Gas sensor readings
   - id, value, timestamp

5. **rfid_scans** - All RFID scan attempts
   - id, card_id, success, user_id, timestamp

## MQTT Topics

### Sensors
- ks5009/house/sensors/climate - Combined temp + humidity (JSON)

### Events
- ks5009/house/events/motion_detected - "1"
- ks5009/house/events/gas_detected - "1"/"0"
- ks5009/house/events/asthma_alert - "1"/"0"
- ks5009/house/events/rfid_scan - JSON

### Device Commands (Web → ESP32)
- ks5009/house/devices/door/command - "open"/"close"
- ks5009/house/devices/window/command - "open"/"close"
- ks5009/house/devices/fan/command - "on"/"off"

### Device States (ESP32 → Web)
- ks5009/house/devices/door/state - "open"/"close"
- ks5009/house/devices/window/state - "open"/"close"
- ks5009/house/devices/fan/state - "on"/"off"

## Hardware Configuration

**Pin Assignments:** (See [config.py](../micropython/config.py))

### Outputs
- LED_PIN = 12 (Yellow LED)
- RGB_LED_PIN = 26 (NeoPixel RGB x4)
- BUZZER_PIN = 25
- FAN_PIN1 = 19, FAN_PIN2 = 18
- DOOR_SERVO_PIN = 13
- WINDOW_SERVO_PIN = 5

### Inputs
- DHT_PIN = 17 (Temperature/Humidity)
- PIR_SENSOR_PIN = 14
- GAS_SENSOR_PIN = 23
- WATER_SENSOR_PIN = 34

### Communication
- RFID (SPI): SCK=18, MOSI=23, MISO=19, SDA=5, RST=22
- LCD (I2C): SCL=22, SDA=21

## How to Run

### ESP32
```bash
# Upload all code
ampy --port COM5 put micropython/main.py
ampy --port COM5 put micropython/config.py
ampy --port COM5 put micropython/components
ampy --port COM5 put micropython/tasks

# Reset ESP32 - runs main.py automatically
```

### Web App
```bash
cd web-app
npm install
npm run dev
# Open http://localhost:3000
```

## Progress

**Total Tasks:** 8
**Completed:** 8 (100%)

```
Task 1: ████████████████████ 100% ✅
Task 2: ████████████████████ 100% ✅
Task 3: ████████████████████ 100% ✅
Task 4: ████████████████████ 100% ✅
Task 5: ████████████████████ 100% ✅
Task 6: ████████████████████ 100% ✅
Task 7: ████████████████████ 100% ✅
Task 8: ████████████████████ 100% ✅
```

## Important Notes

### No Python Bridge
- ESP32 connects directly to HiveMQ Cloud MQTT broker
- Web app connects directly to HiveMQ Cloud and Supabase
- All communication is MQTT-based

### Code Quality
- No test code in production files
- Modular architecture with separate task files
- Reusable components in components/ folder
- Centralized RGB LED management (RGBController)

### MQTT Configuration
- Broker: 26cba3f4929a4be4942914ec72fe5b4b.s1.eu.hivemq.cloud
- Port: 8883 (TLS/SSL)
- Username: smarthome
- Password: SmartHome123!

**Status:** ALL 8 TASKS COMPLETE!
