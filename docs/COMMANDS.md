# Quick Command Reference

All the commands you need for your smart home project.

---

## 🔧 Setup Commands (One-Time)

### Install Tools
```bash
# Install esptool (for flashing firmware)
pip install esptool

# Install ampy (for uploading files)
pip install adafruit-ampy

# Install pyserial (for serial terminal)
pip install pyserial
```

### Flash MicroPython (One-Time Setup)
```bash
# 1. Erase ESP32
python -m esptool --chip esp32 --port COM5 erase_flash

# 2. Flash MicroPython
python -m esptool --chip esp32 --port COM5 --baud 460800 write_flash -z 0x1000 firmware/esp32-micropython.bin
```

---

## 📤 File Upload Commands

### Upload Single File
```bash
# Upload main program
ampy --port COM5 put micropython/main.py

# Upload config
ampy --port COM5 put micropython/config.py

# Upload library
ampy --port COM5 put micropython/lib/neopixel.py
```

### Upload Entire Folder
```bash
# Upload lib folder
ampy --port COM5 put micropython/lib
```

### Download File from ESP32
```bash
# Download main.py from ESP32
ampy --port COM5 get main.py

# Download to specific location
ampy --port COM5 get main.py > backup_main.py
```

---

## 🧪 Testing Commands

### Run Individual Tests
```bash
# Test LED
ampy --port COM5 run tests/test_led.py

# Test buzzer
ampy --port COM5 run tests/test_buzzer.py

# Test motion sensor
ampy --port COM5 run tests/test_pir.py

# Test temperature
ampy --port COM5 run tests/test_dht.py

# Test RGB LEDs
ampy --port COM5 run tests/test_rgb.py

# Test door servo
ampy --port COM5 run tests/test_door.py

# Test window servo
ampy --port COM5 run tests/test_window.py

# Test WiFi
ampy --port COM5 run tests/test_wifi.py

# Test ALL hardware
ampy --port COM5 run tests/test_all_hardware.py
```

---

## 💻 ESP32 Terminal Access

### Connect to REPL (Python Prompt)
```bash
# Access Python shell on ESP32
python -m serial.tools.miniterm COM5 115200

# Exit: Press Ctrl+]
```

### Run Code Directly in REPL
```python
>>> print("Hello ESP32!")
Hello ESP32!

>>> from machine import Pin
>>> led = Pin(12, Pin.OUT)
>>> led.on()
```

---

## 📁 File Management

### List Files on ESP32
```bash
ampy --port COM5 ls

# List specific folder
ampy --port COM5 ls /lib
```

### Delete File from ESP32
```bash
ampy --port COM5 rm main.py

# Delete folder
ampy --port COM5 rmdir lib
```

### Create Directory
```bash
ampy --port COM5 mkdir lib
```

---

## 🔍 Debugging Commands

### Check COM Port
```bash
# Windows - List ports
python -m serial.tools.list_ports

# Should show: COM5
```

### Test Connection
```bash
# Quick test - list files
ampy --port COM5 ls

# If works → Connection is good
# If fails → Check USB cable, try different port
```

### Reset ESP32
```bash
# Soft reset (in REPL)
>>> import machine
>>> machine.reset()

# Or just unplug and replug USB
```

---

## 🚀 Development Workflow

### Standard Workflow
```bash
# 1. Write code on computer (in VSCode)
# Edit: micropython/main.py

# 2. Upload to ESP32
ampy --port COM5 put micropython/main.py

# 3. Connect to see output
python -m serial.tools.miniterm COM5 115200

# 4. Press Ctrl+D in terminal to run main.py

# 5. View output, debug, repeat
```

### Quick Test Workflow
```bash
# 1. Write test code

# 2. Run without uploading (temporary)
ampy --port COM5 run tests/test_new_feature.py

# 3. If works, add to main.py
```

---

## 🌐 WiFi Commands (In REPL)

### Connect to WiFi
```python
>>> import network
>>> wlan = network.WLAN(network.STA_IF)
>>> wlan.active(True)
>>> wlan.connect("CyFi", "SecurityA40")
>>> wlan.isconnected()
True
>>> wlan.ifconfig()
('10.52.126.34', '255.255.254.0', '10.52.126.1', '96.45.45.45')
```

### Check WiFi Status
```python
>>> wlan.isconnected()
True  # Connected
# or
False  # Not connected

>>> wlan.status()
# Various status codes
```

---

## 🔧 Common Fixes

### Fix: "Can't connect to COM5"
```bash
# 1. Unplug ESP32
# 2. Plug it back in
# 3. Try again
ampy --port COM5 ls
```

### Fix: "Module not found"
```bash
# Upload missing library
ampy --port COM5 put micropython/lib/neopixel.py

# Verify it's there
ampy --port COM5 ls /lib
```

### Fix: "Timeout waiting for EOF"
```bash
# ESP32 is busy or crashed
# Solution: Reset ESP32
# Unplug and replug USB
```

