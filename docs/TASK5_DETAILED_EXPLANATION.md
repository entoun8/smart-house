# Task 5: Gas Detection - Detailed Code Explanation

**Simple, step-by-step breakdown of how everything works**

---

## 📁 Files Involved in Task 5

### **ESP32 Side (MicroPython):**
1. `micropython/task5_gas_detection.py` - Standalone gas detection
2. `micropython/all_tasks.py` - All tasks combined (includes Task 5)
3. `micropython/components/sensors/gas_sensor.py` - Gas sensor class
4. `micropython/components/actuators/fan.py` - Fan motor class
5. `micropython/components/actuators/rgb.py` - RGB LED class
6. `micropython/config.py` - Pin configuration

### **Bridge Side (Python on PC):**
7. `unified_bridge.py` - Monitors ESP32 and handles DB + MQTT

### **Web Dashboard (Next.js):**
8. `web-app/components/features/dashboard/GasStatus.tsx` - Gas alert UI
9. `web-app/components/features/dashboard/DashboardContent.tsx` - Main dashboard
10. `web-app/lib/mqtt.ts` - MQTT connection and topics

### **Database:**
11. Database table: `gas_logs` (in Supabase)

---

## 🔄 Complete Flow (From Sensor to Web)

```
┌──────────────────────────────────────────────────────────────┐
│                    THE COMPLETE JOURNEY                       │
└──────────────────────────────────────────────────────────────┘

1. 🔥 Gas Sensor (Hardware)
   └─→ GPIO 23 reads HIGH when gas detected
        │
        ▼
2. 🤖 GasSensor Class (components/sensors/gas_sensor.py)
   └─→ is_detected() returns True
        │
        ▼
3. 📝 task5_gas_detection.py or all_tasks.py
   └─→ Calls handle_gas_detected()
        │
        ├─→ 4. 🌀 Fan Class → fan.on() → GPIO 18,19 turn ON
        │
        ├─→ 5. 🔴 RGB Class → rgb.red() → GPIO 26 shows red
        │
        └─→ 6. 📡 print("Gas detected!") → Serial output
                │
                ▼
7. 🖥️ Bridge (unified_bridge.py) on PC
   └─→ Reads serial port
        │
        ├─→ Detects "Gas detected!" in serial
        │
        ├─→ 8. 💾 log_gas_to_database()
        │    └─→ POST to Supabase → gas_logs table
        │
        └─→ 9. 📨 publish_gas_mqtt()
             └─→ Publishes to MQTT broker
                  │
                  ▼
10. 🌐 Web Dashboard (GasStatus.tsx)
    └─→ Subscribed to MQTT topic
         │
         ├─→ Receives "Gas detected!" message
         │
         ├─→ Updates UI (red border, pulsing icon)
         │
         └─→ Fetches total count from database
              │
              ▼
11. 👤 User sees alert on http://localhost:3000
```

---

## 📖 File-by-File Detailed Explanation

---

### **File 1: `micropython/components/sensors/gas_sensor.py`**

**Purpose:** Wrapper class to read the gas sensor

**Code:**
```python
from machine import Pin
from config import GAS_SENSOR_PIN

class GasSensor:
    def __init__(self):
        # GPIO 23 configured as INPUT
        self.sensor = Pin(GAS_SENSOR_PIN, Pin.IN)

    def is_detected(self):
        """Returns True if gas detected, False otherwise"""
        # When gas detected, pin goes HIGH (1)
        return self.sensor.value() == 1
```

**Explanation:**
- Creates a Pin object on GPIO 23
- `Pin.IN` means "read from this pin" (not write)
- `sensor.value()` reads the pin (0 = no gas, 1 = gas detected)
- Returns `True` when gas is detected

**Real-world behavior:**
- Most gas sensors output HIGH when gas detected
- Some output LOW - adjust `== 1` to `== 0` if needed

---

### **File 2: `micropython/components/actuators/fan.py`**

**Purpose:** Controls the fan motor

