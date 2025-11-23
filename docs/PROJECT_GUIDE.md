# Smart House IoT Project - Complete Guide

**Last Updated:** 2025-11-23
**Status:** 100% Complete (8/8 tasks) 🎉

---

## 🚀 Quick Start

### One-Click Launch
```bash
# 1. Plug in ESP32 to USB
# 2. Double-click: RUN.bat
# 3. Open: http://localhost:3000
```

Everything starts automatically!

---

## 📊 Project Overview

### What This Is
ESP32-based smart home system with:
- **Hardware:** ESP32 with 15 components (sensors, actuators, displays)
- **Firmware:** MicroPython 1.24.0
- **Backend:** Supabase (PostgreSQL) + MQTT (HiveMQ)
- **Frontend:** Next.js 14 web dashboard
- **Bridge:** Python script for ESP32 ↔ Cloud communication

### Architecture
```
ESP32 (Sensors + Actuators)
    ↓ Serial
Bridge (Python on PC)
    ↓ HTTP + MQTT
Database (Supabase) + MQTT Broker
    ↓ WebSocket + API
Web Dashboard (Next.js)
    ↓ Browser
User
```

---

## ✅ Completed Tasks (8/8)

### Task 1: LED Auto Control
- **File:** [micropython/task1_led_simple.py](../micropython/task1_led_simple.py)
- **What:** LED ON 8pm-7am, OFF 7am-8pm
- **Implementation:** Simple time-based, no MQTT/DB

### Task 2: Temperature & Humidity
- **Files:** [temperature_mqtt.py](../micropython/temperature_mqtt.py), [TemperatureStatus.tsx](../web-app/components/features/dashboard/TemperatureStatus.tsx)
- **What:** Logs every 30 min, displays on dashboard
- **Implementation:** MQTT + Database + Web

### Task 3: Motion Detection
- **Files:** [task3_pir_mqtt.py](../micropython/task3_pir_mqtt.py), [MotionStatus.tsx](../web-app/components/features/dashboard/MotionStatus.tsx)
- **What:** RGB orange on motion, logs to DB, shows count on web
- **Implementation:** Serial → Bridge → MQTT + Database

### Task 4: Steam Detection
- **Files:** [task4_steam_detection.py](../micropython/task4_steam_detection.py)
- **What:** Auto-closes window + RGB blue when moisture detected
- **Implementation:** Simple, no MQTT/DB

### Task 5: Gas Detection
- **Files:** [task5_gas_detection.py](../micropython/task5_gas_detection.py), [GasStatus.tsx](../web-app/components/features/dashboard/GasStatus.tsx)
- **What:** Fan ON + RGB red when gas detected, logs to DB
- **Implementation:** Serial → Bridge → MQTT + Database

### Task 6: Asthma Alert
- **Files:** [task6_asthma_alert.py](../micropython/task6_asthma_alert.py), [AsthmaAlert.tsx](../web-app/components/features/dashboard/AsthmaAlert.tsx)
- **What:** LCD + web alert when humidity >50% AND temp >27°C
- **Implementation:** MQTT only (no DB logging)

### Task 7: RFID Access Control
- **Files:** [task7_rfid_access.py](../micropython/task7_rfid_access.py), [rfid/page.tsx](../web-app/app/rfid/page.tsx)
- **What:** Scan RFID → Check DB → Open door or deny + buzz
- **Implementation:** Serial → Bridge → Database + MQTT

### Task 8: Device Control (Web App)
- **Files:** [device_control.py](../micropython/tasks/device_control.py), [ControlsContent.tsx](../web-app/components/features/controls/ControlsContent.tsx)
- **What:** Control door, window, fan remotely via web app
- **Implementation:** Web App → MQTT → ESP32

---

## 🗂️ Project Structure

```
smart-house/
├── RUN.bat                    ⭐ ONE-CLICK LAUNCHER
├── README.md                  Project overview
├── unified_bridge.py          Bridge for all tasks
│
├── micropython/               ESP32 code
│   ├── boot.py               Auto-starts all tasks
│   ├── all_tasks.py          Tasks 1-7 combined
│   ├── config.py             Configuration
│   └── components/           OOP component classes
│       ├── sensors/          PIR, DHT, Gas, Water, RFID
│       ├── actuators/        LED, RGB, Buzzer, Fan, Servos
│       ├── displays/         LCD
│       └── connectivity/     WiFi, MQTT
│
├── web-app/                   Next.js dashboard
│   ├── app/
│   │   ├── page.tsx          Main dashboard
│   │   └── rfid/page.tsx     RFID logs page
│   ├── components/features/dashboard/
│   │   ├── TemperatureStatus.tsx
│   │   ├── HumidityStatus.tsx
│   │   ├── MotionStatus.tsx
│   │   ├── GasStatus.tsx
│   │   └── AsthmaAlert.tsx
│   └── lib/
│       ├── mqtt.ts           MQTT client
│       └── supabase.ts       Database client
│
├── database/                  SQL schemas
│   └── CLEAN_SCHEMA.sql      5 tables
│
├── docs/                      Documentation
│   ├── PROJECT_GUIDE.md      This file (START HERE!)
│   ├── PROJECT_STATUS.md     Detailed status
│   ├── ARCHITECTURE.md       System architecture
│   └── TASK_REQUIREMENTS.md  Original requirements
│
└── tests/                     Hardware tests
```

---

## 🗄️ Database Schema

### Tables (5)
1. **users** - RFID authorized users
2. **temperature_logs** - Temp/humidity readings
3. **motion_logs** - PIR motion events
4. **gas_logs** - Gas sensor readings
5. **rfid_scans** - Access attempts log

---

## 📡 MQTT Topics

