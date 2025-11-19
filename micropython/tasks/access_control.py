"""
Task 7: RFID Access Control
- Scans RFID cards
- Checks against authorized users (via serial to bridge)
- Opens door for authorized users
- Flashes RGB red + buzzer for unauthorized users
- Logs all scans (success/fail) via bridge
"""

import time
from components import RFID, RGBStrip, Buzzer, DoorServo, WiFi, MQTT
from config import TOPICS

# Initialize components
rfid = RFID()
rgb = RGBStrip()
buzzer = Buzzer()
door = DoorServo()
wifi = WiFi()
mqtt = MQTT()

# Track last scanned card to prevent duplicate scans
last_card_id = None
last_scan_time = 0
SCAN_COOLDOWN = 3  # Seconds between same card scans

def handle_authorized_access(card_id):
    """Handle successful RFID authorization"""
    print(f"RFID authorized: {card_id}")

    # Open door
    door.open()

    # Flash RGB green
    rgb.green()
    time.sleep(2)
    rgb.off()

    # Close door after 5 seconds
    time.sleep(3)
    door.close()

    print(f"RFID authorized complete: {card_id}")

def handle_unauthorized_access(card_id):
    """Handle failed RFID authorization"""
    print(f"RFID unauthorized: {card_id}")

    # Flash RGB red and buzz
    for _ in range(3):
        rgb.red()
        buzzer.on()
        time.sleep(0.3)
        rgb.off()
        buzzer.off()
        time.sleep(0.3)

    print(f"RFID unauthorized complete: {card_id}")

print("=" * 50)
print("RFID ACCESS CONTROL - TASK 7")
print("=" * 50)

print("\nConnecting to WiFi...")
if not wifi.is_connected():
    if wifi.connect():
        print(f"WiFi connected! IP: {wifi.get_ip()}")
    else:
        print("WiFi connection failed!")
else:
    print(f"WiFi already connected! IP: {wifi.get_ip()}")

time.sleep(2)

print("Connecting to MQTT...")
if mqtt.connect():
    print("MQTT connected!")

    # Subscribe to authorization responses from bridge
    mqtt.subscribe(TOPICS.event("rfid_auth_response"))
    print(f"Subscribed to: {TOPICS.event('rfid_auth_response')}")
else:
    print("MQTT connection failed! Will work offline.")

# Close door at start
door.close()

print("\nSetup complete! Waiting for RFID cards...")
print("=" * 50)

# Track pending authorization check
pending_card = None
pending_time = 0
AUTH_TIMEOUT = 5  # Seconds to wait for bridge response

while True:
    try:
        # Check for RFID card
        card_id = rfid.scan()

        current_time = time.time()

        # New card detected
        if card_id and card_id != last_card_id or (card_id and current_time - last_scan_time > SCAN_COOLDOWN):
            print(f"\nRFID card scanned: {card_id}")

            # Send to bridge for authorization check
            print(f"RFID check request: {card_id}")

            # Set pending card
            pending_card = card_id
            pending_time = current_time

            # Update tracking
            last_card_id = card_id
            last_scan_time = current_time

        # Check for authorization response from bridge
        if pending_card and mqtt.is_connected():
            # Check for messages
            try:
                mqtt.check_messages()
            except:
                pass

            # Check if timeout
            if current_time - pending_time > AUTH_TIMEOUT:
                print(f"Authorization timeout for {pending_card}, denying access")
                handle_unauthorized_access(pending_card)
                pending_card = None

        time.sleep(0.2)

    except KeyboardInterrupt:
        print("\n\nStopping RFID access control...")
        rgb.off()
        buzzer.off()
        door.close()
        mqtt.disconnect()
        break
    except Exception as e:
        print(f"\nError: {e}")
        time.sleep(1)


# MQTT callback for authorization responses
def handle_auth_response(topic, msg):
    """Handle authorization response from bridge"""
    global pending_card

    if not pending_card:
        return

    try:
        # Message format: "card_id:authorized" or "card_id:unauthorized"
        parts = msg.decode().split(':')
        if len(parts) != 2:
            return

        card_id, result = parts

        if card_id == pending_card:
            if result == "authorized":
                handle_authorized_access(card_id)
            else:
                handle_unauthorized_access(card_id)

            pending_card = None
    except Exception as e:
        print(f"Error processing auth response: {e}")


# Set MQTT callback
if mqtt.is_connected():
    mqtt.set_callback(handle_auth_response)
