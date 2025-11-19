# 📋 Task Requirements

Complete list of features to implement for the Smart House IoT project.

---

## 🎯 ESP32 Requirements (Hardware Side)

### 1. LED Control
- **Requirement**: LED lights up between 8pm to 7am
- **Component**: Yellow LED (GPIO 12)
- **Logic**: Time-based automation using RTC or system clock

### 2. Temperature & Humidity Logging
- **Requirement**: Logs temperature and humidity every 30 minutes
- **Component**: DHT11 Sensor (GPIO 17)
- **Logic**: Timer-based logging to database via MQTT
- **Data**: Temperature (°C), Humidity (%), Timestamp

### 3. PIR Motion Detection
- **Requirement 1**: If PIR movement detected, light up RGB in orange
- **Requirement 2**: If PIR movement detected, log into database (time and date)
- **Component**: PIR Sensor (GPIO 14), RGB LEDs (GPIO 26)
- **Logic**: Event-driven, trigger on motion
- **Database Log**: Motion detection event with timestamp

### 4. Steam/Moisture Detection
- **Requirement**: If steam sensor detects moisture (water droplet), close window, flash RGB blue
- **Component**: Water/Steam Sensor (GPIO 34), Window Servo (GPIO 5), RGB LEDs
- **Logic**:
  - Sensor detects moisture → Close window immediately
  - Flash RGB blue as visual alert
  - Return to normal after event

### 5. Gas Detection & Fan Control
- **Requirement 1**: If gas sensor detects gas/flame, turn on fan until sensor stops detecting, solid RGB red
- **Requirement 2**: Log every gas sensor detection (time, date, value)
- **Component**: Gas Sensor (GPIO 23), Fan Motor (GPIO 18, 19), RGB LEDs
- **Logic**:
  - Gas detected → Fan ON + RGB solid red
  - Fan stays on until gas clears
  - Log all detection events with values and timestamps

### 6. Asthma Alert
- **Requirement**: Show asthma alert on LCD if humidity is greater than 50% and temperature is over 27 degrees celsius
- **Component**: LCD1602 (I2C), DHT11
- **Logic**: Continuous monitoring, display alert when conditions met
- **Alert Message**: "ASTHMA ALERT!" or similar warning

### 7. RFID Access Control
- **Requirement 1**: RFID logs in user against users in database
- **Requirement 2**: RGB flashes red and buzzer buzzes when unknown RFID card is scanned
- **Requirement 3**: Logs ALL RFID scans (success or fail, time)
- **Component**: RFID RC522 (SPI), Buzzer (GPIO 25), RGB LEDs, Door Servo (GPIO 13)
- **Logic**:
  - Read RFID card → Check against database
  - If authorized: Open door, log success
  - If unauthorized: Flash RGB red, buzzer alarm, log failure
  - Log every scan attempt with timestamp

---

## 🌐 Web App Requirements (Dashboard Side)

### Dashboard Display

#### 1. Real-Time Sensor Data
- **Display current temperature in celsius**
  - Live updates from ESP32 via MQTT/Database
  - Visual display with appropriate icon

- **Display current humidity as a percentage**
  - Live updates from ESP32
  - Visual display with appropriate icon

#### 2. Alerts & Notifications
- **Alert when gas sensor detects**
  - Real-time notification system
  - Visual alert indicator
  - Show gas detection status

- **Display asthma alert**
  - Show when conditions met (humidity >50% AND temp >27°C)
  - Clear visual warning

#### 3. Motion Detection Stats
- **Display number of PIR detections in the last hour**
  - Counter display
  - Auto-refresh
  - Time-based filtering

### Historical Data & Logs

#### 4. RFID Access Logs
- **Show a list of all RFID scans**
  - Display all scan attempts
  - Include: User ID, Timestamp, Success/Fail status

- **Allow filter for successful and failed scans**
  - Filter buttons: All / Successful / Failed
  - Search functionality

#### 5. Device Status Display
- **Show status (open/closed) of door and window**
  - Door servo position indicator
  - Window servo position indicator
  - Real-time status updates

- **Show status of fan (on/off)**
  - Fan motor state indicator
  - Real-time status updates

### Remote Control Features

#### 6. Device Control
- **Open window and door via web app**
  - Button controls for door servo
  - Button controls for window servo
  - Send commands via MQTT to ESP32

- **Turn on fan via web app**
  - Fan on/off toggle button
  - Send commands via MQTT to ESP32

---

## 🗄️ Database Schema Requirements

### Tables Needed

#### 1. `sensor_logs` Table
```sql
- id (primary key)
- temperature (decimal)
- humidity (decimal)
- timestamp (datetime)
```

#### 2. `motion_events` Table
```sql
- id (primary key)
- detected (boolean)
- timestamp (datetime)
```

#### 3. `gas_events` Table
```sql
- id (primary key)
- detected (boolean)
- value (integer)
- timestamp (datetime)
```

#### 4. `rfid_scans` Table
```sql
- id (primary key)
- card_id (string)
- user_id (foreign key, nullable)
- success (boolean)
- timestamp (datetime)
```

#### 5. `users` Table
```sql
- id (primary key)
- name (string)
- rfid_card_id (string, unique)
- created_at (datetime)
```

#### 6. `device_status` Table
```sql
- id (primary key)
- device_name (string) - "door", "window", "fan"
- status (string) - "open", "closed", "on", "off"
- updated_at (datetime)
```

---

## 📊 Feature Breakdown by Component

### Component: LED (Yellow)
- ✅ Auto on/off based on time (8pm-7am)

