# Smart House IoT Project - Complete Guide

**Last Updated:** 2025-11-29
**Status:** 100% Complete (8/8 tasks)

## Quick Start

### One-Line Setup
1. Plug in ESP32 → Auto-starts all tasks
2. Open web dashboard: http://localhost:3000

## Project Overview

ESP32-based smart home system with 15 hardware components running 8 automated tasks.

**Tech Stack:**
- Hardware: ESP32 + 15 components
- Firmware: MicroPython
- Backend: Supabase (PostgreSQL) + HiveMQ (MQTT)
- Frontend: Next.js 14

**Architecture:**
```
ESP32 → WiFi → MQTT Broker → Web Dashboard → Database
```

No Python bridge required - direct ESP32-to-Cloud communication.

## Completed Tasks (8/8)

### Task 1: LED Auto Control
- LED ON: 8pm-7am
- LED OFF: 7am-8pm
- Implementation: Time-based, no MQTT/DB
- File: [tasks/led_control.py](../micropython/tasks/led_control.py)

### Task 2: Temperature & Humidity
- Logs every 15 minutes
- Displays current readings on dashboard
- Implementation: MQTT + Database
- Files: [tasks/temperature.py](../micropython/tasks/temperature.py), Web components

### Task 3: Motion Detection
- RGB orange when motion detected
- Logs to database
- Shows count on dashboard
- Implementation: MQTT + Database
- File: [tasks/motion.py](../micropython/tasks/motion.py)

### Task 4: Steam Detection
- Auto-closes window when moisture detected
- RGB blue flash
- Implementation: Local control, MQTT for status
- File: [tasks/steam.py](../micropython/tasks/steam.py)

### Task 5: Gas Detection
- Fan ON when gas detected
- RGB solid red
- Logs to database
- Implementation: MQTT + Database
- File: [tasks/gas.py](../micropython/tasks/gas.py)

### Task 6: Asthma Alert
- LCD + web alert when humidity >50% AND temp >27°C
- Implementation: MQTT only (no DB)
- File: [tasks/asthma.py](../micropython/tasks/asthma.py)

### Task 7: RFID Access Control
- Checks card against hardcoded value
- Opens door for authorized card (0x7cdab502)
- Buzzer + RGB red flash for unauthorized
- Logs all scans
- Implementation: MQTT + Database
- File: [tasks/access_control.py](../micropython/tasks/access_control.py)

### Task 8: Device Control
- Web app controls door, window, fan
- Real-time status updates
- Implementation: Web → MQTT → ESP32
- File: [tasks/device_control.py](../micropython/tasks/device_control.py)

## Project Structure

```
smart-house/
├── micropython/                ESP32 code
│   ├── main.py                Main entry (all tasks)
│   ├── config.py              Pin & WiFi config
│   ├── components/            Hardware classes
│   │   ├── sensors/           PIR, DHT, Gas, Water, RFID
│   │   ├── actuators/         LED, RGB, Buzzer, Fan, Servos
│   │   ├── displays/          LCD
│   │   └── connectivity/      WiFi, MQTT
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
├── web-app/                   Next.js dashboard
│   ├── app/(main)/
│   │   ├── page.tsx           Dashboard home
│   │   ├── dashboard/         Main dashboard
│   │   ├── rfid/              RFID logs
│   │   └── controls/          Device controls
│   ├── components/features/
│   │   ├── dashboard/         Dashboard components
│   │   └── controls/          Control components
│   └── lib/
│       ├── mqtt.ts            MQTT client
│       └── supabase.ts        Database client
│
├── database/
│   └── schema.sql             5 tables
│
└── docs/
    ├── START_HERE_CLAUDE.md   Read first!
    ├── PROJECT_GUIDE.md       This file
    ├── PROJECT_STATUS.md      Detailed status
    ├── ARCHITECTURE.md        System design
    └── TASK_REQUIREMENTS.md   Original requirements
```

## Database Schema

### Tables (5)
1. **users** - Authorized RFID users
2. **temperature_logs** - Temp/humidity readings
3. **motion_logs** - Motion events
4. **gas_logs** - Gas detections
5. **rfid_scans** - Access attempts

