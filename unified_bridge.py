#!/usr/bin/env python3
"""
Unified Bridge - Handles Database/MQTT Tasks
Reads serial output from ESP32 and handles:
- Task 2: Temperature & Humidity logging
- Task 3: Motion detection logging
- Task 5: Gas detection logging
- Task 6: Asthma alert (MQTT only, no database)
- Task 7: RFID access control (database + MQTT)
"""

import serial
import time
import sys
import requests
import subprocess
import re

print("=" * 60)
print("Smart House - Unified Bridge (Tasks 2, 3, 5, 6, 7)")
print("=" * 60)

# Serial connection to ESP32
ESP32_PORT = 'COM5'  # ESP32 port
BAUD_RATE = 115200

# MQTT settings
MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 8000

# Supabase settings
SUPABASE_URL = "https://ktpswojqtskcnqlxzhwa.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt0cHN3b2pxdHNrY25xbHh6aHdhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIyOTMyNDgsImV4cCI6MjA3Nzg2OTI0OH0.A0qUts3FYeOicpLlLoEkz9YpIFhjYTMKrN3jif_lHG4"

# ============================================
# TASK 2: TEMPERATURE & HUMIDITY
# ============================================

def log_temperature_to_database(temp, humidity):
    """Log temperature and humidity to Supabase"""
    try:
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }

        payload = {'temp': temp, 'humidity': humidity}

        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/temperature_logs",
            headers=headers,
            json=payload,
            timeout=5
        )

        if response.status_code in [200, 201]:
            print(f"  [DB] Temperature logged! ({temp}°C, {humidity}%)")
            return True
        else:
            print(f"  [WARN] Temperature DB failed (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"  [WARN] Temperature DB error: {e}")
        return False

def publish_temperature_mqtt(temp, humidity):
    """Publish temperature and humidity to MQTT"""
    try:
        # Publish temperature
        cmd_temp = f'''node -e "const mqtt = require('mqtt'); const client = mqtt.connect('ws://{MQTT_BROKER}:{MQTT_PORT}/mqtt'); client.on('connect', () => {{ client.publish('ks5009/house/sensors/temperature', '{temp}'); setTimeout(() => client.end(), 500); }});"'''

        # Publish humidity
        cmd_hum = f'''node -e "const mqtt = require('mqtt'); const client = mqtt.connect('ws://{MQTT_BROKER}:{MQTT_PORT}/mqtt'); client.on('connect', () => {{ client.publish('ks5009/house/sensors/humidity', '{humidity}'); setTimeout(() => client.end(), 500); }});"'''

        subprocess.run(cmd_temp, shell=True, cwd='web-app', capture_output=True, timeout=10)
        subprocess.run(cmd_hum, shell=True, cwd='web-app', capture_output=True, timeout=10)

        print(f"  [MQTT] Temperature published!")
        return True
    except subprocess.TimeoutExpired:
        print(f"  [WARN] Temperature MQTT timeout (continuing anyway)")
        return False
    except Exception as e:
        print(f"  [WARN] Temperature MQTT error: {e}")
        return False

# ============================================
# TASK 3: MOTION DETECTION
# ============================================

def log_motion_to_database():
    """Log motion event to Supabase"""
    try:
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }

        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/motion_logs",
            headers=headers,
            json={},
            timeout=5
        )

        if response.status_code in [200, 201]:
            print(f"  [DB] Motion logged!")
            return True
        else:
            print(f"  [WARN] Motion DB failed (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"  [WARN] Motion DB error: {e}")
        return False

def publish_motion_mqtt():
    """Publish motion event to MQTT"""
    try:
        cmd = f'''node -e "const mqtt = require('mqtt'); const client = mqtt.connect('ws://{MQTT_BROKER}:{MQTT_PORT}/mqtt'); client.on('connect', () => {{ client.publish('ks5009/house/events/motion_detected', '1'); setTimeout(() => client.end(), 500); }});"'''

        result = subprocess.run(cmd, shell=True, cwd='web-app', capture_output=True, timeout=10)

        if result.returncode == 0:
            print(f"  [MQTT] Motion published!")
            return True
        else:
            print(f"  [WARN] Motion MQTT failed")
            return False
    except subprocess.TimeoutExpired:
        print(f"  [WARN] Motion MQTT timeout (continuing anyway)")
        return False
    except Exception as e:
        print(f"  [WARN] Motion MQTT error: {e}")
        return False

# ============================================
# TASK 5: GAS DETECTION
# ============================================

def log_gas_to_database():
    """Log gas detection event to Supabase"""
    try:
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }

        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/gas_logs",
            headers=headers,
            json={'value': 1},
            timeout=5
        )

        if response.status_code in [200, 201]:
            print(f"  [DB] Gas detection logged!")
            return True
        else:
            print(f"  [WARN] Gas DB failed (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"  [WARN] Gas DB error: {e}")
        return False

def publish_gas_mqtt(status="1"):
    """Publish gas detection event to MQTT
    Args:
        status: "1" for gas detected, "0" for gas cleared
    """
    try:
        cmd = f'''node -e "const mqtt = require('mqtt'); const client = mqtt.connect('ws://{MQTT_BROKER}:{MQTT_PORT}/mqtt'); client.on('connect', () => {{ client.publish('ks5009/house/events/gas_detected', '{status}'); setTimeout(() => client.end(), 500); }});"'''

        result = subprocess.run(cmd, shell=True, cwd='web-app', capture_output=True, timeout=10)

        if result.returncode == 0:
            msg = "Gas alert published!" if status == "1" else "Gas cleared published!"
            print(f"  [MQTT] {msg}")
            return True
        else:
            print(f"  [WARN] Gas MQTT failed")
            return False
    except subprocess.TimeoutExpired:
        print(f"  [WARN] Gas MQTT timeout (continuing anyway)")
        return False
    except Exception as e:
        print(f"  [WARN] Gas MQTT error: {e}")
        return False

# ============================================
# TASK 6: ASTHMA ALERT
# ============================================

def publish_asthma_mqtt(status="1"):
    """Publish asthma alert status to MQTT
    Args:
        status: "1" for alert active, "0" for alert cleared
    """
    try:
        cmd = f'''node -e "const mqtt = require('mqtt'); const client = mqtt.connect('ws://{MQTT_BROKER}:{MQTT_PORT}/mqtt'); client.on('connect', () => {{ client.publish('ks5009/house/events/asthma_alert', '{status}'); setTimeout(() => client.end(), 500); }});"'''

        result = subprocess.run(cmd, shell=True, cwd='web-app', capture_output=True, timeout=10)

        if result.returncode == 0:
            msg = "Asthma alert published!" if status == "1" else "Asthma cleared published!"
            print(f"  [MQTT] {msg}")
            return True
        else:
            print(f"  [WARN] Asthma MQTT failed")
            return False
    except subprocess.TimeoutExpired:
        print(f"  [WARN] Asthma MQTT timeout (continuing anyway)")
        return False
    except Exception as e:
        print(f"  [WARN] Asthma MQTT error: {e}")
        return False

# ============================================
# TASK 7: RFID ACCESS CONTROL
# ============================================

def check_rfid_authorization(card_id):
    """Check if RFID card is authorized in database

    Args:
        card_id: RFID card ID (e.g., "0x12345678")

    Returns:
        tuple: (is_authorized, user_id, user_name)
    """
    try:
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json'
        }

        # Query users table for this RFID card
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/users?rfid_card=eq.{card_id}",
            headers=headers,
            timeout=5
        )

        if response.status_code == 200:
            users = response.json()
            if users and len(users) > 0:
                user = users[0]
                return (True, user['id'], user['name'])
            else:
                return (False, None, None)
        else:
            print(f"  [WARN] RFID auth check failed (Status: {response.status_code})")
            return (False, None, None)
    except Exception as e:
        print(f"  [WARN] RFID auth check error: {e}")
        return (False, None, None)

