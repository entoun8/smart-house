# ESP32 Pin Configuration
LED_PIN = 12
RGB_LED_PIN = 26
BUZZER_PIN = 25
FAN_PIN1 = 19
FAN_PIN2 = 18
WINDOW_SERVO_PIN = 5
DOOR_SERVO_PIN = 13

DHT_PIN = 17
WATER_SENSOR_PIN = 34
GAS_SENSOR_PIN = 23
PIR_SENSOR_PIN = 14

# Button Sensors
BUTTON_LEFT_PIN = 16
BUTTON_RIGHT_PIN = 27

# Relay Module
RELAY_PIN = 15

I2C_SCL_PIN = 22
I2C_SDA_PIN = 21

# RFID RC522 (SPI)
RFID_SCK = 18
RFID_MOSI = 23
RFID_MISO = 19
RFID_SDA = 5
RFID_RST = 22

RGB_LED_COUNT = 4

# WiFi
WIFI_SSID = "Telstra099B26"
WIFI_PASSWORD = "56jh79sqcfx6vnta"

# MQTT Broker (HiveMQ Cloud with SSL)
MQTT_BROKER = "26cba3f4929a4be4942914ec72fe5b4b.s1.eu.hivemq.cloud"
MQTT_PORT = 8883  # SSL port
MQTT_USER = "smarthome"
MQTT_PASSWORD = "SmartHome123!"
MQTT_CLIENT_ID = "ks5009-smart-house"
MQTT_KEEPALIVE = 60

# Topics
class MQTTTopics:
    def __init__(self):
        self.base = "ks5009/house"

    def sensor(self, name):
        return f"{self.base}/sensors/{name}"

    def device_state(self, name):
        return f"{self.base}/devices/{name}/state"

    def device_command(self, name):
        return f"{self.base}/devices/{name}/command"

    def all_commands(self):
        return f"{self.base}/devices/+/command"

    def status(self, type):
        return f"{self.base}/status/{type}"

    def event(self, name):
        return f"{self.base}/events/{name}"

TOPICS = MQTTTopics()
