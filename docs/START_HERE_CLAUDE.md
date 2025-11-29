# Start Here (For Claude)

**Last Updated:** 2025-11-29

Read these files to understand the project quickly.

## Quick Start

### 1. PROJECT_GUIDE.md (Read First)
Complete project overview - everything you need to know.

### 2. PROJECT_STATUS.md
Detailed implementation status of each task.

### 3. ARCHITECTURE.md
System architecture and data flow.

## Current Status

**Completion: 8/8 tasks (100%)**

- Task 1: LED Auto (8pm-7am)
- Task 2: Temperature & Humidity (every 15 min)
- Task 3: Motion Detection
- Task 4: Steam Detection
- Task 5: Gas Detection
- Task 6: Asthma Alert
- Task 7: RFID Access
- Task 8: Device Control (Web → ESP32)

## System Architecture

```
ESP32 (15 hardware components)
    ↓ WiFi/MQTT (Direct connection)
HiveMQ Cloud (MQTT Broker)
    ↓ WebSocket
Next.js Web Dashboard
    ↓ HTTP
Supabase (Database)
```

**Key:** No Python bridge - ESP32 connects directly to cloud services.

## File Organization

```
smart-house/
├── micropython/           ESP32 code
│   ├── main.py           All tasks combined
│   ├── config.py         Pin & WiFi config
│   ├── tasks/            Task modules
│   └── components/       Hardware classes
│
├── web-app/              Next.js dashboard
│   ├── app/(main)/       3 pages (dashboard, rfid, controls)
│   ├── components/       React components
│   └── lib/              MQTT + Supabase clients
│
├── database/
│   └── schema.sql        5 tables
│
└── docs/
    ├── PROJECT_GUIDE.md
    ├── PROJECT_STATUS.md
    ├── ARCHITECTURE.md
    └── TASK_REQUIREMENTS.md
```

## Key Concepts

### Direct ESP32-to-Cloud
No Python bridge. ESP32 connects to MQTT broker via WiFi. Web app logs to database.

### OOP Component Design
All hardware abstracted into classes in `components/` folder.

### Auto-Start
ESP32 runs all tasks automatically via main.py on boot.

## Common Commands

```bash
# Upload to ESP32
ampy --port COM5 put micropython/main.py
ampy --port COM5 put micropython/config.py
ampy --port COM5 put micropython/components
ampy --port COM5 put micropython/tasks

# Monitor ESP32
python -m serial.tools.miniterm COM5 115200

# Start web dashboard
cd web-app
npm run dev
```

## Quick Reference

- **Port:** COM5
- **WiFi:** Telstra099B26
- **MQTT:** HiveMQ Cloud (TLS, port 8883)
- **Database:** Supabase (5 tables)
- **Web:** http://localhost:3000
- **RFID Card:** 0x7cdab502
