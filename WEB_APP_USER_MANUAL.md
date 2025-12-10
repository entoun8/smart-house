# Smart House Web Dashboard - User Manual

**Version:** 1.0
**Last Updated:** December 10, 2025
**Live Dashboard:** https://gregarious-semifreddo-257864.netlify.app/

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Dashboard Overview](#dashboard-overview)
4. [Features Guide](#features-guide)
   - [Real-Time Monitoring](#real-time-monitoring)
   - [Device Controls](#device-controls)
   - [RFID Access Logs](#rfid-access-logs)
5. [Navigation](#navigation)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## Introduction

Welcome to the **Smart House IoT Dashboard**! This web application allows you to monitor and control your smart home system in real-time. The dashboard connects to your ESP32 device and displays sensor data, alerts, and provides remote control capabilities for your home devices.

### What Can You Do?

- **Monitor** temperature, humidity, motion, and gas levels in real-time
- **Control** doors, windows, and fans remotely
- **View** RFID access logs and security events
- **Receive** automatic alerts for asthma triggers and gas detection
- **Track** environmental conditions over time

---

## Getting Started

### Accessing the Dashboard

1. Open your web browser (Chrome, Firefox, Safari, or Edge)
2. Navigate to: **https://gregarious-semifreddo-257864.netlify.app/**
   - Or for local development: `http://localhost:3000`
3. The dashboard will automatically load

### System Requirements

- **Browser:** Modern web browser with JavaScript enabled
- **Internet Connection:** Required for real-time updates
- **ESP32 Device:** Must be powered on and connected to WiFi

### First-Time Setup

When you first access the dashboard:

1. The system will attempt to connect to the MQTT broker automatically
2. You'll see connection status in the browser console
3. Once connected, live data will start appearing within seconds
4. If you see "No data available," ensure your ESP32 is powered on

---

## Dashboard Overview

The web application has **3 main pages**:

| Page | Purpose | What You'll See |
|------|---------|-----------------|
| **Dashboard** | Monitor sensors & alerts | Temperature, humidity, motion count, gas status, asthma alerts |
| **Controls** | Operate devices remotely | Door, window, and fan controls with real-time status |
| **RFID Logs** | View access history | Complete log of all RFID card scans with success/fail status |

### Interface Layout

```
┌─────────────────────────────────────────────────────┐
│  Smart House Dashboard        [Theme Toggle] [Menu] │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [Current Page Content]                             │
│                                                     │
│  • Dashboard: Sensor cards                          │
│  • Controls: Device control buttons                 │
│  • RFID: Access logs table                          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Features Guide

### Real-Time Monitoring

The main **Dashboard** page displays live sensor data from your smart home.

#### 1. Temperature Status

**Location:** Top-left card
**Icon:** Thermometer 🌡️

**What It Shows:**
- Current temperature in Celsius (°C)
- Updates automatically every 15 minutes
- Data from DHT11 sensor on ESP32

**Example Display:**
```
🌡️ Temperature
23°C
```

**Status Indicators:**
- **Green:** Normal temperature (below 27°C)
- **Red:** High temperature (27°C or above - asthma risk)

---

#### 2. Humidity Status

**Location:** Top-center card
**Icon:** Water droplet 💧

**What It Shows:**
- Current humidity percentage (%)
- Updates automatically every 15 minutes
- Data from DHT11 sensor on ESP32

**Example Display:**
```
💧 Humidity
41%
```

**Status Indicators:**
- **Green:** Normal humidity (below 50%)
- **Red:** High humidity (50% or above - asthma risk)

---

#### 3. Motion Detection Count

**Location:** Top-right card
**Icon:** Motion sensor 🚶

**What It Shows:**
- Number of motion detections in the last hour
- Resets automatically every hour
- Detects movement via PIR sensor

**Example Display:**
```
🚶 Motion Detected (Last Hour)
5 detections
```

**How It Works:**
- PIR sensor detects movement
- RGB LED on ESP32 turns orange
- Count increments on dashboard
- Historical data saved to database

---

#### 4. Gas Detection Alert

**Location:** Bottom-left card
**Icon:** Warning ⚠️

**What It Shows:**
- Current gas sensor status
- Real-time detection alerts
- Automatic fan activation status

**Display States:**

**Normal (No Gas Detected):**
```
✓ Gas Status
No gas detected
```
- Green checkmark
- Safe status message

**Alert (Gas Detected):**
```
⚠️ GAS DETECTED!
Ventilation activated
```
- Red warning badge
- Automatic fan turned on
- RGB LED on ESP32 shows solid red
- Event logged to database

---

#### 5. Asthma Alert

**Location:** Full-width banner below sensor cards
**Icon:** Health alert ⚕️

**What It Shows:**
- Active warning when asthma trigger conditions are met
- Displays on both web dashboard and ESP32 LCD screen

**Trigger Conditions:**
- Humidity > 50% **AND**
- Temperature > 27°C

**Display When Active:**
```
⚠️ ASTHMA ALERT
High humidity (52%) and temperature (28°C) detected.
Environment may trigger asthma symptoms.
```

**Display When Inactive:**
- Alert banner is hidden
- Normal sensor cards show current values

**What to Do:**
- Increase ventilation
- Use air conditioning to reduce temperature
- Use dehumidifier if available
- Monitor sensor readings

---

### Device Controls

The **Controls** page lets you remotely operate smart home devices.

**Location:** Click "Controls" in navigation menu

#### How Remote Control Works

1. You click a button on the web dashboard
2. Command is sent via MQTT to ESP32
3. ESP32 receives command and operates the device
4. ESP32 confirms new status back to web dashboard
5. Dashboard updates to show current state

**Response Time:** Typically 1-2 seconds

---

#### 1. Door Control

**Component:** Servo motor on GPIO 13

**Controls:**
- **OPEN** button - Opens the door
- **CLOSE** button - Closes the door

**Status Display:**
```
Door Status: OPEN ✅
Door Status: CLOSED 🔒
```

**Color Indicators:**
- **Green:** Door is open
- **Gray:** Door is closed

**Automatic Operations:**
- Authorized RFID card scan automatically opens door for 3 seconds
- Door closes automatically after timeout

**Safety Note:** Ensure no obstructions before operating remotely

---

#### 2. Window Control

**Component:** Servo motor on GPIO 5

**Controls:**
- **OPEN** button - Opens the window
- **CLOSE** button - Closes the window

**Status Display:**
```
Window Status: OPEN ✅
Window Status: CLOSED 🔒
```

**Color Indicators:**
- **Green:** Window is open
- **Gray:** Window is closed

**Automatic Operations:**
- Window automatically closes when steam/moisture is detected
- RGB LED flashes blue when auto-close activates

---

#### 3. Fan Control

**Component:** DC motor on GPIO 18 & 19

**Controls:**
- **ON** button - Turns fan on
- **OFF** button - Turns fan off

**Status Display:**
```
Fan Status: ON ✅
Fan Status: OFF ⭕
```

**Color Indicators:**
- **Green:** Fan is running
- **Gray:** Fan is off

**Automatic Operations:**
- Fan automatically turns ON when gas is detected
- Fan stays ON until gas sensor clears
- RGB LED shows solid red during automatic activation
- You can manually override after automatic activation

**Use Cases:**
- Ventilation when cooking
- Air circulation
- Emergency gas/smoke evacuation

---

### RFID Access Logs

The **RFID Logs** page shows complete access history and security events.

**Location:** Click "RFID Logs" in navigation menu

#### Statistics Overview

**Top Section** displays summary cards:

```
┌─────────────────┬─────────────────┬─────────────────┐
│  Total Scans    │  Successful     │  Failed         │
│       15        │       12        │       3         │
└─────────────────┴─────────────────┴─────────────────┘
```

- **Total Scans:** All RFID card attempts (authorized + unauthorized)
- **Successful:** Authorized cards that opened the door
- **Failed:** Unauthorized cards that were rejected

---

#### Access Logs Table

**Table Columns:**

| Column | Description |
|--------|-------------|
| **Card ID** | Unique identifier of the scanned RFID card |
| **User** | Name of authorized user (if registered) or "Unknown" |
| **Status** | Success ✅ / Failed ❌ |
| **Timestamp** | Date and time of scan |

**Example Table:**
```
Card ID      User        Status      Timestamp
0x7cdab502   John Doe    Success ✅  Dec 10, 2025, 2:30 PM
0x1a2b3c4d   Unknown     Failed ❌   Dec 10, 2025, 2:25 PM
0x7cdab502   John Doe    Success ✅  Dec 10, 2025, 9:15 AM
```

---

#### Filter Options

Use the dropdown menu to filter scan results:

**Filter Types:**
- **All Scans** - Shows every card scan attempt
- **Successful Only** - Shows only authorized access
- **Failed Only** - Shows only unauthorized attempts

**How to Filter:**
1. Click the filter dropdown at the top of the table
2. Select your desired filter
3. Table updates automatically

**Use Cases:**
- **All Scans:** Daily security review
- **Successful:** Track authorized user activity
- **Failed:** Security monitoring for intrusion attempts

---

#### Pagination

If you have more than 10 scans, use pagination controls at the bottom:

- **Previous** button - View older entries
- **Page numbers** - Jump to specific page
- **Next** button - View newer entries

**Display:** Shows 10 entries per page by default

---

#### Latest Scan Highlight

The most recent scan appears at the top of the table and may be highlighted.

**Real-Time Updates:**
- New scans appear automatically (no page refresh needed)
- Table updates within 1-2 seconds of card scan
- Statistics counters update in real-time

---

## Navigation

### Main Menu

Access the menu using the **hamburger icon** (☰) in the top-right corner.

**Menu Options:**
- **Dashboard** - Main sensor monitoring page
- **Controls** - Device control page
- **RFID Logs** - Access history page

**Quick Navigation:**
- Click any menu item to navigate instantly
- Current page is highlighted in the menu
- Menu closes automatically after selection

---

### Theme Toggle

Switch between light and dark modes using the theme toggle button.

**Location:** Top-right corner (sun/moon icon)

**Themes:**
- **Light Mode:** White background, dark text (default)
- **Dark Mode:** Dark background, light text (easier on eyes)

**How to Change:**
1. Click the sun ☀️ or moon 🌙 icon
2. Theme switches immediately
3. Preference is saved in your browser

**Tip:** Use dark mode in low-light environments to reduce eye strain.

---

## Troubleshooting

### Common Issues & Solutions

#### Issue: Dashboard shows "No data available"

**Possible Causes:**
1. ESP32 is not powered on
2. ESP32 not connected to WiFi
3. MQTT broker connection failed

**Solutions:**
- Check ESP32 power supply
- Verify WiFi credentials in ESP32 config.py
- Check MQTT broker status (HiveMQ Cloud)
- Refresh the web page
- Check browser console for error messages

---

#### Issue: Data is not updating in real-time

**Possible Causes:**
1. Internet connection lost
2. MQTT connection dropped
3. Browser tab is inactive

**Solutions:**
- Check your internet connection
- Refresh the web page
- Ensure browser tab is active (some browsers pause inactive tabs)
- Check if ESP32 is still connected (check serial monitor)

---

#### Issue: Device controls not working

**Possible Causes:**
1. MQTT connection issue
2. ESP32 not receiving commands
3. Device already in requested state

**Solutions:**
- Check MQTT connection status in browser console
- Verify ESP32 is powered on and connected
- Wait 2-3 seconds for response
- Try the opposite command first (e.g., CLOSE then OPEN)
- Check ESP32 serial output for errors

---

#### Issue: RFID scans not appearing in logs

**Possible Causes:**
1. Database connection issue
2. RFID reader not working
3. Web app not connected to MQTT

**Solutions:**
- Check database connection (Supabase status)
- Verify RFID reader is properly connected to ESP32
- Test RFID card on ESP32 (check serial monitor)
- Refresh the RFID Logs page
- Check for JavaScript errors in browser console

---

#### Issue: Asthma alert not showing

**Possible Causes:**
1. Conditions not met (humidity ≤50% or temp ≤27°C)
2. Temperature sensor not sending data
3. MQTT message not received

**Solutions:**
- Check current temperature and humidity values on dashboard
- Verify DHT11 sensor is working (check Dashboard page)
- Alert only shows when BOTH conditions are met
- Wait for next sensor reading (updates every 15 minutes)

---

## FAQ

### General Questions

**Q: Do I need an account to use the dashboard?**
A: No, the current version does not require login. Simply access the URL and start monitoring.

**Q: Can multiple people view the dashboard at the same time?**
A: Yes, unlimited users can view the dashboard simultaneously. All will see the same real-time data.

**Q: Does the dashboard work on mobile devices?**
A: Yes! The dashboard is fully responsive and works on smartphones and tablets.

**Q: How often does the dashboard update?**
A:
- Temperature/Humidity: Every 15 minutes
- Motion/Gas/RFID: Instantly (1-2 seconds)
- Device status: Real-time after command execution

**Q: Is my data saved?**
A: Yes, all sensor readings and events are stored in the database for historical tracking.

---

### Technical Questions

**Q: What browsers are supported?**
A: Any modern browser (Chrome, Firefox, Safari, Edge) with JavaScript enabled.

**Q: Can I access the dashboard remotely (outside my home network)?**
A: Yes! The dashboard is deployed at https://gregarious-semifreddo-257864.netlify.app/ and can be accessed from anywhere with an internet connection.

**Q: What happens if WiFi connection is lost?**
A:
- ESP32 will attempt to reconnect automatically
- Dashboard will show last known values
- Data resumes once connection is restored

**Q: How much data does the dashboard use?**
A: Very minimal - only small JSON messages via MQTT. Approximately 1-2 MB per day.

**Q: Can I export the data?**
A: Not currently built-in. Data is stored in Supabase database which can be exported manually if needed.

---

### Security Questions

**Q: How do I add a new authorized RFID card?**
A: Currently, the authorized card (0x7cdab502) is hardcoded in ESP32. To add more, you'll need to modify the ESP32 code.

**Q: Can unauthorized cards open the door?**
A: No. Only the authorized card can open the door. Unauthorized cards trigger buzzer and red LED flash.

**Q: Are my commands encrypted?**
A: Yes, MQTT communication uses TLS/SSL encryption (port 8883).

**Q: Who can see the access logs?**
A: Anyone with access to the dashboard URL can view logs. Future versions may include authentication.

---

### Feature Questions

**Q: Can I schedule devices to operate at specific times?**
A: Not currently available in the web dashboard. The LED has automatic scheduling (8pm-7am) in ESP32 code.

**Q: Can I add more sensors?**
A: Yes, but requires hardware setup on ESP32 and code modifications.

**Q: Can I get notifications on my phone?**
A: Not currently implemented. This would be a future enhancement.

**Q: How do I clear old RFID logs?**
A: Logs are stored permanently in the database. Manual deletion would require database access.

**Q: Can I control the RGB LED colors?**
A: No, RGB LED colors are automatic based on events:
- Orange = Motion detected
- Blue = Steam/moisture detected
- Red = Gas detected or unauthorized RFID

---

## Tips & Best Practices

### Monitoring Tips

1. **Check dashboard daily** for unusual activity in RFID logs
2. **Monitor motion count** to understand traffic patterns
3. **Watch temperature/humidity trends** for comfort optimization
4. **Keep browser tab open** for best real-time performance

### Control Tips

1. **Wait 2-3 seconds** after clicking control buttons for response
2. **Avoid rapid clicking** - one click is enough
3. **Check status indicators** to confirm command execution
4. **Use manual controls sparingly** - let automation handle routine tasks

### Safety Tips

1. **Don't open doors remotely** if you're unsure of physical surroundings
2. **Monitor gas alerts immediately** - ensure proper ventilation
3. **Check asthma alerts** especially for sensitive individuals
4. **Test controls regularly** to ensure system responsiveness

---

## Support & Additional Help

### Need More Help?

- **Project Documentation:** See [docs/PROJECT_GUIDE.md](PROJECT_GUIDE.md)
- **System Architecture:** See [docs/ARCHITECTURE.md](ARCHITECTURE.md)
- **Task Details:** See [docs/PROJECT_STATUS.md](PROJECT_STATUS.md)

### Reporting Issues

If you experience technical issues:

1. Check browser console for error messages (F12 → Console tab)
2. Check ESP32 serial monitor for device errors
3. Document the exact steps that caused the issue
4. Note any error messages displayed
5. Check the troubleshooting section above

---

## Quick Reference Card

### Dashboard At-A-Glance

| Feature | Update Frequency | Location |
|---------|------------------|----------|
| Temperature | Every 15 min | Dashboard - Top Left |
| Humidity | Every 15 min | Dashboard - Top Center |
| Motion Count | Real-time | Dashboard - Top Right |
| Gas Status | Real-time | Dashboard - Bottom |
| Asthma Alert | Every 15 min | Dashboard - Banner |
| Door Control | Real-time | Controls - Left |
| Window Control | Real-time | Controls - Center |
| Fan Control | Real-time | Controls - Right |
| RFID Logs | Real-time | RFID Logs - Table |

### Status Colors

- 🟢 **Green:** Normal / Active / Success
- 🔴 **Red:** Alert / Warning / Failed
- ⚪ **Gray:** Inactive / Closed / Off
- 🟠 **Orange:** Motion detected (RGB LED)
- 🔵 **Blue:** Steam detected (RGB LED)

---

**End of User Manual**

For the latest updates and detailed technical information, refer to the complete project documentation in the `docs/` folder.

**Version:** 1.0
**Last Updated:** December 10, 2025
**Project:** Smart House IoT System
