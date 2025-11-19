"use client";

import { useEffect, useState } from "react";
import { connectMQTT } from "@/lib/mqtt";
import DashboardHeader from "./DashboardHeader";
import AsthmaAlert from "./AsthmaAlert";
import TemperatureStatus from "./TemperatureStatus";
import HumidityStatus from "./HumidityStatus";
import MotionStatus from "./MotionStatus";
import GasStatus from "./GasStatus";

export default function DashboardContent() {
  const [temperature, setTemperature] = useState<number | null>(null);
  const [humidity, setHumidity] = useState<number | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Connect to MQTT
    const client = connectMQTT();

    // Set connection status
    client.on("connect", () => {
      console.log("Dashboard: MQTT connected!");
      setIsConnected(true);
    });

    client.on("offline", () => {
      console.log("Dashboard: MQTT offline");
      setIsConnected(false);
    });

    client.on("error", (error) => {
      console.error("Dashboard: MQTT error", error);
      setIsConnected(false);
    });

    // Subscribe to sensor topics (using correct topics)
    client.subscribe("ks5009/house/sensors/temperature", (err) => {
      if (!err) console.log("Subscribed to temperature");
    });

    // Handle incoming messages
    client.on("message", (topic, message) => {
      const payload = message.toString();
      console.log("Received:", topic, payload);

      // Temperature/Humidity
      if (topic === "ks5009/house/sensors/temperature") {
        try {
          const data = JSON.parse(payload);
          setTemperature(data.value);
          setHumidity(data.humidity || null);
        } catch (e) {
          console.error("Failed to parse temperature:", e);
        }
      }
    });

    return () => {
      client.end();
    };
  }, []);

  return (
    <>
      <DashboardHeader isConnected={isConnected} />

      {/* Sensor Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
        {/* Temperature Status */}
        <TemperatureStatus />

        {/* Humidity Status */}
        <HumidityStatus />

        {/* Motion Status */}
        <MotionStatus />

        {/* Gas Status */}
        <GasStatus />
      </div>

      {/* Asthma Risk Alert - Now using MQTT */}
      <AsthmaAlert />
    </>
  );
}
