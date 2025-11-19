# 📚 Task 6: Asthma Alert - Complete Detailed Explanation

**Last Updated:** 2025-11-17
**Status:** ✅ 100% Complete

---

## 🎯 What is Task 6?

**Simple Goal:** When temperature is high AND humidity is high, show an alert on the LCD screen and on the web dashboard.

**Alert Conditions:**
- Humidity > 50% **AND**
- Temperature > 27°C

**What Happens:**
- LCD shows: `! ASTHMA ALERT !`
- Web dashboard shows red alert card

---

## 📁 ALL FILES INVOLVED (In Flow Order)

### 1️⃣ Configuration Files (Setup)

#### `micropython/config.py` - Pin & Settings Configuration
**Location:** On ESP32
**Purpose:** Stores all pin numbers and settings
**What it does:** Tells ESP32 which pin the LCD is connected to

```python
# LCD pins
I2C_SCL_PIN = 22  # Clock pin for LCD
I2C_SDA_PIN = 21  # Data pin for LCD

# DHT sensor pin (for temperature/humidity)
DHT_PIN = 17

# MQTT topics
TOPICS.event("asthma_alert")  # = "ks5009/house/events/asthma_alert"
```

**Key Point:** LCD uses I2C communication on pins 22 and 21.

---

### 2️⃣ Component Classes (Building Blocks)

#### `micropython/components/displays/lcd.py` - LCD Component
**Location:** On ESP32
**Purpose:** Makes LCD easy to control
**What it does:** Provides simple functions to display text on LCD

```python
class LCD:
    def __init__(self):
        # Connect to LCD via I2C
        self.i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        # Find LCD address (0x27 or 0x3F)
        self.addr = 0x27  # Your LCD is at 0x27
        # Load LCD library
        from i2c_lcd import I2cLcd
        self.lcd = I2cLcd(self.i2c, self.addr, 2, 16)

    def display_alert(self, line1, line2=""):
        """Display 2 lines of text on LCD"""
        self.lcd.clear()
        self.lcd.move_to(0, 0)  # Row 0
        self.lcd.putstr(line1[:16])  # Max 16 characters
        if line2:
            self.lcd.move_to(0, 1)  # Row 1
            self.lcd.putstr(line2[:16])
```

**Key Functions:**
- `display_alert("Text Line 1", "Text Line 2")` - Shows 2 lines
- `clear()` - Clears the screen
- `is_connected()` - Checks if LCD is working

**Why this matters:** Makes it easy to show messages without dealing with I2C complexity.

---

#### `micropython/components/sensors/dht_sensor.py` - DHT Sensor
**Location:** On ESP32
**Purpose:** Reads temperature and humidity
**What it does:** Gets current temperature and humidity from DHT11 sensor

```python
class DHT:
    def __init__(self):
        import dht
        self.sensor = dht.DHT11(Pin(17))  # DHT on pin 17

    def read(self):
        """Read temperature and humidity"""
        try:
            self.sensor.measure()
            return {
                'temp': self.sensor.temperature(),      # e.g., 17
                'humidity': self.sensor.humidity()      # e.g., 63
            }
        except:
            return None  # Failed to read
```

**Returns:** Dictionary with temp and humidity, or None if failed.

---

### 3️⃣ Main Task Files (The Logic)

#### `micropython/task6_asthma_alert.py` - Standalone Task 6
**Location:** On ESP32
**Purpose:** Runs ONLY Task 6 (for testing)
**What it does:** Continuously monitors temperature/humidity and shows alert when needed

**Step-by-Step Code Explanation:**

