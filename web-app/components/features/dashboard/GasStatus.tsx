"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { connectMQTT, TOPICS } from "@/lib/mqtt";
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
  const [timeoutId, setTimeoutId] = useState<NodeJS.Timeout | null>(null);

  useEffect(() => {
    console.log("[GasStatus] Component mounted");
    console.log("[GasStatus] TOPICS.gas:", TOPICS.gas);

    const client = connectMQTT();
    console.log("[GasStatus] MQTT client created");

    client.on("connect", () => {
      console.log(
        "[GasStatus] MQTT connected, subscribing to:",
        TOPICS.gas
      );

      client.subscribe(TOPICS.gas, (err) => {
        if (!err) {
          console.log("[GasStatus] ✅ Subscribed to", TOPICS.gas);
        } else {
          console.error("[GasStatus] ❌ Subscribe failed:", err);
        }
      });
    });

    const handleMessage = (topic: string, message: Buffer) => {
      if (topic === TOPICS.gas) {
        const msg = message.toString();
        console.log(
          "🚨 [GasStatus] Gas message from MQTT:",
          msg
        );

        // If gas is detected (value "1")
        if (msg === "1") {
          setGasDetected(true);
          setLastDetection(new Date().toLocaleTimeString());
          setDetectionCount((prev) => prev + 1);

          // Clear any existing timeout
          if (timeoutId) {
            clearTimeout(timeoutId);
          }

          // Auto-clear after 30 seconds of no updates (safety)
          const timeout = setTimeout(() => {
            setGasDetected(false);
            console.log("[GasStatus] Auto-cleared after 30s timeout");
          }, 30000);
          setTimeoutId(timeout);
        }
        // If gas cleared (value "0")
        else if (msg === "0") {
          setGasDetected(false);
          console.log("[GasStatus] Gas cleared");
          if (timeoutId) {
            clearTimeout(timeoutId);
          }
        }
      }
    };

    client.on("message", handleMessage);

    fetchGasCount();

    return () => {
      client.off("message", handleMessage);
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, [timeoutId]);

  const fetchGasCount = async () => {
    const { data, count } = await supabase
      .from("gas_logs")
      .select("*", { count: "exact", head: true });

    if (count !== null) {
      setDetectionCount(count);
    }
  };

  return (
    <Card className={`hover:shadow-lg transition-all ${gasDetected ? 'border-red-500 border-2' : ''}`}>
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
