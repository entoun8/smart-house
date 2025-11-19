# Task 6: Asthma Alert System - Complete Guide

**Status:** ✅ **COMPLETE**

---

## 📋 Requirements

### ESP32 (Hardware)
- Show asthma alert on LCD if:
  - Humidity > 50% **AND**
  - Temperature > 27°C

### Web App (Dashboard)
- Display asthma alert on dashboard in real-time

### Database
- **NOT REQUIRED** (requirements don't specify logging)

---

## 🎯 Implementation Summary

**Pattern:** Simple + MQTT (like Task 4, but with MQTT for web display)

**Components:**
- LCD1602 display (I2C) - Shows alert message
- DHT11 sensor - Already used in Task 2 for temp/humidity
- MQTT - For web dashboard real-time updates
- No database - Not required by specifications

---

## 📁 Files Created/Modified

### ESP32 Code
1. **[micropython/task6_asthma_alert.py](../micropython/task6_asthma_alert.py)** ✅
   - Standalone Task 6 implementation
   - Monitors DHT sensor continuously
   - Displays alert on LCD when conditions met
   - Publishes to MQTT for web dashboard

2. **[micropython/components/displays/lcd.py](../micropython/components/displays/lcd.py)** ✅
   - Enhanced LCD component with proper I2C handling
   - Added `display_alert()` method for 2-line messages
   - Auto-detects LCD address (0x27 or 0x3F)

3. **[micropython/all_tasks.py](../micropython/all_tasks.py)** ✅
   - Integrated Task 6 into main combined script
   - Shares DHT readings with Task 2 (efficient!)
   - Checks asthma conditions every 30 minutes with temp logging

### Web App
1. **[web-app/components/features/dashboard/AsthmaAlert.tsx](../web-app/components/features/dashboard/AsthmaAlert.tsx)** ✅
   - Converted from prop-based to MQTT-based
   - Subscribes to `ks5009/house/events/asthma_alert` topic
   - Shows alert card only when active
   - Auto-clears after 60 seconds if no update

2. **[web-app/lib/mqtt.ts](../web-app/lib/mqtt.ts)** ✅
   - Added `asthma` topic to TOPICS object
   - Topic: `ks5009/house/events/asthma_alert`

3. **[web-app/components/features/dashboard/DashboardContent.tsx](../web-app/components/features/dashboard/DashboardContent.tsx)** ✅
   - Already includes AsthmaAlert component
   - Updated to use MQTT-based component (no props needed)

---

## 🔄 How It Works

### Flow Diagram

```
┌─────────────┐
│ DHT11       │ Reads temp & humidity every 30 min (Task 2)
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│ Task 6: Check Conditions                │
│ If humidity > 50% AND temp > 27°C       │
└──────┬──────────────────────────────────┘
       │
       ├─────────────────┬─────────────────┐
       ▼                 ▼                 ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ LCD Display │   │ Serial Log  │   │ MQTT Publish│
│ Shows Alert │   │ "ASTHMA     │   │ Value: "1"  │
│ 2 Lines     │   │  ALERT!"    │   │             │
└─────────────┘   └─────────────┘   └──────┬──────┘
                                            │
                                            ▼
                                    ┌─────────────┐
                                    │ Web App     │
                                    │ Shows Alert │
                                    │ Card        │
                                    └─────────────┘
```

### Step-by-Step Process

1. **Task 2 reads DHT sensor** every 30 minutes
2. **Task 6 uses the same reading** (efficient!)
3. **Check conditions:** `humidity > 50 AND temp > 27`
4. **If TRUE:**
   - Display on LCD: "! ASTHMA ALERT !" / "H>50% T>27C"
   - Print to serial: "⚠️  ASTHMA ALERT!"
   - Publish MQTT: `ks5009/house/events/asthma_alert` = `"1"`
5. **Web dashboard receives MQTT message**
6. **Alert card appears** with red border and warning icon
7. **If FALSE (conditions clear):**
   - Display normal readings on LCD: "Temp: 25C" / "Humidity: 45%"
   - Publish MQTT: `ks5009/house/events/asthma_alert` = `"0"`
   - Alert card disappears from web
8. **When no alert:**
   - LCD continuously shows current temperature and humidity
   - Updates every 5 seconds (standalone) or every 30 minutes (all_tasks)

---

## 💻 Code Examples

### ESP32 - Check Asthma Conditions

```python
def check_asthma_conditions(temp, humidity):
    """Check if asthma alert conditions are met"""
    return humidity > 50 and temp > 27

def handle_asthma_alert():
    """Handle asthma alert"""
    print("⚠️  ASTHMA ALERT!")

    # Display on LCD
    if lcd.is_connected():
        lcd.display_alert("! ASTHMA ALERT !", "H>50% T>27C")

    # Publish to MQTT
    if mqtt.is_connected():
        mqtt.publish(TOPICS.event("asthma_alert"), "1")

def handle_asthma_cleared(temp, humidity):
    """Handle when alert clears - show normal readings"""
    print("✅ Asthma alert cleared")

    # Display normal readings on LCD
    if lcd.is_connected():
        lcd.display_alert(f"Temp: {temp}C", f"Humidity: {humidity}%")

    if mqtt.is_connected():
        mqtt.publish(TOPICS.event("asthma_alert"), "0")

def update_normal_display(temp, humidity):
    """Update LCD with current readings when no alert"""
    if lcd.is_connected():
        lcd.display_alert(f"Temp: {temp}C", f"Humidity: {humidity}%")
```

### Web App - Subscribe to Alert

```typescript
useEffect(() => {
  const client = connectMQTT();

  client.on("connect", () => {
    client.subscribe(TOPICS.asthma, (err) => {
      if (!err) console.log("Subscribed to asthma alerts");
    });
  });

  client.on("message", (topic, message) => {
    if (topic === TOPICS.asthma) {
      const msg = message.toString();
      if (msg === "1") {
        setAlertActive(true);  // Show alert
      } else if (msg === "0") {
        setAlertActive(false);  // Hide alert
      }
    }
  });
}, []);
```

---

## 🧪 Testing

### Test LCD Display

```bash
# Test LCD component
ampy --port COM4 run tests/test_lcd.py

# Expected output:
# ✓ LCD initialized at address 0x27
# ✓ Text displayed: "Smart House" / "ESP32 Ready!"
```

### Test Task 6 Standalone

```bash
# Run Task 6 only
ampy --port COM4 run micropython/task6_asthma_alert.py

# Manually trigger by:
# 1. Heat up DHT sensor (>27°C)
# 2. Add humidity (breathe on it for >50%)
```

### Test in All Tasks

```bash
# Run all tasks including Task 6
ampy --port COM4 run micropython/all_tasks.py

# Monitor serial output
# Every 30 minutes it will check conditions
```

### Test Web Dashboard

1. Start web app: `npm run dev`
2. Open browser: `http://localhost:3000`
3. Trigger alert on ESP32
4. Watch alert card appear on dashboard

---

## 🎛️ Configuration

### MQTT Topic

```python
# config.py
TOPICS.event("asthma_alert")  # Expands to:
# "ks5009/house/events/asthma_alert"
```

### Alert Thresholds

```python
# To change thresholds, edit:
def check_asthma_conditions(temp, humidity):
    return humidity > 50 and temp > 27  # Change these values
```

### LCD I2C Address

```python
# LCD auto-detects, but if needed:
# micropython/components/displays/lcd.py
self.addr = 0x27  # Common addresses: 0x27 or 0x3F
```

---

## 📊 MQTT Message Format

### Alert Active
```
Topic: ks5009/house/events/asthma_alert
Payload: "1"
```

### Alert Cleared
```
Topic: ks5009/house/events/asthma_alert
Payload: "0"
```

---

## 🔧 Troubleshooting

### LCD Not Working

**Problem:** LCD doesn't display anything

**Solutions:**
1. Check I2C connection (SCL=GPIO22, SDA=GPIO21)
2. Check LCD address: Run `tests/test_lcd.py` to scan
3. Adjust contrast potentiometer on back of LCD
4. Verify power (VCC to 5V, GND to GND)

### LCD Shows Old Temperature

**Problem:** LCD displays outdated temperature/humidity values

**Solutions:**
1. In standalone mode: LCD updates every 5 seconds automatically
2. In all_tasks mode: LCD updates every 30 minutes with DHT reading
3. Check if DHT sensor is working: Run `tests/test_dht.py`
4. Verify update interval in code: `DISPLAY_UPDATE_INTERVAL = 5`

### Alert Not Appearing on Web

**Problem:** Web dashboard doesn't show alert

**Solutions:**
1. Check MQTT connection in browser console
2. Verify MQTT broker is public (broker.hivemq.com)
3. Check topic subscription: `TOPICS.asthma`
4. Trigger alert manually by publishing MQTT:
   ```bash
   mosquitto_pub -h broker.hivemq.com -t "ks5009/house/events/asthma_alert" -m "1"
   ```

### Alert Triggers at Wrong Values

**Problem:** Alert shows when temp/humidity are below threshold

**Solutions:**
1. Verify DHT sensor readings: Run `tests/test_dht.py`
2. Check threshold logic in `check_asthma_conditions()`
3. Print values before checking:
   ```python
   print(f"Checking: T={temp}°C, H={humidity}%")
   ```

---

## ✅ Completion Checklist

- [x] ESP32 displays alert on LCD when conditions met
- [x] ESP32 publishes to MQTT for web dashboard
- [x] Web dashboard shows alert in real-time
- [x] Web dashboard hides alert when cleared
- [x] Integrated into all_tasks.py
- [x] Efficient (shares DHT reading with Task 2)
- [x] Simple (no database, not required)
- [x] LCD component enhanced with proper I2C

---

## 🎯 Key Features

✅ **Simple Implementation** - Only what's required
✅ **Efficient** - Shares DHT reading with Task 2
✅ **Real-time Web Updates** - Uses MQTT
✅ **Visual Feedback** - LCD display + Web alert
✅ **Auto-clear** - Alert disappears when conditions clear
✅ **No Database** - Not required, kept simple
✅ **Always-On Display** - LCD shows current temp/humidity when no alert

---

## 📈 Next Steps

Task 6 is complete! Remaining task:

- **Task 7: RFID Access Control** (Most complex - includes database, MQTT, web controls)

---

**Task 6 Status:** ✅ **100% COMPLETE**

**Pattern Used:** Simple + MQTT (Perfect for alerts with web display)

**Total Implementation Time:** ~30 minutes
