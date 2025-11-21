"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { connectMQTT, TOPICS, subscribe } from "@/lib/mqtt";
import { Droplets } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function HumidityStatus() {
  const [humidity, setHumidity] = useState<number | null>(null);
  const [lastUpdate, setLastUpdate] = useState<string>("");

  useEffect(() => {
    // Connect to MQTT
    connectMQTT();

    // Subscribe to humidity topic (real-time updates from ESP32)
    subscribe(TOPICS.humidity, async (message) => {
      const hum = parseFloat(message);
      setHumidity(hum);
      setLastUpdate(new Date().toLocaleTimeString());
      console.log("Humidity from MQTT:", hum);

      // Log to database (get temp from localStorage set by TemperatureStatus)
      const tempStr = localStorage.getItem("lastTemp");
      const temp = tempStr ? parseFloat(tempStr) : null;
      if (temp !== null) {
        const { error } = await supabase
          .from("temperature_logs")
          .insert({ temp, humidity: hum });
        if (!error) {
          console.log("✅ Temperature logged to DB:", temp, hum);
        }
      }
    });

    // Fetch initial humidity from database (in case ESP32 is offline)
    const fetchInitialHumidity = async () => {
      const { data } = await supabase
        .from("temperature_logs")
        .select("humidity, timestamp")
        .order("timestamp", { ascending: false })
        .limit(1);

      if (data && data.length > 0) {
        setHumidity(data[0].humidity);
        setLastUpdate(new Date(data[0].timestamp).toLocaleTimeString());
      }
    };

    fetchInitialHumidity();
  }, []);

  // Determine humidity status
  const getHumidityStatus = () => {
    if (humidity === null) return { color: "secondary", label: "Unknown" };
    if (humidity < 30) return { color: "default", label: "Dry" };
    if (humidity <= 60) return { color: "default", label: "Comfortable" };
    return { color: "destructive", label: "High" };
  };

  const status = getHumidityStatus();

  return (
    <Card className="hover:shadow-lg transition-all">
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <Droplets
            className={`w-6 h-6 ${
              humidity !== null && humidity > 50
                ? "text-blue-500"
                : "text-gray-400"
            }`}
          />
          Humidity
        </CardTitle>
        <CardDescription>Current humidity as a percentage</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <p className="text-4xl font-bold">
            {humidity !== null ? `${humidity}%` : "--"}
          </p>
          {humidity !== null && (
            <Badge variant={status.color as "default" | "secondary" | "destructive" | "outline"}>
              {status.label}
            </Badge>
          )}
          {lastUpdate && (
            <p className="text-sm text-muted-foreground">
              Last update: {lastUpdate}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
