# Quick Start - Smart House

## 🚀 Start Everything in ONE Click!

### Step 1: Plug in ESP32
```
Connect ESP32 to laptop via USB
```
✅ All tasks start automatically on ESP32 (boot.py)

### Step 2: Start the System
```
Double-click: RUN.bat
```
✅ Web dashboard starts automatically at http://localhost:3000
✅ Bridge starts automatically
✅ Everything works now!

---

## 🎯 What This Starts

### Web Dashboard
- **URL:** http://localhost:3000
- **Shows:** Temperature, Humidity, Motion counter
- **Updates:** Real-time via MQTT

### Unified Bridge
- **Monitors:** All ESP32 tasks
- **Handles:** Database logging + MQTT publishing
- **Tasks:**
  - Task 2: Temperature & Humidity (every 30 min)
  - Task 3: Motion Detection (on event)
  - Future tasks: Gas, Steam, RFID, etc.

---

## 🧪 Test It

### Test Task 2 (Temperature):
- Wait for temperature reading (every 30 min, or immediate on ESP32 boot)
- Check bridge window: Should show `[TASK 2] Temperature Reading!`
- Check dashboard: Temperature and humidity values should appear

### Test Task 3 (Motion):
- Wave your hand in front of PIR sensor
- 🟠 ESP32: Orange LED lights up
- 📊 Bridge: Shows `[TASK 3] Motion Detected!`
- 🌐 Dashboard: Motion count increases

---

## 💡 Important Notes

### Keep Bridge Window Open!
- The bridge window MUST stay open
- It's the connection between ESP32 and the internet
- Shows all ESP32 output and system status

### Web App Window
- Opens minimized in background
- Access at http://localhost:3000
- To stop: Close the minimized window or press Ctrl+C in bridge window

### ESP32 Auto-Start
- ESP32 runs ALL tasks automatically on boot
- No need to manually upload code each time
- Just plug in and run START_SMART_HOUSE.bat

---

## 🛑 How to Stop

**Option 1:** Press `Ctrl+C` in the bridge window
- Stops bridge
- Web app keeps running (close separately)

**Option 2:** Close all windows
- Close bridge window
- Find minimized web app window and close

---

## 🔧 Troubleshooting

### Problem: "No COM ports detected"
**Solution:**
1. Unplug and replug ESP32
2. Try a different USB port
3. Check Device Manager for COM port

### Problem: "Python not found"
**Solution:**
1. Install Python from python.org
2. During install, check "Add to PATH"
3. Restart computer

### Problem: "Node.js not found"
**Solution:**
1. Install Node.js from nodejs.org
2. Restart computer
3. Run START_SMART_HOUSE.bat again

### Problem: Temperature not showing
**Solution:**
1. Make sure bridge is running (START_SMART_HOUSE.bat)
2. Wait for temperature reading (every 30 min)
3. Or reset ESP32 for immediate reading

### Problem: Motion not working
**Solution:**
1. Make sure bridge is running
2. Wave hand in front of PIR sensor
3. Check bridge window for `[TASK 3] Motion Detected!`

---

## 📁 File Structure

```
smart-house/
├── START_SMART_HOUSE.bat     ⭐ ONE-CLICK LAUNCHER (Use this!)
├── unified_bridge.py          Bridge script (auto-started)
├── README.md                  Project overview
├── QUICK_START.md             This file
│
├── micropython/               ESP32 code
│   ├── boot.py               Auto-starts all tasks
│   ├── all_tasks.py          Task 2 + Task 3 combined
│   └── ...
│
├── web-app/                   Next.js dashboard
├── docs/                      Documentation
├── tests/                     Hardware tests
└── database/                  SQL schema
```

---

## ✅ That's It!

**Just remember:**
1. Plug in ESP32
2. Double-click: `START_SMART_HOUSE.bat`
3. Open: http://localhost:3000
4. Everything works! 🎉

**Need detailed help?** See [docs/START_HERE_CLAUDE.md](docs/START_HERE_CLAUDE.md)
