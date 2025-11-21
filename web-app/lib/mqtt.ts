import mqtt from "mqtt";

const MQTT_CONFIG = {
  broker: process.env.NEXT_PUBLIC_MQTT_BROKER || "wss://26cba3f4929a4be4942914ec72fe5b4b.s1.eu.hivemq.cloud:8884/mqtt",
  username: process.env.NEXT_PUBLIC_MQTT_USERNAME || "smarthome",
  password: process.env.NEXT_PUBLIC_MQTT_PASSWORD || "SmartHome123!",
};

export const TOPICS = {
  ledState: "ks5009/house/devices/led/state",
  ledCommand: "ks5009/house/devices/led/command",

  temperature: "ks5009/house/sensors/temperature",
  humidity: "ks5009/house/sensors/humidity",

  motion: "ks5009/house/events/motion_detected",
  gas: "ks5009/house/events/gas_detected",
  asthma: "ks5009/house/events/asthma_alert",
  rfid: "ks5009/house/events/rfid_scan",

  // Device control topics
  doorCommand: "ks5009/house/devices/door/command",
  doorState: "ks5009/house/devices/door/state",
  windowCommand: "ks5009/house/devices/window/command",
  windowState: "ks5009/house/devices/window/state",
  fanCommand: "ks5009/house/devices/fan/command",
  fanState: "ks5009/house/devices/fan/state",

  online: "ks5009/house/status/online",
};

let client: mqtt.MqttClient | null = null;

export function connectMQTT() {
  if (client && client.connected) {
    return client;
  }

  console.log("Connecting to MQTT...");

  client = mqtt.connect(MQTT_CONFIG.broker, {
    username: MQTT_CONFIG.username,
    password: MQTT_CONFIG.password,
    clientId: "webapp-" + Math.random().toString(16).slice(2, 10),
    clean: true,
    reconnectPeriod: 5000,
  });

  client.on("connect", () => {
    console.log("✅ MQTT connected!");
  });

  client.on("error", (error) => {
    console.error("❌ MQTT error:", error);
  });

  return client;
}

export function subscribe(topic: string, callback: (message: string) => void) {
  if (!client) {
    client = connectMQTT();
  }

  client.subscribe(topic, (err) => {
    if (!err) {
      console.log(`Subscribed to ${topic}`);
    }
  });

  client.on("message", (receivedTopic, message) => {
    if (receivedTopic === topic) {
      callback(message.toString());
    }
  });
}

export function publish(topic: string, message: string) {
  if (!client) {
    client = connectMQTT();
  }

  client.publish(topic, message, { qos: 0, retain: true });
}

export function disconnect() {
  if (client) {
    client.end();
    client = null;
  }
}