def log_rfid_scan(card_id, success, user_id=None):
    """Log RFID scan to database

    Args:
        card_id: RFID card ID
        success: True if authorized, False if not
        user_id: User ID if authorized, None otherwise
    """
    try:
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }

        payload = {
            'card_id': card_id,
            'success': success,
            'user_id': user_id
        }

        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/rfid_scans",
            headers=headers,
            json=payload,
            timeout=5
        )

        if response.status_code in [200, 201]:
            result = "success" if success else "failure"
            print(f"  [DB] RFID scan logged ({result})")
            return True
        else:
            print(f"  [WARN] RFID scan log failed (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"  [WARN] RFID scan log error: {e}")
        return False

def publish_rfid_mqtt(card_id, authorized, user_name=None):
    """Publish RFID scan event to MQTT

    Args:
        card_id: RFID card ID
        authorized: True if authorized, False if not
        user_name: User name if authorized
    """
    try:
        # Publish scan event
        status = "authorized" if authorized else "unauthorized"
        user_info = user_name if user_name else "Unknown"

        scan_data = f'{{"card_id": "{card_id}", "authorized": {str(authorized).lower()}, "user": "{user_info}"}}'

        cmd = f'''node -e "const mqtt = require('mqtt'); const client = mqtt.connect('ws://{MQTT_BROKER}:{MQTT_PORT}/mqtt'); client.on('connect', () => {{ client.publish('ks5009/house/events/rfid_scan', '{scan_data}'); setTimeout(() => client.end(), 500); }});"'''

        result = subprocess.run(cmd, shell=True, cwd='web-app', capture_output=True, timeout=10)

        if result.returncode == 0:
            print(f"  [MQTT] RFID scan published ({status})")
            return True
        else:
            print(f"  [WARN] RFID MQTT failed")
            return False
    except subprocess.TimeoutExpired:
        print(f"  [WARN] RFID MQTT timeout (continuing anyway)")
        return False
    except Exception as e:
        print(f"  [WARN] RFID MQTT error: {e}")
        return False

def send_auth_response_to_esp32(ser, card_id, authorized):
    """Send authorization response back to ESP32 via serial

    Args:
        ser: Serial connection
        card_id: RFID card ID
        authorized: True if authorized, False if not
    """
    try:
        result = "authorized" if authorized else "unauthorized"
        message = f"AUTH_RESPONSE:{card_id}:{result}\n"
        ser.write(message.encode())
        print(f"  [ESP32] Auth response sent ({result})")
    except Exception as e:
        print(f"  [WARN] Failed to send auth response: {e}")

# ============================================
# MAIN BRIDGE LOGIC
# ============================================

print(f"\nConnecting to ESP32 on {ESP32_PORT}...")
try:
    ser = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)
    print(f"[OK] Connected to ESP32!")
