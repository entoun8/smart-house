# Task 2: Temperature & Humidity Logging - Complete Explanation

**Task:** Logs temperature and humidity every 30 minutes

**Solution:** MQTT (real-time) + Database (history)

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     TASK 2 FLOW                             │
└─────────────────────────────────────────────────────────────┘

ESP32                          MQTT Broker              Web App
  │                                 │                      │
  │ 1. Read DHT11 sensor            │                      │
  │    (every 30 minutes)           │                      │
  │                                 │                      │
  │ 2. Publish to MQTT              │                      │
  │────────────────────────────────>│                      │
  │    Topic: sensors/temperature   │                      │
  │    Message: "23.5"              │                      │
  │    Topic: sensors/humidity      │                      │
  │    Message: "41.2"              │                      │
  │                                 │                      │
  │                                 │ 3. Forward to Web    │
  │                                 │─────────────────────>│
  │                                 │                      │
  │ 4. Save to Database             │                      │ 5. Update UI
  │────────────────────────────────────────────────────────>│    instantly!
        (Supabase API)
```

---

## 🗂️ Files Involved

### 1️⃣ ESP32 Code (Hardware Control)
**File:** `micropython/temperature_mqtt.py`

### 2️⃣ Web App Components (Display)
**Files:**
- `web-app/components/features/dashboard/TemperatureStatus.tsx`
- `web-app/components/features/dashboard/HumidityStatus.tsx`

### 3️⃣ Database Functions
**File:** `micropython/database.py` (already has `log_temperature()` function)

---

# 📝 DETAILED LINE-BY-LINE EXPLANATION

---

## 1️⃣ ESP32 CODE: `temperature_mqtt.py`

### **Purpose:**
Read DHT11 sensor every 30 minutes, publish to MQTT, save to database

---

### **Lines 1-15: Import Libraries**

```python
import time
import ntptime
from components import DHT, WiFi, MQTT
from database import Database
from config import TOPICS

# Melbourne timezone offset (UTC+11)
MELBOURNE_OFFSET = 11 * 3600
```

**Why each line:**
- `import time` → Get current time, sleep
- `import ntptime` → Sync time with internet
- `from components import DHT, WiFi, MQTT` → Use OOP classes
- `from database import Database` → Save to Supabase
- `from config import TOPICS` → MQTT topic paths
- `MELBOURNE_OFFSET = 11 * 3600` → Convert UTC to Melbourne time

---

### **Lines 17-24: Initialize Components**

```python
# Initialize components
dht = DHT()
wifi = WiFi()
mqtt = MQTT()
db = Database()

# Logging interval: 30 minutes = 1800 seconds
LOG_INTERVAL = 1800  # 30 minutes

# Track last log time
last_log_time = 0
```

**Why:**
- `dht = DHT()` → Create DHT11 sensor object (auto-loads pin 17)
- `wifi = WiFi()` → Create WiFi object
- `mqtt = MQTT()` → Create MQTT object
- `db = Database()` → Create database object
- `LOG_INTERVAL = 1800` → 30 minutes in seconds
- `last_log_time = 0` → Track when we last logged (for 30-minute interval)

---

### **Lines 26-34: Time Sync Function**

```python
def sync_time():
    """Sync time with NTP server"""
    try:
        ntptime.settime()
        print("✅ Time synced!")
        return True
    except Exception as e:
        print(f"⚠️  Time sync failed: {e}")
        return False
```

**Why:**
- ESP32 doesn't know the time when it boots
- `ntptime.settime()` gets current UTC time from internet
- Needed for accurate timestamps and timing intervals

---

### **Lines 36-42: Get Time String**

```python
def get_time_str():
    """Get Melbourne time as string (HH:MM)"""
    utc = time.time()
    melbourne = utc + MELBOURNE_OFFSET
    t = time.localtime(int(melbourne))
    return f"{t[3]:02d}:{t[4]:02d}"