**Code:**
```python
from machine import Pin
from config import FAN_PIN1, FAN_PIN2

class Fan:
    def __init__(self):
        # Fan motor has 2 pins (for direction control)
        self.pin1 = Pin(FAN_PIN1, Pin.OUT)  # GPIO 19
        self.pin2 = Pin(FAN_PIN2, Pin.OUT)  # GPIO 18

    def on(self):
        """Turn fan ON"""
        self.pin1.high()  # Set GPIO 19 to HIGH
        self.pin2.low()   # Set GPIO 18 to LOW
        # This makes fan spin in one direction

    def off(self):
        """Turn fan OFF"""
        self.pin1.low()   # Both pins LOW = motor off
        self.pin2.low()
```

**Explanation:**
- Fan motor uses 2 pins (H-bridge control)
- `pin1 HIGH + pin2 LOW` = Fan spins forward
- `pin1 LOW + pin2 HIGH` = Fan spins backward
- `Both LOW` = Fan stops

**Real-world behavior:**
- This controls a DC motor via L298N or similar motor driver
- The motor driver amplifies the ESP32's 3.3V signal to drive the motor

---

### **File 3: `micropython/components/actuators/rgb.py`**

**Purpose:** Controls the RGB LED strip

**Code:**
```python
from neopixel import NeoPixel
from machine import Pin
from config import RGB_LED_PIN, RGB_LED_COUNT

class RGBStrip:
    def __init__(self):
        # Create NeoPixel object (4 LEDs on GPIO 26)
        self.np = NeoPixel(Pin(RGB_LED_PIN), RGB_LED_COUNT)

    def red(self):
        """Turn all LEDs solid red"""
        for i in range(RGB_LED_COUNT):
            self.np[i] = (255, 0, 0)  # (Red, Green, Blue)
        self.np.write()  # Send data to LEDs

    def off(self):
        """Turn all LEDs off"""
        for i in range(RGB_LED_COUNT):
            self.np[i] = (0, 0, 0)  # Black = off
        self.np.write()
```

**Explanation:**
- `NeoPixel` controls WS2812B RGB LEDs (smart LEDs)
- Each LED has 3 values: (Red, Green, Blue) from 0-255
- `(255, 0, 0)` = full red, no green, no blue = RED
- `write()` sends the colors to the LEDs

**Color codes:**
- Red: `(255, 0, 0)` - for gas
- Orange: `(255, 165, 0)` - for motion
- Blue: `(0, 0, 255)` - for steam

---

### **File 4: `micropython/task5_gas_detection.py`**

**Purpose:** Main logic for Task 5 (standalone version)

**Full Code with Line-by-Line Explanation:**

```python
# ===== IMPORTS =====
import time
from components import GasSensor, Fan, RGBStrip, WiFi, MQTT
from database import Database
from config import TOPICS

# ===== CREATE OBJECTS =====
gas = GasSensor()      # Create gas sensor object
fan = Fan()            # Create fan object
rgb = RGBStrip()       # Create RGB LED object
wifi = WiFi()          # Create WiFi connection object
mqtt = MQTT()          # Create MQTT client object
db = Database()        # Create database object

# ===== STATE TRACKING =====
previous_gas = False   # Remember previous sensor state
                       # This helps detect CHANGES (off→on, on→off)

# ===== EVENT HANDLERS =====

def handle_gas_detected():
    """Called when gas is FIRST detected (transition from no gas → gas)"""
    print("Gas detected!")    # Print to serial (bridge detects this!)

    fan.on()                  # Turn on fan motor
    rgb.red()                 # Turn RGB solid red

    # Try to publish to MQTT (if connected)
    if mqtt.is_connected():
        mqtt.publish(TOPICS.event("gas_detected"), "1")

    # Try to log to database (usually fails due to network)
    db.log_gas()

def handle_gas_cleared():
    """Called when gas clears (transition from gas → no gas)"""
    print("Gas cleared!")     # Print to serial
    fan.off()                 # Turn off fan
    rgb.off()                 # Turn off RGB

# ===== SETUP =====
print("=" * 50)
print("GAS DETECTION & FAN CONTROL - TASK 5")
print("=" * 50)

# Connect to WiFi
print("\nConnecting to WiFi...")
if not wifi.is_connected():
    if wifi.connect():
        print(f"WiFi connected! IP: {wifi.get_ip()}")
    else:
        print("WiFi connection failed!")
else:
    print(f"WiFi already connected! IP: {wifi.get_ip()}")

time.sleep(2)  # Wait for WiFi to stabilize

# Connect to MQTT (usually fails, bridge handles it instead)
print("Connecting to MQTT...")
if mqtt.connect():
    print("MQTT connected!")
else:
    print("MQTT connection failed! Bridge will handle logging.")

print("\nSetup complete! Monitoring for gas...")
print("=" * 50)

# ===== MAIN LOOP =====
while True:
    try:
        # Read sensor (returns True or False)
        gas_detected = gas.is_detected()

        # Check if state CHANGED from False to True
        if gas_detected and not previous_gas:
            handle_gas_detected()      # Gas just detected!

        # Check if state CHANGED from True to False
        elif not gas_detected and previous_gas:
            handle_gas_cleared()       # Gas just cleared!

        # Remember current state for next loop
        previous_gas = gas_detected

        # Check for incoming MQTT messages (if connected)
        mqtt.check_messages()

        # Wait 0.5 seconds before next check
        time.sleep(0.5)

    except KeyboardInterrupt:
        # User pressed Ctrl+C
        print("\n\nStopping gas detector...")
        fan.off()           # Turn off fan
        rgb.off()           # Turn off RGB
        mqtt.disconnect()   # Disconnect MQTT
        break               # Exit loop

    except Exception as e:
        # Any other error
        print(f"\nError: {e}")
        time.sleep(1)       # Wait before retrying
```

