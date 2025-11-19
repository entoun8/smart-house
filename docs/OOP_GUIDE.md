# OOP Component Guide

## What is OOP?

**Object-Oriented Programming (OOP)** means creating reusable "classes" for each component.

**Key benefit:** Pins are auto-loaded from config.py - no need to pass them!

---

## How to Use

### 1. Upload components library
```bash
ampy --port COM5 put micropython/components.py
```

### 2. Test it works
```bash
ampy --port COM5 run tests/test_oop.py
```

### 3. Use in your code
```python
from components import LED, RGBStrip, DHT

# Create objects (no pins needed!)
led = LED()
rgb = RGBStrip()
dht = DHT()

# Use them
led.on()
rgb.set_color(255, 0, 0)  # Red
data = dht.read()
```

---

## Available Classes

### Output Devices

**LED** - Simple LED
```python
led = LED()  # Auto-loads pin from config
led.on()
led.off()
led.blink(times=3, delay=0.5)
```

**RGBStrip** - RGB LED strip
```python
rgb = RGBStrip()  # Auto-loads pin and LED count
rgb.set_color(255, 0, 0)  # Red (r, g, b)
rgb.off()
```

**Buzzer** - Buzzer/alarm
```python
buzzer = Buzzer()
buzzer.on()
buzzer.off()
buzzer.beep(duration=0.5)
```

**Fan** - DC motor fan
```python
fan = Fan()
fan.on()
fan.off()
```

**DoorServo** - Door servo motor
```python
door = DoorServo()
door.set_angle(90)  # 0-180 degrees
door.open()  # 180°
door.close()  # 0°
```

**WindowServo** - Window servo motor
```python
window = WindowServo()
window.open()
window.close()
```

### Input Devices

**PIR** - Motion sensor
```python
pir = PIR()
if pir.motion_detected():
    print("Motion!")
```

**DHT** - Temperature & humidity
```python
dht = DHT()
data = dht.read()
if data:
    print(data['temp'])      # Temperature in °C
    print(data['humidity'])  # Humidity %
```

**GasSensor** - Gas detection
```python
gas = GasSensor()
level = gas.read()  # 0-4095
if gas.is_detected(threshold=2000):
    print("Gas detected!")
```

**WaterSensor** - Water/steam
```python
water = WaterSensor()
level = water.read()  # 0-4095
if water.is_wet(threshold=2000):
    print("Water detected!")
```

---

## Complete Example

```python
from components import LED, PIR, DHT, GasSensor

# Create components (no pins needed!)
led = LED()
pir = PIR()
dht = DHT()
gas = GasSensor()

# Main loop
while True:
    # Motion detection
    if pir.motion_detected():
        led.on()
    else:
        led.off()

    # Temperature check
    data = dht.read()
    if data and data['temp'] > 30:
        print("Hot!")

    # Gas check
    if gas.is_detected():
        print("⚠️ GAS!")

    time.sleep(1)
```

---

## Benefits

### Before OOP:
```python
# Messy - repeat everything
led_pin = Pin(12, Pin.OUT)
led_pin.on()
led_pin.off()

pir_pin = Pin(14, Pin.IN)
if pir_pin.value() == 1:
    print("Motion!")
```

### After OOP:
```python
# Clean - simple to use
led = LED()
led.on()
led.off()

pir = PIR()
if pir.motion_detected():
    print("Motion!")
```

---

## Tips

- All pins are in `config.py` - change there once
- No need to remember pin numbers
- Classes handle all hardware details
- Easy to read and understand
- Professional code style

---

## Next Steps

1. Test: `ampy --port COM5 run tests/test_oop.py`
2. Upload main: `ampy --port COM5 put micropython/main.py`
3. Customize main.py for your needs!
