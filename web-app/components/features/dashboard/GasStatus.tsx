"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { subscribe, TOPICS } from "@/lib/mqtt";
import { Flame } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function GasStatus() {
  const [gasDetected, setGasDetected] = useState<boolean>(false);
  const [lastDetection, setLastDetection] = useState<string>("");
  const [detectionCount, setDetectionCount] = useState<number>(0);

  useEffect(() => {
    const unsubscribe = subscribe(TOPICS.gas, async (message) => {
      if (message === "1") {
        setGasDetected(true);
        setLastDetection(new Date().toLocaleTimeString());
        setDetectionCount((prev) => prev + 1);
        await supabase.from("gas_logs").insert({ value: 1 });
      } else if (message === "0") {
        setGasDetected(false);
      }
    });

    fetchGasCount();

    return unsubscribe;
  }, []);

  const fetchGasCount = async () => {
    const { data, count } = await supabase
      .from("gas_logs")
      .select("*", { count: "exact", head: true });

    if (count !== null) {
      setDetectionCount(count);
    }
  };

  return (
    <Card
      className={`hover:shadow-lg transition-all ${
        gasDetected ? "border-red-500 border-2" : ""
      }`}
    >
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <Flame
            className={`w-6 h-6 ${
              gasDetected ? "text-red-500 animate-pulse" : "text-gray-400"
            }`}
          />
          Gas Detection
        </CardTitle>
        <CardDescription>Gas sensor alerts</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {gasDetected ? (
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
              <p className="text-lg font-bold text-red-500">GAS DETECTED!</p>
            </div>
          ) : (
            <p className="text-lg font-semibold text-green-500">All Clear</p>
          )}
          <p className="text-sm text-muted-foreground">
            Total detections: {detectionCount}
          </p>
          {lastDetection && (
            <p className="text-sm text-muted-foreground">
              Last detection: {lastDetection}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
