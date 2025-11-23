# Task 8: Device Control (Web App)

**Last Updated:** 2025-11-23

---

## Requirements

From TASK_REQUIREMENTS.md:
- **Web App:** Open window and door via web app
- **Web App:** Turn on fan via web app

---

## Implementation

### ESP32 Side
- **File:** [tasks/device_control.py](../micropython/tasks/device_control.py)
- **Class:** `DeviceControlTask`
- **MQTT Subscription:** `ks5009/house/devices/+/command`

### Web App Side
- **Controls Page:** [app/controls/page.tsx](../web-app/app/controls/page.tsx)
- **Components:**
  - [DoorControl.tsx](../web-app/components/features/controls/devices/DoorControl.tsx)
  - [WindowControl.tsx](../web-app/components/features/controls/devices/WindowControl.tsx)
  - [FanControl.tsx](../web-app/components/features/controls/devices/FanControl.tsx)

---

## MQTT Topics

| Topic | Message | Action |
|-------|---------|--------|
| `ks5009/house/devices/door/command` | `open` / `close` | Open/close door servo |
| `ks5009/house/devices/window/command` | `open` / `close` | Open/close window servo |
| `ks5009/house/devices/fan/command` | `on` / `off` | Turn fan on/off |

---

## How It Works

```
1. User clicks button on web dashboard
   ↓
2. Web app publishes MQTT command
   (e.g., "ks5009/house/devices/door/command" → "open")
   ↓
3. HiveMQ broker routes message
   ↓
4. ESP32 subscribed to "ks5009/house/devices/+/command"
   receives the message
   ↓
5. DeviceControlTask.handle_command() processes it
   ↓
6. Actuator responds (door/window/fan)
```

---

## Code Overview

### ESP32 - DeviceControlTask

```python
class DeviceControlTask:
    def __init__(self, mqtt_wrapper):
        self.door = DoorServo()
        self.window = WindowServo()
        self.fan = Fan()
        self.mqtt = mqtt_wrapper
        self.mqtt.set_command_callback(self.handle_command)

    def handle_command(self, topic, message):
        msg = message.lower()

        if "door" in topic:
            if msg == "open":
                self.door.open()
            elif msg == "close":
                self.door.close()

        elif "window" in topic:
            if msg == "open":
                self.window.open()
            elif msg == "close":
                self.window.close()

        elif "fan" in topic:
            if msg == "on":
                self.fan.on()
            elif msg == "off":
                self.fan.off()
```

### Web App - Control Button

```typescript
// DoorControl.tsx
<Button onClick={() => sendCommand(TOPICS.doorCommand, "open", "Door")}>
  Open
</Button>
```

---

## Hardware Used

| Component | Pin | Function |
|-----------|-----|----------|
| Door Servo | GPIO 13 | Open/close door |
| Window Servo | GPIO 5 | Open/close window |
| Fan Motor | GPIO 18, 19 | Turn on/off fan |

---

## Key Features

- ✅ **Direct MQTT** - No bridge needed (ESP32 connects directly to HiveMQ)
- ✅ **Real-time** - Instant response when button clicked
- ✅ **Bidirectional** - Web → MQTT → ESP32
- ✅ **Integrated** - Part of main.py task loop

---

## Testing

1. Start ESP32 (main.py runs automatically)
2. Open web dashboard: http://localhost:3000/controls
3. Click Door/Window/Fan buttons
4. Observe actuators respond

---

## Status

✅ **100% COMPLETE**

- ✅ Door open/close via web
- ✅ Window open/close via web
- ✅ Fan on/off via web
- ✅ MQTT communication working
- ✅ Integrated in main.py