## MQTT Topics

### Sensors
- `ks5009/house/sensors/climate` - Combined temp + humidity JSON

### Events
- `ks5009/house/events/motion_detected` - "1"
- `ks5009/house/events/gas_detected` - "1"/"0"
- `ks5009/house/events/asthma_alert` - "1"/"0"
- `ks5009/house/events/rfid_scan` - JSON with card & status

### Device Commands (Web → ESP32)
- `ks5009/house/devices/door/command` - "open"/"close"
- `ks5009/house/devices/window/command` - "open"/"close"
- `ks5009/house/devices/fan/command` - "on"/"off"

### Device States (ESP32 → Web)
- `ks5009/house/devices/door/state` - "open"/"close"
- `ks5009/house/devices/window/state` - "open"/"close"
- `ks5009/house/devices/fan/state` - "on"/"off"

## Hardware Components

| Component | Pin | Task |
|-----------|-----|------|
| Yellow LED | 12 | Task 1 |
| RGB LEDs (4x) | 26 | Tasks 3,4,5,7 |
| Buzzer | 25 | Task 7 |
| PIR Sensor | 14 | Task 3 |
| DHT11 | 17 | Tasks 2,6 |
| Gas Sensor | 23 | Task 5 |
| Water Sensor | 34 | Task 4 |
| Fan Motor | 18,19 | Task 5 |
| Door Servo | 13 | Task 7,8 |
| Window Servo | 5 | Task 4,8 |
| LCD1602 | I2C (22,21) | Task 6 |
| RFID RC522 | SPI | Task 7 |

## How to Use

### Upload Code to ESP32
```bash
ampy --port COM5 put micropython/main.py
ampy --port COM5 put micropython/config.py
ampy --port COM5 put micropython/components
ampy --port COM5 put micropython/tasks
```

### Monitor ESP32
```bash
python -m serial.tools.miniterm COM5 115200
```

### Start Web Dashboard
```bash
cd web-app
npm install
npm run dev
```

Open http://localhost:3000

## Configuration

### WiFi (config.py)
```python
WIFI_SSID = "Telstra099B26"
WIFI_PASSWORD = "56jh79sqcfx6vnta"
```

### MQTT (config.py)
```python
MQTT_BROKER = "26cba3f4929a4be4942914ec72fe5b4b.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "smarthome"
MQTT_PASSWORD = "SmartHome123!"
```

### Authorized RFID Card (tasks/access_control.py)
```python
AUTHORIZED_CARD = "0x7cdab502"
```

## Key Concepts

### Direct ESP32-to-Cloud
ESP32 connects directly to HiveMQ Cloud MQTT broker via WiFi. No Python bridge needed. Web app handles database logging.

### Component Organization
All hardware abstracted into OOP classes:
```python
from components import LED, DHT, PIR, RFID

led = LED()      # Auto-loads pin from config
dht = DHT()
pir = PIR()

led.on()
temp = dht.read()
if pir.motion_detected():
    print("Motion!")
```

### Centralized RGB Control
RGBController manages priority-based RGB LED control to prevent task conflicts.

## Troubleshooting

### ESP32 Not Connecting
- Check WiFi credentials in config.py
- Ensure correct MQTT broker and port
- Verify ESP32 has internet access

### Web Dashboard Not Updating
- Check MQTT connection in browser console
- Verify web app has internet access
- Check Supabase credentials

### RFID Not Working
- Check SPI wiring
- Verify card ID matches AUTHORIZED_CARD
- Check serial output for scanned card ID

## Project Stats

- **Total Tasks:** 8/8 (100%)
- **Hardware Components:** 15
- **Software Components:** 12 OOP classes
- **Database Tables:** 5
- **MQTT Topics:** 10
- **Web Pages:** 3
- **Lines of Code:** ~2000+

## What You'll Learn

- IoT system design (hardware to cloud)
- Embedded programming (MicroPython on ESP32)
- Full-stack development (Next.js + Supabase)
- Real-time communication (MQTT)
- Hardware interfacing (GPIO, I2C, SPI, PWM)
- Database design (PostgreSQL)
- System integration

Project complete and ready for deployment!