**Key Concepts:**

1. **State Tracking:**
   - `previous_gas` remembers the last sensor reading
   - This lets us detect CHANGES, not just the current state
   - Only triggers action when state CHANGES

2. **Edge Detection:**
   ```python
   if gas_detected and not previous_gas:  # OFF → ON
       # Gas JUST appeared

   elif not gas_detected and previous_gas:  # ON → OFF
       # Gas JUST cleared
   ```

3. **Why print()?**
   - Bridge monitors serial output
   - When bridge sees "Gas detected!", it logs to database
   - This bypasses ESP32 network restrictions

---

### **File 5: `unified_bridge.py` (Task 5 Section)**

**Purpose:** Monitors ESP32 serial output and handles database + MQTT

**Task 5 Code:**

```python
# ===== DATABASE FUNCTION =====
def log_gas_to_database():
    """Log gas detection to Supabase database"""
    try:
        # Prepare HTTP headers for Supabase API
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }

        # Make POST request to gas_logs table
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/gas_logs",
            headers=headers,
            json={'value': 1},  # Log value=1 (gas detected)
            timeout=5
        )

        # Check if successful
        if response.status_code in [200, 201]:
            print(f"  [DB] Gas detection logged!")
            return True
        else:
            print(f"  [WARN] Gas DB failed (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"  [WARN] Gas DB error: {e}")
        return False

# ===== MQTT FUNCTION =====
def publish_gas_mqtt():
    """Publish gas event to MQTT broker"""
    try:
        # Use Node.js to publish MQTT (faster than Python MQTT)
        cmd = f'''node -e "const mqtt = require('mqtt');
                  const client = mqtt.connect('ws://{MQTT_BROKER}:{MQTT_PORT}/mqtt');
                  client.on('connect', () => {{
                      client.publish('ks5009/house/events/gas_detected', '1');
                      setTimeout(() => client.end(), 500);
                  }});"'''

        result = subprocess.run(cmd, shell=True, cwd='web-app',
                                capture_output=True, timeout=10)

        if result.returncode == 0:
            print(f"  [MQTT] Gas alert published!")
            return True
        else:
            print(f"  [WARN] Gas MQTT failed")
            return False
    except subprocess.TimeoutExpired:
        print(f"  [WARN] Gas MQTT timeout (continuing anyway)")
        return False
    except Exception as e:
        print(f"  [WARN] Gas MQTT error: {e}")
        return False

# ===== MAIN LOOP DETECTION =====
gas_count = 0  # Track number of detections

while True:
    if ser.in_waiting > 0:
        # Read line from ESP32 serial
        line = ser.readline().decode('utf-8', errors='ignore').strip()

        if line:
            print(f"[ESP32] {line}")  # Echo ESP32 output

        # Detect Task 5: Gas Detection
        if "Gas detected" in line:
            gas_count += 1
            print(f"\n[TASK 5] Gas Detected! (#{gas_count})")
            log_gas_to_database()    # Save to DB
            publish_gas_mqtt()       # Publish to MQTT
            print("=" * 60)

    time.sleep(0.1)  # Check every 0.1 seconds
```