---

## 📊 Project Commands

### Full Deploy (Upload Everything)
```bash
# Upload config
ampy --port COM5 put micropython/config.py

# Upload libraries
ampy --port COM5 put micropython/lib/neopixel.py

# Upload main program
ampy --port COM5 put micropython/main.py

# Reset to run
# Unplug and replug ESP32
```

### Backup Everything
```bash
# Download all files from ESP32
ampy --port COM5 get main.py > backup/main.py
ampy --port COM5 get config.py > backup/config.py
```

---

## 🎯 Most Common Commands (Cheat Sheet)

```bash
# Test hardware
ampy --port COM5 run tests/test_all_hardware.py

# Upload main program
ampy --port COM5 put micropython/main.py

# Connect to terminal
python -m serial.tools.miniterm COM5 115200

# List files
ampy --port COM5 ls

# Test WiFi
ampy --port COM5 run tests/test_wifi.py
```

---

## 🐛 Debugging Tips

### See Real-Time Output
```bash
# 1. Upload your code
ampy --port COM5 put micropython/main.py

# 2. Connect terminal BEFORE resetting
python -m serial.tools.miniterm COM5 115200

# 3. Press Ctrl+D to run main.py
# or unplug/replug ESP32

# 4. See all print() output in terminal
```

### Add Debug Prints
```python
# In your code
print("DEBUG: Motion detected!")
print(f"DEBUG: Temperature = {temp}")
```

---

## 📱 MQTT Commands (In Code)

### Connect to MQTT
```python
from umqtt.simple import MQTTClient

mqtt = MQTTClient("smart_home", "broker.hivemq.com")
mqtt.connect()
mqtt.publish("home/test", "Hello MQTT!")
```

### Subscribe to Topic
```python
def callback(topic, msg):
    print(f"Received: {msg}")

mqtt.set_callback(callback)
mqtt.subscribe("home/commands")
```

---

## 🎓 Command Patterns

### Pattern: Upload + Run
```bash
# Upload file and immediately run it
ampy --port COM5 put micropython/main.py && \
python -m serial.tools.miniterm COM5 115200
```

### Pattern: Test → Upload → Deploy
```bash
# 1. Test locally
ampy --port COM5 run tests/test_led.py

# 2. If works, integrate into main
# Edit main.py

# 3. Upload
ampy --port COM5 put micropython/main.py
```

---

## 🔄 Auto-Run on Boot

### Make Code Run Automatically

**ESP32 looks for these files on boot:**
1. `boot.py` (runs first)
2. `main.py` (runs second)

**To auto-run your code:**
```bash
# Upload as main.py
ampy --port COM5 put micropython/smart_home.py main.py

# Now it runs automatically when ESP32 powers on!
```

---

## 💡 Pro Tips

### Tip 1: Use --delay for Reliability
```bash
# If upload fails, add delay
ampy --port COM5 --delay 1 put micropython/main.py
```

### Tip 2: Batch Operations
```bash
# Upload multiple files
ampy --port COM5 put micropython/config.py && \
ampy --port COM5 put micropython/main.py && \
ampy --port COM5 put micropython/lib/neopixel.py
```

### Tip 3: Quick File Check
```bash
# See what's on ESP32
ampy --port COM5 ls

# Check file content
ampy --port COM5 get main.py
```

---

## 🎯 Your Current Project Status

### What's Already Uploaded
- ✅ `lib/neopixel.py` (RGB LED library)

### What's NOT Uploaded Yet
- ⏳ `config.py` (pin configuration)
- ⏳ `main.py` (main program - not created yet)

### Next Commands You'll Use
```bash
# When you create main.py:
ampy --port COM5 put micropython/config.py
ampy --port COM5 put micropython/main.py

# To run it:
python -m serial.tools.miniterm COM5 115200
# Press Ctrl+D
```

---

## 📚 Full Command Reference

### ampy Commands
```bash
ampy --help                    # Show all commands
ampy --port COM5 ls            # List files
ampy --port COM5 put <file>    # Upload file
ampy --port COM5 get <file>    # Download file
ampy --port COM5 rm <file>     # Delete file
ampy --port COM5 run <file>    # Run file (temporary)
ampy --port COM5 mkdir <dir>   # Create directory
ampy --port COM5 rmdir <dir>   # Delete directory
```

### esptool Commands
```bash
python -m esptool --help                           # Show help
python -m esptool --chip esp32 --port COM5 erase_flash   # Erase
python -m esptool --chip esp32 --port COM5 write_flash   # Flash
```

### Serial Terminal
```bash
python -m serial.tools.miniterm COM5 115200   # Connect
# Ctrl+]  = Exit
# Ctrl+D  = Run main.py
# Ctrl+C  = Interrupt running program
```

---

**Save this file - it has every command you'll need!** 🎉
