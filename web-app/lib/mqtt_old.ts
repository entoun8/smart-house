import mqtt from "mqtt";

const MQTT_BROKER = process.env.NEXT_PUBLIC_MQTT_BROKER!;
const MQTT_USERNAME = process.env.NEXT_PUBLIC_MQTT_USERNAME;
const MQTT_PASSWORD = process.env.NEXT_PUBLIC_MQTT_PASSWORD;

export function connectMQTT() {
  // Build connection options
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const options: any = {};

  // Only add credentials if they exist (for public broker, they won't)
  if (MQTT_USERNAME && MQTT_PASSWORD) {
    options.username = MQTT_USERNAME;
    options.password = MQTT_PASSWORD;
  }

  const client = mqtt.connect(MQTT_BROKER, options);

  client.on("connect", () => {
    console.log("✅ Connected to MQTT broker");
  });

  client.on("error", (error) => {
    console.error("❌ MQTT Error:", error);
  });

  return client;
}
