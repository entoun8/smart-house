"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { connectMQTT, TOPICS, subscribe } from "@/lib/mqtt";
import { Thermometer } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function TemperatureStatus() {
  const [temperature, setTemperature] = useState<number | null>(null);
  const [lastUpdate, setLastUpdate] = useState<string>("");

  useEffect(() => {
    connectMQTT();

    const unsubscribe = subscribe(TOPICS.climate, async (message) => {
      const data = JSON.parse(message);
      setTemperature(data.temp);
      setLastUpdate(new Date().toLocaleTimeString());

      await supabase.from("temperature_logs").insert({
        temp: data.temp,
        humidity: data.humidity
      });
    });

    const fetchInitialTemperature = async () => {
      const { data } = await supabase
        .from("temperature_logs")
        .select("temp, timestamp")
        .order("timestamp", { ascending: false })
        .limit(1);

      if (data && data.length > 0) {
        setTemperature(data[0].temp);
        setLastUpdate(new Date(data[0].timestamp).toLocaleTimeString());
      }
    };

    fetchInitialTemperature();

    return unsubscribe;
  }, []);

  const getTempStatus = (): {
    color: "secondary" | "default" | "destructive";
    label: string;
  } => {
    if (temperature === null) return { color: "secondary", label: "Unknown" };
    if (temperature < 18) return { color: "default", label: "Cold" };
    if (temperature <= 25) return { color: "default", label: "Comfortable" };
    if (temperature <= 30) return { color: "default", label: "Warm" };
    return { color: "destructive", label: "Hot" };
  };

  const status = getTempStatus();

  return (
    <Card className="hover:shadow-lg transition-all">
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <Thermometer
            className={`w-6 h-6 ${
              temperature !== null && temperature > 27
                ? "text-red-500"
                : "text-blue-500"
            }`}
          />
          Temperature
        </CardTitle>
        <CardDescription>Current temperature in celsius</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <p className="text-4xl font-bold">
            {temperature !== null ? `${temperature}°C` : "--"}
          </p>
          {temperature !== null && (
            <Badge variant={status.color}>{status.label}</Badge>
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
