import time
from components import WaterSensor, WindowServo, RGBStrip

water = WaterSensor()
window = WindowServo()
rgb = RGBStrip()

previous_steam = False

def handle_steam_detected():
    """Handle steam/moisture detection event"""
    print("Steam detected!")

    window.close()

    rgb.blue()

def handle_steam_stopped():
    """Handle when steam stops"""
    rgb.off()

print("=" * 50)
print("STEAM DETECTION - TASK 4")
print("=" * 50)
print("\nMonitoring for steam/moisture...")
print("Requirements:")
print("  - Close window when detected")
print("  - Flash RGB blue")
print("=" * 50)

while True:
    try:
        steam = water.is_wet()

        if steam and not previous_steam:
            handle_steam_detected()

        elif not steam and previous_steam:
            handle_steam_stopped()

        previous_steam = steam

        time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n\nStopping steam detector...")
        rgb.off()
        break
    except Exception as e:
        print(f"\nError: {e}")
        time.sleep(1)