```python
# ============================================
# STEP 1: IMPORT COMPONENTS
# ============================================
import time
from components import DHT, LCD, WiFi, MQTT
from config import TOPICS

# ============================================
# STEP 2: INITIALIZE COMPONENTS
# ============================================
dht = DHT()       # Create DHT sensor object
lcd = LCD()       # Create LCD object
wifi = WiFi()     # Create WiFi object
mqtt = MQTT()     # Create MQTT object

previous_alert = False  # Track if alert was shown before

# ============================================
# STEP 3: DEFINE HELPER FUNCTIONS
# ============================================

def check_asthma_conditions(temp, humidity):
    """Check if alert should be shown"""
    return humidity > 50 and temp > 27
    # Returns True if BOTH conditions met
    # Returns False otherwise

def handle_asthma_alert():
    """What to do when alert triggers"""
    print("⚠️  ASTHMA ALERT!")  # Print to serial

    # Show on LCD
    if lcd.is_connected():
        lcd.display_alert("! ASTHMA ALERT !", "H>50% T>27C")

    # Send to web dashboard via MQTT
    if mqtt.is_connected():
        mqtt.publish(TOPICS.event("asthma_alert"), "1")

def handle_alert_cleared(temp, humidity):
    """What to do when conditions return to normal"""
    print("✅ Asthma alert cleared")

    # Show normal readings on LCD
    if lcd.is_connected():
        lcd.display_alert(f"Temp: {temp}C", f"Humidity: {humidity}%")

    # Tell web dashboard alert is cleared
    if mqtt.is_connected():
        mqtt.publish(TOPICS.event("asthma_alert"), "0")

# ============================================
# STEP 4: CONNECT WIFI & MQTT
# ============================================
wifi.connect()
mqtt.connect()

# ============================================
# STEP 5: MAIN LOOP (Runs Forever)
# ============================================
while True:
    try:
        # Read DHT sensor
        data = dht.read()

        if data:
            temp = data['temp']          # e.g., 17
            humidity = data['humidity']  # e.g., 63

            # Check if alert conditions are met
            alert_active = check_asthma_conditions(temp, humidity)
            # alert_active = (63 > 50 and 17 > 27) = False

            # Handle state changes
            if alert_active and not previous_alert:
                # Alert just triggered! (was off, now on)
                handle_asthma_alert()

            elif not alert_active and previous_alert:
                # Alert just cleared! (was on, now off)
                handle_alert_cleared(temp, humidity)

            elif not alert_active:
                # No alert, just update display normally
                if lcd.is_connected():
                    lcd.display_alert(f"Temp: {temp}C", f"Humidity: {humidity}%")

            # Remember current state for next loop
            previous_alert = alert_active

        # Check for incoming MQTT messages
        mqtt.check_messages()

        # Wait 1 second before next reading
        time.sleep(1)

    except KeyboardInterrupt:
        # User pressed Ctrl+C, stop program
        lcd.clear()
        mqtt.disconnect()
        break
```

**Key Logic:**
1. Read temperature/humidity every 1 second
2. Check if conditions met (H>50% AND T>27°C)
3. If conditions just became true → Show alert
4. If conditions just became false → Show normal
5. If no change → Update display anyway

---

#### `micropython/all_tasks.py` - Combined All Tasks
**Location:** On ESP32
**Purpose:** Runs ALL tasks (1-6) together
**What it does:** Same as task6_asthma_alert.py but integrated with other tasks

**Key Differences from Standalone:**

```python
# Only checks temperature every 30 minutes (when Task 2 reads DHT)
if should_log_temperature():
    data = dht.read()
    if data:
        temp = data['temp']
        humidity = data['humidity']

        # Task 2: Log temperature
        print(f"  Temperature: {temp}°C")
        print(f"  Humidity: {humidity}%")

        # Task 6: Check asthma alert
        asthma_alert = check_asthma_conditions(temp, humidity)

        if asthma_alert and not previous_asthma:
            handle_asthma_alert()
        elif not asthma_alert and previous_asthma:
            handle_asthma_cleared(temp, humidity)
        elif not asthma_alert:
            # Update LCD with current readings
            update_normal_display(temp, humidity)

        previous_asthma = asthma_alert
```

**Why every 30 minutes?**
- Saves power
- DHT sensor doesn't need constant reading
- Task 2 already reads every 30 minutes, so Task 6 shares that reading

---

#### `micropython/boot.py` - Auto-Start on Power Up
**Location:** On ESP32
**Purpose:** Runs automatically when ESP32 boots
**What it does:** Starts all_tasks.py without manual command

```python
import time
print("ESP32 Boot - Waiting 2 seconds...")
time.sleep(2)

print("Starting ALL tasks (Task 1 + 2 + 3 + 4 + 5 + 6)...")
try:
    import all_tasks  # This loads and runs all_tasks.py
except Exception as e:
    print(f"Error loading all_tasks: {e}")
```

