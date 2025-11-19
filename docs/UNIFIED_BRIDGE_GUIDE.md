# 🌉 Unified Bridge Guide - All Tasks

## 📋 What is the Unified Bridge?

The **unified_bridge.py** script monitors your ESP32's serial output and handles database logging + MQTT publishing for tasks that need it.

### Why Do We Need a Bridge?

Your ESP32 **cannot directly connect** to MQTT broker or database due to network restrictions. The bridge script runs on your PC and acts as a relay:

```
ESP32 → Serial (USB) → Bridge (PC) → Database + MQTT → Web Dashboard
```

---

## ✅ Tasks Handled by Unified Bridge

| Task | Bridge Function | Database | MQTT |
|------|----------------|----------|------|
| **Task 1** | ❌ No bridge | No | No |
| **Task 2** | ✅ Temperature | Yes | Yes |
| **Task 3** | ✅ Motion | Yes | Yes |
| **Task 4** | ❌ No bridge | No | No |
| **Task 5** | ✅ Gas | Yes | Yes |
| **Task 6** | ✅ Asthma Alert | **No** | Yes |

### Task Breakdown:

**Task 1 (LED):** Simple time-based, no connectivity needed
**Task 2 (Temperature):** Logs every 30 min to database + MQTT
**Task 3 (Motion):** Logs each detection to database + MQTT
**Task 4 (Steam):** Simple hardware control, no connectivity
**Task 5 (Gas):** Logs each detection to database + MQTT
**Task 6 (Asthma):** MQTT only (no database logging required!)

---

## 🚀 How to Use the Unified Bridge

### Step 1: Start ESP32
Press **RESET** button on ESP32 or power it on. All tasks start automatically via boot.py.

### Step 2: Start Unified Bridge
```bash
python unified_bridge.py
```

### What You'll See:
```
============================================================
Smart House - Unified Bridge (Tasks 2, 3, 5, 6)
============================================================

Connecting to ESP32 on COM4...
[OK] Connected to ESP32!

Monitoring ESP32 for database logging tasks...
============================================================

Active Tasks:
  - Task 2: Temperature & Humidity (every 30 min)
  - Task 3: Motion Detection (on motion)
  - Task 5: Gas Detection (on gas detected)
  - Task 6: Asthma Alert (MQTT only, no DB)
============================================================

[ESP32] Setup complete! All tasks monitoring...
[ESP32] Reading DHT sensor...
[ESP32] Temperature: 17°C
[ESP32] Humidity: 63%

[TASK 2] Temperature Reading! (#1)
  Temperature: 17.0°C
  Humidity: 63.0%
  [DB] Temperature logged! (17°C, 63%)
  [MQTT] Temperature published!
============================================================
```

---

## 📡 What the Bridge Detects

### Task 2: Temperature & Humidity
**Detects:**
```
Temperature: 17°C
Humidity: 63%
```
**Actions:**
- ✅ Logs to `temperature_logs` table
- ✅ Publishes MQTT: `ks5009/house/sensors/temperature`
- ✅ Publishes MQTT: `ks5009/house/sensors/humidity`

---

### Task 3: Motion Detection
**Detects:**
```
Motion detected!
```
**Actions:**
- ✅ Logs to `motion_logs` table
- ✅ Publishes MQTT: `ks5009/house/events/motion_detected`

---

### Task 5: Gas Detection
**Detects:**
```
Gas detected!
Gas cleared!
```
**Actions:**
- ✅ Logs to `gas_logs` table (on "detected" only)
- ✅ Publishes MQTT: `ks5009/house/events/gas_detected` = "1"
- ✅ Publishes MQTT: `ks5009/house/events/gas_detected` = "0" (cleared)

---

### Task 6: Asthma Alert ⭐ NEW!
**Detects:**
```
⚠️  ASTHMA ALERT!
✅ Asthma alert cleared
```
**Actions:**
- ❌ **NO database logging** (not required)
- ✅ Publishes MQTT: `ks5009/house/events/asthma_alert` = "1"
- ✅ Publishes MQTT: `ks5009/house/events/asthma_alert` = "0" (cleared)

