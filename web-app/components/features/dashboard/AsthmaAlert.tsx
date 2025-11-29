"use client";

import { useEffect, useState } from "react";
import { subscribe, TOPICS } from "@/lib/mqtt";
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

  useEffect(() => {
    const unsubscribe = subscribe(TOPICS.asthma, (message) => {
      if (message === "1") {
        setAlertActive(true);
        setLastAlert(new Date().toLocaleTimeString());
      } else if (message === "0") {
        setAlertActive(false);
      }
    });

    return unsubscribe;
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