**Key Point:** When you press RESET or power on ESP32, this runs automatically!

---

### 4️⃣ Web Dashboard Files (User Interface)

#### `web-app/components/features/dashboard/AsthmaAlert.tsx` - Alert Component
**Location:** On your PC (web-app folder)
**Purpose:** Shows red alert card on web dashboard
**What it does:** Subscribes to MQTT and displays alert when active

```typescript
export default function AsthmaAlert() {
  // State to track if alert is active
  const [alertActive, setAlertActive] = useState<boolean>(false);

  useEffect(() => {
    // Connect to MQTT
    const client = connectMQTT();

    // Subscribe to asthma alert topic
    client.subscribe("ks5009/house/events/asthma_alert");

    // Listen for messages
    client.on("message", (topic, message) => {
      const msg = message.toString();

      if (msg === "1") {
        setAlertActive(true);   // Show alert
      } else if (msg === "0") {
        setAlertActive(false);  // Hide alert
      }
    });
  }, []);

  // If no alert, don't show anything
  if (!alertActive) {
    return null;
  }

  // Show red alert card
  return (
    <Card className="border-red-500 bg-red-500/10">
      <CardHeader>
        <CardTitle className="text-red-500">
          🚨 Asthma Risk Alert
        </CardTitle>
        <CardDescription>
          High temperature and humidity detected
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ul>
          <li>Temperature &gt; 27°C</li>
          <li>Humidity &gt; 50%</li>
        </ul>
      </CardContent>
    </Card>
  );
}
```

**Key Logic:**
- Subscribe to MQTT topic `ks5009/house/events/asthma_alert`
- When receives "1" → Show red alert card
- When receives "0" → Hide alert card

---

#### `web-app/lib/mqtt.ts` - MQTT Configuration
**Location:** On your PC (web-app folder)
**Purpose:** Defines MQTT topics and connection
**What it does:** Connects web app to MQTT broker

```typescript
export const TOPICS = {
  temperature: "ks5009/house/sensors/temperature",
  humidity: "ks5009/house/sensors/humidity",
  motion: "ks5009/house/events/motion_detected",
  gas: "ks5009/house/events/gas_detected",
  asthma: "ks5009/house/events/asthma_alert",  // ← Task 6 topic
};

export function connectMQTT() {
  const client = mqtt.connect("ws://broker.hivemq.com:8000/mqtt");
  return client;
}
```

**Key Point:** All MQTT topics are defined here in one place.

---

### 5️⃣ Bridge Script (PC Communication Helper)

#### `unified_bridge.py` - Serial to MQTT Bridge
**Location:** On your PC
**Purpose:** Helps ESP32 communicate with web dashboard
**What it does:** Reads ESP32 serial messages and publishes to MQTT

**Why needed?** ESP32 can't reach MQTT broker directly (network blocked), so bridge helps.

```python
# Task 6 Detection
if "ASTHMA ALERT!" in line:
    print("[TASK 6] Asthma Alert Triggered!")
    publish_asthma_mqtt("1")  # Tell web dashboard: alert active

if "Asthma alert cleared" in line:
    print("[TASK 6] Asthma Alert Cleared!")
    publish_asthma_mqtt("0")  # Tell web dashboard: alert cleared

def publish_asthma_mqtt(status="1"):
    """Publish to MQTT broker"""
    # Uses Node.js to publish MQTT message
    cmd = f'''node -e "const mqtt = require('mqtt');
              const client = mqtt.connect('ws://broker.hivemq.com:8000/mqtt');
              client.on('connect', () => {{
                client.publish('ks5009/house/events/asthma_alert', '{status}');
                setTimeout(() => client.end(), 500);
              }});"'''
    subprocess.run(cmd, shell=True, cwd='web-app')
```

**Key Logic:**
1. Monitor ESP32 serial output
2. When sees "ASTHMA ALERT!" → Publish MQTT "1"
3. When sees "cleared" → Publish MQTT "0"
4. No database logging (not required!)

---

## 🔄 COMPLETE FLOW (Step-by-Step)

### Scenario 1: Alert Triggers