**Why no database?**
The requirements only say "Show alert on LCD" and "Display on web dashboard". No database logging is mentioned, so we kept it simple!

---

## 🎯 Complete System Flow

### Example: Asthma Alert Triggered

```
1. ESP32 reads DHT sensor
   ├─ Temperature: 28°C
   └─ Humidity: 55%

2. Conditions check: H>50% AND T>27°C → TRUE ✅

3. ESP32 actions:
   ├─ LCD displays: "! ASTHMA ALERT !"
   └─ Prints to serial: "⚠️  ASTHMA ALERT!"

4. Bridge detects serial message

5. Bridge actions:
   └─ Publishes MQTT: asthma_alert = "1"

6. Web dashboard:
   └─ Receives MQTT
   └─ Shows red alert card 🚨
```

---

## 🛠️ Requirements

### Python Packages:
```bash
pip install pyserial paho-mqtt requests
```

### Node.js (for MQTT):
The bridge uses Node.js to publish MQTT messages. Make sure you have Node.js installed and `mqtt` package in your web-app:

```bash
cd web-app
npm install
```

---

## 📊 Session Statistics

When you stop the bridge (Ctrl+C), you'll see:

```
[STOPPED] Bridge stopped by user

Session Statistics:
  - Motion detections: 5
  - Temperature readings: 2
  - Gas detections: 1
  - Asthma alerts: 3

Goodbye!
```

---

## 🔍 Troubleshooting

### Bridge Can't Connect to ESP32
**Error:** `Failed to connect to ESP32`

**Solutions:**
1. Check ESP32 is plugged in USB
2. Verify COM port (should be COM4)
3. Close any other programs using COM4 (Arduino IDE, serial monitor, etc.)
4. Reset ESP32 and try again

---

### MQTT Publish Fails
**Error:** `[WARN] MQTT timeout`

**Solutions:**
1. Check internet connection
2. Verify web-app folder exists with node_modules
3. Test MQTT manually:
   ```bash
   cd web-app
   node -e "const mqtt = require('mqtt'); console.log('MQTT loaded!');"
   ```

---

### Database Logging Fails
**Error:** `[WARN] DB failed (Status: 401)`

**Solutions:**
1. Check Supabase URL and API key in `unified_bridge.py`
2. Verify tables exist in Supabase:
   - `temperature_logs`
   - `motion_logs`
   - `gas_logs`
3. Check Supabase is online

---

### Bridge Doesn't Detect Messages
**Problem:** ESP32 sends messages but bridge doesn't react

**Solutions:**
1. Check ESP32 is running all_tasks.py (press RESET)
2. Verify serial output format matches what bridge expects
3. Add debug:
   ```python
   print(f"[DEBUG] Line: {line}")  # Add after line 260
   ```

---

## 🎯 Summary

### What You Need:

1. ✅ **ESP32 running** (all_tasks.py via boot.py)
2. ✅ **unified_bridge.py running** (on PC)
3. ✅ **Web app running** (optional, for dashboard)

### What It Does:

- **Monitors** ESP32 serial output
- **Logs** to database (Tasks 2, 3, 5 only)
- **Publishes** MQTT (Tasks 2, 3, 5, 6)
- **Updates** web dashboard in real-time

### Task 6 Specific:

- ✅ Detects asthma alerts from serial
- ✅ Publishes to MQTT for web dashboard
- ❌ **No database logging** (kept simple!)

---

## 📝 Quick Start Commands

```bash
# Terminal 1: Start unified bridge
python unified_bridge.py

# Terminal 2: Start web dashboard (optional)
cd web-app
npm run dev

# Terminal 3: Monitor ESP32 directly (optional)
python -m serial.tools.miniterm COM4 115200
```

---

**Bridge Status:** ✅ Updated with Task 6 support!
**Tasks Covered:** 2, 3, 5, 6
**Last Updated:** 2025-11-17
