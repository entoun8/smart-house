# Task 4: Steam Detection - Implementation Guide

**⚠️ OUTDATED:** This document describes the over-implemented version with database/MQTT.
**✅ See [TASK4_SIMPLIFIED.md](TASK4_SIMPLIFIED.md) for the correct, simplified version.**

**Status:** ❌ OUTDATED (Use TASK4_SIMPLIFIED.md instead)
**Date:** 2025-11-17

---

## 📋 Requirements

### ESP32 Requirements:
- ✅ Detect moisture with water/steam sensor
- ✅ Close window when steam detected
- ✅ Flash RGB blue when steam detected

### Web Dashboard:
- ✅ Display steam detections in last hour
- ✅ Real-time updates via MQTT

### Database:
- ✅ Log all steam detection events with timestamp

---

## 🗂️ Files Created/Modified

### ESP32 Code:
- **`micropython/task4_steam_detection.py`** - Standalone Task 4 code
- **`micropython/all_tasks.py`** - Updated to include Task 4
- **`micropython/boot.py`** - Updated to show Task 4

### Bridge:
- **`unified_bridge.py`** - Added Task 4 handling (steam detection logging)

### Web App:
- **`web-app/components/features/dashboard/SteamStatus.tsx`** - New component
- **`web-app/components/features/dashboard/DashboardContent.tsx`** - Added SteamStatus
- **`web-app/lib/mqtt.ts`** - Added steam topic

### Database:
- **`database/add_steam_logs.sql`** - SQL migration to create steam_logs table

---

## 🚀 How It Works

### Architecture:

```
┌─────────────┐
│   ESP32     │ 1. Water sensor detects moisture
│  (Task 4)   │ 2. Window closes
└──────┬──────┘ 3. RGB → Blue
       │        4. Serial: "Steam detected!"
       │
       │ Serial (COM5)
       ▼
┌─────────────────────────┐
│  Bridge (PC)            │
│  unified_bridge.py      │ 5. Reads serial
├─────────────────────────┤ 6. Logs to database
│  • Database logging ✅  │ 7. Publishes MQTT
│  • MQTT publishing ✅   │
└────┬───────────┬────────┘
     │           │
     ▼           ▼
┌──────────┐  ┌──────────┐
│ Supabase │  │   MQTT   │
│ Database │  │  Broker  │
│ ✅ Logs  │  │ ✅ Pub   │
└──────────┘  └─────┬────┘
                    │
                    ▼
              ┌──────────────┐
              │ Web Dashboard│
              │ ✅ Updates   │
              └──────────────┘
```

---

## 🔧 Setup Instructions

### 1. Create Database Table

Run this SQL in Supabase:
```sql
-- File: database/add_steam_logs.sql
CREATE TABLE steam_logs (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_steam_timestamp ON steam_logs(timestamp DESC);
```

### 2. Upload Code to ESP32

```bash
# Upload updated all_tasks.py
ampy --port COM5 put micropython/all_tasks.py

# Upload updated boot.py
ampy --port COM5 put micropython/boot.py

# (Optional) Upload standalone task4 file
ampy --port COM5 put micropython/task4_steam_detection.py
```

### 3. Start the System

```bash
# Option 1: Use the unified launcher (runs all tasks)
double-click RUN.bat

# Option 2: Start bridge manually
python unified_bridge.py
```

---

## 📊 MQTT Topics

- **Steam Detection:** `ks5009/house/events/steam_detected`
  - Payload: `"1"` when steam detected

---

## 🧪 Testing

### Test Steam Detection:

1. Start unified bridge: `python unified_bridge.py`
2. Touch water sensor with wet finger
3. Observe:
   - 🪟 Window servo closes
   - 🔵 RGB LED turns blue
   - 📺 Bridge shows: `[TASK 4] Steam Detected!`
   - 💾 Database logs the event
   - 🌐 Web dashboard updates

---

## 💻 Code Overview

### ESP32 (all_tasks.py):

```python
# Task 4 initialization
water = WaterSensor()
window = WindowServo()
previous_steam = False

# Main loop
while True:
    steam = water.is_wet()

    if steam and not previous_steam:
        print("💧 Steam detected!")
        window.close()
        rgb.blue()

    elif not steam and previous_steam:
        rgb.off()

    previous_steam = steam
```

### Bridge (unified_bridge.py):

```python
# Detect steam in serial output
if "Steam detected" in line:
    steam_count += 1
    print(f"[TASK 4] Steam Detected! (#{steam_count})")
    log_steam_to_database()
    publish_steam_mqtt()
```

### Web Component (SteamStatus.tsx):

```tsx
export default function SteamStatus() {
  const [steamCount, setSteamCount] = useState(0);

  // Subscribe to MQTT
  client.subscribe(TOPICS.steam);

  // Update on message
  client.on("message", (topic, message) => {
    if (topic === TOPICS.steam) {
      setSteamCount(prev => prev + 1);
    }
  });
}
```

---

## 🎯 Success Criteria

- ✅ Water sensor detects moisture
- ✅ Window closes automatically
- ✅ RGB LED flashes blue
- ✅ Event logged to database
- ✅ MQTT published to broker
- ✅ Web dashboard updates in real-time
- ✅ Auto-starts on ESP32 boot

---

## 📝 Notes

- Task 4 follows the same pattern as Task 3
- Bridge pattern is used for database/MQTT (network restrictions)
- ESP32 runs all tasks simultaneously (Task 2, 3, 4)
- Simple implementation - just what's required!

---

## 🔄 Next Tasks

- Task 5: Gas detection → Fan + RGB red + logging
- Task 6: Asthma alert → LCD display
- Task 7: RFID access control → Door + logging

**Pattern established! Copy Task 4 for future tasks.**
