# Smart Home IoT Project

ESP32-based smart home system with MicroPython, Next.js, Supabase, and MQTT.

## 🚀 Quick Start

### Status: 100% Complete (7/7 tasks) 🎉

```bash
# 1. Plug in ESP32 to USB
# 2. Double-click: RUN.bat
# 3. Open: http://localhost:3000
```

That's it! Everything starts automatically.

---

## ✅ What's Implemented

- ✅ **Task 1:** LED Auto Control (8pm-7am)
- ✅ **Task 2:** Temperature & Humidity Logging (MQTT + DB + Web)
- ✅ **Task 3:** PIR Motion Detection (MQTT + DB + Web)
- ✅ **Task 4:** Steam Detection (Auto-close window + RGB blue)
- ✅ **Task 5:** Gas Detection (Fan + RGB red + MQTT + DB + Web)
- ✅ **Task 6:** Asthma Alert (LCD + Web via MQTT)
- ✅ **Task 7:** RFID Access Control (DB + MQTT + Web)

---

## 📚 Documentation

**👉 Start Here:** [docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md) - Complete project guide

### Essential Docs
- **[PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md)** - Complete overview (READ THIS FIRST!)
- **[PROJECT_STATUS.md](docs/PROJECT_STATUS.md)** - Current implementation status
- **[QUICK_START.md](docs/QUICK_START.md)** - How to run the system
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture
- **[TASK_REQUIREMENTS.md](docs/TASK_REQUIREMENTS.md)** - Original requirements

### Reference Guides
- **[OOP_GUIDE.md](docs/OOP_GUIDE.md)** - How to use component classes
- **[CONFIG_GUIDE.md](docs/CONFIG_GUIDE.md)** - Understanding config.py
- **[COMMANDS.md](docs/COMMANDS.md)** - Common commands
- **[UNIFIED_BRIDGE_GUIDE.md](docs/UNIFIED_BRIDGE_GUIDE.md)** - Bridge script explained

---

## 🗂️ Project Structure

```
smart-house/
├── RUN.bat                     # ⭐ ONE-CLICK LAUNCHER
├── unified_bridge.py           # Bridge for ESP32 ↔ Cloud
├── README.md                   # This file
│
├── micropython/                # ESP32 code
│   ├── boot.py                # Auto-starts all tasks
│   ├── all_tasks.py           # Tasks 1-7 combined
│   ├── config.py              # Configuration
│   └── components/            # OOP component classes
│
├── web-app/                    # Next.js dashboard
│   ├── app/                   # Pages
│   ├── components/            # React components
│   └── lib/                   # MQTT + Supabase clients
│
├── docs/                       # Documentation
├── database/                   # SQL schemas
└── tests/                      # Hardware tests
```

---

## 🔧 Hardware Components

| Component | Pin | Tasks |
|-----------|-----|-------|
| Yellow LED | GPIO 12 | Task 1 |
| RGB LEDs (4x) | GPIO 26 | Tasks 3,4,5,7 |
| Buzzer | GPIO 25 | Task 7 |
| PIR Sensor | GPIO 14 | Task 3 |
| DHT11 | GPIO 17 | Tasks 2,6 |
| Gas Sensor | GPIO 23 | Task 5 |
| Water Sensor | GPIO 34 | Task 4 |
| Fan Motor | GPIO 18, 19 | Task 5 |
| Door Servo | GPIO 13 | Task 7 |
| Window Servo | GPIO 5 | Task 4 |
| LCD1602 | I2C (22, 21) | Task 6 |
| RFID RC522 | SPI | Task 7 |

---

## 💻 Tech Stack

- **Hardware:** ESP32 (Keystudio KS5009)
- **Firmware:** MicroPython 1.24.0
- **Backend:** Supabase (PostgreSQL)
- **Frontend:** Next.js 14 (React)
- **Communication:** MQTT (HiveMQ)
- **Bridge:** Python (Serial + HTTP + MQTT)

---

## 🎯 Component Usage Example

```python
from components import LED, DHT, PIR, RFID

# Initialize (auto-loads pins from config)
led = LED()
dht = DHT()
pir = PIR()

# Use them
led.on()
temp = dht.temperature()
if pir.motion_detected():
    print("Motion detected!")
```

---

## 📖 Quick Commands

```bash
# Upload all code to ESP32
ampy --port COM4 put micropython/components
ampy --port COM4 put micropython/all_tasks.py
ampy --port COM4 put micropython/boot.py

# Start system (one-click)
RUN.bat

# Or start manually
python unified_bridge.py

# Monitor ESP32
python -m serial.tools.miniterm COM4 115200

# Start web dashboard manually
cd web-app
npm run dev
```

---

## 🎓 What You'll Learn

- **IoT System Design** - Full-stack architecture
- **Embedded Programming** - MicroPython on ESP32
- **Hardware Interfacing** - GPIO, I2C, SPI, PWM
- **Real-time Communication** - MQTT pub/sub
- **Full-Stack Development** - Next.js + Supabase
- **Database Design** - PostgreSQL schemas
- **System Integration** - Multiple technologies working together

---

## 📞 Project Info

- **Board:** Keystudio KS5009 (ESP32)
- **Port:** COM4
- **WiFi:** CyFi
- **MicroPython:** v1.24.0
- **Database:** Supabase
- **MQTT Broker:** HiveMQ Cloud

---

## 🎉 Project Complete!

All 7 tasks implemented and fully functional. System includes:
- ✅ ESP32 with 15 hardware components
- ✅ 12 OOP component classes
- ✅ Python bridge for cloud connectivity
- ✅ Next.js web dashboard with real-time updates
- ✅ Supabase database with 5 tables
- ✅ MQTT messaging system
- ✅ Auto-start functionality
- ✅ Comprehensive documentation

**For complete details, see [docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md)**
