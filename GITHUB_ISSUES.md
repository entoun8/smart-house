# GitHub Issues for Smart House Project

This file contains all the issues to create in GitHub for requirement tracking.

---

## Epic: ESP32 Hardware Automation

### Issue 1: LED Auto Control (Task 1)
**Title:** [STORY] LED Auto Control - Time-based automation (8pm-7am)

**Labels:** user-story, enhancement, esp32, task-1

**Description:**
## User Story
As a **homeowner**, I want **the LED to automatically turn on between 8pm and 7am** so that **I have lighting during nighttime without manual control**.

## Acceptance Criteria
- [ ] LED turns ON at 8pm (20:00)
- [ ] LED turns OFF at 7am (07:00)
- [ ] Time-based control works reliably
- [ ] No MQTT or database logging required

## Technical Details
- Component: Yellow LED
- Pin: GPIO 12
- Implementation: Time-based check in main loop
- File: `micropython/tasks/led_control.py`

## Definition of Done
- [x] Code implemented
- [x] Tested on hardware
- [x] Documentation updated

---

### Issue 2: Temperature & Humidity Logging (Task 2)
**Title:** [STORY] Temperature & Humidity Logging - Every 15 minutes

**Labels:** user-story, enhancement, esp32, web, database, task-2

**Description:**
## User Story
As a **homeowner**, I want **temperature and humidity logged every 15 minutes** so that **I can monitor climate conditions over time**.

## Acceptance Criteria
- [ ] DHT11 sensor reads temperature and humidity
- [ ] Data logged every 15 minutes (900 seconds)
- [ ] Combined data published to MQTT as JSON: `{"temp": 23, "humidity": 41}`
- [ ] Web app receives and stores data in database
- [ ] Current readings displayed on dashboard

## Technical Details
- Component: DHT11 Sensor
- Pin: GPIO 17
- MQTT Topic: `ks5009/house/sensors/climate`
- Database Table: `temperature_logs`
- Files:
  - ESP32: `micropython/tasks/temperature.py`
  - Web: `web-app/components/features/dashboard/TemperatureStatus.tsx`
  - Web: `web-app/components/features/dashboard/HumidityStatus.tsx`

## Definition of Done
- [x] Code implemented
- [x] Tested on hardware
- [x] Database logging works
- [x] Web dashboard displays data
- [x] Documentation updated

---

### Issue 3: PIR Motion Detection (Task 3)
**Title:** [STORY] PIR Motion Detection - RGB indicator and logging

**Labels:** user-story, enhancement, esp32, web, database, task-3

**Description:**
## User Story
As a **homeowner**, I want **motion detection to trigger a visual indicator and log events** so that **I can track activity in my home**.

## Acceptance Criteria
- [ ] PIR sensor detects motion
- [ ] RGB LED turns orange when motion detected
- [ ] Motion event published to MQTT
- [ ] Web app logs event to database
- [ ] Dashboard shows motion count

## Technical Details
- Components: PIR Sensor, RGB LEDs
- Pins: GPIO 14 (PIR), GPIO 26 (RGB)
- MQTT Topic: `ks5009/house/events/motion_detected`
- Database Table: `motion_logs`
- Files:
  - ESP32: `micropython/tasks/motion.py`
  - Web: `web-app/components/features/dashboard/MotionStatus.tsx`

## Definition of Done
- [x] Code implemented
- [x] Tested on hardware
- [x] RGB control works via RGBController
- [x] Database logging works
- [x] Web dashboard displays count
- [x] Documentation updated

---

### Issue 4: Steam Detection & Window Control (Task 4)
**Title:** [STORY] Steam Detection - Auto-close window with visual alert

**Labels:** user-story, enhancement, esp32, task-4

**Description:**
## User Story
As a **homeowner**, I want **the window to automatically close when steam is detected** so that **moisture doesn't damage my home**.

## Acceptance Criteria
- [ ] Water sensor detects moisture
- [ ] Window servo closes automatically
- [ ] RGB LED flashes blue as visual alert
- [ ] Window state published to MQTT

## Technical Details
- Components: Water Sensor, Window Servo, RGB LEDs
- Pins: GPIO 34 (Water), GPIO 5 (Window Servo), GPIO 26 (RGB)
- MQTT Topic: `ks5009/house/devices/window/state`
- File: `micropython/tasks/steam.py`

## Definition of Done
- [x] Code implemented
- [x] Tested on hardware
- [x] Window closes reliably
- [x] RGB visual feedback works
- [x] Documentation updated

---

### Issue 5: Gas Detection & Fan Control (Task 5)
**Title:** [STORY] Gas Detection - Auto-activate fan with alerts

**Labels:** user-story, enhancement, esp32, web, database, task-5

**Description:**
## User Story
As a **homeowner**, I want **the fan to automatically turn on when gas is detected** so that **hazardous gases are ventilated immediately**.