```

**Why:**
- Convert UTC time to Melbourne time
- Return formatted string for console messages
- Example: "14:30"

---

### **Lines 44-81: Read and Log Function** (CORE LOGIC!)

```python
def read_and_log():
    """Read DHT sensor and log to MQTT + Database"""
    global last_log_time

    print(f"\n[{get_time_str()}] Reading DHT sensor...")

    # Read sensor
    data = dht.read()

    if data:
        temp = data['temp']
        humidity = data['humidity']

        print(f"  Temperature: {temp}°C")
        print(f"  Humidity: {humidity}%")

        # 1. Publish to MQTT (real-time for web app)
        mqtt.publish(TOPICS.sensor("temperature"), str(temp))
        mqtt.publish(TOPICS.sensor("humidity"), str(humidity))
        print("  ✅ Published to MQTT")

        # 2. Save to database (history)
        success = db.log_temperature(temp, humidity)
        if success:
            print("  ✅ Saved to database")
        else:
            print("  ⚠️  Database save failed")

        # Update last log time
        last_log_time = time.time()

        return True
    else:
        print("  ⚠️  Failed to read sensor")
        return False
```

**Why line by line:**

**Line 46: `global last_log_time`**
- Need to modify global variable

**Lines 48-50: Read Sensor**
```python
print(f"\n[{get_time_str()}] Reading DHT sensor...")
data = dht.read()
```
- Print timestamp
- Read temperature and humidity from DHT11 sensor
- `data` is a dictionary: `{'temp': 23.5, 'humidity': 41.2}`

**Lines 52-56: Extract Data**
```python
if data:
    temp = data['temp']
    humidity = data['humidity']
    print(f"  Temperature: {temp}°C")
    print(f"  Humidity: {humidity}%")
```
- Check if sensor read was successful
- Extract temperature and humidity values
- Print to console for debugging

**Lines 59-61: Publish to MQTT**
```python
mqtt.publish(TOPICS.sensor("temperature"), str(temp))
mqtt.publish(TOPICS.sensor("humidity"), str(humidity))
print("  ✅ Published to MQTT")
```
- `TOPICS.sensor("temperature")` → Returns `"ks5009/house/sensors/temperature"`
- `TOPICS.sensor("humidity")` → Returns `"ks5009/house/sensors/humidity"`
- Publish temperature: `"23.5"`
- Publish humidity: `"41.2"`
- Web app receives these instantly!

**Lines 64-69: Save to Database**
```python
success = db.log_temperature(temp, humidity)
if success:
    print("  ✅ Saved to database")
else:
    print("  ⚠️  Database save failed")
```
- Call Supabase API
- `INSERT INTO temperature_logs (temp, humidity) VALUES (23.5, 41.2)`
- History preserved!

**Lines 72-74: Update Timer**
```python
last_log_time = time.time()
return True
```
- Remember when we logged
- So we wait 30 minutes before next log

---

### **Lines 83-88: Should Log Now Function**

```python
def should_log_now():
    """Check if it's time to log (every 30 minutes)"""
    if last_log_time == 0:
        return True  # First run

    elapsed = time.time() - last_log_time
    return elapsed >= LOG_INTERVAL
```

**Why:**
- `last_log_time == 0` → First run, log immediately
- `elapsed >= LOG_INTERVAL` → 30 minutes have passed
- Returns `True` or `False`

**Example:**
- 14:00 → Log (first time)
- 14:10 → Don't log (only 10 minutes passed)
- 14:30 → Log (30 minutes passed)

---

### **Lines 95-114: Main Program**

```python
print("=" * 50)
print("TEMPERATURE & HUMIDITY LOGGING - TASK 2")
print("=" * 50)

# Connect WiFi
print("\n🌐 Connecting to WiFi...")
wifi.connect()

# Connect MQTT
print("📡 Connecting to MQTT...")
mqtt.connect()

# Sync time
print("⏰ Syncing time...")
sync_time()

print(f"\n📊 Current time: {get_time_str()}")
print(f"📅 Logging interval: {LOG_INTERVAL // 60} minutes")
print("=" * 50)

# Do initial reading immediately
print("\n🚀 Starting initial reading...")
read_and_log()

print("\n✅ Setup complete! Logging every 30 minutes...")
print("=" * 50)
```

**Why:**
- Print banner
- Connect to WiFi (needed for MQTT and database)
- Connect to MQTT broker
- Sync time with internet
- Print current time and interval
- Do initial reading immediately (don't wait 30 minutes!)
- Show ready message

---

### **Lines 117-131: Main Loop**

```python
while True:
    try:
        # Check if it's time to log
        if should_log_now():
            read_and_log()

        # Check for MQTT messages (for future commands)
        mqtt.check_messages()

        # Sleep for 1 minute before checking again
        time.sleep(60)

    except KeyboardInterrupt:
        print("\n\n🛑 Stopping temperature logger...")
        mqtt.disconnect()
        break
    except Exception as e:
        print(f"\n❌ Error: {e}")
        time.sleep(60)  # Wait before retrying
