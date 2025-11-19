# Button Tests for Tasks 4, 5, 6, 7

Easy-to-test versions of tasks using buttons instead of sensors.

## 📁 Files

| File | Task | Description | Button |
|------|------|-------------|--------|
| `task4_steam.py` | Task 4 | Steam Detection | LEFT = Toggle steam |
| `task5_gas.py` | Task 5 | Gas Detection | LEFT = Toggle gas |
| `task6_asthma.py` | Task 6 | Asthma Alert | LEFT = Toggle alert |
| `task7_rfid.py` | Task 7 | RFID Access | LEFT = Authorized, RIGHT = Denied |

## 🚀 How to Run

### Upload and run a test:
```bash
# From project root folder
ampy --port COM5 run button-tests/task4_steam.py
```

### Run all tasks with bridge:
```bash
# 1. Upload button test to ESP32
ampy --port COM5 run button-tests/task7_rfid.py

# 2. In another terminal, start bridge
RUN.bat
```

## 🎮 Button Controls

**Task 4 - Steam Detection:**
- LEFT button → Simulates steam → Window closes + RGB blue

**Task 5 - Gas Detection:**
- LEFT button → Simulates gas → Fan ON + RGB red

**Task 6 - Asthma Alert:**
- LEFT button → Toggle asthma alert → LCD + Web dashboard

**Task 7 - RFID Access:**
- LEFT button → Authorized card → Door opens + RGB green
- RIGHT button → Unauthorized card → RGB red + Buzzer

## 📊 Bridge Integration

When running with `RUN.bat`:
- Bridge monitors ESP32 serial output
- Logs events to Supabase database
- Publishes to MQTT for web dashboard
- Website updates in real-time

## ⚙️ Requirements

- ESP32 on COM5
- Buttons on GPIO 16 (LEFT) and GPIO 27 (RIGHT)
- All hardware components connected per config.py

## 🔧 Troubleshooting

**"Failed to access COM5":**
- Unplug and replug ESP32
- Close other programs using the port

**Button not responding:**
- Check button connections (GPIO 16, 27)
- Ensure pull-up resistors enabled
- Try the other button

**Website not updating:**
- Make sure RUN.bat is running
- Check bridge sees "Gas detected!" or "RFID check request:" messages
- Verify Supabase connection