**Explanation:**

1. **Serial Monitoring:**
   - Bridge reads ESP32's serial output line by line
   - Looks for keyword "Gas detected"
   - When found, triggers database and MQTT functions

2. **Database Logging:**
   - Makes HTTP POST to Supabase REST API
   - Inserts new row in `gas_logs` table
   - Timestamp is auto-generated by database

3. **MQTT Publishing:**
   - Uses Node.js (because it's simpler than Python MQTT)
   - Publishes to topic: `ks5009/house/events/gas_detected`
   - Payload: `"1"` (means gas detected)

4. **Why Bridge?**
   - ESP32 has network restrictions (can't reach MQTT/DB directly)
   - PC has full internet access
   - Bridge acts as a "relay" between ESP32 and internet

---

### **File 6: `web-app/lib/mqtt.ts`**

**Purpose:** MQTT configuration and connection

**Code:**
```typescript
import mqtt from "mqtt";

// MQTT Configuration
const MQTT_CONFIG = {
  broker: "ws://broker.hivemq.com:8000/mqtt",  // Public MQTT broker
  username: undefined,  // No authentication needed
  password: undefined,
};

// Topic definitions
export const TOPICS = {
  temperature: "ks5009/house/sensors/temperature",
  humidity: "ks5009/house/sensors/humidity",
  motion: "ks5009/house/events/motion_detected",
  gas: "ks5009/house/events/gas_detected",  // ← Task 5 topic
};

// Connect to MQTT broker
export function connectMQTT() {
  const client = mqtt.connect(MQTT_CONFIG.broker, {
    clientId: "webapp-" + Math.random().toString(16).slice(2, 10),
    clean: true,
    reconnectPeriod: 5000,  // Auto-reconnect every 5 seconds
  });

  return client;
}
```

**Explanation:**
- `ws://` = WebSocket protocol (for browser compatibility)
- `broker.hivemq.com:8000` = Public MQTT broker (no firewall issues)
- `TOPICS.gas` = Full topic path for gas events
- Client ID is random to avoid conflicts

---

### **File 7: `web-app/components/features/dashboard/GasStatus.tsx`**

**Purpose:** React component to display gas alerts

**Full Code with Explanation:**

```typescript
"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { connectMQTT, TOPICS } from "@/lib/mqtt";
import { Flame } from "lucide-react";  // Fire icon
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function GasStatus() {
  // ===== STATE VARIABLES =====
  const [gasDetected, setGasDetected] = useState<boolean>(false);  // Current alert state
  const [lastDetection, setLastDetection] = useState<string>("");  // Time of last detection
  const [detectionCount, setDetectionCount] = useState<number>(0); // Total from DB

  // ===== COMPONENT MOUNT =====
  useEffect(() => {
    console.log("[GasStatus] Component mounted");

    // Connect to MQTT
    const client = connectMQTT();

    // When connected to MQTT broker
    client.on("connect", () => {
      console.log("[GasStatus] MQTT connected, subscribing to:", TOPICS.gas);

      // Subscribe to gas detection topic
      client.subscribe(TOPICS.gas, (err) => {
        if (!err) {
          console.log("[GasStatus] ✅ Subscribed to", TOPICS.gas);
        } else {
          console.error("[GasStatus] ❌ Subscribe failed:", err);
        }
      });
    });

    // Handle incoming MQTT messages
    const handleMessage = (topic: string, message: Buffer) => {
      if (topic === TOPICS.gas) {
        console.log("🚨 [GasStatus] Gas detected from MQTT:", message.toString());

        setGasDetected(true);  // Show alert
        setLastDetection(new Date().toLocaleTimeString());  // Save time
        setDetectionCount((prev) => prev + 1);  // Increment counter

        // Auto-clear alert after 5 seconds
        setTimeout(() => {
          setGasDetected(false);
        }, 5000);
      }
    };

    // Register message handler
    client.on("message", handleMessage);

    // Fetch initial count from database
    fetchGasCount();

    // Cleanup when component unmounts
    return () => {
      client.off("message", handleMessage);
    };
  }, []);  // Run once on mount

  // ===== DATABASE FETCH =====
  const fetchGasCount = async () => {
    // Get total count from gas_logs table
    const { data, count } = await supabase
      .from("gas_logs")
      .select("*", { count: "exact", head: true });  // Count only, no data

    if (count !== null) {
      setDetectionCount(count);
    }
  };

  // ===== RENDER UI =====
  return (
    <Card className={`hover:shadow-lg transition-all ${gasDetected ? 'border-red-500 border-2' : ''}`}>
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <Flame
            className={`w-6 h-6 ${
              gasDetected ? "text-red-500 animate-pulse" : "text-gray-400"
            }`}
          />
          Gas Detection
        </CardTitle>
        <CardDescription>Gas sensor alerts</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {/* Show current state */}
          {gasDetected ? (
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
              <p className="text-lg font-bold text-red-500">GAS DETECTED!</p>
            </div>
          ) : (
            <p className="text-lg font-semibold text-green-500">All Clear</p>
          )}

          {/* Show total count */}
          <p className="text-sm text-muted-foreground">
            Total detections: {detectionCount}
          </p>

          {/* Show last detection time */}
          {lastDetection && (
            <p className="text-sm text-muted-foreground">
              Last detection: {lastDetection}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
```

**Explanation:**

1. **State Management:**
   - `gasDetected`: Boolean for showing alert NOW
   - `lastDetection`: String showing last alert time
   - `detectionCount`: Total count from database

2. **MQTT Subscription:**
   - Connects to MQTT broker when component loads
   - Subscribes to `ks5009/house/events/gas_detected`
   - Listens for messages

3. **Message Handling:**
   - When MQTT message arrives:
     - Set alert to TRUE
     - Save current time
     - Increment counter
     - Auto-clear after 5 seconds

4. **Visual Feedback:**
   - Alert state: Red border, pulsing icon, "GAS DETECTED!" text
   - Normal state: Gray icon, "All Clear" text
   - Always shows total count and last detection time

---

## 🔄 Timing Diagram

**What happens when gas is detected:**

```
Time | ESP32          | Bridge              | Database        | Web Dashboard
-----|----------------|---------------------|-----------------|------------------
0.0s | Gas detected   | -                   | -               | -
0.0s | fan.on()       | -                   | -               | -
0.0s | rgb.red()      | -                   | -               | -
0.0s | print("Gas")   | -                   | -               | -
0.1s | -              | Reads "Gas"         | -               | -
0.2s | -              | POST /gas_logs      | -               | -
0.3s | -              | -                   | Row inserted    | -
0.4s | -              | Publish MQTT        | -               | -
0.5s | -              | -                   | -               | Receives MQTT
0.5s | -              | -                   | -               | Shows alert 🔴
5.5s | -              | -                   | -               | Alert clears ✅
```

---

## 🎯 Key Takeaways

### **1. Why Three Components?**
- **ESP32:** Fast hardware control (fan, RGB)
- **Bridge:** Internet connectivity (database, MQTT)
- **Web:** User interface (alerts, history)

### **2. Why Serial Communication?**
- ESP32 has network restrictions
- Serial is reliable and always works
- Bridge can access internet freely

### **3. Why MQTT?**
- Real-time updates (no polling needed)
- Lightweight protocol
- Web browser can subscribe directly

### **4. Data Flow Summary:**
```
Sensor → ESP32 → Serial → Bridge → Database (permanent)
                                 → MQTT → Web (real-time)
```

### **5. State Detection:**
- Don't just check current value
- Track CHANGES (off→on, on→off)
- This prevents repeated triggers

---

## 📚 Related Patterns

This same pattern is used in:
- **Task 2:** Temperature (ESP32 → Bridge → DB + MQTT → Web)
- **Task 3:** Motion (ESP32 → Bridge → DB + MQTT → Web)
- **Task 5:** Gas (ESP32 → Bridge → DB + MQTT → Web) ← YOU ARE HERE

Simple tasks (1, 4) skip the bridge and just control hardware directly!

---

**Everything is simple when broken down step by step!** 🚀
