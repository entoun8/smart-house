"use client";

import { useEffect, useState, useRef } from "react";
import { connectMQTT, TOPICS } from "@/lib/mqtt";
import { AlertTriangle } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function AsthmaAlert() {
  const [alertActive, setAlertActive] = useState<boolean>(false);
  const [lastAlert, setLastAlert] = useState<string>("");
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    const client = connectMQTT();
    console.log("[AsthmaAlert] MQTT client created");

    client.on("connect", () => {
      console.log(
        "[AsthmaAlert] MQTT connected, subscribing to:",
        TOPICS.asthma
      );

      client.subscribe(TOPICS.asthma, (err) => {
        if (!err) {
          console.log("[AsthmaAlert] ✅ Subscribed to", TOPICS.asthma);
        } else {
          console.error("[AsthmaAlert] ❌ Subscribe failed:", err);
        }
      });
    });

    const handleMessage = (topic: string, message: Buffer) => {
      if (topic === TOPICS.asthma) {
        const msg = message.toString();
        console.log("⚠️  [AsthmaAlert] Asthma alert message from MQTT:", msg);

        if (msg === "1") {
          setAlertActive(true);
          setLastAlert(new Date().toLocaleTimeString());

          if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
          }

          timeoutRef.current = setTimeout(() => {
            setAlertActive(false);
            console.log("[AsthmaAlert] Auto-cleared after 60s timeout");
          }, 60000);
        } else if (msg === "0") {
          setAlertActive(false);
          console.log("[AsthmaAlert] Alert cleared");

          if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
            timeoutRef.current = null;
          }
        }
      }
    };

    client.on("message", handleMessage);

    return () => {
      client.off("message", handleMessage);
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  if (!alertActive) {
    return null;
  }

  return (
    <Card className="mt-6 border-red-500 bg-red-500/10 border-2">
      <CardHeader>
        <CardTitle className="text-red-500 dark:text-red-400 flex items-center gap-2">
          <AlertTriangle className="w-6 h-6 animate-pulse" />
          🚨 Asthma Risk Alert
        </CardTitle>
        <CardDescription className="text-red-600 dark:text-red-300">
          High temperature and humidity detected - conditions may trigger asthma
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <p className="text-sm font-semibold text-red-600 dark:text-red-400">
            ⚠️ Alert Conditions:
          </p>
          <ul className="text-sm text-red-600 dark:text-red-400 list-disc list-inside">
            <li>Temperature &gt; 27°C</li>
            <li>Humidity &gt; 50%</li>
          </ul>
          {lastAlert && (
            <p className="text-xs text-muted-foreground mt-2">
              Last alert: {lastAlert}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
