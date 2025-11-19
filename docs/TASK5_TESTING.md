# Task 5: Gas Detection - Testing Guide

**Quick and Simple Testing Instructions**

---

## 🚀 Option 1: Full System Test (Recommended)

### Prerequisites:
- ESP32 plugged into USB (COM4 or COM5)
- ESP32 already has `all_tasks.py` and `boot.py` uploaded

### Steps:

**1. Start Everything:**
```bash
# Just double-click:
RUN.bat
```
This automatically starts:
- Bridge (monitors ESP32)
- Web dashboard (http://localhost:3000)

**2. Test Gas Detection (Choose ONE method):**

**🎯 Method A: Manual Trigger (EASIEST - Recommended!):**
```
Use a jumper wire to connect:
  GPIO 23 → GND
This simulates gas detection - no actual gas needed!
```

**🔥 Method B: Lighter/Flame (If you have MQ-2/MQ-5):**
```
- Hold lighter flame 5-10cm from sensor
- Wait 1-2 seconds for reaction
- ⚠️ Don't touch sensor with flame!
```

**💧 Method C: Alcohol/Hand Sanitizer (Safest for real sensor):**
```
- Put hand sanitizer on your finger
- Wave it near the sensor (5-10cm away)
- Alcohol vapor triggers the sensor
```

**3. Watch the Results:**

**Bridge Window (should show):**
```
[ESP32] 🔥 Gas detected!
[TASK 5] Gas Detected! (#1)
  [DB] Gas detection logged!
  [MQTT] Gas alert published!
```

**Web Dashboard (http://localhost:3000):**
```
┌─────────────────────────┐ ← Red border appears
│ 🔥 Gas Detection        │
│ Gas sensor alerts       │
├─────────────────────────┤
│ 🔴 GAS DETECTED!        │ ← Pulsing red text
│ Total detections: 1     │
│ Last: 14:23:15         │
└─────────────────────────┘
```

**ESP32 (physical hardware):**
- ✅ Fan spins ON
- ✅ RGB LED glows solid red

**4. Clear Gas:**
- Remove trigger from sensor

**Expected:**
- ✅ Fan stops
- ✅ RGB turns off
- ✅ Dashboard alert clears after 5 seconds

---

## 🧪 Option 2: Test Task 5 Standalone (ESP32 Only)

If you want to test JUST Task 5 without bridge/web:

### Steps:

**1. Upload Task 5 Code:**
```bash
# Put the file on ESP32
ampy --port COM4 put micropython/task5_gas_detection.py

# Run it
ampy --port COM4 run micropython/task5_gas_detection.py
```

**2. Watch Serial Output:**
```bash
# Connect to ESP32 console
python -m serial.tools.miniterm COM4 115200
```

**3. Trigger Gas Sensor:**

**Expected Serial Output:**
```
==================================================
GAS DETECTION & FAN CONTROL - TASK 5
==================================================

Connecting to WiFi...
WiFi connected! IP: 10.52.126.70
Connecting to MQTT...
MQTT connected!

Setup complete! Monitoring for gas...
==================================================

Gas detected!      ← When you trigger sensor
Gas cleared!       ← When sensor clears
```

**Expected Hardware:**
- Fan turns ON when gas detected
- RGB LED turns red
- Fan turns OFF when gas clears
- RGB LED turns off

---

## 🔧 Option 3: Test with Manual Bridge

If `RUN.bat` doesn't work, run manually:

### Steps:

**1. Start Bridge:**
```bash
python unified_bridge.py
```

**2. In Another Terminal, Start Web App:**
```bash
cd web-app
npm run dev
```

**3. Open Browser:**
```
http://localhost:3000
```

**4. Trigger Gas Sensor:**
- Watch bridge terminal for "Gas detected!"
- Check web dashboard for alert

---

## 🛠️ Troubleshooting

### Problem: "Gas detected!" prints but nothing in database/web

**Solution:**
1. Make sure bridge is running (`unified_bridge.py`)
2. Check bridge is connected to correct COM port
3. Bridge should show:
   ```
   [TASK 5] Gas Detected!
   [DB] Gas detection logged!
   [MQTT] Gas alert published!
   ```

### Problem: Fan doesn't turn on

**Possible causes:**
1. **Check wiring:** Fan motor connected to GPIO 18 & 19?
2. **Check component:** Test fan manually:
   ```bash
   ampy --port COM4 run tests/test_fan.py
   ```
3. **Power supply:** Fan might need external power (ESP32 can't power large motors)

### Problem: RGB doesn't turn red

**Possible causes:**
1. **Check wiring:** RGB connected to GPIO 26?
2. **Test RGB:**
   ```bash
   ampy --port COM4 run tests/test_rgb.py
   ```

### Problem: Sensor always triggered / never triggers

**For digital gas sensor (MQ-2, MQ-5):**
1. Sensor needs warm-up time (1-2 minutes after power on)
2. Adjust sensitivity potentiometer on sensor board
3. Check sensor is getting 5V power (not 3.3V)

**Test sensor manually:**
```bash
ampy --port COM4 run tests/test_gas.py
```

### Problem: Bridge can't find COM port

**Solution:**
1. Check which port ESP32 is on:
   ```bash
   # Windows:
   Device Manager → Ports (COM & LPT)

   # The bridge auto-detects, but you can also check:
   python -c "import serial.tools.list_ports; print([p.device for p in serial.tools.list_ports.comports()])"
   ```

2. Update port in `unified_bridge.py` if needed:
   ```python
   ESP32_PORT = 'COM4'  # Change to your port
   ```

---

## ✅ Quick Test Checklist

When you trigger gas sensor, verify:

- [ ] Bridge shows `[TASK 5] Gas Detected!`
- [ ] Bridge shows `[DB] Gas detection logged!`
- [ ] Bridge shows `[MQTT] Gas alert published!`
- [ ] Fan motor spins
- [ ] RGB LED turns red
- [ ] Web dashboard shows red alert
- [ ] When sensor clears:
  - [ ] Fan stops
  - [ ] RGB turns off
  - [ ] Web alert clears after 5 seconds

---

## 📝 Expected Output Examples

### Bridge Output (Normal):
```
==================================================
Smart House - Unified Bridge (All Tasks)
==================================================

Connecting to ESP32 on COM5...
[OK] Connected to ESP32!

Monitoring ESP32 for database logging tasks...
==================================================

Active Tasks:
  - Task 2: Temperature & Humidity (every 30 min)
  - Task 3: Motion Detection (on motion)
  - Task 5: Gas Detection (on gas detected)
==================================================

[ESP32] ==================================================
[ESP32] ALL TASKS - Task 1 + 2 + 3 + 4 + 5
[ESP32] ==================================================
[ESP32] Connecting to WiFi...
[ESP32] WiFi connected! IP: 10.52.126.70
[ESP32] Task 5: Gas detection (continuous)
[ESP32] ==================================================
[ESP32] Setup complete! All tasks monitoring...

[ESP32] 🔥 Gas detected!

[TASK 5] Gas Detected! (#1)
  [DB] Gas detection logged!
  [MQTT] Gas alert published!
==================================================

[ESP32] ✅ Gas cleared!
```

### Web Dashboard Console (F12):
```
[GasStatus] Component mounted
[GasStatus] TOPICS.gas: ks5009/house/events/gas_detected
[GasStatus] MQTT client created
[GasStatus] MQTT connected, subscribing to: ks5009/house/events/gas_detected
[GasStatus] ✅ Subscribed to ks5009/house/events/gas_detected
🚨 [GasStatus] Gas detected from MQTT: 1
```

---

## 🎯 Simple Test Flow

**Easiest way to test:**

1. **Plug in ESP32** (it auto-starts all tasks)
2. **Double-click `RUN.bat`** (starts bridge + web)
3. **Open http://localhost:3000**
4. **Trigger gas sensor** (touch to ground or use lighter)
5. **Watch:**
   - Fan spins ✅
   - RGB red ✅
   - Bridge logs ✅
   - Web alert ✅

**Done!** 🎉

---

## 💡 Tips

### Simulate Gas Without Sensor:

If you don't have a gas sensor or want to test software only:

**Modify `task5_gas_detection.py` temporarily:**
```python
# Add test mode
import random

while True:
    # Simulate random gas detection every 10 seconds
    if random.random() < 0.1:  # 10% chance
        handle_gas_detected()
        time.sleep(5)
        handle_gas_cleared()

    time.sleep(1)
```

### Check Database Directly:

**Go to Supabase Dashboard:**
1. Open https://supabase.com
2. Go to your project
3. Table Editor → `gas_logs`
4. Should see entries when gas detected

### Check MQTT Directly:

**Use MQTT Explorer (optional):**
1. Download: http://mqtt-explorer.com/
2. Connect to: `broker.hivemq.com:8000`
3. Subscribe to: `ks5009/house/events/gas_detected`
4. Should see messages when gas detected

---

## 🚀 Ready to Test!

**Simplest command:**
```bash
# 1. Plug in ESP32
# 2. Run this:
RUN.bat

# 3. Open browser:
# http://localhost:3000

# 4. Trigger sensor
# 5. Watch it work! 🎉
```

---

## 📌 Visual Guide: How to Trigger Gas Sensor

### Method A: Jumper Wire (Recommended!)

```
ESP32 Board:
┌─────────────────┐
│                 │
│   GPIO 23 ●────┼──┐  Use jumper wire
│                 │  │  to connect these
│      GND  ●────┼──┘  two pins
│                 │
└─────────────────┘

Result: Gas sensor reads as "detected"
```

### Method B: Physical Sensor Testing

```
Gas Sensor (MQ-2/MQ-5):
┌─────────────────┐
│    [  Sensor  ] │
│                 │
│  VCC  GND  OUT  │
│   │    │    │   │
└───┼────┼────┼───┘
    │    │    └─── To ESP32 GPIO 23
    │    └──────── To ESP32 GND
    └───────────── To ESP32 5V

Trigger:
  💨 Wave hand sanitizer (alcohol) 5-10cm away
  🔥 Hold lighter flame 5-10cm away (careful!)
  💨 Spray deodorant/perfume 5-10cm away
```

### Which Method Should You Use?

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Jumper Wire** | ✅ Instant<br>✅ Safe<br>✅ No materials needed | ❌ Doesn't test actual sensor | Quick software testing |
| **Hand Sanitizer** | ✅ Safe<br>✅ Tests real sensor<br>✅ Common item | ⏱️ Slower reaction | Real sensor testing |
| **Lighter** | ✅ Tests real sensor<br>⏱️ Fast reaction | ⚠️ Fire hazard<br>⚠️ Can damage sensor | Realistic gas simulation |

**My recommendation: Start with jumper wire to test the software, then use hand sanitizer to test the actual sensor!**

---

**Need help?** Check:
- [TASK5_GAS_DETECTION.md](TASK5_GAS_DETECTION.md) - Implementation details
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Overall project status
- [COMMANDS.md](COMMANDS.md) - All available commands