```
┌─────────────────────────────────────────────────────┐
│ 1. ESP32 reads DHT sensor every 30 minutes         │
│    File: all_tasks.py (line 315)                   │
│    Code: data = dht.read()                         │
│    Result: temp=28, humidity=55                    │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 2. Check conditions                                 │
│    File: all_tasks.py (line 327)                   │
│    Code: check_asthma_conditions(28, 55)           │
│    Logic: (55 > 50 AND 28 > 27) = TRUE ✅          │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 3. Trigger alert (first time)                      │
│    File: all_tasks.py (line 330)                   │
│    Code: handle_asthma_alert()                     │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 4. Display on LCD                                   │
│    File: components/displays/lcd.py                │
│    Code: lcd.display_alert("! ASTHMA ALERT !", ... │
│    LCD shows:                                       │
│    ┌────────────────┐                              │
│    │! ASTHMA ALERT !│ ← Line 1                     │
│    │H>50% T>27C     │ ← Line 2                     │
│    └────────────────┘                              │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 5. Print to serial                                  │
│    Code: print("⚠️  ASTHMA ALERT!")                 │
│    Serial output: ⚠️  ASTHMA ALERT!                 │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 6. Bridge detects serial message                   │
│    File: unified_bridge.py (line 293)              │
│    Code: if "ASTHMA ALERT!" in line:                │
│    Bridge sees: ⚠️  ASTHMA ALERT!                   │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 7. Bridge publishes to MQTT                        │
│    File: unified_bridge.py (line 296)              │
│    Code: publish_asthma_mqtt("1")                  │
│    MQTT: ks5009/house/events/asthma_alert = "1"    │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 8. Web dashboard receives MQTT                     │
│    File: AsthmaAlert.tsx (line 44)                 │
│    Code: if (msg === "1") setAlertActive(true)     │
│    Result: Alert card appears!                     │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 9. User sees alert on web                          │
│    Browser shows:                                   │
│    ┌──────────────────────────────────┐            │
│    │ 🚨 Asthma Risk Alert              │            │
│    │ High temperature and humidity...  │            │
│    │ • Temperature > 27°C              │            │
│    │ • Humidity > 50%                  │            │
│    └──────────────────────────────────┘            │
└─────────────────────────────────────────────────────┘
```

---

### Scenario 2: Alert Clears

```
┌─────────────────────────────────────────────────────┐
│ 1. ESP32 reads DHT again (30 min later)            │
│    Result: temp=25, humidity=45                    │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 2. Check conditions                                 │
│    Logic: (45 > 50 AND 25 > 27) = FALSE ❌         │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 3. Clear alert (was true, now false)               │
│    Code: handle_asthma_cleared(25, 45)             │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 4. Display normal on LCD                            │
│    LCD shows:                                       │
│    ┌────────────────┐                              │
│    │Temp: 25C       │ ← Line 1                     │
│    │Humidity: 45%   │ ← Line 2                     │
│    └────────────────┘                              │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 5. Print to serial                                  │
│    Serial: ✅ Asthma alert cleared                  │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 6. Bridge publishes MQTT "0"                       │
│    MQTT: ks5009/house/events/asthma_alert = "0"    │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 7. Web dashboard hides alert card                  │
│    Code: if (msg === "0") setAlertActive(false)    │
└─────────────────────────────────────────────────────┘
```

---

## 📦 File Dependency Tree

```
all_tasks.py (Main ESP32 program)
├── Imports: components/__init__.py
│   ├── components/sensors/dht_sensor.py
│   │   └── Uses: config.DHT_PIN
│   ├── components/displays/lcd.py
│   │   ├── Uses: config.I2C_SCL_PIN, config.I2C_SDA_PIN
│   │   └── Requires: lib/i2c_lcd.py (on ESP32)
│   ├── components/connectivity/wifi.py
│   └── components/connectivity/mqtt.py
└── Imports: config.py
    └── Defines: TOPICS.event("asthma_alert")

boot.py (Auto-runs on ESP32 boot)
└── Imports: all_tasks.py

unified_bridge.py (Runs on PC)
├── Monitors: ESP32 serial output
└── Publishes: MQTT to broker.hivemq.com

AsthmaAlert.tsx (Web component)
├── Imports: lib/mqtt.ts
│   └── Connects: broker.hivemq.com
└── Subscribes: TOPICS.asthma
```

---

## 🎯 Key Points Summary

### What Makes Task 6 Different?