## Acceptance Criteria
- [ ] Gas sensor detects gas/flame
- [ ] Fan turns ON automatically
- [ ] RGB LED shows solid red
- [ ] Gas detection published to MQTT
- [ ] Fan state published to MQTT
- [ ] Web app logs event to database
- [ ] Dashboard shows gas alert

## Technical Details
- Components: Gas Sensor, Fan Motor, RGB LEDs
- Pins: GPIO 23 (Gas), GPIO 18/19 (Fan), GPIO 26 (RGB)
- MQTT Topics:
  - `ks5009/house/events/gas_detected`
  - `ks5009/house/devices/fan/state`
- Database Table: `gas_logs`
- Files:
  - ESP32: `micropython/tasks/gas.py`
  - Web: `web-app/components/features/dashboard/GasStatus.tsx`

## Definition of Done
- [x] Code implemented
- [x] Tested on hardware (30s warmup + debouncing)
- [x] Fan control works
- [x] RGB visual feedback works
- [x] Database logging works
- [x] Web dashboard shows alert
- [x] Documentation updated

---

### Issue 6: Asthma Alert System (Task 6)
**Title:** [STORY] Asthma Alert - LCD and web notification system

**Labels:** user-story, enhancement, esp32, web, task-6

**Description:**
## User Story
As a **person with asthma**, I want **to be alerted when air conditions are dangerous** so that **I can take preventive measures**.

## Acceptance Criteria
- [ ] System monitors temperature and humidity continuously
- [ ] Alert triggered when humidity > 50% AND temperature > 27°C
- [ ] LCD displays alert message
- [ ] MQTT message sent to web app
- [ ] Web dashboard shows alert

## Technical Details
- Components: DHT11, LCD1602
- Dependencies: Reads data from Task 2 (Temperature Task)
- MQTT Topic: `ks5009/house/events/asthma_alert`
- Files:
  - ESP32: `micropython/tasks/asthma.py`
  - Web: `web-app/components/features/dashboard/AsthmaAlert.tsx`

## Definition of Done
- [x] Code implemented
- [x] Tested on hardware
- [x] LCD displays correctly
- [x] Web dashboard shows alert
- [x] Documentation updated

---

### Issue 7: RFID Access Control (Task 7)
**Title:** [STORY] RFID Access Control - Secure door entry with logging

**Labels:** user-story, enhancement, esp32, web, database, task-7

**Description:**
## User Story
As a **homeowner**, I want **secure RFID-based door access** so that **only authorized people can enter my home**.

## Acceptance Criteria
- [ ] RFID reader scans cards
- [ ] Authorized card (0x7cdab502) opens door for 3 seconds
- [ ] Unauthorized card triggers RGB red flash and buzzer (3 times)
- [ ] All scans published to MQTT as JSON
- [ ] Web app logs all scans to database
- [ ] Web page displays scan history

## Technical Details
- Components: RFID RC522, Door Servo, Buzzer, RGB LEDs
- Pins: SPI (RFID), GPIO 13 (Door), GPIO 25 (Buzzer), GPIO 26 (RGB)
- Authorized Card: `0x7cdab502`
- MQTT Topics:
  - `ks5009/house/events/rfid_scan`
  - `ks5009/house/devices/door/state`
- Database Tables: `rfid_scans`, `users`
- Files:
  - ESP32: `micropython/tasks/access_control.py`
  - Web: `web-app/app/(main)/rfid/page.tsx`

## Definition of Done
- [x] Code implemented
- [x] Tested on hardware
- [x] Door opens for authorized card
- [x] Alert works for unauthorized card
- [x] Database logging works
- [x] Web page shows history
- [x] Documentation updated

---

### Issue 8: Web-Based Device Control (Task 8)
**Title:** [STORY] Web Device Control - Remote control of door, window, and fan

**Labels:** user-story, enhancement, web, esp32, task-8

**Description:**
## User Story
As a **homeowner**, I want **to control my smart home devices from a web interface** so that **I can manage my home remotely**.

## Acceptance Criteria
- [ ] Web app has control buttons for door, window, and fan
- [ ] Clicking buttons publishes commands to MQTT
- [ ] ESP32 subscribes to command topics
- [ ] ESP32 executes commands (open/close/on/off)
- [ ] ESP32 publishes state updates to MQTT
- [ ] Web app displays real-time device status

## Technical Details
- MQTT Topics (Commands - Web → ESP32):
  - `ks5009/house/devices/door/command`
  - `ks5009/house/devices/window/command`
  - `ks5009/house/devices/fan/command`
- MQTT Topics (States - ESP32 → Web):
  - `ks5009/house/devices/door/state`
  - `ks5009/house/devices/window/state`
  - `ks5009/house/devices/fan/state`
- Files:
  - ESP32: `micropython/tasks/device_control.py`
  - Web: `web-app/components/features/controls/`

## Definition of Done
- [x] Code implemented
- [x] Tested on hardware
- [x] Web controls work reliably
- [x] Real-time status updates work
- [x] Bi-directional communication verified
- [x] Documentation updated

---

