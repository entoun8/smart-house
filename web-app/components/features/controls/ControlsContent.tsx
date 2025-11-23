"use client";

import { useEffect, useState } from "react";
import { connectMQTT } from "@/lib/mqtt";
import ControlsHeader from "./ControlsHeader";
import ConnectionWarning from "./ConnectionWarning";
import DoorControl from "./devices/DoorControl";
import WindowControl from "./devices/WindowControl";
import FanControl from "./devices/FanControl";

export default function ControlsContent() {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [client, setClient] = useState<any>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastCommand, setLastCommand] = useState<string>("");

  useEffect(() => {
    const mqttClient = connectMQTT();
    setClient(mqttClient);

    mqttClient.on("connect", () => {
      setIsConnected(true);
    });

    mqttClient.on("error", () => {
      setIsConnected(false);
    });

    return () => {
      mqttClient.end();
    };
  }, []);

  const sendCommand = (topic: string, message: string, label: string) => {
    if (client) {
      client.publish(topic, message);
      setLastCommand(`${label}: ${message}`);
      console.log(`📤 Sent: ${topic} -> ${message}`);
    }
  };

  return (
    <>
      {/* Header */}
      <ControlsHeader isConnected={isConnected} lastCommand={lastCommand} />

      {/* Controls Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
        <DoorControl isConnected={isConnected} sendCommand={sendCommand} />
        <WindowControl isConnected={isConnected} sendCommand={sendCommand} />
        <FanControl isConnected={isConnected} sendCommand={sendCommand} />
      </div>

      {/* Connection Warning */}
      <ConnectionWarning isConnected={isConnected} />
    </>
  );
}