### Component: DHT11 Sensor
- ✅ Log temperature & humidity every 30 min
- ✅ Display live temp on web app
- ✅ Display live humidity on web app
- ✅ Trigger asthma alert on LCD

### Component: PIR Sensor
- ✅ Light up RGB orange on motion
- ✅ Log motion to database
- ✅ Display last hour count on web app

### Component: Gas Sensor
- ✅ Turn on fan when detected
- ✅ Show RGB solid red
- ✅ Log all detections
- ✅ Alert on web app

### Component: Steam/Water Sensor
- ✅ Close window when moisture detected
- ✅ Flash RGB blue

### Component: RFID RC522
- ✅ Check card against database
- ✅ Open door for authorized users
- ✅ Flash RGB red + buzzer for unauthorized
- ✅ Log all scans (success/fail)
- ✅ Display all scans on web app with filter

### Component: RGB LEDs
- ✅ Orange for motion
- ✅ Blue flash for steam
- ✅ Red solid for gas
- ✅ Red flash for RFID fail

### Component: Fan
- ✅ Auto on during gas detection
- ✅ Manual control via web app
- ✅ Status display on web app

### Component: Door Servo
- ✅ Open for authorized RFID
- ✅ Manual control via web app
- ✅ Status display on web app

### Component: Window Servo
- ✅ Auto close on steam detection
- ✅ Manual control via web app
- ✅ Status display on web app

### Component: LCD1602
- ✅ Display asthma alert

### Component: Buzzer
- ✅ Sound alarm for unauthorized RFID

---

## 🎯 Implementation Priority

### Phase 1: Core Automation (ESP32)
1. LED time-based control
2. Temperature/humidity logging (30 min intervals)
3. PIR motion → RGB orange + log
4. Gas detection → Fan + RGB red + log
5. Steam detection → Window close + RGB blue flash

### Phase 2: RFID System (ESP32)
1. RFID card reading
2. Database user verification
3. Door control for authorized users
4. RGB red flash + buzzer for unauthorized
5. Log all RFID scans

### Phase 3: Alerts (ESP32)
1. Asthma alert on LCD
2. MQTT event publishing

### Phase 4: Web Dashboard (Next.js)
1. Real-time temperature & humidity display
2. Gas detection alerts
3. PIR detection counter (last hour)
4. Device status displays (door, window, fan)

### Phase 5: Web Controls (Next.js)
1. Door open/close button
2. Window open/close button
3. Fan on/off toggle
4. MQTT command publishing

### Phase 6: Web Logs (Next.js)
1. RFID scan history with filter
2. Historical charts
3. Event timeline

---

## 📝 Testing Checklist

### ESP32 Testing
- [ ] LED turns on at 8pm, off at 7am
- [ ] Temperature/humidity logged every 30 minutes
- [ ] PIR triggers RGB orange and logs to DB
- [ ] Gas detection turns on fan, shows RGB red, logs event
- [ ] Steam detection closes window, flashes RGB blue
- [ ] Asthma alert shows on LCD when conditions met
- [ ] Authorized RFID opens door
- [ ] Unauthorized RFID triggers buzzer and RGB red flash
- [ ] All RFID scans logged to database

### Web App Testing
- [ ] Temperature displays in real-time
- [ ] Humidity displays in real-time
- [ ] Gas alert appears when detected
- [ ] PIR count shows last hour detections
- [ ] Door status shows correctly (open/closed)
- [ ] Window status shows correctly (open/closed)
- [ ] Fan status shows correctly (on/off)
- [ ] Door can be opened via web button
- [ ] Window can be opened via web button
- [ ] Fan can be toggled via web button
- [ ] RFID logs display all scans
- [ ] RFID filter works (all/success/fail)

---

## 🔗 Integration Requirements

### MQTT Topics Structure
```
smart-house/sensors/temperature
smart-house/sensors/humidity
smart-house/sensors/pir
smart-house/sensors/gas
smart-house/sensors/steam
smart-house/rfid/scan
smart-house/devices/door/status
smart-house/devices/window/status
smart-house/devices/fan/status
smart-house/devices/door/control
smart-house/devices/window/control
smart-house/devices/fan/control
```

### Data Flow
1. **ESP32 → MQTT → Supabase → Web App**
   - Sensor readings
   - Event logs
   - Device status updates

2. **Web App → MQTT → ESP32**
   - Device control commands
   - Manual overrides

---

## 📈 Success Criteria

### Automation Working
- ✅ All automated responses function correctly without user intervention
- ✅ Logs are created automatically at correct intervals
- ✅ Alerts trigger based on correct conditions

### Web Dashboard Working
- ✅ Real-time data displays accurately
- ✅ All historical logs are accessible
- ✅ Manual controls work reliably
- ✅ Filters and search functions operate correctly

### System Reliability
- ✅ ESP32 reconnects to WiFi/MQTT automatically
- ✅ Database connections are stable
- ✅ No data loss during network interruptions
- ✅ Web app handles offline/online states gracefully

---

**Total Requirements**:
- **ESP32 Features**: 7 main automation tasks
- **Web App Features**: 11 display/control features
- **Database Tables**: 6 tables
- **Components Used**: 15/15 (100% utilization)

**Estimated Completion Time**:
- ESP32 Implementation: 8-12 hours
- Web App Development: 12-16 hours
- Testing & Integration: 4-6 hours
- **Total**: 24-34 hours

---

**Last Updated**: 2025-11-12
**Status**: Requirements documented, ready for implementation
