import time
from components import PIR, RGBStrip, WiFi, MQTT
from utils.database import Database
from config import TOPICS

pir = PIR()
rgb = RGBStrip()
wifi = WiFi()
mqtt = MQTT()
db = Database()

previous_motion = False

def handle_motion_detected():
    """Handle motion detection event"""
    print("Motion detected!")

    rgb.orange()

    if mqtt.is_connected():
        mqtt.publish(TOPICS.event("motion_detected"), "1")

    db.log_motion()

def handle_motion_stopped():
    """Handle when motion stops"""
    rgb.off()

print("=" * 50)
print("PIR MOTION DETECTION - TASK 3")
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
else:
    print("MQTT connection failed! Bridge will handle logging.")

print("\nSetup complete! Monitoring for motion...")
print("=" * 50)

while True:
    try:
        motion = pir.motion_detected()

        if motion and not previous_motion:
            handle_motion_detected()

        elif not motion and previous_motion:
            handle_motion_stopped()

        previous_motion = motion

        mqtt.check_messages()

        time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n\nStopping PIR motion detector...")
        rgb.off()
        mqtt.disconnect()
        break
    except Exception as e:
        print(f"\nError: {e}")
        time.sleep(1)