## Epic: Web Dashboard Features

### Issue 9: Dashboard - Temperature Display
**Title:** [FEATURE] Dashboard - Display current temperature in celsius

**Labels:** enhancement, web, dashboard

**Description:**
Display real-time temperature data from DHT11 sensor on the web dashboard.

**Acceptance Criteria:**
- [ ] Live temperature display
- [ ] Updates automatically via MQTT
- [ ] Appropriate icon/styling
- [ ] Shows °C unit

**Status:** ✅ Complete

---

### Issue 10: Dashboard - Humidity Display
**Title:** [FEATURE] Dashboard - Display current humidity as percentage

**Labels:** enhancement, web, dashboard

**Description:**
Display real-time humidity data from DHT11 sensor on the web dashboard.

**Acceptance Criteria:**
- [ ] Live humidity display
- [ ] Updates automatically via MQTT
- [ ] Appropriate icon/styling
- [ ] Shows % unit

**Status:** ✅ Complete

---

### Issue 11: Dashboard - Gas Alert Display
**Title:** [FEATURE] Dashboard - Gas detection alert notification

**Labels:** enhancement, web, dashboard, alert

**Description:**
Show visual alert on dashboard when gas is detected.

**Acceptance Criteria:**
- [ ] Real-time notification
- [ ] Clear visual indicator
- [ ] Updates via MQTT
- [ ] Shows current gas detection status

**Status:** ✅ Complete

---

### Issue 12: Dashboard - Motion Detection Counter
**Title:** [FEATURE] Dashboard - PIR detection count in last hour

**Labels:** enhancement, web, dashboard

**Description:**
Display the number of motion detection events in the last hour.

**Acceptance Criteria:**
- [ ] Counter display
- [ ] Auto-refresh
- [ ] Time-based filtering (last 60 minutes)
- [ ] Updates from database

**Status:** ✅ Complete

---

### Issue 13: RFID Logs Page
**Title:** [FEATURE] RFID Access Logs - View and filter scan history

**Labels:** enhancement, web, rfid

**Description:**
Web page showing all RFID scan attempts with filtering capability.

**Acceptance Criteria:**
- [ ] Display all scan attempts
- [ ] Show: Card ID, Timestamp, Success/Fail status
- [ ] Filter: All / Successful / Failed
- [ ] Pagination support
- [ ] Real-time updates

**Status:** ✅ Complete

---

### Issue 14: Device Status Display
**Title:** [FEATURE] Dashboard - Device status indicators

**Labels:** enhancement, web, dashboard

**Description:**
Show real-time status of door, window, and fan on dashboard.

**Acceptance Criteria:**
- [ ] Door status (open/closed)
- [ ] Window status (open/closed)
- [ ] Fan status (on/off)
- [ ] Real-time updates via MQTT
- [ ] Visual indicators

**Status:** ✅ Complete

---

## Epic: Database & Backend

### Issue 15: Database Schema Setup
**Title:** [SETUP] Database - Create all required tables

**Labels:** setup, database

**Description:**
Set up Supabase database with all required tables for the smart house system.

**Tables:**
- users
- temperature_logs
- motion_logs
- gas_logs
- rfid_scans

**Status:** ✅ Complete

---

## Epic: Documentation

### Issue 16: Project Documentation
**Title:** [DOCS] Complete project documentation

**Labels:** documentation

**Description:**
Comprehensive documentation for the entire smart house project.

**Files:**
- START_HERE_CLAUDE.md
- PROJECT_GUIDE.md
- PROJECT_STATUS.md
- ARCHITECTURE.md
- TASK_REQUIREMENTS.md

**Status:** ✅ Complete

---

## How to Create These Issues on GitHub

### Option 1: Manual Creation
1. Go to: https://github.com/entoun8/smart-house/issues
2. Click "New Issue"
3. Copy/paste each issue description above
4. Add appropriate labels
5. Click "Submit new issue"

### Option 2: Using GitHub CLI (if installed)
```bash
# Install GitHub CLI first
# Then authenticate
gh auth login

# Create issues from this file (requires scripting)
```

### Option 3: Using GitHub API (Python script)
Create a Python script to automatically create all issues using GitHub's REST API.

---

## Project Board Setup

After creating issues:

1. Go to: https://github.com/entoun8/smart-house/projects
2. Click "New project"
3. Choose "Board" template
4. Name it "Smart House Development"
5. Add columns:
   - 📋 Backlog
   - 🚧 In Progress
   - ✅ Done
6. Add all issues to the board
7. Move completed issues to "Done"

---

## Labels to Create

Go to: https://github.com/entoun8/smart-house/labels

Create these labels:
- `user-story` (blue)
- `enhancement` (green)
- `bug` (red)
- `documentation` (gray)
- `esp32` (purple)
- `web` (cyan)
- `database` (yellow)
- `task-1` through `task-8` (orange)
- `alert` (red)
- `rfid` (pink)
- `dashboard` (blue)
- `setup` (gray)