1. **No Database Logging** ✅
   - Task 3 logs to database
   - Task 5 logs to database
   - **Task 6 does NOT** log to database (not required!)

2. **Uses LCD Display** ✅
   - Only task that uses LCD
   - Shows alert message or current readings

3. **MQTT Only** ✅
   - Bridge only publishes MQTT
   - No database calls in bridge code

4. **Shares DHT Reading** ✅
   - Task 2 reads DHT every 30 min
   - Task 6 reuses that same reading
   - Efficient! No duplicate sensor reads

---

## 🚀 How to Test Everything

### Test 1: LCD Component
```bash
ampy --port COM4 run tests/test_lcd_component.py
```
**Expected:** LCD shows "Temp: 25C" / "Humidity: 45%"

### Test 2: Standalone Task 6
```bash
ampy --port COM4 run micropython/task6_asthma_alert.py
```
**Expected:** LCD shows current temp/humidity, updates every 5 seconds

### Test 3: All Tasks Together
```bash
# Just reset ESP32 (boot.py runs automatically)
```
**Expected:** LCD shows temp/humidity, updates every 30 minutes

### Test 4: Alert Trigger
```bash
ampy --port COM4 run tests/test_alert_lcd_only.py
```
**Expected:**
- Shows alert for 10 seconds
- Shows normal for 10 seconds
- Clears

### Test 5: Bridge
```bash
# Terminal 1: Reset ESP32
# Terminal 2:
python unified_bridge.py
```
**Expected:** Bridge detects serial and publishes MQTT

### Test 6: Web Dashboard
```bash
# Terminal 1: Bridge running
# Terminal 2:
cd web-app
npm run dev
# Open browser: http://localhost:3000
```
**Expected:** Red alert card appears when conditions met

---

## 🔍 Troubleshooting Guide

### LCD Shows Nothing

**Check:**
1. ✅ LCD component uploaded? `ampy --port COM4 put micropython/components/displays/lcd.py components/displays/lcd.py`
2. ✅ i2c_lcd library exists? `ampy --port COM4 ls lib` (should show i2c_lcd.py)
3. ✅ LCD connected to pins 22 (SCL) and 21 (SDA)?

### Alert Doesn't Trigger

**Check:**
1. Current temperature: Must be >27°C (currently 17°C, too low!)
2. Current humidity: Must be >50% (63% is OK ✓)
3. Both conditions must be TRUE at same time

### Web Dashboard No Alert

**Check:**
1. ✅ Bridge running? `python unified_bridge.py`
2. ✅ Web app running? `npm run dev`
3. ✅ MQTT topic correct in mqtt.ts? Should be `asthma: "ks5009/house/events/asthma_alert"`

---

## ✅ Complete Checklist

**ESP32 Files (All uploaded):**
- [x] `boot.py` - Auto-starts all tasks
- [x] `all_tasks.py` - Main program with Task 6
- [x] `task6_asthma_alert.py` - Standalone Task 6
- [x] `config.py` - Pin configuration
- [x] `components/displays/lcd.py` - LCD component
- [x] `components/sensors/dht_sensor.py` - DHT sensor
- [x] `lib/i2c_lcd.py` - LCD library

**PC Files:**
- [x] `unified_bridge.py` - Bridge with Task 6 support
- [x] `web-app/components/features/dashboard/AsthmaAlert.tsx` - Web component
- [x] `web-app/lib/mqtt.ts` - MQTT configuration

**Everything working:**
- [x] LCD displays current temp/humidity
- [x] LCD shows alert when conditions met
- [x] Bridge publishes to MQTT
- [x] Web dashboard shows alert card

---

## 📊 Final Summary

**Task 6 is complete and working!**

**What you have:**
1. ✅ LCD showing temp/humidity at all times
2. ✅ Alert triggers when H>50% AND T>27°C
3. ✅ Web dashboard real-time alerts via MQTT
4. ✅ Auto-starts on ESP32 boot
5. ✅ Integrated with unified bridge

**What you DON'T have:**
- ❌ Database logging (not required!)

**Total Files:** 10 files working together
**Lines of Code:** ~500 lines
**Complexity:** Medium (uses LCD, MQTT, DHT, state management)

---

**Task 6 Status:** ✅ 100% COMPLETE!