```

**Why line by line:**

**Line 117: `while True:`**
- Run forever

**Line 119-120: Check Time**
```python
if should_log_now():
    read_and_log()
```
- Every minute, check if 30 minutes have passed
- If yes, read sensor and log

**Line 123: Check Messages**
```python
mqtt.check_messages()
```
- Check for commands from web app (future feature)

**Line 126: Sleep**
```python
time.sleep(60)
```
- Wait 1 minute before checking again
- Saves CPU power

**Lines 128-131: Error Handling**
```python
except KeyboardInterrupt:
    mqtt.disconnect()
    break
except Exception as e:
    print(f"\n❌ Error: {e}")
    time.sleep(60)
```
- Ctrl+C: Disconnect cleanly
- Any error: Print and retry after 1 minute

---

## 2️⃣ WEB APP COMPONENT: `TemperatureStatus.tsx`

### **Purpose:**
Display current temperature in real-time using MQTT

---

### **Lines 1-14: Imports**

```tsx
"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { connectMQTT, TOPICS, subscribe } from "@/lib/mqtt";
import { Thermometer } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
```

**Why:**
- `"use client"` → Next.js: runs in browser
- `useEffect, useState` → React hooks
- `supabase` → Fetch from database
- `connectMQTT, subscribe` → Real-time updates
- `Thermometer` → Icon for temperature
- `Card, Badge` → UI components

---

### **Lines 16-18: State Variables**

```tsx
export default function TemperatureStatus() {
  const [temperature, setTemperature] = useState<number | null>(null);
  const [lastUpdate, setLastUpdate] = useState<string>("");
```

**Why:**
- `temperature` → Current temp (null if unknown)
- `lastUpdate` → Time of last update

---

### **Lines 20-47: Connect to MQTT and Database**

```tsx
useEffect(() => {
  // Connect to MQTT
  connectMQTT();

  // Subscribe to temperature topic (real-time updates from ESP32)
  subscribe(TOPICS.temperature, (message) => {
    const temp = parseFloat(message);
    setTemperature(temp);
    setLastUpdate(new Date().toLocaleTimeString());
    console.log("Temperature from MQTT:", temp);
  });

  // Fetch initial temperature from database (in case ESP32 is offline)
  const fetchInitialTemperature = async () => {
    const { data } = await supabase
      .from("temperature_logs")
      .select("temp, timestamp")
      .order("timestamp", { ascending: false })
      .limit(1);

    if (data && data.length > 0) {
      setTemperature(data[0].temp);
      setLastUpdate(new Date(data[0].timestamp).toLocaleTimeString());
    }
  };

  fetchInitialTemperature();
}, []);
```

**Why:**

**Lines 22-30: MQTT Subscription**
```tsx
subscribe(TOPICS.temperature, (message) => {
  const temp = parseFloat(message);
  setTemperature(temp);
  setLastUpdate(new Date().toLocaleTimeString());
});
```
- Subscribe to `ks5009/house/sensors/temperature`
- When ESP32 publishes → callback runs
- `message` → "23.5" (string)
- `parseFloat(message)` → 23.5 (number)
- Update state → UI re-renders

**Lines 33-45: Database Fallback**
```tsx
const fetchInitialTemperature = async () => {
  const { data } = await supabase
    .from("temperature_logs")
    .select("temp, timestamp")
    .order("timestamp", { ascending: false })
    .limit(1);

  if (data && data.length > 0) {
    setTemperature(data[0].temp);
    setLastUpdate(...);
  }
};
fetchInitialTemperature();
```
- Query Supabase for latest temperature
- If ESP32 offline, show last known value

---

### **Lines 50-58: Temperature Status Logic**

```tsx
const getTempStatus = () => {
  if (temperature === null) return { color: "secondary", label: "Unknown" };
  if (temperature < 18) return { color: "default", label: "Cold" };
  if (temperature <= 25) return { color: "default", label: "Comfortable" };
  if (temperature <= 30) return { color: "default", label: "Warm" };
  return { color: "destructive", label: "Hot" };
};

const status = getTempStatus();
```

**Why:**
- Determine status badge based on temperature
- < 18°C → Cold
- 18-25°C → Comfortable
- 26-30°C → Warm
- > 30°C → Hot (red badge)

---

### **Lines 62-92: Render UI**

```tsx
return (
  <Card className="hover:shadow-lg transition-all">
    <CardHeader>
      <CardTitle className="flex items-center gap-3">
        <Thermometer
          className={`w-6 h-6 ${
            temperature !== null && temperature > 27
              ? "text-red-500"
              : "text-blue-500"
          }`}
        />
        Temperature
      </CardTitle>
      <CardDescription>Current temperature in celsius</CardDescription>
    </CardHeader>
    <CardContent>
      <div className="space-y-3">
        <p className="text-4xl font-bold">
          {temperature !== null ? `${temperature}°C` : "--"}
        </p>
        {temperature !== null && (
          <Badge variant={status.color as any}>
            {status.label}
          </Badge>
        )}
        {lastUpdate && (
          <p className="text-sm text-muted-foreground">
            Last update: {lastUpdate}
          </p>
        )}
      </div>
    </CardContent>
  </Card>
);
```

**Why:**

**Lines 66-72: Dynamic Icon**
```tsx
<Thermometer
  className={temperature > 27 ? "text-red-500" : "text-blue-500"}
/>
```
- If temp > 27°C → Red icon (hot)
- Otherwise → Blue icon (cool)

**Lines 79-81: Display Temperature**
```tsx
{temperature !== null ? `${temperature}°C` : "--"}
```
- Show temperature or "--" if unknown

**Lines 82-86: Status Badge**
```tsx
{temperature !== null && (
  <Badge variant={status.color}>
    {status.label}
  </Badge>
)}
```
- Show badge: "Cold", "Comfortable", "Warm", or "Hot"

---

## 3️⃣ WEB APP COMPONENT: `HumidityStatus.tsx`

### **Similar to TemperatureStatus, but for humidity**

**Key differences:**
- Subscribes to `TOPICS.humidity` instead of `TOPICS.temperature`
- Uses Droplets icon instead of Thermometer
- Status levels:
  - < 30% → Dry
  - 30-60% → Comfortable
  - > 60% → High

---

## 🔄 COMPLETE FLOW (Putting It All Together)

### **Scenario: ESP32 Reads Sensor at 14:00**

#### **Step 1: ESP32 Checks Time**
```python
# Every minute, check if 30 minutes passed
if should_log_now():  # True (30 minutes since last log)
    read_and_log()
```

#### **Step 2: ESP32 Reads DHT11**
```python
data = dht.read()
# Returns: {'temp': 23.5, 'humidity': 41.2}
temp = 23.5
humidity = 41.2
```

#### **Step 3: ESP32 Publishes to MQTT**
```python
mqtt.publish("ks5009/house/sensors/temperature", "23.5")
mqtt.publish("ks5009/house/sensors/humidity", "41.2")
```

**What happens:**
1. ESP32 sends messages to HiveMQ broker
2. Messages sent over WiFi/Internet
3. Broker stores messages (retain=true)

#### **Step 4: ESP32 Saves to Database**
```python
db.log_temperature(23.5, 41.2)
# Calls Supabase API
# INSERT INTO temperature_logs (temp, humidity) VALUES (23.5, 41.2)
```

#### **Step 5: HiveMQ Forwards to Web App**
```typescript
// TemperatureStatus.tsx
subscribe(TOPICS.temperature, (message) => {
  setTemperature(parseFloat(message));  // message = "23.5"
});

// HumidityStatus.tsx
subscribe(TOPICS.humidity, (message) => {
  setHumidity(parseFloat(message));  // message = "41.2"
});
```

**What happens:**
1. Web app is subscribed to both topics
2. HiveMQ sends "23.5" and "41.2" to web app via WebSocket
3. Callbacks run
4. State updates → React re-renders

#### **Step 6: Web App Updates UI**
```tsx
// TemperatureStatus
<p className="text-4xl font-bold">23.5°C</p>
<Badge>Comfortable</Badge>

// HumidityStatus
<p className="text-4xl font-bold">41.2%</p>
<Badge>Comfortable</Badge>
```

**User sees:**
```
┌─────────────────────────┐  ┌─────────────────────────┐
│ 🌡️ Temperature          │  │ 💧 Humidity             │
│ Current temperature     │  │ Current humidity        │
│                         │  │                         │
│ 23.5°C                  │  │ 41.2%                   │
│ ✓ Comfortable           │  │ ✓ Comfortable           │
│ Last update: 2:00:23 PM │  │ Last update: 2:00:23 PM │
└─────────────────────────┘  └─────────────────────────┘
```

---

## ⏰ Timeline Example

**14:00:00:**
- ESP32: "30 minutes passed, time to log!"
- ESP32: Read sensor → 23.5°C, 41.2%
- ESP32: Publish to MQTT
- ESP32: Save to database
- Web App: Receive MQTT messages
- Web App: Update UI
- **Total time:** ~200 milliseconds

**14:30:00:**
- ESP32: "30 minutes passed, time to log!"
- ESP32: Read sensor → 24.0°C, 43.5%
- (Repeat process)

**14:15:00:**
- ESP32: "Only 15 minutes passed, don't log"
- ESP32: Sleep 1 minute, check again

---

## 📊 Data Storage

### **Database Table: `temperature_logs`**

| id | temp | humidity | timestamp           |
|----|------|----------|---------------------|
| 1  | 23.5 | 41.2     | 2025-01-14 14:00:00 |
| 2  | 24.0 | 43.5     | 2025-01-14 14:30:00 |
| 3  | 22.8 | 39.7     | 2025-01-14 15:00:00 |

**Used for:**
- History charts
- Analytics (average temp per day)
- Fallback if ESP32 offline

### **MQTT Messages (Not Stored)**

```
Topic: ks5009/house/sensors/temperature
Message: "23.5"
Retained: Yes

Topic: ks5009/house/sensors/humidity
Message: "41.2"
Retained: Yes
```

**Used for:**
- Real-time updates
- Live dashboard
- Instant feedback

---

## 🎯 Key Differences from Task 1

| Aspect | Task 1 (LED) | Task 2 (Temperature) |
|--------|-------------|----------------------|
| **Trigger** | Time-based (8pm-7am) | Interval-based (every 30 min) |
| **Hardware** | LED (GPIO output) | DHT11 sensor (GPIO input) |
| **Data** | State ("on"/"off") | Readings (23.5°C, 41.2%) |
| **MQTT Topics** | 1 topic (led/state) | 2 topics (temperature, humidity) |
| **Web Components** | 1 component | 2 components |
| **Logic** | Simple on/off | Read, parse, validate |

---

## 🔍 Debugging Tips

### **Temperature shows "--"?**
1. Check ESP32 console: Should see "Reading DHT sensor..."
2. Check sensor reading: Should show temperature value
3. Check MQTT publish: Should see "✅ Published to MQTT"

### **Web app not updating?**
1. Check browser console (F12)
2. Should see: `Subscribed to ks5009/house/sensors/temperature`
3. Should see: `Temperature from MQTT: 23.5`

### **Sensor read fails?**
1. Check wiring: DHT11 connected to GPIO 17
2. Check power: DHT11 needs 3.3V
3. Wait a few seconds between reads

---

## 📝 Summary

**ESP32 Code:**
1. Every 30 minutes, read DHT11 sensor
2. Extract temperature and humidity
3. Publish to MQTT (2 separate topics)
4. Save to database (1 row with both values)
5. Wait 30 minutes, repeat

**Web App:**
1. Connect to MQTT broker
2. Subscribe to temperature and humidity topics
3. When messages received → update UI
4. Fetch from database as fallback
5. Show status badges based on values

**Result:**
- Temperature logged every 30 minutes ✅
- Humidity logged every 30 minutes ✅
- Web app shows real-time values ✅
- History saved in database ✅
- Everything simple and clean! ✅

---

## 🎉 Task 2 Complete!

**Next tasks:**
- Task 3: Motion detection → RGB orange + log
- Task 4: Steam detection → Close window + RGB blue
- Task 5: Gas detection → Fan + RGB red + log
- Task 6: Asthma alert → LCD display
- Task 7: RFID access control

Follow the same pattern for all tasks! 🚀