except Exception as e:
    print(f"[ERROR] Failed to connect to ESP32: {e}")
    print(f"\nMake sure:")
    print(f"  1. ESP32 is plugged in")
    print(f"  2. No other program is using {ESP32_PORT}")
    print(f"  3. Task code is running on ESP32")
    sys.exit(1)

print(f"\nMonitoring ESP32 for database logging tasks...")
print("=" * 60)
print("\nActive Tasks:")
print("  - Task 2: Temperature & Humidity (every 30 min)")
print("  - Task 3: Motion Detection (on motion)")
print("  - Task 5: Gas Detection (on gas detected)")
print("  - Task 6: Asthma Alert (MQTT only, no DB)")
print("  - Task 7: RFID Access Control (database + MQTT)")
print("=" * 60)
print()

motion_count = 0
temp_count = 0
gas_count = 0
asthma_count = 0
rfid_count = 0

# Track temperature readings (they come on separate lines)
temp_buffer = None
humidity_buffer = None

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()

            if line:
                print(f"[ESP32] {line}")

            # ============================================
            # DETECT TASK 3: MOTION
            # ============================================
            if "Motion detected" in line:
                motion_count += 1
                print(f"\n[TASK 3] Motion Detected! (#{motion_count})")
                log_motion_to_database()
                publish_motion_mqtt()
                print("=" * 60)

            # ============================================
            # DETECT TASK 5: GAS
            # ============================================
            if "Gas detected" in line:
                gas_count += 1
                print(f"\n[TASK 5] Gas Detected! (#{gas_count})")
                log_gas_to_database()
                publish_gas_mqtt("1")  # Gas detected
                print("=" * 60)

            if "Gas cleared" in line:
                print(f"\n[TASK 5] Gas Cleared!")
                publish_gas_mqtt("0")  # Gas cleared
                print("=" * 60)

            # ============================================
            # DETECT TASK 6: ASTHMA ALERT
            # ============================================
            if "ASTHMA ALERT!" in line or "⚠️  ASTHMA ALERT!" in line:
                asthma_count += 1
                print(f"\n[TASK 6] Asthma Alert Triggered! (#{asthma_count})")
                publish_asthma_mqtt("1")  # Alert active
                print("=" * 60)

            if "Asthma alert cleared" in line or "✅ Asthma alert cleared" in line:
                print(f"\n[TASK 6] Asthma Alert Cleared!")
                publish_asthma_mqtt("0")  # Alert cleared
                print("=" * 60)

            # ============================================
            # DETECT TASK 7: RFID ACCESS CONTROL
            # ============================================
            if "RFID check request:" in line:
                rfid_count += 1

                # Extract card ID from line
                card_id = line.split("RFID check request:")[-1].strip()

                print(f"\n[TASK 7] RFID Card Scanned! (#{rfid_count})")
                print(f"  Card ID: {card_id}")

                # Check authorization in database
                authorized, user_id, user_name = check_rfid_authorization(card_id)

                if authorized:
                    print(f"  ✅ Authorized: {user_name}")
                else:
                    print(f"  ❌ Unauthorized")

                # Log scan to database
                log_rfid_scan(card_id, authorized, user_id)

                # Publish to MQTT
                publish_rfid_mqtt(card_id, authorized, user_name)

                # Send response back to ESP32
                send_auth_response_to_esp32(ser, card_id, authorized)

                print("=" * 60)

            # ============================================
            # DETECT TASK 2: TEMPERATURE & HUMIDITY
            # ============================================
            temp_match = re.search(r'Temperature:\s*(\d+(?:\.\d+)?)°?C', line)
            humidity_match = re.search(r'Humidity:\s*(\d+(?:\.\d+)?)%', line)

            if temp_match:
                temp_buffer = float(temp_match.group(1))

            if humidity_match:
                humidity_buffer = float(humidity_match.group(1))

            # If we have both temp and humidity, log them
            if temp_buffer is not None and humidity_buffer is not None:
                temp_count += 1

                print(f"\n[TASK 2] Temperature Reading! (#{temp_count})")
                print(f"  Temperature: {temp_buffer}°C")
                print(f"  Humidity: {humidity_buffer}%")
                log_temperature_to_database(temp_buffer, humidity_buffer)
                publish_temperature_mqtt(temp_buffer, humidity_buffer)
                print("=" * 60)

                # Reset buffers
                temp_buffer = None
                humidity_buffer = None

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\n[STOPPED] Bridge stopped by user")
    print(f"\nSession Statistics:")
    print(f"  - Motion detections: {motion_count}")
    print(f"  - Temperature readings: {temp_count}")
    print(f"  - Gas detections: {gas_count}")
    print(f"  - Asthma alerts: {asthma_count}")
    print(f"  - RFID scans: {rfid_count}")
    ser.close()
    print("\nGoodbye!")

except Exception as e:
    print(f"\n[ERROR] Error: {e}")
    ser.close()
    sys.exit(1)
