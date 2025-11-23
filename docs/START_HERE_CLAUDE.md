# 👋 Start Here (For Claude After Context Clear)

**Last Updated:** 2025-11-23

When you clear context, read these files to understand the project quickly.

---

## 🚀 Quick Start (2 minutes)

### 1️⃣ **PROJECT_GUIDE.md** (MUST READ FIRST!)
**Location:** [docs/PROJECT_GUIDE.md](PROJECT_GUIDE.md)

**What:** Complete project overview - everything you need to know
**Contains:**
- Project status (100% complete, 8/8 tasks)
- Quick start guide
- All task descriptions
- Project structure
- Hardware components
- How the system works
- Common commands

**Why read:** This single file contains everything to understand the project

---

## 📚 Additional Context (Optional)

### 2️⃣ **PROJECT_STATUS.md** - Detailed Status
**Location:** [docs/PROJECT_STATUS.md](PROJECT_STATUS.md)

**What:** Detailed implementation status of each task
**Contains:**
- Task-by-task breakdown
- File locations
- Database schema
- MQTT topics
- Progress tracking

**Why read:** Deep dive into current implementation

---

### 3️⃣ **TASK_REQUIREMENTS.md** - Original Requirements
**Location:** [docs/TASK_REQUIREMENTS.md](TASK_REQUIREMENTS.md)

**What:** Original task requirements from the assignment
**Contains:**
- ESP32 requirements (what device should do)
- Web app requirements (what to display)
- Database requirements (what to log)

**Why read:** Understand the original specifications

---

### 4️⃣ **ARCHITECTURE.md** - System Design
**Location:** [docs/ARCHITECTURE.md](ARCHITECTURE.md)

**What:** System architecture and data flow
**Contains:**
- Complete system architecture
- Component relationships
- Pin connections
- MQTT topic structure
- Data flow examples

**Why read:** Understand how all parts communicate

---

## 🎯 What to Do After Reading

1. ✅ Read [PROJECT_GUIDE.md](PROJECT_GUIDE.md) - This covers everything!
2. ✅ Ask user what they need help with
3. ✅ Check relevant task documentation if needed (TASK[X]_*.md files)
4. ✅ Start working!

---

## 📊 Current Status Summary

### ✅ Completed: 8 of 8 tasks (100%)

**Task 1:** LED Auto (8pm-7am) - Simple, no MQTT/DB
**Task 2:** Temperature & Humidity - MQTT + DB + Web
**Task 3:** Motion Detection - MQTT + DB + Web (via bridge)
**Task 4:** Steam Detection - Simple, no MQTT/DB
**Task 5:** Gas Detection - MQTT + DB + Web (via bridge)
**Task 6:** Asthma Alert - MQTT + Web (no DB)
**Task 7:** RFID Access - MQTT + DB + Web (via bridge)
**Task 8:** Device Control - Web → MQTT → ESP32 (door, window, fan)

### 🏗️ System Architecture

```
ESP32 (15 hardware components)
    ↓ Serial USB
unified_bridge.py (Python on PC)
    ↓ HTTP + MQTT
Supabase (Database) + HiveMQ (MQTT Broker)
    ↓ API + WebSocket
Next.js Web Dashboard
    ↓ Browser
User
```

### 📁 File Organization

```
smart-house/
├── RUN.bat                    # ⭐ One-click launcher
├── unified_bridge.py          # Bridge script
├── README.md                  # Project overview
│
├── micropython/               # ESP32 code
│   ├── boot.py               # Auto-starts main.py
│   ├── main.py               # Tasks 1-8 combined
│   ├── config.py             # Configuration
│   ├── tasks/                # Task modules
│   └── components/           # OOP classes
│
├── web-app/                   # Next.js dashboard
│   ├── app/page.tsx          # Main dashboard
│   ├── app/rfid/page.tsx     # RFID logs
│   ├── app/controls/page.tsx # Device controls
│   └── components/           # React components
│
├── docs/                      # Documentation
│   ├── PROJECT_GUIDE.md      # ⭐ START HERE
│   ├── PROJECT_STATUS.md     # Detailed status
│   └── ...
│
└── database/                  # SQL schemas
    └── CLEAN_SCHEMA.sql      # 5 tables
```

---

## 💡 Key Concepts

### Bridge Pattern
ESP32 can't directly reach MQTT/Database due to network restrictions.
Solution: Python bridge on PC monitors serial output and handles cloud connectivity.

**Pattern:**
```
ESP32 → Serial → Bridge (PC) → Database + MQTT → Web Dashboard
```

### OOP Component Design
All hardware abstracted into classes:
```python
from components import LED, DHT, PIR, RFID
led = LED()  # Auto-loads pin from config
led.on()
```

### Auto-Start
ESP32 runs all tasks automatically on boot via boot.py

---

## 🔧 Common Commands

```bash
# Start everything (one-click)
RUN.bat

# Or start manually
python unified_bridge.py

# Upload code to ESP32
ampy --port COM5 put micropython/main.py
ampy --port COM5 put micropython/boot.py

# Monitor ESP32
python -m serial.tools.miniterm COM5 115200

# Start web dashboard
cd web-app
npm run dev
```

---

## ✅ Essential Files Checklist

After context clear, you should have:

**Root:**
- ✅ README.md - Project overview

**Docs:**
- ✅ PROJECT_GUIDE.md - **START HERE** (complete guide)
- ✅ PROJECT_STATUS.md - Detailed status
- ✅ TASK_REQUIREMENTS.md - Original requirements
- ✅ ARCHITECTURE.md - System design
- ✅ START_HERE_CLAUDE.md - This file

**Total:** 5 essential files (PROJECT_GUIDE.md is the most important!)

---

## 📝 Quick Reference

**Port:** COM5
**WiFi:** CyFi
**Database:** Supabase (5 tables)
**MQTT:** HiveMQ Cloud
**Web:** http://localhost:3000
**All Tasks:** Running on ESP32 via boot.py → main.py

---

**TL;DR: Read [PROJECT_GUIDE.md](PROJECT_GUIDE.md) - it has everything you need!** 🚀