```
ks5009/house/sensors/temperature       (Task 2)
ks5009/house/sensors/humidity          (Task 2)
ks5009/house/events/motion_detected    (Task 3)
ks5009/house/events/gas_detected       (Task 5)
ks5009/house/events/asthma_alert       (Task 6)
ks5009/house/events/rfid_scan          (Task 7)
```

---

## 🔧 Hardware Components

| Component | Pin | Task |
|-----------|-----|------|
| Yellow LED | GPIO 12 | Task 1 |
| RGB LEDs (4x) | GPIO 26 | Tasks 3,4,5,7 |
| Buzzer | GPIO 25 | Task 7 |
| PIR Sensor | GPIO 14 | Task 3 |
| DHT11 | GPIO 17 | Tasks 2,6 |
| Gas Sensor | GPIO 23 | Task 5 |
| Water Sensor | GPIO 34 | Task 4 |
| Fan Motor | GPIO 18,19 | Task 5 |
| Door Servo | GPIO 13 | Task 7 |
| Window Servo | GPIO 5 | Task 4 |
| LCD1602 | I2C (22,21) | Task 6 |
| RFID RC522 | SPI | Task 7 |

---

## 🛠️ How to Use

### Daily Usage
1. **Plug in ESP32** → All tasks auto-start (via boot.py)
2. **Double-click RUN.bat** → Starts bridge + web dashboard
3. **Open browser** → http://localhost:3000
4. **Done!** System is running

### What Each Part Does

**ESP32:**
- Reads sensors continuously
- Controls actuators (LED, fan, servos, RGB)
- Prints events to serial

**Bridge (unified_bridge.py):**
- Monitors ESP32 serial output
- Logs events to database
- Publishes MQTT messages
- Sends responses to ESP32 (Task 7)

**Web Dashboard:**
- Displays real-time sensor data
- Shows alerts (gas, asthma)
- RFID access logs
- Updates via MQTT

---

## 🧪 Testing Individual Tasks

```bash
# Upload components
ampy --port COM4 put micropython/components

# Test Task 1 (LED)
ampy --port COM4 run micropython/task1_led_simple.py

# Test Task 2 (Temperature)
ampy --port COM4 run micropython/temperature_mqtt.py

# Test all tasks together
ampy --port COM4 put micropython/all_tasks.py
ampy --port COM4 put micropython/boot.py
# Reset ESP32
```

---

## 🔍 Troubleshooting

### ESP32 Not Auto-Starting
**Solution:** Check boot.py is uploaded
```bash
ampy --port COM4 put micropython/boot.py
# Reset ESP32
```

### Bridge Can't Connect
**Solution:**
1. Close other programs using COM4
2. Check ESP32 is plugged in
3. Verify port in Device Manager

### Web Dashboard Not Updating
**Solution:**
1. Make sure bridge is running
2. Check MQTT connection in browser console
3. Verify internet connection

### Database Logging Fails
**Solution:**
1. Check Supabase credentials in unified_bridge.py
2. Verify tables exist in Supabase
3. Test database connection

---

## 🎯 Key Concepts

### Why Bridge Pattern?
ESP32 can't directly connect to MQTT/Database due to network restrictions. The bridge runs on PC and acts as gateway:
- **Task 1:** No bridge (simple time-based)
- **Task 2:** Bridge for DB + MQTT
- **Task 3:** Bridge for DB + MQTT
- **Task 4:** No bridge (simple hardware control)
- **Task 5:** Bridge for DB + MQTT
- **Task 6:** Bridge for MQTT only
- **Task 7:** Bridge for DB + MQTT + auth response

### Component Organization (OOP)
All hardware abstracted into classes:
```python
from components import LED, DHT, PIR, RFID

led = LED()         # Auto-loads pin from config
dht = DHT()
pir = PIR()

led.on()
temp = dht.temperature()
if pir.motion_detected():
    print("Motion!")
```

---

## 📚 Documentation Files

### Essential (Keep These)
- **PROJECT_GUIDE.md** (this file) - Complete overview
- **PROJECT_STATUS.md** - Detailed current status
- **ARCHITECTURE.md** - System design
- **TASK_REQUIREMENTS.md** - Original requirements

### Reference (In docs/)
- **OOP_GUIDE.md** - Component classes usage
- **CONFIG_GUIDE.md** - Configuration explained
- **COMMANDS.md** - Common commands
- **TASK[X]_*.md** - Individual task details

---

## 🎓 What You'll Learn

- **IoT System Design** - Hardware to cloud architecture
- **Embedded Programming** - MicroPython on ESP32
- **Full-Stack Development** - Next.js + Supabase
- **Real-time Communication** - MQTT pub/sub
- **Hardware Interfacing** - GPIO, I2C, SPI, PWM
- **Database Design** - PostgreSQL schemas
- **System Integration** - Multiple technologies working together

---

## 📈 Project Stats

- **Total Tasks:** 7 of 7 (100%)
- **Hardware Components:** 15
- **Software Components:** 12 OOP classes
- **Database Tables:** 5
- **MQTT Topics:** 6
- **Web Pages:** 2 (Dashboard + RFID logs)
- **Lines of Code:** ~2000+

---

## 🎉 Project Complete!

All 7 tasks implemented and working. System ready for:
- Real-world deployment
- Further enhancements
- Portfolio showcase
- Learning platform

---

## 💡 Quick Commands

```bash
# Upload all code to ESP32
ampy --port COM4 put micropython/components
ampy --port COM4 put micropython/all_tasks.py
ampy --port COM4 put micropython/boot.py

# Start system
RUN.bat  # or: python unified_bridge.py

# Monitor ESP32
python -m serial.tools.miniterm COM4 115200

# Start web app manually
cd web-app
npm run dev
```

---

**For detailed task explanations, see individual TASK*.md files in docs/ folder.**
