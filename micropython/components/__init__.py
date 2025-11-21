"""
Smart Home Components Library - Organized by Category

Import all components from their categorized folders
"""

# Sensors
from .sensors import PIR, DHT, GasSensor, WaterSensor, RFID

# Actuators
from .actuators import LED, RGBStrip, Buzzer, Fan, DoorServo, WindowServo

# Connectivity
from .connectivity import WiFi, MQTT

# Displays
from .displays import LCD

__all__ = [
    # Sensors
    'PIR',
    'DHT',
    'GasSensor',
    'WaterSensor',
    'RFID',

    # Actuators
    'LED',
    'RGBStrip',
    'Buzzer',
    'Fan',
    'DoorServo',
    'WindowServo',

    # Connectivity
    'WiFi',
    'MQTT',

    # Displays
    'LCD'
]
